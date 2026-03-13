# -*- coding: utf-8 -*-
"""
zhihu_hot Skill：获取知乎当前热榜，入参 limit、save；输出 items、update_time。
符合 agent-info spec，供 skill_loader 发现并注册。
"""
from __future__ import annotations

import json
import sys
from datetime import datetime
from pathlib import Path
from urllib.request import Request, urlopen

# 契约：供加载器发现
name = "zhihu_hot"
description = "获取知乎当前热榜，可用于选题与写作素材；可选保存到 materials/links。"
input_schema = {
    "limit": {"type": "integer", "description": "最多返回条数", "default": 30},
    "save": {"type": "boolean", "description": "是否保存为 materials/links/zhihu-hot-YYYYMMDD.md", "default": False},
}

ZHIHU_HOT_API = "https://www.tianchenw.com/hot/zhihu/"
USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"


def _fetch_hot_list():
    """拉取知乎热榜，返回 (items, update_time) 或 (None, '') 表示失败。"""
    try:
        req = Request(ZHIHU_HOT_API, headers={"User-Agent": USER_AGENT})
        with urlopen(req, timeout=15) as r:
            data = json.loads(r.read().decode())
        if data.get("code") != 200 or "data" not in data:
            return None, "", 0
        return data["data"], data.get("updateTime", ""), data.get("total", 0)
    except Exception:
        return None, "", 0


def _format_hot(hot_num: int) -> str:
    if hot_num >= 1_000_000:
        return f"{hot_num / 1_000_000:.1f}M"
    if hot_num >= 1_000:
        return f"{hot_num / 1_000:.1f}K"
    return str(hot_num)


def _save_to_markdown(items: list, update_time: str, out_path: Path) -> None:
    if not items:
        return
    lines = [
        "# 知乎热榜",
        "",
        f"更新于: {update_time}",
        "",
        "| 排名 | 标题 | 热度 | 链接 |",
        "|------|------|------|------|",
    ]
    for item in items:
        idx = item.get("index", 0)
        title = (item.get("title", "") or "").replace("|", "\\|")
        hot = _format_hot(item.get("hot", 0))
        url = item.get("url", "")
        lines.append(f"| {idx} | {title} | {hot} | [链接]({url}) |")
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def execute(params: dict) -> dict:
    """
    执行 zhihu_hot：拉取热榜，可选保存。
    返回符合契约的 dict：status, result(items, update_time) 或 error。
    """
    limit = params.get("limit", 30)
    save = params.get("save", False)
    if not isinstance(limit, int) or limit <= 0:
        limit = 30
    items, update_time, _total = _fetch_hot_list()
    if items is None:
        return {
            "task_id": "",
            "status": "failure",
            "error": {"code": "FETCH_FAILED", "message": "拉取知乎热榜失败", "details": {}},
        }
    items = items[:limit]
    result = {
        "items": [
            {
                "index": i.get("index"),
                "title": i.get("title"),
                "hot": i.get("hot"),
                "url": i.get("url"),
            }
            for i in items
        ],
        "update_time": update_time,
        "count": len(items),
    }
    if save:
        # 项目根：假定从 contents 为根，skill 在 agent/sub_agents/info/skills/
        try:
            root = Path(__file__).resolve().parent.parent.parent.parent.parent
            out_path = root / "materials" / "links" / f"zhihu-hot-{datetime.now().strftime('%Y%m%d')}.md"
            _save_to_markdown(items, update_time, out_path)
            result["saved_path"] = str(out_path)
        except Exception as e:
            result["save_error"] = str(e)
    return {"task_id": "", "status": "success", "result": result}
