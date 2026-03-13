# Agent 配置说明

## 当前状态：未使用大模型

主 Agent 的**规划与匹配**目前为**规则实现**（如关键词「知乎」「热榜」→ zhihu_hot），**未调用任何 LLM**，因此**无需配置 API Key、Base URL 或模型名**即可运行现有能力（内置工具、zhihu_hot Skill 等）。

## 按 Agent 配置不同 LLM（预留）

主 Agent 与每个 Sub-Agent **均可单独配置一套 LLM**（API Key、Base URL、模型名），便于：

- 主 Agent 用强模型做规划与汇总，Sub-Agent 用轻量模型或专用模型；
- 不同领域 Sub-Agent 使用不同厂商或不同模型。

配置通过**环境变量**读取，由 `agent.core.config.get_llm_config(agent_id)` 统一获取。

### 环境变量规则

对每个 Agent 使用前缀 `LLM_<AGENT_ID>_`（`agent_id` 大写、中划线转下划线）。未设置时回退到通用 `LLM_*`。

| 变量名格式 | 说明 | 示例（主 Agent） | 示例（info Sub-Agent） |
|------------|------|------------------|------------------------|
| `LLM_<AGENT_ID>_API_KEY` | API 密钥 | `LLM_MAIN_API_KEY` | `LLM_INFO_API_KEY` |
| `LLM_<AGENT_ID>_BASE_URL` | API 基地址 | `LLM_MAIN_BASE_URL` | `LLM_INFO_BASE_URL` |
| `LLM_<AGENT_ID>_MODEL` | 模型名称 | `LLM_MAIN_MODEL` | `LLM_INFO_MODEL` |

**通用回退**（未配置某 Agent 专属变量时使用）：

- `LLM_API_KEY`、`LLM_BASE_URL`、`LLM_MODEL`
- 或 `OPENAI_API_KEY`、`OPENAI_BASE_URL`、`OPENAI_MODEL`

### 在代码中读取

```python
from agent.core.config import get_llm_config, LLMConfig

# 主 Agent 的 LLM 配置
main_cfg = get_llm_config("main")
# main_cfg.api_key, main_cfg.base_url, main_cfg.model
# main_cfg.is_configured()  # 是否已配置

# 某 Sub-Agent 的 LLM 配置（如 info）
info_cfg = get_llm_config("info")
```

接入 LLM 时，Orchestrator 使用 `get_llm_config("main")`，各 Sub-Agent 使用 `get_llm_config(self.agent_id)` 即可拿到各自配置。

### 配置示例

**主 Agent 与 info 使用同一套密钥、不同模型：**

```bash
LLM_API_KEY=sk-xxx
LLM_BASE_URL=https://api.openai.com/v1
LLM_MAIN_MODEL=gpt-4o
LLM_INFO_MODEL=gpt-4o-mini
```

**主 Agent 用 OpenAI，info 用本地/代理：**

```bash
LLM_MAIN_API_KEY=sk-openai-xxx
LLM_MAIN_BASE_URL=https://api.openai.com/v1
LLM_MAIN_MODEL=gpt-4o-mini

LLM_INFO_API_KEY=sk-local
LLM_INFO_BASE_URL=http://localhost:8000/v1
LLM_INFO_MODEL=qwen-plus
```

**全部使用通用变量（所有 Agent 同一套）：**

```bash
LLM_API_KEY=sk-xxx
LLM_BASE_URL=https://api.openai.com/v1
LLM_MODEL=gpt-4o-mini
```

### 配置模板与本地配置

仓库根目录提供 **`.env.example`**，列出全部可选变量与说明。复制为 `.env` 后填入真实值即可（`.env` 已在 .gitignore 中，不会提交）：

```bash
cp .env.example .env
# 编辑 .env 填入 API Key 等
```

应用启动时需自行加载 `.env`（如使用 `python-dotenv`：`load_dotenv()`）。本地配置示例：

```bash
# 主 Agent 与 info 分别配置
LLM_MAIN_API_KEY=sk-main-key
LLM_MAIN_BASE_URL=https://api.openai.com/v1
LLM_MAIN_MODEL=gpt-4o-mini

LLM_INFO_API_KEY=sk-info-key
LLM_INFO_BASE_URL=http://localhost:8000/v1
LLM_INFO_MODEL=qwen-plus
```
