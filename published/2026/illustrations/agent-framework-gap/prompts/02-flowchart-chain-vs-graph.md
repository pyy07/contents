---
illustration_id: 02
type: flowchart
style: blueprint
---

线性链 vs 图编排 — 流程对比图（中文标签）

Layout: 左右分屏对比，中间可有一条虚线分隔。

LEFT PANEL — 「链式调用」:
- 四个圆角矩形节点自上而下：输入 → 步骤A → 步骤B → 输出
- 单向箭头连接，无回路
- 小字标注：状态分散

RIGHT PANEL — 「图 + 检查点」:
- 四个节点成图状：含一条从「失败处理」回到「步骤A」的回路箭头
- 醒目标注节点「Checkpoint / 检查点」
- 小字标注：可恢复、可审批

LABELS: 全部中文。不出现 LangChain 等商标字样，可用通用词「链」「图状态机」。
COLORS: 左半冷灰，右半浅蓝底突出；检查点用绿色描边。
STYLE: 蓝图线稿风，简洁图标。
ASPECT: 16:9

Clean composition with generous white space.
