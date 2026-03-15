# 设计：LLM 驱动 Agent 规划

## Context

- 主 Agent 当前通过 `Orchestrator.plan()` 做规则匹配（关键词 + `Registry.find_by_description`），无 LLM 调用。
- 已有 `get_llm_config("main")` 与 `LLM_*` / `OPENAI_*` 环境变量，需在规划路径中实际使用。
- 目标：用户请求仅由 LLM 理解并输出「应调用的 skill 名称 + params」；完全去掉规则匹配，无回退。

## Goals / Non-Goals

- **Goals**：主 Agent 规划仅由 LLM 驱动；使用现有 config；移除 Orchestrator 中全部规则匹配逻辑。
- **Non-Goals**：Sub-Agent 内部是否用 LLM 不在本变更范围；不实现多步/链式规划（首版仍为单步 plan）；不引入新配置格式（沿用环境变量）。

## Decisions

### 1. LLM 调用方式

- **决策**：使用 OpenAI 兼容的 Chat Completions API（`/v1/chat/completions`），通过 `base_url` + `api_key` + `model` 调用；由 `agent/core/config.get_llm_config("main")` 提供配置。
- **备选**：直接依赖 `openai` 包并设置 `OPENAI_API_BASE`；或抽象成「LLM 适配器」以支持多厂商。首版采用单一实现、通过 `base_url` 兼容其他兼容 API 的厂商，避免过度抽象。

### 2. 规划输出形态

- **决策**：LLM 输出结构化单步计划：`{"skill": "<name>", "params": {...}, "agent_id": "main"|"info"|...}`。通过 prompt 约束输出格式（如 JSON），解析后与现有 `plan_step` 一致，便于直接交给 `dispatch()`。
- **备选**：自然语言再解析。采用结构化输出可降低解析错误并复用现有 `dispatch` 逻辑。

### 3. Prompt 与上下文（精心设计以支撑主控与功能）

- **决策**：提示词须精心设计，确保模型能完成主控流程并选出正确 skill 与 params。Prompt 包含：(1) 角色与职责说明（主控 Agent 的定位与任务）；(2) 当前可用 Skill 列表（name + description，来自 `Registry.list_skills()`）；(3) 用户当前请求；(4) 明确要求仅输出指定结构的 JSON（如 `{"skill": "...", "params": {...}, "agent_id": "..."}`），便于解析与校验；(5) 可选：最近几轮 Context 中的消息与结果摘要。设计需在实现与文档中可追溯。
- **备选**：不注入 Context。首版可先不注入，后续在「可选」中增加 Context 摘要以支持多轮。

### 4. 无规则回退

- **决策**：完全去掉规则匹配逻辑。若 `get_llm_config("main").is_configured()` 为 False，或 LLM 调用抛错/超时/返回无法解析，则 `plan()` 返回 None，`request()` 返回失败结果；不执行任何关键词或 find_by_description 回退。
- **备选**：保留规则回退。已拒绝；仅保留 LLM 驱动。

### 5. 依赖与实现位置

- **决策**：新增 `agent/core/llm.py`，提供如 `call_llm_for_plan(user_request: str, skills_snapshot: list, context_snapshot: list | None) -> dict | None`，返回与 `plan_step` 同形的 dict 或 None。Orchestrator 的 `plan()` 仅调用该函数（并做 skill 存在性校验），不包含任何规则匹配逻辑；未配置或返回 None 时直接返回 None。
- **备选**：把 LLM 调用写在 `orchestrator.py` 内。独立模块便于单测与后续扩展（如换模型、加重试）。

## Risks / Trade-offs

- **LLM 输出不稳定**：可能返回非 JSON 或错误 skill 名。通过 prompt 约束 + 解析后校验 `skill` 是否在 Registry 中存在来缓解；无效则 plan() 返回 None。
- **延迟与成本**：每次规划多一次 API 调用。首版不缓存；若后续有性能需求再考虑缓存或批量。
- **必须配置 LLM**：无 API Key 时主 Agent 无法生成计划，需在文档中明确说明。

## Migration Plan

- 无数据迁移。部署前必须设置 `LLM_*` / `OPENAI_*`，否则主 Agent 无法规划。
- 回滚：恢复规则匹配逻辑并可选保留或移除 `llm.py` 调用。

## Open Questions

- 是否在首版就向 LLM 注入 Context 摘要（多轮/续写）？建议实现单步 LLM 规划后再加。
