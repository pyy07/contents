---
illustration_id: 03
type: flowchart
style: blueprint
---

传统顺序执行 vs 事件驱动与响应式

Layout: 上半部分「传统」从左到右单箭头链；下半部分「事件驱动」多源汇入一条处理流。

STEPS（上）: 1. main() 2. 顺序执行 3. 步骤A→B→C
STEPS（下）: 左侧多个事件源（用户点击、消息队列、传感器）用箭头指向中央「事件流」；右侧「可观察流 / 依赖更新」；标注 Node.js、Reactor/Rx。

CONNECTIONS: 上方直线箭头；下方多箭头汇聚，粗线表示“流”。可标注「异步、非阻塞、背压」。

LABELS（中文）: 传统顺序 | 事件驱动；用户点击、消息队列、传感器、事件流、响应式。

COLORS: 浅底 #F5F0E6，箭头与框深蓝 #1E3A5F，强调处淡蓝。Blueprint 线稿风格。

STYLE: Flat vector flowchart. Bold arrows, geometric step boxes. Simple icons (e.g. small circles for events). No gradients.
ASPECT: 16:9

Clean composition, generous white space. Chinese labels. Main elements centered.
