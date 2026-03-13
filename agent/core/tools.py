# -*- coding: utf-8 -*-
"""
内置工具：run_code、list_dir、read_file、write_file。
路径在项目目录内直接执行，项目外返回需授权提示（不执行）。
"""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path
from typing import Callable

from .types import TaskResult, TaskStatus, ErrorInfo
from .orchestrator import MAIN_AGENT_ID

# 工具执行函数：(params, project_root, path_allowed?) -> TaskResult
PathAllowed = Callable[[Path | None], bool]


def _resolve_path(path_str: str, project_root: Path) -> Path:
    p = Path(path_str)
    if not p.is_absolute():
        p = (project_root / p).resolve()
    return p.resolve()


def _in_project(path: Path, project_root: Path) -> bool:
    try:
        path.resolve().relative_to(project_root.resolve())
        return True
    except ValueError:
        return False


def _path_check(path: Path | None, project_root: Path, path_allowed: PathAllowed) -> tuple[bool, str]:
    """返回 (是否允许, 错误信息)。"""
    if path is None:
        return True, ""
    if _in_project(path, project_root):
        return True, ""
    if path_allowed(path):
        return True, ""
    return False, "访问项目外路径需用户授权"


def run_code_impl(
    params: dict,
    project_root: Path,
    path_allowed: PathAllowed,
) -> TaskResult:
    """执行代码工具：code[, workdir[, timeout]]。"""
    code = params.get("code") or ""
    workdir = params.get("workdir")
    timeout = params.get("timeout", 30)
    if not code:
        return TaskResult(
            task_id="",
            status=TaskStatus.FAILURE,
            error=ErrorInfo(code="INVALID_PARAMS", message="缺少 code 参数"),
        )
    cwd = None
    if workdir:
        cwd = _resolve_path(workdir, project_root)
        ok, err = _path_check(cwd, project_root, path_allowed)
        if not ok:
            return TaskResult(
                task_id="",
                status=TaskStatus.FAILURE,
                error=ErrorInfo(code="PATH_NOT_ALLOWED", message=err),
            )
    try:
        r = subprocess.run(
            [sys.executable, "-c", code],
            capture_output=True,
            text=True,
            timeout=timeout,
            cwd=cwd,
        )
        return TaskResult(
            task_id="",
            status=TaskStatus.SUCCESS,
            result={
                "stdout": r.stdout or "",
                "stderr": r.stderr or "",
                "returncode": r.returncode,
            },
        )
    except subprocess.TimeoutExpired:
        return TaskResult(
            task_id="",
            status=TaskStatus.FAILURE,
            error=ErrorInfo(code="TIMEOUT", message="执行超时"),
        )
    except Exception as e:
        return TaskResult(
            task_id="",
            status=TaskStatus.FAILURE,
            error=ErrorInfo(code="RUN_ERROR", message=str(e)),
        )


def list_dir_impl(
    params: dict,
    project_root: Path,
    path_allowed: PathAllowed,
) -> TaskResult:
    """列出目录/文件工具。"""
    path_str = params.get("path", ".")
    p = _resolve_path(path_str, project_root)
    ok, err = _path_check(p, project_root, path_allowed)
    if not ok:
        return TaskResult(task_id="", status=TaskStatus.FAILURE, error=ErrorInfo(code="PATH_NOT_ALLOWED", message=err))
    if not p.exists():
        return TaskResult(task_id="", status=TaskStatus.FAILURE, error=ErrorInfo(code="NOT_FOUND", message="路径不存在"))
    if not p.is_dir():
        return TaskResult(task_id="", status=TaskStatus.FAILURE, error=ErrorInfo(code="NOT_DIR", message="路径不是目录"))
    try:
        entries = [
            {"name": e.name, "is_dir": e.is_dir()}
            for e in sorted(p.iterdir(), key=lambda x: (not x.is_dir(), x.name.lower()))
        ]
        return TaskResult(task_id="", status=TaskStatus.SUCCESS, result={"path": str(p), "entries": entries})
    except Exception as e:
        return TaskResult(task_id="", status=TaskStatus.FAILURE, error=ErrorInfo(code="LIST_ERROR", message=str(e)))


def read_file_impl(
    params: dict,
    project_root: Path,
    path_allowed: PathAllowed,
) -> TaskResult:
    """读取文件工具。"""
    path_str = params.get("path", "")
    if not path_str:
        return TaskResult(task_id="", status=TaskStatus.FAILURE, error=ErrorInfo(code="INVALID_PARAMS", message="缺少 path"))
    p = _resolve_path(path_str, project_root)
    ok, err = _path_check(p, project_root, path_allowed)
    if not ok:
        return TaskResult(task_id="", status=TaskStatus.FAILURE, error=ErrorInfo(code="PATH_NOT_ALLOWED", message=err))
    if not p.exists() or not p.is_file():
        return TaskResult(task_id="", status=TaskStatus.FAILURE, error=ErrorInfo(code="NOT_FOUND", message="文件不存在"))
    try:
        content = p.read_text(encoding="utf-8", errors="replace")
        return TaskResult(task_id="", status=TaskStatus.SUCCESS, result={"path": str(p), "content": content})
    except Exception as e:
        return TaskResult(task_id="", status=TaskStatus.FAILURE, error=ErrorInfo(code="READ_ERROR", message=str(e)))


def write_file_impl(
    params: dict,
    project_root: Path,
    path_allowed: PathAllowed,
) -> TaskResult:
    """写入文件工具。"""
    path_str = params.get("path", "")
    content = params.get("content", "")
    if not path_str:
        return TaskResult(task_id="", status=TaskStatus.FAILURE, error=ErrorInfo(code="INVALID_PARAMS", message="缺少 path"))
    p = _resolve_path(path_str, project_root)
    ok, err = _path_check(p, project_root, path_allowed)
    if not ok:
        return TaskResult(task_id="", status=TaskStatus.FAILURE, error=ErrorInfo(code="PATH_NOT_ALLOWED", message=err))
    try:
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(content, encoding="utf-8")
        return TaskResult(task_id="", status=TaskStatus.SUCCESS, result={"path": str(p), "written": True})
    except Exception as e:
        return TaskResult(task_id="", status=TaskStatus.FAILURE, error=ErrorInfo(code="WRITE_ERROR", message=str(e)))


# 工具描述与参数 schema，供注册为 main Agent 的 Skill
BUILTIN_TOOLS: list[tuple[dict, Callable]] = [
    (
        {
            "name": "run_code",
            "description": "在受控环境中执行 Python 代码片段；可选 workdir（项目内直接执行，项目外需授权）、timeout。",
            "input_schema": {
                "code": {"type": "string", "description": "Python 代码"},
                "workdir": {"type": "string", "description": "工作目录，可选"},
                "timeout": {"type": "integer", "description": "超时秒数", "default": 30},
            },
        },
        run_code_impl,
    ),
    (
        {
            "name": "list_dir",
            "description": "列出指定路径下的目录与文件（名称、是否目录）；路径在项目内直接执行，项目外需授权。",
            "input_schema": {
                "path": {"type": "string", "description": "目录路径", "default": "."},
            },
        },
        list_dir_impl,
    ),
    (
        {
            "name": "read_file",
            "description": "读取指定路径的文本文件内容；路径在项目内直接执行，项目外需授权。",
            "input_schema": {
                "path": {"type": "string", "description": "文件路径"},
            },
        },
        read_file_impl,
    ),
    (
        {
            "name": "write_file",
            "description": "将内容写入指定路径；路径在项目内直接执行，项目外需授权。",
            "input_schema": {
                "path": {"type": "string", "description": "文件路径"},
                "content": {"type": "string", "description": "写入内容"},
            },
        },
        write_file_impl,
    ),
]


def register_builtin_tools(
    registry: "Registry",
    project_root: Path,
    path_allowed: PathAllowed | None = None,
) -> None:
    """将内置工具注册到 Registry，归属 main Agent。"""
    from .types import SkillDescriptor
    from .registry import SkillExecute

    path_allowed = path_allowed or (lambda _: False)
    skills: list[tuple[SkillDescriptor, SkillExecute]] = []
    for meta, impl in BUILTIN_TOOLS:
        def make_execute(i, proot, allowed):
            def execute(params: dict) -> TaskResult:
                return i(params, proot, allowed)
            return execute
        execute = make_execute(impl, project_root, path_allowed)
        desc = SkillDescriptor(
            name=meta["name"],
            description=meta["description"],
            sub_agent=MAIN_AGENT_ID,
            input_schema=meta["input_schema"],
        )
        skills.append((desc, execute))
    registry.register_skills(MAIN_AGENT_ID, skills)
