# -*- coding: utf-8 -*-
"""
Agent 运行配置：按 Agent 区分的 LLM 配置（API Key、Base URL、模型名）。
主 Agent 与各 Sub-Agent 可配置不同 LLM；当前未实际调用，为接入 LLM 时预留。
"""
from __future__ import annotations

import os
from dataclasses import dataclass


@dataclass
class LLMConfig:
    """单 Agent 的 LLM 配置。"""
    api_key: str | None
    base_url: str | None
    model: str | None

    def is_configured(self) -> bool:
        """是否已配置（至少具备可调用的 api_key 或 base_url）。"""
        return bool(self.api_key or self.base_url)


def _env(key: str, *alt_keys: str) -> str | None:
    """读取环境变量，可试多个键名。"""
    for k in (key, *alt_keys):
        v = os.environ.get(k)
        if v and v.strip():
            return v.strip()
    return None


def _agent_env_prefix(agent_id: str) -> str:
    """Agent 对应环境变量前缀，如 main -> LLM_MAIN_, info -> LLM_INFO_。"""
    safe = (agent_id or "main").strip().upper().replace("-", "_")
    return f"LLM_{safe}_"


def get_llm_config(agent_id: str) -> LLMConfig:
    """
    按 Agent 获取 LLM 配置。
    优先读取该 Agent 专属变量（LLM_<AGENT_ID>_API_KEY 等），未设置时回退到通用 LLM_*。
    agent_id 示例：main（主 Agent）、info（信息获取 Sub-Agent）。
    """
    prefix = _agent_env_prefix(agent_id)
    api_key = _env(
        f"{prefix}API_KEY",
        "LLM_API_KEY",
        "OPENAI_API_KEY",
    )
    base_url = _env(
        f"{prefix}BASE_URL",
        "LLM_BASE_URL",
        "OPENAI_BASE_URL",
    )
    model = _env(
        f"{prefix}MODEL",
        "LLM_MODEL",
        "OPENAI_MODEL",
    )
    return LLMConfig(api_key=api_key, base_url=base_url, model=model)


# 兼容：默认主 Agent 的配置（get_llm_config("main") 的快捷方式）
def _default_llm() -> LLMConfig:
    return get_llm_config("main")


llm_api_key: str | None = None
llm_base_url: str | None = None
llm_model: str | None = None


def _refresh_default_llm() -> None:
    global llm_api_key, llm_base_url, llm_model
    c = _default_llm()
    llm_api_key, llm_base_url, llm_model = c.api_key, c.base_url, c.model


_refresh_default_llm()
