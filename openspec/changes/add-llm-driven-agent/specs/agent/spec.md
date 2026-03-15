## ADDED Requirements

### Requirement: LLM 驱动主 Agent 规划

主 Agent 的规划 SHALL 仅由 LLM 驱动。系统 SHALL 根据用户请求与当前已注册 Skill 列表，通过 LLM 生成单步执行计划（skill 名称与 params）；计划格式可直接交由 dispatch 执行。不保留任何规则匹配逻辑；未配置 LLM 或 LLM 调用失败时无法生成计划。

#### Scenario: LLM 已配置且返回有效计划

- **WHEN** 环境变量已设置 LLM_API_KEY（或 OPENAI_API_KEY）且用户发起自然语言请求
- **THEN** Orchestrator 调用 LLM 并解析返回为 plan_step（含 skill、params、agent_id）
- **AND** 若解析出的 skill 在 Registry 中存在，则返回该计划并进入 dispatch

#### Scenario: LLM 未配置时无法生成计划

- **WHEN** get_llm_config("main").is_configured() 为 False（未设置 API Key 与 Base URL）
- **THEN** plan() 返回 None，不执行任何规则匹配
- **AND** request() 返回表示无法生成执行计划的结果（如 NO_PLAN）

#### Scenario: LLM 调用失败或返回无效 skill 时无法生成计划

- **WHEN** LLM 调用抛错、超时或返回的 skill 在 Registry 中不存在
- **THEN** plan() 返回 None
- **AND** request() 返回表示无法生成执行计划的结果（如 NO_PLAN）

### Requirement: 精心设计 LLM 提示词以支撑主控与功能

系统 SHALL 精心设计用于规划阶段的提示词（含系统角色、任务说明、可用 Skill 列表与输出格式约束），确保模型能够正确理解主控流程并选出合适的 skill 与参数，从而完成相应功能；提示词设计 SHALL 覆盖「角色与职责」「当前可选技能及描述」「用户请求」「仅输出指定 JSON 结构」等要素，并在实现与文档中可追溯。

#### Scenario: 提示词使模型产出可执行计划

- **WHEN** 用户请求与某已注册 Skill 的语义相符（如「拉取知乎热榜」对应 zhihu_hot）
- **THEN** 所用提示词使模型能够根据 Skill 列表选出正确 skill 与合理 params
- **AND** 解析后的 plan_step 可直接被 dispatch 执行并完成对应功能

#### Scenario: 提示词约束输出格式

- **WHEN** 调用 LLM 进行规划
- **THEN** 提示词中明确要求模型仅输出指定结构的 JSON（如 skill、params、agent_id）
- **AND** 实现中对该格式有解析与校验，便于主控流程稳定运行
