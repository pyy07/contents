# agent-orchestration

## ADDED Requirements

### Requirement: 主 Agent 任务规划与分配

系统 SHALL 提供主 Agent（Orchestrator），负责理解请求、制定执行计划、将子任务分配给 Sub-Agent，并依据 Sub-Agent 返回结果继续决策或汇总回复。

#### Scenario: 主 Agent 将「获取知乎热文」分配给信息获取 Sub-Agent

- **WHEN** 用户或上层请求意图为获取知乎热榜（或等价描述）
- **THEN** 主 Agent 通过 Registry 匹配到信息获取 Sub-Agent 的 zhihu_hot Skill，并下发包含 task_id、skill、params 的任务消息

#### Scenario: 主 Agent 收到 Sub-Agent 成功结果后继续流程

- **WHEN** 主 Agent 收到某 task_id 的完成消息且 status 为 success
- **THEN** 主 Agent 将 result 纳入上下文，并可决定汇总回复或发起下一轮任务分配

### Requirement: 任务与结果契约

系统 SHALL 使用约定的任务与结果格式，使主 Agent 与 Sub-Agent 解耦。任务消息 SHALL 包含 task_id、skill、params、可选的 context；结果消息 SHALL 包含 task_id、status（success 或 failure）、result（成功时）或 error（失败时）。

#### Scenario: 主 Agent 下发任务格式

- **WHEN** 主 Agent 向 Sub-Agent 下发任务
- **THEN** 消息包含 task_id、skill 名称、params（与 Skill 的 input_schema 一致）、可选的 context

#### Scenario: Sub-Agent 返回结果格式

- **WHEN** Sub-Agent 完成 Skill 执行
- **THEN** 返回消息包含与任务相同的 task_id、status、以及 result 或 error，主 Agent 仅依赖该格式做后续决策

### Requirement: 主 Agent 与 Sub-Agent 各自拥有 Skills

系统 SHALL 允许主 Agent 与各 Sub-Agent 各自挂载自身的 Skills。主 Agent 的 Skills 用于规划、汇总或调用内置工具等；Sub-Agent 的 Skills 用于执行领域任务（如信息获取）。Registry 中按所属 Agent 区分，任务分配时主 Agent 可匹配并下发到 Sub-Agent 的 Skill，也可调用自身 Skill 或内置工具。

#### Scenario: 主 Agent 拥有仅自身可用的 Skill

- **WHEN** 主 Agent 注册了仅归属自身的 Skill（如规划辅助或调用内置工具）
- **THEN** 该 Skill 仅对主 Agent 可见与可调用，不参与「下发给 Sub-Agent」的任务匹配

#### Scenario: Sub-Agent 拥有其领域 Skill

- **WHEN** 信息获取 Sub-Agent 注册了 zhihu_hot Skill
- **THEN** 主 Agent 通过 Registry 可发现该 Skill 属于 info Sub-Agent，并用于向该 Sub-Agent 下发任务

### Requirement: Skill 注册与发现

系统 SHALL 提供 Registry，供主 Agent 与各 Sub-Agent 分别注册其 Skill（名称、描述、input_schema、所属 Agent），并供主 Agent 按任务意图或 skill 名称查询，以选择目标 Agent 与 Skill（含 Sub-Agent 的 Skill 与主 Agent 自身 Skill）。内置工具（见 agent-tools）以统一方式暴露，供 Agent 调用。

#### Scenario: Sub-Agent 注册 Skill 后主 Agent 可发现

- **WHEN** 信息获取 Sub-Agent 注册了 zhihu_hot Skill（含 name、description、input_schema）
- **THEN** 主 Agent 通过 Registry 可查询到该 Skill 及其所属 Sub-Agent，并用于任务分配

### Requirement: Skill 可加载与自动发现

系统 SHALL 支持从约定位置**加载** Skill，使用户在添加新 Skill 时**无需改动调度或路由代码**即可被 Agent 发现并使用。约定 Skill 的存放位置与契约格式（如指定目录下按约定导出 name、description、input_schema 及执行函数）；系统在启动或显式刷新时从该位置自动发现、校验并注册到 Registry，主 Agent 与 Sub-Agent 仅依赖 Registry 查询，不依赖硬编码 Skill 列表。

#### Scenario: 新增 Skill 放入约定位置后自动被发现

- **WHEN** 用户将符合契约的新 Skill 实现放入约定目录（或按约定在 manifest 中声明），并触发加载或重启
- **THEN** 系统发现并注册该 Skill 到对应 Sub-Agent（或主 Agent），主 Agent 通过 Registry 可查询到并用于任务分配，无需修改 Orchestrator 或 Sub-Agent 路由逻辑

#### Scenario: 仅符合契约的 Skill 被加载

- **WHEN** 约定位置内某模块缺少 name、description、input_schema 或执行入口等必需契约
- **THEN** 加载器跳过或报错该模块，不影响已合规 Skill 的注册与使用

### Requirement: 上下文管理与自动 compact

所有 Agent（主 Agent 与各 Sub-Agent）SHALL 支持**上下文管理**，维护当前会话/任务相关的历史消息、任务结果与计划。系统 SHALL 在上下文长度或条数超过约定阈值时**自动 compact**（如对较早内容摘要、保留最近 N 条完整、或滑动窗口丢弃最旧），防止上下文爆炸，保证长对话或多轮任务下仍可稳定运行。

#### Scenario: 上下文超阈值时触发 compact

- **WHEN** 某 Agent 的上下文长度或条数达到配置的阈值
- **THEN** 系统自动执行 compact（如摘要旧消息、截断或滑动窗口），使上下文保持在可接受范围内，后续规划与决策仍基于 compact 后的上下文

#### Scenario: compact 后保留关键信息

- **WHEN** 执行 compact
- **THEN** 系统保留或摘要对当前任务仍关键的信息（如最近任务结果、未完成任务、用户最新意图），不因 compact 丢失导致决策错误所必需的内容

### Requirement: 经验沉淀与自我演进

系统 SHALL 支持将运行中的**经验**（如某 Skill 在某类请求下的成功/失败、用户反馈、有效任务链等）**沉淀**为结构化记录并存储；规划与匹配时 SHALL 可**参考经验**（如优先选用历史上有效的 Skill、避免曾失败策略），实现**自我演进**，随使用逐步优化而无需人工改配置。

#### Scenario: 任务结果被沉淀为经验

- **WHEN** 某次任务执行完成（成功或失败）或用户给出反馈
- **THEN** 系统将可复用的信息（如 skill、params、请求类型、结果状态）写入经验存储，供后续查询与参考

#### Scenario: 规划时参考经验做演进

- **WHEN** 主 Agent 进行任务规划或 Skill 匹配
- **THEN** 可查询经验存储（如同类请求下曾成功的 Skill、曾失败的组合），在可选范围内优先选用历史有效策略或避免已知失败策略，实现自我演进
