---
illustration_id: 01
type: infographic
style: blueprint
---

Agent 框架演进驱动力总览 - Data Visualization

Layout: hierarchical

ZONES:
- Zone 1: 早期阶段（LLM 调用封装层，目标是快速 Demo）
- Zone 2: 演进驱动（三个驱动：长期任务与可恢复执行、多智能体协作与状态一致性、执行安全边界）
- Zone 3: 当前阶段（生产系统基础设施，强调可审计、可观测、可治理）

NODES:
- 早期能力：Prompt Chain、工具调用封装、快速原型
- 驱动一：长期任务、Checkpoint、恢复执行
- 驱动二：异步协作、事件驱动、状态管理
- 驱动三：沙盒执行、权限边界、审计日志
- 目标能力：稳定运行、成本可控、风险可控

RELATIONSHIPS:
- 由 Zone 1 向 Zone 3 单向演进
- Zone 2 的三个驱动同时推动演进
- 每个驱动都连接“生产级能力”标签

LABELS:
- “LLM 调用封装层”
- “生产系统基础设施”
- “长期任务”
- “可恢复执行”
- “多智能体协作”
- “状态一致性”
- “执行安全边界”
- “可审计 / 可观测 / 可治理”

COLORS:
- 蓝色表示编排与控制流
- 紫色表示协作与通信
- 橙色表示执行与安全
- 灰蓝表示系统底座与治理

STYLE: Blueprint technical infographic, flat vector, clean lines, Chinese labels, no gradients.
ASPECT: 16:9

Clean composition with generous white space. Main visual centered. Text large and readable.
