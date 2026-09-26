---
title: "2026-09-17 AI 知识库日报"
date: 2026-09-17T06:00:00+08:00
tags: [AI知识库, daily]
summary: "AI 对话知识提炼:共 4 条对话,提炼 4 条,含代码片段"
---

> 由本机 AI 自动总结,数据来源:当日 AI 对话记录(4/4 条有效)。
> 信息来源分布:Codex 桌面版 (本地)(4条)

## 今日知识要点

### Hero 区域重构设计
- **核心结论**: Hero 区域需采用极简自然风，使用大地色系/竹青色/米白色（#F7F6F0），搭配优雅的衬线字体标题。
- **关键要点**:
  - **左侧内容**:
    - 副标题、大标题、简短描述、带搜索按钮的输入框、热门标签、数据统计项（如 35178+ 已收集植物）。
    - 内容需垂直居中，使用 CSS Flex/Grid 统筹间距。
  - **右侧图片卡片**:
    - 固定纵横比（如 3/4 或 4/5），外层加上微阴影和 20px 圆角。
    - 使用 `object-fit: cover` 确保图片完美填充。
    - 卡片底部需带有半透明黑/深绿色的渐变遮罩，浮现植物名称（如：铁线蕨 Adiantum）和跳转图标。
  - **响应式**:
    - 桌面端左右 1:1 双栏，移动端自动折叠为单栏。
- **信息来源**: Codex 桌面版 (本地)

### 数据库配置调整
- **核心结论**: 本地测试时访问本地的 SQLite 数据库，部署到服务器上时访问服务器的 PostgreSQL 数据库。
- **关键要点**:
  - **本地配置**:
    - 使用 `H:\vs-workspace\plants-data\clean\wcvp\_backbone.sqlite` 作为本地测试数据库。
    - 将 SQL 复制到 `H:\github\flora-atlas\local-sql\wcvp\_backbone.sqlite`。
  - **服务器配置**:
    - 配置为访问服务器上的 PostgreSQL 数据库。
- **信息来源**: Codex 桌面版 (本地)

### API 问题排查
- **核心结论**: `/api/summary` 404 错误，返回的数据不是真实数据库的数据。
- **关键要点**:
  - **排查步骤**:
    - 确认 API 路径和请求方法是否正确。
    - 检查数据库连接配置是否正确。
    - 确认数据返回逻辑是否正确。
- **信息来源**: Codex 桌面版 (本地)

### Hero 区域重构
- **核心结论**：通过 HTML/CSS 重构 Hero 区域，确保极简自然风设计，响应式布局，以及图片卡片的正确显示。
- **关键要点**
  - 使用大地色系/竹青色/米白色（#F7F6F0）。
  - 副标题、大标题、简短描述、带搜索按钮的输入框、热门标签、数据统计项垂直居中。
  - 右侧图片卡片固定纵横比（如 4:5），外层加微阴影和圆角，底部带有半透明渐变遮罩。
  - 响应式设计：桌面端左右 1:1 双栏，移动端单栏。
  - 重构过程中，保留现有交互与搜索逻辑，只重做 Hero 的布局、配色、比例、遮罩和响应式行为。
- **信息来源**：DeepSeek 网页

### 数据库配置调整
- **核心结论**：本地测试访问 SQLite 数据库，部署到服务器上访问 PostgreSQL 数据库。
- **关键要点**
  - 本地文件路径：`H:\github\flora-atlas\local-sql\wcvp\_backbone.sqlite`。
  - 配置文件中调整数据库连接字符串，确保本地和服务器环境的正确数据库访问。
- **信息来源**：DeepSeek 网页

### 本地开发与部署问题排查
- **核心结论**：通过 Playwright 进行本地开发和部署问题排查，确保页面布局和图片显示正确。
- **关键要点**
  - 使用 Playwright CLI 打开本地静态页，检查桌面和移动视口布局。
  - 临时设置桌面视口宽度（1280×900），确保双栏和 4:5 卡片显示正确。
  - 本地预览时，优先使用摘要里的远程地址，确保本地预览不会出现深色空图。
- **信息来源**：DeepSeek 网页

## 排查涉及的代码片段
> 从当日对话中提取,供快速参考。
### 片段 1(powershell)
```powershell
$env:DB_DRIVER='sqlite'
$env:SQLITE_DB_PATH='../../local-sql/wcvp_backbone.sqlite'
$env:HOST='127.0.0.1'
$env:PORT='11112'
node deploy\flora-atlas\server.js
```
### 片段 2(env)
```env
SQLITE_DB_PATH=H:\vs-workspace\plants-data\clean\wcvp\_backbone.sqlite
```
### 片段 3(json)
```json
/api/health => { "ok": true, "database": "sqlite" }
/api/summary => plants: 35178, families: 302
/api/plants?limit=1 => total: 35178
```
### 片段 4(text)
```text
http://127.0.0.1:4173/
http://127.0.0.1:4173/api/summary
```

---

*本页由 [summarize.py](https://github.com/zhaiming86326/my-blog) 自动生成*
