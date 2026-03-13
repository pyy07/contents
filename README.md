# Contents — 写作与发布管理

个人写作与发布管理仓库：管理草稿、已发表文章和素材，支持多端同步与后续 AI 辅助创作。

## 目录结构

| 目录 | 说明 |
|------|------|
| **drafts/** | 写作中的草稿，每篇一个 Markdown 文件 |
| **published/** | 已发表文章，按年份归档（如 `published/2025/`） |
| **materials/** | 素材：`quotes/` 摘录、`links/` 链接、`notes/` 零散笔记 |
| **templates/** | 文章模板（如 `article.md`），便于统一 frontmatter |
| **ai/** | 预留：AI 提示词、生成草稿等辅助创作内容 |

## 使用方式

- **写作**：在 `drafts/` 下新建 `.md`，可复制 `templates/article.md` 作为开头。
- **发表后**：将文章移到 `published/年份/`，并在 frontmatter 中写上 `published_at`、平台等。
- **素材**：在 `materials/` 下按类型存放摘录、链接和笔记，写作时引用。

## 托管在 GitHub

本仓库适合直接放在 GitHub 上，便于：

- 在不同电脑、手机（配合 GitHub 网页或 App）随时查看与编辑
- 用 Git 做版本历史，可回滚、对比修改
- 私有仓库可设为 Private，仅自己可见

### 首次推送到 GitHub

1. 在 GitHub 新建仓库（如 `pyy07/contents`），可选 Private。
2. 本地在项目根目录执行：

```bash
git init
git add .
git commit -m "init: 写作项目结构"
git branch -M main
git remote add origin https://github.com/你的用户名/contents.git
git push -u origin main
```

### 日常同步

- 写完后：`git add .` → `git commit -m "更新：xxx"` → `git push`
- 换设备时：`git clone` 或 `git pull` 即可继续写

## 后续扩展

- **AI 辅助**：在 `ai/` 中放 prompt、角色设定；从 `materials/` 取素材做检索或续写。
- **自动化**：可加脚本根据 frontmatter 生成文章索引、按 tag 筛选等。
