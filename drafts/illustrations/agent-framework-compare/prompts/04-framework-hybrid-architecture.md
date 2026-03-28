---
illustration_id: 04
type: framework
style: blueprint
---

Agent 混合架构分层图 - Hybrid Architecture Blueprint

Layout: layered-architecture

ZONES:
- Zone 1: 用户与业务入口层（需求、任务、审批）
- Zone 2: 编排控制层（LangGraph，确定性工作流与状态机）
- Zone 3: 协作推理层（AutoGen，多智能体研判子任务）
- Zone 4: 知识检索层（LlamaIndex，RAG 与引用追溯）
- Zone 5: 执行隔离层（DeerFlow，沙盒执行与工具运行）
- Zone 6: 边缘与私有节点（Nanobot，本地优先与低资源运行）
- Zone 7: 可观测与治理横切层（日志、审计、成本、告警）

RELATIONSHIPS:
- 用户请求进入编排控制层
- 编排层按任务类型调用协作层、检索层、执行层
- 执行层输出结果回编排层
- 边缘节点作为可选执行目标
- 可观测治理层覆盖所有层

LABELS:
- “LlamaIndex：知识检索底层”
- “LangGraph：顶层确定性编排”
- “AutoGen：复杂研判子任务”
- “DeerFlow：高风险执行隔离”
- “Nanobot：边缘/私有轻量节点”
- “可审计 / 可观测 / 成本可控”

COLORS:
- 编排层蓝色
- 检索层绿色
- 协作层紫色
- 执行隔离层橙色
- 边缘节点灰蓝
- 治理层使用中性深灰线框

STYLE: Blueprint system architecture diagram, flat vector, clean layers, Chinese labels, no gradients.
ASPECT: 16:9

Clean composition with generous white space. Main visual centered. Text large and readable.
