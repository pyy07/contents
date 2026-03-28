---
type: mixed
preset_base: tech-explainer
density: balanced
style: blueprint
image_count: 4
language: zh
article: "../Agent 开发框架：从「能跑」到「能用」的那道坎.md"
---

# 配图大纲：Agent 框架焦虑与选型

## Illustration 1

**Position**: 开篇「市面上的框架，本质上都是在回答同一组焦虑」之后
**Purpose**: 把六个工程焦虑可视化，与正文问题一一对应（信息图，非品牌 Logo）
**Visual Content**: 六栏或六边形信息图，每区一个短标签：状态存储、流程回滚、多智能体成本、数据与引用、真执行/沙盒、可观测与调试
**Filename**: 01-infographic-six-anxieties.png

## Illustration 2

**Position**: 「当链式调用不够用时：LangChain 与 LangGraph」小节末
**Purpose**: 对比线性链路与图状态机+检查点（概念示意，非官方商标）
**Visual Content**: 左：单向箭头流水线；右：带回路节点与「Checkpoint」标记的有向图
**Filename**: 02-flowchart-chain-vs-graph.png

## Illustration 3

**Position**: 「AutoGen 与 CrewAI」小节末
**Purpose**: 对比「消息/事件基础设施」与「角色班组剧本」两种多智能体心智模型
**Visual Content**: 双栏对比：左为异步消息气泡与拓扑示意；右为角色卡片（研究员/写手/评审）与任务箭头
**Filename**: 03-comparison-multiagent-models.png

## Illustration 4

**Position**: 倒数第二节「没有万能框架…」之前
**Purpose**: 收束全文六个选型维度
**Visual Content**: 中心「对症选型」，周围六维：控制流、数据、协作、执行环境、可观测性、成本
**Filename**: 04-framework-six-dimensions.png
