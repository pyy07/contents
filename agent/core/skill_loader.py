# -*- coding: utf-8 -*-
"""
Skill 加载机制：从约定目录扫描并注册符合契约的 Skill，无需硬编码。
约定：sub_agents/<domain>/skills/ 下每模块导出 name、description、input_schema、execute。
"""
from __future__ import annotations

import importlib.util
import sys
from pathlib import Path
from typing import TYPE_CHECKING, Callable

from .registry import Registry, SkillExecute
from .types import SkillDescriptor, TaskResult

if TYPE_CHECKING:
    pass

# 契约要求的模块属性
REQUIRED_ATTRS = ("name", "description", "input_schema", "execute")


def _load_skill_from_file(
    file_path: Path,
    sub_agent_id: str,
) -> tuple[SkillDescriptor, Callable[..., object]] | None:
    """从单文件加载 Skill，返回 (SkillDescriptor, execute_callable 所在类或模块) 或 None。"""
    spec = importlib.util.spec_from_file_location(
        f"skill_{file_path.stem}",
        file_path,
        submodule_search_locations=[str(file_path.parent)],
    )
    if spec is None or spec.loader is None:
        return None
    mod = importlib.util.module_from_spec(spec)
    # 将 agent 包所在路径加入，便于 skill 内 import agent.core 等
    try:
        spec.loader.exec_module(mod)
    except Exception:
        return None
    for attr in REQUIRED_ATTRS:
        if not hasattr(mod, attr):
            return None
    name = getattr(mod, "name")
    description = getattr(mod, "description")
    input_schema = getattr(mod, "input_schema")
    execute = getattr(mod, "execute")
    if not callable(execute):
        return None
    desc = SkillDescriptor(
        name=name,
        description=description,
        sub_agent=sub_agent_id,
        input_schema=input_schema if isinstance(input_schema, dict) else {},
    )
    return (desc, execute)


def _ensure_task_result(value: object) -> TaskResult:
    """若 execute 返回 dict，转为 TaskResult；已是 TaskResult 则返回。"""
    from .types import ErrorInfo, TaskStatus

    if isinstance(value, TaskResult):
        return value
    if isinstance(value, dict):
        task_id = value.get("task_id", "")
        status = TaskStatus.SUCCESS if value.get("status") == "success" else TaskStatus.FAILURE
        result = value.get("result")
        err = value.get("error")
        if isinstance(err, dict):
            error_info = ErrorInfo(
                code=err.get("code", ""),
                message=err.get("message", ""),
                details=err.get("details", {}),
            )
        else:
            error_info = None
        return TaskResult(task_id=task_id, status=status, result=result, error=error_info)
    return TaskResult(
        task_id="",
        status=TaskStatus.FAILURE,
        error=ErrorInfo(message="Skill 返回格式无效"),
    )


def load_skills_from_sub_agents(agent_root: Path, registry: Registry) -> int:
    """
    从 agent_root/sub_agents/<domain>/skills/ 扫描 .py 文件，加载符合契约的 Skill 并注册到 registry。
    同一 domain 下本次扫描到的 skills 会先清空再注册（便于刷新时覆盖）。返回成功注册的 Skill 数量。
    """
    sub_agents_dir = agent_root / "sub_agents"
    if not sub_agents_dir.is_dir():
        return 0
    # 保证 agent 包可被导入
    agent_parent = agent_root.parent
    if str(agent_parent) not in sys.path:
        sys.path.insert(0, str(agent_parent))

    domains_to_load: dict[str, list[tuple[SkillDescriptor, SkillExecute]]] = {}
    for domain_dir in sub_agents_dir.iterdir():
        if not domain_dir.is_dir():
            continue
        domain_id = domain_dir.name
        skills_dir = domain_dir / "skills"
        if not skills_dir.is_dir():
            continue
        domains_to_load.setdefault(domain_id, [])
        for py_file in skills_dir.glob("*.py"):
            if py_file.name.startswith("_"):
                continue
            loaded = _load_skill_from_file(py_file, domain_id)
            if loaded is None:
                continue
            desc, execute_fn = loaded

            def _wrap(ef):  # 闭包绑定执行函数
                def _run(params: dict) -> TaskResult:
                    out = ef(params)
                    return _ensure_task_result(out)
                return _run

            wrapped = _wrap(execute_fn)
            domains_to_load[domain_id].append((desc, wrapped))

    count = 0
    for domain_id, skills in domains_to_load.items():
        if not skills:
            continue
        registry.register_agent(domain_id, skills)
        count += len(skills)
    return count
