# -*- coding: utf-8 -*-
"""
主 Agent（Orchestrator）：接收请求、生成执行计划、下发任务、处理结果。
支持将任务分配给 Sub-Agent 或调用自身 Skill / 内置工具。
"""
from __future__ import annotations

import json
import uuid
from pathlib import Path
from .types import Task, TaskResult, TaskStatus, ErrorInfo
from .registry import Registry
from .sub_agent import SubAgent
from .context import AgentContext, ContextConfig
from .experience import append_experience
from .config import get_llm_config
from . import llm as llm_module


MAIN_AGENT_ID = "main"


class Orchestrator:
    """主 Agent：规划、下发、汇总。"""

    def __init__(
        self,
        registry: Registry,
        sub_agents: dict[str, SubAgent] | None = None,
        context: AgentContext | None = None,
        experience_path: Path | None = None,
    ) -> None:
        self._registry = registry
        self._sub_agents = sub_agents or {}
        self._context = context
        self._experience_path = experience_path

    def plan(self, user_request: str) -> dict | None:
        """
        根据用户请求生成单步执行计划（选一个 Skill + params）。
        仅由 LLM 驱动；未配置 LLM 或调用失败时返回 None。
        """
        request_stripped = (user_request or "").strip()
        if not request_stripped:
            return None
        if not get_llm_config("main").is_configured():
            return None
        agents_and_skills = self._registry.list_agents_and_skills()
        context_snapshot = None
        if self._context:
            # 可选：传入最近消息/结果摘要供 LLM 参考
            context_snapshot = getattr(self._context, "_messages", [])[-10:]
        plan_step = llm_module.call_llm_for_plan(
            request_stripped,
            agents_and_skills,
            context_snapshot=context_snapshot,
        )
        return plan_step

    def dispatch(self, plan_step: dict, task_id: str | None = None, user_request: str = "") -> TaskResult:
        """
        根据计划执行：分配给 sub-agent 时只传 task_description，由 sub-agent 自选技能；
        分配给 main 时传 skill + params 直接执行。
        """
        task_id = task_id or str(uuid.uuid4())
        agent_id = plan_step.get("agent_id", MAIN_AGENT_ID)
        task_description = (plan_step.get("task_description") or "").strip() or user_request

        if agent_id == MAIN_AGENT_ID:
            skill_name = plan_step.get("skill")
            params = plan_step.get("params") or {}
            found = self._registry.find_skill(skill_name)
            if not found:
                return TaskResult(
                    task_id=task_id,
                    status=TaskStatus.FAILURE,
                    error=ErrorInfo(code="SKILL_NOT_FOUND", message=f"未找到 Skill: {skill_name}"),
                )
            _, _, execute = found
            task = Task(task_id=task_id, skill=skill_name, params=params, context=None, task_description=None)
            try:
                result = execute(params)
                return TaskResult(
                    task_id=task_id,
                    status=result.status,
                    result=result.result,
                    error=result.error,
                )
            except Exception as e:
                return TaskResult(
                    task_id=task_id,
                    status=TaskStatus.FAILURE,
                    error=ErrorInfo(code="SKILL_ERROR", message=str(e)),
                )

        sub_agent = self._sub_agents.get(agent_id)
        if not sub_agent:
            return TaskResult(
                task_id=task_id,
                status=TaskStatus.FAILURE,
                error=ErrorInfo(code="AGENT_NOT_FOUND", message=f"未找到 Sub-Agent: {agent_id}"),
            )
        task = Task(
            task_id=task_id,
            skill="",
            params={},
            context=None,
            task_description=task_description or user_request,
        )
        return sub_agent.run(task)

    def request(self, user_request: str) -> TaskResult:
        """接收用户或上层请求：规划 -> 下发 -> 处理返回并判定是否完成 -> 若未完成则下一步计划并再次下发。"""
        if self._context:
            self._context.add_message("user", user_request)
        plan_step = self.plan(user_request)
        if not plan_step:
            if self._context:
                self._context.add_message("system", "无法生成执行计划")
            return TaskResult(
                task_id="",
                status=TaskStatus.FAILURE,
                error=ErrorInfo(code="NO_PLAN", message="无法根据请求生成执行计划"),
            )
        if self._context:
            self._context.set_plan(plan_step)
        res = self.dispatch(plan_step, user_request=user_request)
        if self._context:
            self._context.add_result(
                res.task_id, res.status.value, result=res.result, error=res.error
            )
        if self._experience_path and plan_step:
            append_experience(
                self._experience_path,
                skill=plan_step.get("skill", ""),
                params_type="default",
                request_type="general",
                status=res.status.value,
            )
        # 主控处理返回并判定是否完成；若未完成则进行下一步计划并再次下发（最多一步）
        last_error = None
        if res.error:
            last_error = {"code": getattr(res.error, "code", ""), "message": getattr(res.error, "message", "")}
        done = llm_module.call_llm_evaluate_completion(
            user_request,
            last_result=res.result if res.result else None,
            last_error=last_error,
            context_snapshot=getattr(self._context, "_messages", [])[-10:] if self._context else None,
        )
        if done:
            return res
        if self._context:
            self._context.add_message(
                "system",
                f"上一步执行结果：{json.dumps(res.result or {}, ensure_ascii=False)}；错误：{last_error or '无'}",
            )
        next_plan = self.plan(user_request)
        if not next_plan:
            return res
        if self._context:
            self._context.set_plan(next_plan)
        next_res = self.dispatch(next_plan, user_request=user_request)
        if self._context:
            self._context.add_result(
                next_res.task_id, next_res.status.value, result=next_res.result, error=next_res.error
            )
        return next_res
