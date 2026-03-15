# -*- coding: utf-8 -*-
"""
Sub-Agent 基类：接收任务消息。主控只分配任务（task_description），由本 Agent 自行决定使用何种技能并执行。
"""
from __future__ import annotations

from .types import Task, TaskResult, TaskStatus, ErrorInfo
from .registry import Registry


def _default_params_for_skill(skill_name: str) -> dict:
    """返回某 Skill 的默认 params，与 Orchestrator 原逻辑一致。"""
    if skill_name == "zhihu_hot":
        return {"limit": 10, "save": False}
    return {}


class SubAgent:
    """Sub-Agent：主控只下发 task_description，本 Agent 根据描述自选技能并执行，返回 TaskResult。"""

    def __init__(self, agent_id: str, registry: Registry) -> None:
        self.agent_id = agent_id
        self._registry = registry

    def run(self, task: Task) -> TaskResult:
        """接收任务。若带 task_description 且无 skill，则根据描述自选技能与参数并执行；否则按 task.skill 执行。"""
        skill_name = (task.skill or "").strip()
        params = task.params or {}
        if (task.task_description or "").strip() and not skill_name:
            # 主控只分配了任务描述，由本 Agent 自选技能
            query = (task.task_description or "").strip().lower()
            candidates = self._registry.find_by_description(query)
            for aid, desc, _ in candidates:
                if aid != self.agent_id:
                    continue
                skill_name = desc.name
                params = _default_params_for_skill(skill_name)
                break
            if not skill_name:
                return TaskResult(
                    task_id=task.task_id,
                    status=TaskStatus.FAILURE,
                    error=ErrorInfo(
                        code="NO_MATCHING_SKILL",
                        message="根据任务描述未找到本 Agent 下可用的技能",
                    ),
                )
        found = self._registry.find_skill(skill_name)
        if not found:
            return TaskResult(
                task_id=task.task_id,
                status=TaskStatus.FAILURE,
                error=ErrorInfo(
                    code="SKILL_NOT_FOUND",
                    message=f"未找到 Skill: {task.skill}",
                ),
            )
        agent_id, _, execute = found
        if agent_id != self.agent_id:
            return TaskResult(
                task_id=task.task_id,
                status=TaskStatus.FAILURE,
                error=ErrorInfo(
                    code="SKILL_NOT_OWNED",
                    message=f"Skill {task.skill} 不属于本 Agent",
                ),
            )
        try:
            result = execute(task.params)
            return TaskResult(
                task_id=task.task_id,
                status=result.status,
                result=result.result,
                error=result.error,
            )
        except Exception as e:
            return TaskResult(
                task_id=task.task_id,
                status=TaskStatus.FAILURE,
                error=ErrorInfo(code="SKILL_ERROR", message=str(e)),
            )
