---
illustration_id: 02
type: flowchart
style: blueprint
---

MoE 混合专家架构原理 - 流程图

Layout: left-right，从左到右

STEPS:
1. 输入 Input - 进入门控
2. 门控/路由 Gate - 选择少数专家
3. 专家 1·2·3（仅激活 2 个）- 稀疏计算
4. 输出 Output - 合成结果

CONNECTIONS: 直线或 90 度折线箭头，从 Input → Gate → 两个专家块 → Output；标注「总参数大·激活少」
LABELS: 中文：输入、门控、专家、输出；可加「1/6–1/8 推理成本」
COLORS: 背景 #FAF8F5，主色 #2563EB，辅色 #1E3A5F，#BFDBFE 填充块
STYLE: 精确线条，矩形框表示步骤，工程图风格，无曲线
Clean composition with generous white space. Simple or no background.
ASPECT: 16:9
