## 1. LLM 调用层

- [x] 1.1 新增 `agent/core/llm.py`，实现 OpenAI 兼容的 chat completion 调用（使用 `get_llm_config("main")`）。
- [x] 1.2 精心设计规划用提示词：包含角色与职责、当前可选 Skill 及描述、用户请求、仅输出指定 JSON 的格式约束，确保模型能完成主控并选出正确 skill/params；在 `call_llm_for_plan(user_request, skills_snapshot, context_snapshot=None)` 中构建该 prompt，请求模型并解析返回为 `{skill, params, agent_id}` 或 None。
- [x] 1.3 对返回的 `skill` 做存在性校验（在 Registry 中可解析），无效则返回 None。

## 2. Orchestrator 集成

- [x] 2.1 移除 `Orchestrator.plan()` 中全部规则匹配逻辑（关键词、`find_by_description` 等）。
- [x] 2.2 `plan()` 仅通过 `call_llm_for_plan` 获取计划：未配置 LLM 或返回 None/无效时直接返回 None。
- [x] 2.3 可选：将 `self._context` 的最近消息/结果摘要传入 `call_llm_for_plan` 的 context_snapshot。

## 3. 文档与配置

- [x] 3.1 更新 `agent/CONFIG.md`：说明主 Agent 规划仅由 LLM 驱动，必须配置 `LLM_*`/`OPENAI_*` 才能运行。
- [x] 3.2 更新 `agent/ARCHITECTURE.md`：规划路径改为「仅 LLM 驱动，无规则回退」。
