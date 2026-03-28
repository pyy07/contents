---
illustration_id: 02
type: comparison
style: blueprint
---

五大 Agent 框架对比矩阵 - Comparative Chart

Layout: table

ZONES:
- Zone 1: 表头（框架名称）
- Zone 2: 定位（每个框架一句话定位）
- Zone 3: 适合场景（典型适用场景）
- Zone 4: 代价（主要 trade-off）

COLUMNS:
- LangGraph
- LlamaIndex (Workflows)
- AutoGen v0.4
- DeerFlow v2.0
- Nanobot

ROWS:
- 定位
- 适合
- 代价

CELL_CONTENT:
- LangGraph/定位: 图状态机 + 显式状态 + 检查点
- LangGraph/适合: 审批流、合规流、人在回路
- LangGraph/代价: 建模成本高、学习曲线陡
- LlamaIndex/定位: 数据层 + 检索层 + 事件化工作流
- LlamaIndex/适合: RAG、知识库问答、引用追溯
- LlamaIndex/代价: 超复杂控制流表达一般
- AutoGen/定位: 多智能体异步协作引擎
- AutoGen/适合: 开放研判、并发分工、复杂推理
- AutoGen/代价: 不确定性高、Token 成本易失控
- DeerFlow/定位: 沙盒化执行 + 动态技能系统
- DeerFlow/适合: 脚本执行、浏览器自动化、长任务
- DeerFlow/代价: 资源开销高、运维复杂
- Nanobot/定位: 极小内核 + 本地优先 + 高透明
- Nanobot/适合: 边缘部署、隐私优先、本地化
- Nanobot/代价: 需自行补齐企业能力

LABELS:
- “定位-适合-代价”
- “没有最强，只有最合适”
- “生产可用性”
- “成本曲线”

COLORS:
- 主色深蓝，辅助浅蓝
- 风险信息使用橙色强调
- 低资源与本地优先使用绿色标识

STYLE: Blueprint comparison chart, flat vector, crisp grid, Chinese labels, no gradients.
ASPECT: 16:9

Clean composition with generous white space. Main visual centered. Text large and readable.
