# Tasks: add-multi-agent-skill-orchestration

## 1. Core 契约与类型

- [x] 1.1 定义任务与结果数据结构（task_id, skill, params, context / status, result, error），见 design 与 agent-orchestration spec。
- [x] 1.2 实现 Skill 描述结构（name, description, sub_agent, input_schema），供注册与发现。

## 2. Registry 与发现

- [x] 2.1 实现 Agent（主 Agent 与 Sub-Agent）与 Skill 的注册接口；每个 Agent 注册时提交其自身 Skill 列表（描述 + 执行入口），Registry 按所属 Agent 区分。
- [x] 2.2 实现按 skill name 或描述匹配的查询接口，供主 Agent 选择目标 Agent 与 Skill（含主 Agent 自身 Skill 与 Sub-Agent 的 Skill）。
- [x] 2.3 实现 **Skill 加载机制**：约定 Skill 的存放位置与契约格式（如 `sub_agents/<domain>/skills/` 下每模块导出 name、description、input_schema、execute）；启动或刷新时扫描约定位置，自动发现、校验并注册到 Registry，不依赖硬编码 Skill 列表。

## 3. 主 Agent（Orchestrator）与自有 Skills

- [x] 3.1 实现 Orchestrator：接收用户或上层请求，生成执行计划（可仅为单步：选一个 Sub-Agent + Skill，或调用自身 Skill / 内置工具）。
- [x] 3.2 实现任务下发：根据计划调用 Registry 解析出目标 Agent 与 Skill，若为 Sub-Agent 则构造任务消息并调用；若为主 Agent 自身 Skill 或内置工具则本地调用。
- [x] 3.3 实现结果处理：接收 Sub-Agent 返回的完成消息或自身 Skill/工具结果，根据 status 决定是否继续分配或汇总回复。
- [x] 3.4 支持主 Agent 挂载自有 Skills（如规划辅助、调用内置工具），并在 Registry 中注册为归属主 Agent。

## 4. Sub-Agent 基类与信息获取 Sub-Agent

- [x] 4.1 实现 Sub-Agent 基类：接收任务消息，按 task.skill 路由到对应 Skill 实现，执行后返回约定格式的结果消息。
- [x] 4.2 实现信息获取 Sub-Agent（info），并在注册时声明 zhihu_hot Skill（描述 + input_schema）。

## 5. zhihu_hot Skill 与可加载示例

- [x] 5.1 实现 zhihu_hot Skill：入参（limit, save）与现有脚本一致；执行逻辑复用 `agent/zhihu-hot/fetch_hot.py` 或等价的拉取与可选保存；输出符合 agent-info spec 的 result 结构；并按约定契约格式导出（name、description、input_schema、execute），便于被加载器发现。
- [x] 5.2 将 zhihu_hot 通过 **Skill 加载机制** 挂载到 info Sub-Agent（即置于 `sub_agents/info/skills/` 等约定位置，由加载器注册），确保主 Agent 无需改代码即可发现并分配「获取知乎热文」任务；后续新增 Skill 仅需按同一契约与位置添加即可被 Agent 发现并使用。

## 6. 内置工具（agent-tools）

- [x] 6.1 实现内置工具统一接口（name、description、params、执行入口），并在 core 层注册，供主 Agent 与（按策略）Sub-Agent 查询与调用。
- [x] 6.2 实现「执行代码」工具：在受控环境中运行代码片段或脚本，返回 stdout、stderr、退出状态；超时与异常时返回错误信息。
- [x] 6.3 实现「列出目录/文件」工具：给定路径返回目录下条目列表（名称、是否为目录等），路径非法时返回明确错误。
- [x] 6.4 实现「读取文件」「写入文件」工具：在允许的路径范围内读写文件内容，返回内容或成功/错误状态；首版可限制在项目根或白名单。

## 7. 上下文管理与自动 compact

- [x] 7.1 为所有 Agent（主 Agent 与 Sub-Agent）定义并实现**上下文存储**（当前会话/任务的历史消息、任务结果、计划），供规划与决策使用。
- [x] 7.2 实现**自动 compact**：当上下文长度或条数超过可配置阈值时，对较早内容摘要、保留最近 N 条完整或滑动窗口丢弃最旧，保证 compact 后仍保留对当前任务关键的信息（如最近结果、未完成任务、用户最新意图）。
- [x] 7.3 将 compact 策略做成可配置（阈值、摘要粒度、保留条数等），并在主 Agent 与 Sub-Agent 基类中统一接入。

## 8. 经验沉淀与自我演进

- [x] 8.1 定义**经验**数据结构（如 skill、params 类型、请求类型、结果状态、可选用户反馈），并实现经验存储（首版可为 agent/experience/ 下的文件或简单键值存储）。
- [x] 8.2 在任务完成或用户反馈时，将可复用信息**沉淀**写入经验存储；在规划或 Skill 匹配时提供**查询接口**（如同类请求下曾成功的 Skill、曾失败的组合）。
- [x] 8.3 主 Agent 在规划/匹配时**参考经验**（如优先选用历史有效 Skill、避免已知失败策略），实现自我演进；首版可为简单优先级或过滤规则，后续可扩展为检索或轻量学习。

## 9. 验证与文档

- [x] 9.1 端到端验证：主 Agent 接收「获取知乎热文」类请求 → 分配至 info 的 zhihu_hot → 收到成功结果并可汇总或展示。
- [x] 9.2 验证主 Agent 与 Sub-Agent 各自 Skills 在 Registry 中正确区分，且主 Agent 可调用内置工具（如 list_dir、run_code）。
- [x] 9.3 验证 Skill 加载：在约定位置新增一例占位或简单 Skill 并刷新加载，确认主 Agent 可发现并使用，且未修改 Orchestrator/Sub-Agent 路由代码。
- [x] 9.4 验证上下文 compact：在多轮或长对话下触发 compact，确认上下文不爆炸且关键信息仍可用；验证经验沉淀与参考：执行若干任务后检查经验写入，并在后续规划中能参考经验做选择。
- [x] 9.5 更新 `agent/README.md`，说明多 Agent + Skill、各自 Skills、**Skill 加载与新增方式**、**上下文管理与 compact**、**经验沉淀与自我演进**、内置工具用法，及与 `openspec` 本变更的对应关系。
