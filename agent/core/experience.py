# -*- coding: utf-8 -*-
"""
经验存储与查询：任务结果、成功/失败、可选用户反馈；规划时可供参考。
"""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any


def _default_store_path(agent_root: Path) -> Path:
    return agent_root / "experience" / "store.json"


def load_experiences(store_path: Path) -> list[dict]:
    """从文件加载经验列表。"""
    if not store_path.exists():
        return []
    try:
        data = store_path.read_text(encoding="utf-8")
        return json.loads(data) if data.strip() else []
    except Exception:
        return []


def save_experiences(store_path: Path, records: list[dict]) -> None:
    """写入经验列表到文件。"""
    store_path.parent.mkdir(parents=True, exist_ok=True)
    store_path.write_text(json.dumps(records, ensure_ascii=False, indent=2), encoding="utf-8")


def append_experience(
    store_path: Path,
    skill: str,
    params_type: str,
    request_type: str,
    status: str,
    feedback: str | None = None,
) -> None:
    """沉淀一条经验。"""
    records = load_experiences(store_path)
    records.append({
        "skill": skill,
        "params_type": params_type,
        "request_type": request_type,
        "status": status,
        "feedback": feedback,
    })
    save_experiences(store_path, records)


def query_successful_skills(store_path: Path, request_type: str | None = None) -> list[str]:
    """查询历史上成功的 skill 名称（可选按 request_type 过滤）。"""
    records = load_experiences(store_path)
    out = []
    seen = set()
    for r in reversed(records):
        if r.get("status") != "success":
            continue
        if request_type and r.get("request_type") != request_type:
            continue
        s = r.get("skill", "")
        if s and s not in seen:
            seen.add(s)
            out.append(s)
    return out


def query_failed_combinations(store_path: Path) -> list[tuple[str, str]]:
    """查询曾失败的 (skill, request_type) 组合。"""
    records = load_experiences(store_path)
    out = []
    seen = set()
    for r in reversed(records):
        if r.get("status") != "failure":
            continue
        key = (r.get("skill", ""), r.get("request_type", ""))
        if key not in seen:
            seen.add(key)
            out.append(key)
    return out
