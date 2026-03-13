# -*- coding: utf-8 -*-
"""
Sub-Agent 基类：接收任务消息，按 task.skill 路由到对应 Skill，执行后返回约定格式的结果。
"""
from __future__ import annotations

from .types import Task, TaskResult, TaskStatus, ErrorInfo
from .registry import Registry


class SubAgent:
    """Sub-Agent：按 task.skill 从 Registry 路由到对应 Skill 并执行，返回 TaskResult。"""

    def __init__(self, agent_id: str, registry: Registry) -> None:
        self.agent_id = agent_id
        self._registry = registry

    def run(self, task: Task) -> TaskResult:
        """接收任务，按 task.skill 从 Registry 查找并执行，返回约定格式的结果消息。"""
        found = self._registry.find_skill(task.skill)
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
