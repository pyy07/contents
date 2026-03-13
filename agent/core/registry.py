# -*- coding: utf-8 -*-
"""
Registry：Agent 与 Skill 的注册与按名称/描述查询。
"""
from __future__ import annotations

from typing import Callable

from .types import SkillDescriptor, TaskResult

# Skill 执行函数：(params) -> TaskResult
SkillExecute = Callable[[dict], TaskResult]


class Registry:
    """Agent 与 Skill 注册表，按所属 Agent 区分，支持按 skill name 或描述匹配查询。"""

    def __init__(self) -> None:
        # agent_id -> [(SkillDescriptor, execute), ...]
        self._agents: dict[str, list[tuple[SkillDescriptor, SkillExecute]]] = {}

    def register_agent(
        self,
        agent_id: str,
        skills: list[tuple[SkillDescriptor, SkillExecute]],
    ) -> None:
        """注册 Agent 及其 Skill 列表（描述 + 执行入口）。同一 agent_id 多次调用会追加或覆盖，此处采用覆盖。"""
        self._agents[agent_id] = list(skills)

    def register_skills(self, agent_id: str, skills: list[tuple[SkillDescriptor, SkillExecute]]) -> None:
        """向已存在的 Agent 追加 Skill；若 agent_id 不存在则等同于 register_agent。"""
        if agent_id not in self._agents:
            self._agents[agent_id] = []
        self._agents[agent_id].extend(skills)

    def find_skill(self, skill_name: str) -> tuple[str, SkillDescriptor, SkillExecute] | None:
        """按 skill 名称精确匹配，返回 (agent_id, descriptor, execute)；未找到返回 None。"""
        for agent_id, skill_list in self._agents.items():
            for desc, execute in skill_list:
                if desc.name == skill_name:
                    return (agent_id, desc, execute)
        return None

    def find_by_description(self, query: str) -> list[tuple[str, SkillDescriptor, SkillExecute]]:
        """按描述或 name 包含 query 匹配，返回 [(agent_id, descriptor, execute), ...]。"""
        query_lower = query.strip().lower()
        if not query_lower:
            return []
        out: list[tuple[str, SkillDescriptor, SkillExecute]] = []
        for agent_id, skill_list in self._agents.items():
            for desc, execute in skill_list:
                if query_lower in desc.description.lower() or query_lower in desc.name.lower():
                    out.append((agent_id, desc, execute))
        return out

    def list_skills(self) -> list[tuple[str, SkillDescriptor]]:
        """列出所有已注册的 (agent_id, descriptor)。"""
        result: list[tuple[str, SkillDescriptor]] = []
        for agent_id, skill_list in self._agents.items():
            for desc, _ in skill_list:
                result.append((agent_id, desc))
        return result

    def list_skills_for_agent(self, agent_id: str) -> list[tuple[SkillDescriptor, SkillExecute]]:
        """返回某 Agent 的全部 Skill（描述 + 执行函数）。"""
        return list(self._agents.get(agent_id, []))
