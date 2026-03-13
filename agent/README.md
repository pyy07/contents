# Agent — 多 Agent + Skill 调度

本目录实现**主 Agent（Orchestrator） + Sub-Agent + Skill** 架构：主 Agent 负责理解请求、制定计划、分配任务；Sub-Agent 按领域执行 Skill；任务与结果通过统一契约传递。对应 OpenSpec 变更：`openspec/changes/add-multi-agent-skill-orchestration/`。

## 核心概念

- **主 Agent（Orchestrator）**：接收用户或上层请求，生成执行计划（单步或多步），将任务下发给 Sub-Agent 或调用自身 Skill / 内置工具，并处理返回结果。
- **Sub-Agent**：按领域划分（如 `info` 信息获取），接收主 Agent 下发的任务消息，按 `task.skill` 路由到对应 Skill 执行，返回约定格式的 `TaskResult`。
- **Skill**：最小可调用单元，有明确入参（`input_schema`）与执行函数 `execute(params)`，输出符合契约的 result 或 error。
- **内置工具（Tools）**：系统提供的通用能力（执行代码、列出目录、读/写文件），以 Skill 形式注册到主 Agent，路径在项目目录内直接执行，项目外需用户授权。

## 各自 Skills 与 Skill 加载

- **主 Agent 与 Sub-Agent 各自拥有 Skills**：主 Agent 的 Skill 用于规划、汇总或调用内置工具；Sub-Agent 的 Skill 用于领域任务（如信息获取）。Registry 按所属 Agent 区分。
- **Skill 可加载、自动发现**：无需改调度或路由代码即可扩展。约定：
  - 存放位置：`agent/sub_agents/<domain>/skills/` 下每个 `.py` 模块为一个 Skill。
  - 契约：模块需导出 `name`、`description`、`input_schema`、`execute`（可调用，入参 `params: dict`，返回 `TaskResult` 或 `dict`）。
  - 启动或刷新时调用 `load_skills_from_sub_agents(agent_root, registry)`，扫描上述目录并注册到 Registry；新增 Skill 只需按契约实现并放入对应 `skills/` 目录即可被主 Agent 发现并分配。

## 上下文管理与 compact

- 所有 Agent 支持**上下文存储**（当前会话的历史消息、任务结果、计划），供规划与决策使用。
- 当上下文条数或长度超过可配置阈值时，系统**自动 compact**：对较早内容做摘要、保留最近 N 条完整，避免上下文爆炸。策略在 `ContextConfig` 中配置（`max_entries`、`max_chars`、`keep_recent` 等），主 Agent 构造时传入 `AgentContext` 即可接入。

## 经验沉淀与自我演进

- 运行中的**经验**（某 Skill 在某类请求下的成功/失败等）可**沉淀**到 `agent/experience/store.json`（或指定路径）。
- 规划或 Skill 匹配时可**参考经验**：如优先选用历史上成功的 Skill、避免曾失败的组合，实现自我演进。首版为简单优先级/过滤规则，后续可扩展为检索或轻量学习。

## 内置工具用法

- **run_code**：执行 Python 代码片段；params：`code`（必填）、`workdir`（可选）、`timeout`（可选）。
- **list_dir**：列出指定路径下目录与文件；params：`path`（默认 `.`）。
- **read_file**：读取文件内容；params：`path`。
- **write_file**：写入文件；params：`path`、`content`。

路径在项目根内直接执行；项目外需用户授权，未授权时返回「访问项目外路径需用户授权」。

## 目录结构

```
agent/
├── core/           # types, registry, skill_loader, orchestrator, sub_agent, tools, context, experience
├── sub_agents/     # 按领域划分，每域下 skills/ 中放可加载 Skill
│   └── info/
│       └── skills/
│           └── zhihu_hot.py   # 知乎热榜 Skill
├── experience/     # 经验存储（如 store.json）
└── README.md
```

## 快速使用

在项目根目录（`contents/`）下：

```python
from pathlib import Path
from agent.core import (
    Registry,
    load_skills_from_sub_agents,
    register_builtin_tools,
    Orchestrator,
    SubAgent,
    AgentContext,
    ContextConfig,
)

root = Path(".")
agent_root = root / "agent"
registry = Registry()
register_builtin_tools(registry, root)
load_skills_from_sub_agents(agent_root, registry)

context = AgentContext("main", ContextConfig())
experience_path = agent_root / "experience" / "store.json"
orchestrator = Orchestrator(
    registry,
    sub_agents={"info": SubAgent("info", registry)},
    context=context,
    experience_path=experience_path,
)

result = orchestrator.request("获取知乎热文")
# result.status, result.result / result.error
```

## 与 OpenSpec 的对应关系

- 需求与设计：`openspec/changes/add-multi-agent-skill-orchestration/` 下的 `proposal.md`、`design.md`、`specs/**/*.md`。
- 任务清单与完成状态：`tasks.md`。
