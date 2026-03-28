---
illustration_id: 03
type: infographic
style: blueprint
---

执行环境、资源与安全暴露对比 - Data Visualization

Layout: grid

ZONES:
- Zone 1: 执行环境对比（宿主系统 vs Docker沙盒）
- Zone 2: 关键指标矩阵（资源开销、冷启动、工具执行机制、安全暴露）
- Zone 3: 雷达小图（AutoGen/LangGraph/DeerFlow/Nanobot）

LABELS:
- Nanobot: ~45MB, <10ms
- DeerFlow: AIO Sandbox, 安全暴露极低
- AutoGen/LangGraph: 宿主执行，安全暴露较高

COLORS: 风险等级渐变（绿色低风险，红色高风险），保持蓝图线框。
STYLE: Blueprint data infographic, icons + matrix + radar mini chart, flat vector.
ASPECT: 16:9

Clean composition, large Chinese labels.
