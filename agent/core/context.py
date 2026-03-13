# -*- coding: utf-8 -*-
"""
上下文存储与自动 compact：历史消息、任务结果、计划，超阈值时摘要或截断。
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass
class ContextConfig:
    """compact 策略配置。"""
    max_entries: int = 100
    max_chars: int = 50_000
    keep_recent: int = 20
    summary_prefix: str = "[摘要] "


@dataclass
class AgentContext:
    """单 Agent 的上下文：历史消息、任务结果、当前计划。"""

    def __init__(self, agent_id: str, config: ContextConfig | None = None):
        self.agent_id = agent_id
        self.config = config or ContextConfig()
        self._messages: list[dict[str, Any]] = []
        self._results: list[dict[str, Any]] = []
        self._plan: dict[str, Any] | None = None

    def add_message(self, role: str, content: str | dict) -> None:
        self._messages.append({"role": role, "content": content})
        self._maybe_compact()

    def add_result(self, task_id: str, status: str, result: Any = None, error: Any = None) -> None:
        self._results.append({"task_id": task_id, "status": status, "result": result, "error": error})
        self._maybe_compact()

    def set_plan(self, plan: dict | None) -> None:
        self._plan = plan

    def get_messages(self) -> list[dict]:
        return list(self._messages)

    def get_results(self) -> list[dict]:
        return list(self._results)

    def get_plan(self) -> dict | None:
        return self._plan

    def _total_entries(self) -> int:
        return len(self._messages) + len(self._results)

    def _total_chars(self) -> int:
        def size(x):
            if isinstance(x, str):
                return len(x)
            if isinstance(x, dict):
                return sum(size(v) for v in x.values())
            if isinstance(x, list):
                return sum(size(i) for i in x)
            return 0
        return sum(size(m) for m in self._messages) + sum(size(r) for r in self._results)

    def _maybe_compact(self) -> None:
        cfg = self.config
        if self._total_entries() <= cfg.max_entries and self._total_chars() <= cfg.max_chars:
            return
        # 滑动窗口：保留最近 keep_recent 条，较早的合并为一条摘要
        if len(self._messages) > cfg.keep_recent:
            old = self._messages[:-cfg.keep_recent]
            summary = {"role": "system", "content": cfg.summary_prefix + f"此前 {len(old)} 条消息已压缩"}
            self._messages = [summary] + self._messages[-cfg.keep_recent:]
        if len(self._results) > cfg.keep_recent:
            self._results = self._results[-cfg.keep_recent:]
