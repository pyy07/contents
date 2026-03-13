# Agent 技术架构图

## 1. 组件总览

```mermaid
flowchart TB
    subgraph 用户层
        User[用户请求]
    end

    subgraph 主 Agent
        Orch[Orchestrator<br/>规划 · 下发 · 汇总]
    end

    subgraph 注册与发现
        Reg[Registry<br/>按 Agent 区分 Skill]
    end

    subgraph 主 Agent Skills
        T1[run_code]
        T2[list_dir]
        T3[read_file]
        T4[write_file]
    end

    subgraph Sub-Agent_info["Sub-Agent: info"]
        S1[zhihu_hot]
    end

    subgraph 支撑
        Ctx[AgentContext<br/>消息 · 结果 · 计划]
        Exp[Experience<br/>经验存储]
    end

    User --> Orch
    Orch --> Reg
    Reg --> T1 & T2 & T3 & T4
    Reg --> S1
    Orch --> Sub-Agent_info
    Orch <--> Ctx
    Orch <--> Exp
```

## 2. 请求处理流程

```mermaid
sequenceDiagram
    participant U as 用户
    participant O as Orchestrator
    participant R as Registry
    participant S as Sub-Agent / Skill
    participant C as Context
    participant E as Experience

    U->>O: request("获取知乎热文")
    O->>C: add_message(user, ...)
    O->>E: query_failed_combinations()
    O->>O: plan() → 匹配 zhihu_hot
    O->>C: set_plan(plan_step)
    O->>R: find_skill("zhihu_hot")
    R-->>O: (agent_id=info, descriptor, execute)
    O->>S: SubAgent.run(Task)
    S->>S: execute(params) → 拉取热榜
    S-->>O: TaskResult
    O->>C: add_result(...)
    O->>E: append_experience(...)
    O-->>U: TaskResult
```

## 3. Skill 加载与注册

```mermaid
flowchart LR
    subgraph 约定目录
        D1[sub_agents/info/skills/<br/>zhihu_hot.py]
        D2[sub_agents/.../skills/<br/>*.py]
    end

    subgraph 加载器
        Load[load_skills_from_sub_agents]
    end

    subgraph 注册表
        Reg[Registry]
    end

    subgraph 主 Agent 工具
        Tools[register_builtin_tools<br/>run_code, list_dir, ...]
    end

    D1 & D2 --> Load
    Load --> Reg
    Tools --> Reg
    Reg --> Orch[Orchestrator 查询]
```

## 4. 契约与数据流

```mermaid
flowchart LR
    subgraph 任务契约
        T[Task<br/>task_id, skill, params, context]
    end

    subgraph 结果契约
        R[TaskResult<br/>task_id, status, result|error]
    end

    subgraph Skill 描述
        D[SkillDescriptor<br/>name, description, sub_agent, input_schema]
    end

    T --> Execute[execute(params)]
    Execute --> R
    D --> Reg[Registry]
```

---

说明：

- **Orchestrator**：根据请求做规划（规则匹配或后续扩展 LLM），通过 Registry 解析目标 Agent + Skill，再下发 Task 或本地执行。
- **Registry**：维护「Agent → Skill 列表」；主 Agent 的 Skill（含内置工具）与各 Sub-Agent 的 Skill 分开存储，按 name/description 查询。
- **Sub-Agent**：按 `task.skill` 从 Registry 取执行函数并调用，返回统一 TaskResult。
- **Context**：可选；存历史消息与结果，超阈值时自动 compact。
- **Experience**：可选；记录成功/失败，规划时可参考以自我演进。
