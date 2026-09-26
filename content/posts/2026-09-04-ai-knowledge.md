---
title: "2026-09-04 AI 知识库日报"
date: 2026-09-04T06:00:00+08:00
tags: [AI知识库, daily]
summary: "AI 对话知识提炼:共 2 条对话,提炼 2 条,含代码片段"
---

> 由本机 AI 自动总结,数据来源:当日 AI 对话记录(2/2 条有效)。
> 信息来源分布:Codex VSCode 扩展 (本地)(2条)

## 今日知识要点

### 图片下载脚本优化
- **核心结论**: 通过调整下载脚本，使用 Wikimedia 的缩略图 URL，解决了因频繁请求导致的 `429 Too many requests` 错误。
- **关键要点**:
  - 读取 `missing-local-images.json` 文件，提取 `slug` 和 `downloadUrl` 字段。
  - 使用 Python 脚本下载图片，并根据 `slug` 生成文件路径。
  - 为避免 `429 Too many requests` 错误，脚本会自动尝试使用 `1920px` 缩略图 URL。
  - 优化脚本以处理 Windows 命令解析问题，确保正确执行。
- **信息来源**: Codex VSCode 扩展 (本地)

**信息来源**: Codex VSCode 扩展 (本地)

## 今日知识要点
(无实质内容)

### 项目启动与依赖安装
- **核心结论**: 项目依赖安装过程中遇到 `workspace:*` 协议问题，通过修改为本地 `file:` 引用解决了安装失败。
- **关键要点**:
  - 项目使用 Astro + Vue + Tailwind CSS 技术栈。
  - 遇到 `npm run dev:web` 报错 `Missing field \`moduleType\``。
  - 依赖安装失败原因：npm 访问 registry 被沙箱拦截，同时 npm cache 日志目录权限不足。
  - 解决方案：修改依赖引用协议为本地 `file:`，并请求外部权限完成依赖下载。
- **信息来源**: Codex VSCode 扩展 (本地)

### 项目结构与配置
- **核心结论**: 项目采用 monorepo 结构，前端、API Worker、共享类型分别放在不同目录。
- **关键要点**:
  - 项目目录结构：`apps/web` 放前端代码，`apps/api` 放 API Worker，`packages/shared` 放共享类型。
  - 数据模型设计：植物核心表、分类名表、分布表、图片版权表、来源记录表分开，保证图片作者、许可证和来源 URL 是硬约束字段。
  - API 设计：`GET /api/plants` 支持分页和关键词，`GET /api/plants/:slug` 返回详情，返回结构统一成前端共享类型。
  - 页面设计：主页进入植物索引，不做营销页；列表卡片负责快速扫描，详情页展示分类、分布、图片授权和数据来源。
- **信息来源**: Codex VSCode 扩展 (本地)

## 排查涉及的代码片段
> 从当日对话中提取,供快速参考。
### 片段 1
```
植物ID
科学名
使用类别
使用部位
具体用途
处理方法
安全风险
证据等级
适用地区/文化
原始来源
授权协议
最后核验时间
```
### 片段 2(bash)
```bash
python download_missing_plant_images.py
```
### 片段 3(text)
```text
H:\vs-workspace\plant-encyclopedia\data\images\cache\plants\{slug}\primary.jpg
```
### 片段 4(bash)
```bash
python download_missing_plant_images.py --overwrite
```
### 片段 5(text)
```text
HTTPError status=429 reason='Too many requests ... instead use thumbnail images ...'
```
### 片段 6(text)
```text
https://upload.wikimedia.org/wikipedia/commons/...jpg?utm_content=thumbnail_unscaled
```
### 片段 7(text)
```text
原图直链去掉查询参数：200 OK
1920px 缩略图 URL：200 OK
```
### 片段 8(text)
```text
CC0
CC BY
```
### 片段 9(text)
```text
photo_license=cc0,cc-by
```
### 片段 10(text)
```text
[downloaded] allium-tuberosum -> _inat_test\allium-tuberosum\primary.jpg
license=cc-by
url=https://inaturalist-open-data.s3.amazonaws.com/photos/572343926/large.jpg
```

---

*本页由 [summarize.py](https://github.com/zhaiming86326/my-blog) 自动生成*
