# agent-info

## ADDED Requirements

### Requirement: 信息获取 Sub-Agent

系统 SHALL 提供信息获取 Sub-Agent（info），负责接收主 Agent 下发的任务、按 skill 名称路由到对应 Skill 实现、执行后以约定格式将结果回传主 Agent。

#### Scenario: 收到 zhihu_hot 任务时执行知乎热榜拉取

- **WHEN** 信息获取 Sub-Agent 收到 task 中 skill 为 zhihu_hot、params 含 limit 与可选 save
- **THEN** Sub-Agent 调用 zhihu_hot Skill 实现，拉取知乎热榜并可选保存到 materials/links，随后返回包含 items 与 update_time 的 result 给主 Agent

#### Scenario: Skill 执行失败时返回 failure 与 error

- **WHEN** zhihu_hot 执行过程中发生异常或外部 API 失败
- **THEN** Sub-Agent 向主 Agent 返回 status 为 failure、error 包含可读错误信息的完成消息

### Requirement: zhihu_hot Skill

系统 SHALL 在信息获取 Sub-Agent 下提供 zhihu_hot Skill：获取知乎当前热榜，入参为 limit（条数）与可选 save（是否保存到 materials/links）；输出为热榜条目列表（含 title、hot、url 等）及更新时间，与 agent-orchestration 的结果契约一致。

#### Scenario: 成功拉取并返回结构化结果

- **WHEN** zhihu_hot 以有效 params（如 limit=10）执行且外部热榜 API 可用
- **THEN** Skill 返回 result 包含 items 数组与 update_time，主 Agent 或调用方可直接使用

#### Scenario: 可选保存到素材目录

- **WHEN** params 中 save 为 true
- **THEN** Skill 在成功拉取后将热榜写入 materials/links/zhihu-hot-YYYYMMDD.md（或等价路径），再返回 result
