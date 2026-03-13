# -*- coding: utf-8 -*-
"""
主 Agent（Orchestrator）：接收请求、生成执行计划、下发任务、处理结果。
支持将任务分配给 Sub-Agent 或调用自身 Skill / 内置工具。
"""
from __future__ import annotations

import uuid
from pathlib import Path
from .types import Task, TaskResult, TaskStatus, ErrorInfo
from .registry import Registry
from .sub_agent import SubAgent
from .context import AgentContext, ContextConfig
from .experience import append_experience, query_successful_skills, query_failed_combinations


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
        首版为规则匹配；可参考经验（优先历史成功 Skill、避免曾失败组合）。
        """
        request_lower = (user_request or "").strip().lower()
        if not request_lower:
            return None
        failed_skills = set()
        if self._experience_path and self._experience_path.exists():
            for skill, _ in query_failed_combinations(self._experience_path):
                failed_skills.add(skill)
        # 先按描述匹配
        candidates = self._registry.find_by_description(request_lower)
        for agent_id, desc, _ in candidates:
            if desc.name in failed_skills:
                continue
            params = self._default_params(desc.name)
            return {"skill": desc.name, "params": params, "agent_id": agent_id}
        # 再按名称精确匹配常见意图
        if "知乎" in user_request or "热榜" in user_request or "热文" in user_request:
            found = self._registry.find_skill("zhihu_hot")
            if found:
                agent_id, desc, _ = found
                return {"skill": "zhihu_hot", "params": self._default_params("zhihu_hot"), "agent_id": agent_id}
        return None

    def _default_params(self, skill_name: str) -> dict:
        """返回某 Skill 的默认 params。"""
        if skill_name == "zhihu_hot":
            return {"limit": 10, "save": False}
        return {}

    def dispatch(self, plan_step: dict, task_id: str | None = None) -> TaskResult:
        """
        根据计划执行：若为目标 Sub-Agent 则构造任务并调用其 run；
        若为主 Agent 自身 Skill 或工具则本地调用 execute。
        """
        task_id = task_id or str(uuid.uuid4())
        skill_name = plan_step.get("skill")
        params = plan_step.get("params") or {}
        agent_id = plan_step.get("agent_id", MAIN_AGENT_ID)

        found = self._registry.find_skill(skill_name)
        if not found:
            return TaskResult(
                task_id=task_id,
                status=TaskStatus.FAILURE,
                error=ErrorInfo(code="SKILL_NOT_FOUND", message=f"未找到 Skill: {skill_name}"),
            )
        resolved_agent_id, _, execute = found
        if resolved_agent_id != agent_id:
            agent_id = resolved_agent_id

        task = Task(task_id=task_id, skill=skill_name, params=params, context=None)

        if agent_id == MAIN_AGENT_ID:
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
        return sub_agent.run(task)

    def request(self, user_request: str) -> TaskResult:
        """接收用户或上层请求：规划 -> 下发 -> 写上下文与经验 -> 返回结果。"""
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
        res = self.dispatch(plan_step)
        if self._context:
            self._context.add_result(
                res.task_id, res.status.value, result=res.result, error=res.error
            )
        if self._experience_path and plan_step:
            append_experience(
                self._experience_path,
                skill=plan_step.get("skill", ""),
                params_type="default",
                request_type="zhihu" if "知乎" in user_request or "热" in user_request else "general",
                status=res.status.value,
            )
        return res
