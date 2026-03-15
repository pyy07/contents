# -*- coding: utf-8 -*-
"""
LLM 调用层：主 Agent 规划阶段通过 OpenAI 兼容 API 生成执行计划。
主控 Agent 的主要责任是识别工作应由哪个 sub-agent（或 main）完成，并判定用户需求是否已满足、若未完成则尽量完成任务；提示词据此设计。
"""
from __future__ import annotations

import json
import re
from typing import Any
from urllib.request import Request, urlopen

from .config import get_llm_config

# 规划输出：分配给 sub-agent 时只输出 agent_id + task_description；分配给 main 时输出 agent_id + skill + params
PLAN_OUTPUT_SUB = '{"agent_id": "<info|...>", "task_description": "<用户请求或任务摘要>"}'
PLAN_OUTPUT_MAIN = '{"agent_id": "main", "skill": "<skill_name>", "params": {...}}'


def _build_system_prompt() -> str:
    """系统提示：角色与职责、输出格式约束。"""
    return """你是主控 Agent 的规划模块。你的主要责任是：

1. **只把任务分配给 Agent**：根据各 Agent 的职责描述，判断当前请求应该交给哪个 Agent（main 或某个 sub-agent）。**不要**替 sub-agent 指定使用何种技能——分配给 sub-agent 时只给出 agent_id 和 task_description，由 sub-agent 自行决定用哪个技能完成任务。
2. **仅对 main 指定技能**：当工作由主 Agent 自身（main）完成时（如读写文件、运行代码等内置工具），你才需要指定 skill 与 params；此时 agent_id 为 "main"，skill 与 params 必须与下方 main 的技能列表一致。
3. **处理返回并判定是否完成**：结合上下文与子 Agent 的返回，判断用户需求是否已满足；若未满足，可进行下一步计划（再次分配任务）。

输出规则：
- 分配给 **sub-agent**（agent_id 不为 "main"）：只输出 agent_id 和 task_description，不要输出 skill、params。
- 分配给 **main**：输出 agent_id="main" 以及 skill、params（从下方 main 的技能中选）。

你必须仅输出一个 JSON 对象，不要输出其他文字、解释或 markdown 标记。格式示例：
""" + PLAN_OUTPUT_SUB + """

或（当由 main 执行时）：
""" + PLAN_OUTPUT_MAIN


def _format_agents_and_skills_for_prompt(agents_and_skills: list[tuple[str, str, list[Any]]]) -> str:
    """将 (agent_id, 职责描述, [SkillDescriptor, ...]) 格式化为供模型阅读的文本，主控根据职责分配工作。"""
    lines = []
    for agent_id, responsibility, descriptors in agents_and_skills:
        desc_text = responsibility.strip() if responsibility else "（未填写职责描述）"
        lines.append(f"**Agent {agent_id}**（职责：{desc_text}）")
        for desc in descriptors:
            name = getattr(desc, "name", str(desc))
            description = getattr(desc, "description", "")
            schema = getattr(desc, "input_schema", {})
            lines.append(f"  - skill name: {name}, description: {description}, input_schema: {schema}")
        lines.append("")
    return "\n".join(lines).strip() if lines else "（当前无可用 Agent/技能）"


def _extract_json_from_content(content: str) -> dict | None:
    """从模型返回内容中提取 JSON；支持被 ```json ... ``` 包裹。"""
    text = (content or "").strip()
    # 尝试去掉 ```json ... ``` 包裹
    match = re.search(r"```(?:json)?\s*([\s\S]*?)\s*```", text)
    if match:
        text = match.group(1).strip()
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        return None


def _chat_completion(
    api_key: str,
    base_url: str,
    model: str,
    messages: list[dict[str, str]],
) -> str | None:
    """调用 OpenAI 兼容的 /v1/chat/completions，返回 content 或 None。"""
    url = base_url.rstrip("/") + "/chat/completions"
    payload = {
        "model": model or "gpt-4o-mini",
        "messages": messages,
        "temperature": 0.2,
        "max_tokens": 1024,
    }
    body = json.dumps(payload).encode("utf-8")
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}",
    }
    try:
        req = Request(url, data=body, headers=headers, method="POST")
        with urlopen(req, timeout=60) as resp:
            data = json.loads(resp.read().decode())
        choices = data.get("choices")
        if not choices:
            return None
        return choices[0].get("message", {}).get("content")
    except Exception:
        return None


def call_llm_for_plan(
    user_request: str,
    agents_and_skills: list[tuple[str, str, list[Any]]],
    context_snapshot: list[dict] | None = None,
) -> dict | None:
    """
    使用 LLM 根据用户请求与各 Agent 的职责描述生成单步执行计划。
    分配给 sub-agent 时只返回 agent_id + task_description（不指定技能）；分配给 main 时返回 agent_id + skill + params。
    """
    cfg = get_llm_config("main")
    if not cfg.is_configured():
        return None
    api_key = cfg.api_key or ""
    raw_base = (cfg.base_url or "https://api.openai.com").rstrip("/")
    base_url = raw_base if raw_base.endswith("/v1") else raw_base + "/v1"
    model = cfg.model or "gpt-4o-mini"

    valid_agent_ids = set()
    main_skills = {}  # skill_name -> agent_id (main)
    for agent_id, _, descriptors in agents_and_skills:
        valid_agent_ids.add(agent_id)
        if agent_id == "main":
            for desc in descriptors:
                name = getattr(desc, "name", "")
                if name:
                    main_skills[name] = agent_id

    system_content = _build_system_prompt()
    agents_text = _format_agents_and_skills_for_prompt(agents_and_skills)
    user_content = f"各 Agent 及其负责工作与技能：\n{agents_text}\n\n用户请求：{user_request}"
    if context_snapshot:
        user_content += f"\n\n近期上下文（供参考）：\n{json.dumps(context_snapshot, ensure_ascii=False, indent=2)}"

    messages = [
        {"role": "system", "content": system_content},
        {"role": "user", "content": user_content},
    ]
    content = _chat_completion(api_key, base_url, model, messages)
    if not content:
        return None

    plan = _extract_json_from_content(content)
    if not plan or not isinstance(plan, dict):
        return None
    agent_id = (plan.get("agent_id") or "").strip()
    if not agent_id or agent_id not in valid_agent_ids:
        return None

    if agent_id == "main":
        skill_name = plan.get("skill")
        if not skill_name or skill_name not in main_skills:
            return None
        params = plan.get("params")
        if not isinstance(params, dict):
            params = {}
        return {"agent_id": "main", "skill": skill_name, "params": params}
    # sub-agent：只接受 agent_id + task_description
    task_description = plan.get("task_description") or ""
    if isinstance(task_description, dict):
        task_description = json.dumps(task_description, ensure_ascii=False)
    task_description = str(task_description).strip() or user_request
    return {"agent_id": agent_id, "task_description": task_description}


def call_llm_evaluate_completion(
    user_request: str,
    last_result: dict | None,
    last_error: dict | None,
    context_snapshot: list[dict] | None = None,
) -> bool:
    """
    主控根据用户请求与子 Agent 返回结果，判定用户需求是否已满足。
    返回 True 表示已完成，False 表示未完成、需进行下一步计划。
    """
    cfg = get_llm_config("main")
    if not cfg.is_configured():
        return True  # 无 LLM 时默认视为完成，不再继续
    api_key = cfg.api_key or ""
    raw_base = (cfg.base_url or "https://api.openai.com").rstrip("/")
    base_url = raw_base if raw_base.endswith("/v1") else raw_base + "/v1"
    model = cfg.model or "gpt-4o-mini"

    system_content = """你是主控 Agent 的评估模块。根据用户原始请求与当前已得到的执行结果，判定用户需求是否已经满足。
只回答一个词：DONE 或 NOT_DONE。不要输出其他内容、解释或 markdown。"""
    user_content = f"用户请求：{user_request}\n\n当前执行结果：{json.dumps(last_result or {}, ensure_ascii=False)}\n错误信息（若有）：{json.dumps(last_error or {}, ensure_ascii=False)}"
    if context_snapshot:
        user_content += f"\n\n近期上下文：\n{json.dumps(context_snapshot, ensure_ascii=False, indent=2)}"

    messages = [
        {"role": "system", "content": system_content},
        {"role": "user", "content": user_content},
    ]
    content = _chat_completion(api_key, base_url, model, messages)
    if not content:
        return True
    return "DONE" in (content or "").strip().upper()
