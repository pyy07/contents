# Change: 使用 LLM 驱动 Agent 规划与决策

## Why

当前主 Agent（Orchestrator）的规划完全依赖规则匹配（如关键词「知乎」「热榜」→ zhihu_hot），未调用任何 LLM。已有 `agent/core/config.py` 中的 LLM 配置仅为预留。希望 Agent 由 LLM 驱动，从而支持自然语言理解、多步规划与更灵活的意图识别。

## What Changes

- 主 Agent 的 `plan()` 仅通过 LLM 根据用户请求与可用 Skill 列表生成执行计划（skill 名称 + params）；**完全去掉规则匹配逻辑**，不再使用关键词或 find_by_description 等回退。
- 引入 LLM 调用层：使用 OpenAI 兼容 API（现有 `LLM_*` / `OPENAI_*` 环境变量），支持主 Agent 规划用模型可配置。
- 未配置 LLM 或调用失败时，plan() 返回 None，request() 返回失败，不提供规则回退。
- 精心设计规划阶段提示词（角色、任务、Skill 列表、输出格式约束），确保模型能完成主控流程并选出正确 skill 与参数以完成相应功能。
- 可选：将 Context 中的历史消息与结果作为 LLM 的上下文输入，便于多轮与续写场景。

## Impact

- **Affected specs**: agent（新建 capability 的 ADDED 需求）
- **Affected code**: `agent/core/orchestrator.py`（plan 逻辑）、新增 `agent/core/llm.py`（或等价模块）封装 LLM 调用；`agent/core/config.py` 已具备配置，仅需被实际使用；文档 `agent/CONFIG.md`、`agent/ARCHITECTURE.md` 需更新说明 LLM 驱动行为。
