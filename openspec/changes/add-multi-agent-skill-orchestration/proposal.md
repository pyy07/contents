# Change: 多 Agent + Skill 调度架构

## Why

当前 agent 以单脚本、单能力（如直接跑 `fetch_hot.py`）为主，缺少「主 Agent 理解意图、规划、分配任务 → Sub-Agent 执行 Skill → 回传结果 → 主 Agent 继续决策」的 AI 式调度。需要引入主 Agent 调度 Sub-Agent、Sub-Agent 挂载 Skill 的模式，使能力可组合、可扩展，并支持例如「获取知乎热文」由主 Agent 分配给信息获取 Sub-Agent 的 zhihu_hot Skill 执行。

## What Changes

- 引入**主 Agent（Orchestrator）**：负责任务理解、规划、拆解；将子任务分配给 Sub-Agent；根据 Sub-Agent 返回结果继续决策与规划。主 Agent 拥有**自身的 Skills**，用于规划、汇总、调用内置工具等。
- 引入**Sub-Agent**：按领域（如信息获取）组织，各自拥有**自身的 Skills**（如 zhihu_hot）；接收主 Agent 下发的任务，执行对应 Skill，完成后以约定格式通知主 Agent。
- 引入**Skill**：可调用的最小能力单元（如「获取知乎热榜」），有 name、description、input/output 契约；**主 Agent 与各 Sub-Agent 均可挂载各自 Skills**，供规划与任务匹配使用。
- 定义**任务与结果契约**：主 Agent → Sub-Agent 的任务格式（task_id, skill, params, context）；Sub-Agent → 主 Agent 的完成通知格式（task_id, status, result, error）。
- 引入**内置工具（Tools）**：为 Agent（主 Agent 与 Sub-Agent）提供可调用的基础能力，例如**编写与执行代码**、**查看目录与文件列表**、**读取/写入文件**等，使 Agent 在未配置领域 Skill 时也能完成基础操作。
- **所有 Agent 支持上下文管理**：主 Agent 与各 Sub-Agent 均维护会话/任务上下文；系统 SHALL **自动 compact 上下文**（如摘要、裁剪、滑动窗口等），防止上下文爆炸，保证长对话或多轮任务下仍可稳定运行。
- **经验沉淀与自我演进**：系统 SHALL 支持将运行中的决策、任务结果、用户反馈等**沉淀为经验**（如结构化记录或知识片段），并用于后续规划与匹配的**自我演进**（如优先选用历史有效 Skill、避免重复失败策略等），不依赖人工改配置即可持续优化。
- 实现**信息获取 Sub-Agent**，并为其挂载 **zhihu_hot** Skill（复用或封装现有 `agent/zhihu-hot` 能力），使主 Agent 可分配「获取知乎热文」任务。

## Impact

- **Affected specs**: 无既有 spec；新增 capability：`agent-orchestration`、`agent-info`、`agent-tools`。
- **Affected code**: 新增 `agent/core/`（调度、契约、注册、内置工具、上下文管理、经验存储）；新增 `agent/sub_agents/info/` 及 `skills/zhihu_hot`；新增内置工具实现（如 run_code、list_dir、read_file 等）；上下文 compact 与经验沉淀/演进逻辑；现有 `agent/zhihu-hot/` 可保留为独立 CLI 或由 Skill 内部调用。
