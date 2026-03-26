---
illustration_id: 03
type: flowchart
style: blueprint
---

Agent 框架选型四问决策树 - Decision Flow

Layout: decision-tree

ZONES:
- Zone 1: 起点（我的 Agent 项目）
- Zone 2: 问题 1（流程确定 vs 开放探索）
- Zone 3: 问题 2（知识检索核心 vs 工具执行核心）
- Zone 4: 问题 3（资源成本约束 vs 安全边界约束）
- Zone 5: 问题 4（快交付 vs 可控可审计）
- Zone 6: 推荐输出（LangGraph / AutoGen / LlamaIndex / DeerFlow / Nanobot）

DECISIONS:
- Q1: 流程确定？是→LangGraph 倾向；否→AutoGen 倾向
- Q2: 价值核心在知识检索？是→LlamaIndex；否→DeerFlow
- Q3: 资源受限且本地优先？是→Nanobot；否→继续看安全隔离需求
- Q4: 强调快交付？是→LlamaIndex/Nanobot 轻量路线；否→LangGraph + 可观测体系

OUTPUT_NOTES:
- “复杂项目建议混合架构”
- “高风险执行动作优先隔离”
- “先明确不确定性来源，再选框架”

LABELS:
- “问题 1: 流程确定 or 开放探索”
- “问题 2: 知识检索 or 工具执行”
- “问题 3: 成本约束 or 安全边界”
- “问题 4: 快交付 or 可审计”
- “最终推荐”

COLORS:
- 决策节点使用深蓝
- 分支路径使用浅蓝
- 风险和安全相关路径使用橙色
- 推荐结果节点使用蓝绿区分

STYLE: Blueprint decision flowchart, flat vector, geometric arrows, Chinese labels, no gradients.
ASPECT: 16:9

Clean composition with generous white space. Main visual centered. Text large and readable.
