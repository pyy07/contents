# -*- coding: utf-8 -*-
"""
Core 契约类型：任务、结果、Skill 描述等，供主 Agent 与 Sub-Agent 解耦。
"""
from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any


class TaskStatus(str, Enum):
    """任务执行状态。"""
    SUCCESS = "success"
    FAILURE = "failure"


@dataclass
class ErrorInfo:
    """失败时的错误信息。"""
    code: str = ""
    message: str = ""
    details: dict[str, Any] = field(default_factory=dict)


@dataclass
class Task:
    """主 Agent 下发的任务消息。"""
    task_id: str
    skill: str
    params: dict[str, Any]
    context: dict[str, Any] | None = None


@dataclass
class TaskResult:
    """Sub-Agent 或 Skill 返回的结果消息。"""
    task_id: str
    status: TaskStatus
    result: dict[str, Any] | None = None
    error: ErrorInfo | None = None


@dataclass
class SkillDescriptor:
    """Skill 描述结构，供注册与发现。"""
    name: str
    description: str
    sub_agent: str  # 所属 Agent 标识，主 Agent 可为 "main" 或 "orchestrator"
    input_schema: dict[str, Any]  # 参数 schema，如 {"limit": {"type": "integer"}, "save": {"type": "boolean"}}
