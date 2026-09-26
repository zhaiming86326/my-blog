---
title: "2026-09-16 AI 知识库日报"
date: 2026-09-16T06:00:00+08:00
tags: [AI知识库, daily]
summary: "AI 对话知识提炼:共 2 条对话,提炼 2 条,含代码片段"
---

> 由本机 AI 自动总结,数据来源:当日 AI 对话记录(2/2 条有效)。
> 信息来源分布:Codex 桌面版 (本地)(2条)

## 今日知识要点

### 阿里云服务器磁盘空间估算
- **核心结论**：如果只是部署网站/接口，20GB 系统盘就足够，实际项目占用可以忽略不计。
- **关键要点**
  - `dist` 构建产物约 0.86 MB。
  - `public` 静态站点约 1.60 MB。
  - `worker + migrations + dist + 配置` 约 0.92 MB。
  - 整个仓库（不含 `.git` 和 `_non_deploy`）约 6.36 MB。
  - `.git` 约 47 MB。
  - `_non_deploy` 约 5.54 GB。
- **信息来源**：Codex 桌面版 (本地)

### 数据库选择建议
- **核心结论**：建议使用 PostgreSQL，优先顺序是 ECS 自建 PostgreSQL、阿里云 RDS PostgreSQL。
- **关键要点**
  - 小规模、省钱试运行：ECS 自建 PostgreSQL。
  - 正式上线、少操心：阿里云 RDS PostgreSQL。
  - 数据量很大/后期商业化：PolarDB PostgreSQL。
- **信息来源**：Codex 桌面版 (本地)

### Nginx 使用原因
- **核心结论**：Nginx 用于反向代理和负载均衡，提高服务器性能和安全性。
- **关键要点**
  - Nginx 可以处理静态文件和代理请求。
  - Nginx 提供了更好的性能和安全性。
- **信息来源**：Codex 桌面版 (本地)

### 图片存储建议
- **核心结论**：图片存储在云服务器上比 Cloudflare 快，可以通过访问服务器 IP 地址访问。
- **关键要点**
  - 图片存储在云服务器上比 Cloudflare 快。
  - 通过访问服务器 IP 地址访问图片。
- **信息来源**：Codex 桌面版 (本地)

## 排查涉及的代码片段
> 从当日对话中提取,供快速参考。
### 片段 1(text)
```text
/opt/flora-atlas/
  app/              # 当前运行版本
  releases/         # 每次部署的版本归档，可选
  shared/
    .env            # 环境变量，不进 Git
    logs/           # 应用日志
    uploads/        # 如果以后有上传文件
    backups/        # 小型备份或导出
```
### 片段 2(text)
```text
/opt/flora-atlas/
  dist/
  worker/
  package.json
  ecosystem.config.js 或 systemd service
  .env
  logs/
```
### 片段 3(bash)
```bash
sudo useradd --system --home /opt/flora-atlas --shell /usr/sbin/nologin flora
```
### 片段 4(bash)
```bash
sudo chown -R flora:flora /opt/flora-atlas
```
### 片段 5(text)
```text
/var/www/flora-atlas/
  index.html
  app.js
  style.css
  plant-details/
  fonts/
```
### 片段 6(text)
```text
/opt/flora-atlas/app
```
### 片段 7(bash)
```bash
sudo mkdir -p /opt/flora-atlas/app /opt/flora-atlas/shared/logs
sudo chown -R flora:flora /opt/flora-atlas
sudo chmod 750 /opt/flora-atlas
sudo chmod 700 /opt/flora-atlas/shared
sudo chmod 600 /opt/flora-atlas/shared/.env
```
### 片段 8(bash)
```bash
python -m http.server 4173 --bind 0.0.0.0 --directory public
```
### 片段 9(text)
```text
用户浏览器
   ↓ https://your-domain.com
Nginx :443
   ↓
静态文件：/var/www/flora-atlas
API：127.0.0.1:4173 或其他后端端口
```
### 片段 10(js)
```js
R2_IMAGE_PREFIX
R2_IMAGE_EXTENSION
```

---

*本页由 [summarize.py](https://github.com/zhaiming86326/my-blog) 自动生成*
