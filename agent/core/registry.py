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
    """Agent 与 Skill 注册表，按所属 Agent 区分；各 Agent 可注册职责描述，供主控分配工作。"""

    def __init__(self) -> None:
        # agent_id -> [(SkillDescriptor, execute), ...]
        self._agents: dict[str, list[tuple[SkillDescriptor, SkillExecute]]] = {}
        # agent_id -> 该 Agent 负责工作的描述（主控根据此分配任务）
        self._agent_descriptions: dict[str, str] = {}

    def register_agent(
        self,
        agent_id: str,
        skills: list[tuple[SkillDescriptor, SkillExecute]],
        description: str | None = None,
    ) -> None:
        """注册 Agent 及其 Skill 列表；可选 description 为该 Agent 负责工作的描述，供主控分配时参考。"""
        self._agents[agent_id] = list(skills)
        if description is not None:
            self._agent_descriptions[agent_id] = description

    def set_agent_description(self, agent_id: str, description: str) -> None:
        """设置或更新某 Agent 的职责描述。"""
        self._agent_descriptions[agent_id] = description

    def get_agent_description(self, agent_id: str) -> str:
        """返回某 Agent 的职责描述，未设置则返回空字符串。"""
        return self._agent_descriptions.get(agent_id, "")

    def list_agents_and_skills(self) -> list[tuple[str, str, list[SkillDescriptor]]]:
        """返回 (agent_id, 职责描述, 该 Agent 下 SkillDescriptor 列表)，供主控根据职责分配工作。"""
        result: list[tuple[str, str, list[SkillDescriptor]]] = []
        for agent_id, skill_list in self._agents.items():
            desc_text = self._agent_descriptions.get(agent_id, "")
            descriptors = [desc for desc, _ in skill_list]
            result.append((agent_id, desc_text, descriptors))
        return result

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
