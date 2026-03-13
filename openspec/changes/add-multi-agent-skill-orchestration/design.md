# Design: 多 Agent + Skill 架构

## Context

- 项目为写作与发布管理（drafts、published、materials），agent 目录当前为单脚本形态（如 `zhihu-hot/fetch_hot.py`）。
- 目标：主 Agent 负责调度与决策，Sub-Agent 负责执行领域能力（Skill），形成「规划 → 分配 → 执行 → 回传 → 再规划」的闭环。

## Goals / Non-Goals

- **Goals**: 主 Agent 与各 Sub-Agent 各自拥有 Skills；主 Agent 可发现并调用 Sub-Agent 的 Skill；提供内置工具供 Agent 完成基础能力；任务与结果有统一契约；**所有 Agent 支持上下文管理并自动 compact，防止上下文爆炸**；**沉淀经验并支持自我演进**；至少有一个可用的 Sub-Agent（信息获取）及一个 Skill（知乎热榜）。
- **Non-Goals**: 不规定主 Agent 必须由 LLM 实现；不实现跨进程/网络 RPC，首版可为进程内调用。

## Decisions

- **主 Agent 与 Sub-Agent 各自拥有 Skills**：主 Agent 可挂载仅自身可用的 Skills（如规划辅助、结果汇总、调用内置工具）；每个 Sub-Agent 挂载其领域内 Skills（如 info 的 zhihu_hot）。Registry 中按「所属 Agent」区分，主 Agent 做任务分配时仅匹配 Sub-Agent 的 Skills，主 Agent 自身 Skills 用于本地决策与工具调用。
- **任务契约**：主 Agent 下发的任务包含 `task_id`、`skill`、`params`、可选 `context`；Sub-Agent 回传包含 `task_id`、`status`（success/failure）、`result` 或 `error`。便于主 Agent 与多 Sub-Agent 解耦。
- **Skill 注册与发现**：每个 Agent（主 Agent 与各 Sub-Agent）在注册时声明其 Skill 列表（name、description、input_schema）；主 Agent 通过 Registry 按任务意图匹配目标 Agent + Skill，并填充 params。主 Agent 自身也可查询并调用自己的 Skills 与内置工具。
- **Skill 加载机制**：Skills 支持**加载而非写死**。约定 Skill 的存放位置与契约格式（如 `sub_agents/<domain>/skills/` 下每模块一个 Skill，或统一 manifest 声明）。系统在启动或刷新时从约定位置**自动发现并注册**符合契约的 Skill；用户新增 Skill 时只需按契约实现并放入约定位置，**无需修改 Orchestrator、Registry 或 Sub-Agent 的路由代码**，Agent 即可发现并使用。
- **内置工具（Tools）**：系统提供一组内置工具，主 Agent 与 Sub-Agent 均可调用（或在策略上限制仅主 Agent 可调），用于基础能力：**执行代码**（如运行脚本或片段）、**列出目录/文件**、**读取文件**、**写入文件**等。工具以统一接口暴露（name、description、params），与 Skill 类似但为系统内置、不归属单一领域 Agent。
- **目录结构**：`agent/core/` 放 types、orchestrator、registry、tools（内置工具实现）、skill_loader（可选）、context（上下文管理）、experience（经验存储与演进）；`agent/sub_agents/<domain>/` 下每域一个 Sub-Agent，其下 `skills/` 中每文件对应一个 Skill 实现，由加载器扫描并注册；现有 `agent/zhihu-hot/` 保留，由 `info` Sub-Agent 的 zhihu_hot Skill 封装或调用。
- **上下文管理与自动 compact**：所有 Agent（主 Agent 与 Sub-Agent）均维护当前会话/任务的上下文（如历史消息、任务结果、当前计划）。当上下文长度或条数超过阈值时，系统 SHALL **自动 compact**（如：对较早内容做摘要、保留最近 N 条完整、或按滑动窗口丢弃最旧），避免上下文爆炸导致超长输入或性能下降。compact 策略可配置（阈值、摘要粒度、保留条数等）。
- **经验沉淀与自我演进**：系统将运行中产生的可复用信息**沉淀为经验**（如：某 Skill 在某类请求下成功/失败、用户采纳的回复、任务链的有效顺序等），以结构化形式存储（如 agent/experience/ 或数据库）。规划与匹配时可**参考经验**（如优先选用历史上成功率高的 Skill、避免曾失败的任务组合），实现**自我演进**，无需人工改配置即可随使用逐步优化。首版可为简单键值或文件存储，后续可扩展为检索、统计或轻量学习。
- **Alternatives considered**：单一大 Agent 包含所有能力 — 不利于扩展与职责分离；不定义契约直接传参 — 不利于多 Agent 协作与后续 RPC 化；仅 Sub-Agent 有 Skill — 主 Agent 无法拥有规划/汇总等自有能力。

## Risks / Trade-offs

- **第三方热榜 API 不可用**：zhihu_hot Skill 依赖外部 API，失败时按契约返回 status=failure 与 error，主 Agent 可重试或提示用户。
- **首版进程内调用**：后续若需跨进程/远程，仅需在 core 层替换「调用 Sub-Agent」的传输方式，契约不变。

## Open Questions

- 主 Agent 首版实现方式（规则匹配 vs 本地/远程 LLM）可留待实现阶段选定。
