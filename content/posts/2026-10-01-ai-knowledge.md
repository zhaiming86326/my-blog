---
title: "2026-10-01 AI 知识库日报"
date: 2026-10-01T06:00:00+08:00
tags: [AI知识库, daily]
summary: "AI 对话知识提炼:共 3 条对话,提炼 3 条,含代码片段"
---

> 由本机 AI 自动总结,数据来源:当日 AI 对话记录(3/3 条有效)。
> 信息来源分布:Codex 桌面版 (本地)(3条)

## 今日知识要点

### Spring Cloud 示例工程

- **核心结论**: 创建了一个基于 JDK 21 的 Spring Cloud 示例工程，包含注册、登录、鉴权和权限控制，使用 Spring Security 和 JWT。
- **关键要点**:
  - **工程结构**:
    - 三个模块: Eureka 注册中心、Gateway 网关和用户认证服务。
    - Spring Security 负责密码验证与 JWT 鉴权。
    - 使用 Flyway 建表。
  - **主要功能**:
    - 用户注册: 使用 BCrypt 加密密码。
    - 用户登录: 校验密码和 JWT。
    - 权限控制: 通过方法权限控制管理员接口。
  - **参数校验**: 包含参数错误处理。
  - **编码规范**: 符合阿里 Java 主要编码约定。
  - **配置文件**:
    - **配置模板**: 在 `H:/github/spring-demo/config/application-local.example.yml`，填写数据库信息和 JWT 密钥。
    - **启动命令**: 在 `README.md` 中提供。
  - **测试验证**:
    - `mvn verify` 通过，覆盖普通用户被拒绝、管理员访问成功，以及 JWT 校验。
- **信息来源**: 来源: Codex 桌面版 (本地)

### PostgreSQL 17 配置

- **核心结论**: 提供了 PostgreSQL 17 的配置模板。
- **关键要点**:
  - **配置文件**: 在 `H:/github/spring-demo/config/application-local.example.yml`。
  - **配置项**:
    - 数据库连接信息。
    - JWT 密钥。
- **信息来源**: 来源: Codex 桌面版 (本地)

### 注释与代码示例

- **核心结论**: 代码中包含详细的注释，符合阿里 Java 主要编码约定。
- **关键要点**:
  - **代码示例**:
    ```java
    // 密码使用 BCrypt 加密
    @Autowired
    private BCryptPasswordEncoder bCryptPasswordEncoder;

    @PostMapping("/register")
    public ResponseEntity<String> register(@RequestBody User user) {
        // 参数校验
        if (user == null || user.getUsername() == null || user.getPassword() == null) {
            return ResponseEntity.status(HttpStatus.BAD_REQUEST).body("Invalid request parameters");
        }
        // 加密密码
        String encodedPassword = bCryptPasswordEncoder.encode(user.getPassword());
        user.setPassword(encodedPassword);
        // 保存用户
        userService.save(user);
        return ResponseEntity.ok("User registered successfully");
    }
    ```
- **信息来源**: 来源: Codex 桌面版 (本地)

## 排查涉及的代码片段
> 从当日对话中提取,供快速参考。
### 片段 1(powershell)
```powershell
psql -h YOUR_DB_HOST -U code_atlas -d code_atlas -v ON_ERROR_STOP=1 -f .\database\001_stage2.sql
```
### 片段 2(powershell)
```powershell
cd backend
.\mvnw.cmd spring-boot:run
# 另一终端
cd frontend
npm run dev
```
### 片段 3(yaml)
```yaml
code-atlas:
  models:
    llm:
      base-url: ${LLM_BASE_URL:https://api.openai.com/v1}
      model: ${LLM_MODEL:gpt-4.1-mini-2025-04-14}
      api-key=[已脱敏]
      input-price-per-million: 0.40
      output-price-per-million: 1.60
      price-basis: "OpenAI 官方标准价格，2026-10-01，USD/百万 Token"

    embedding:
      base-url: ${EMBEDDING_BASE_URL:https://api.openai.com/v1}
      model: ${EMBEDDING_MODEL:text-embedding-3-small}
      api-key=[已脱敏]
      dimensions: 1536
      revision: "1"
      input-price-per-million: 0.02
      price-basis: "OpenAI 官方标准价格，2026-10-01，USD/百万 Token"
```
### 片段 4(yaml)
```yaml
llm:
  base-url: ${LLM_BASE_URL:https://api.deepseek.com}
  model: ${LLM_MODEL:deepseek-flash}
  api-key=[已脱敏]
  price-basis: "暂未配置价格，费用未知"
```
### 片段 5(yaml)
```yaml
llm:
  base-url: https://api.deepseek.com
  model: deepseek-flash
  api-key=[已脱敏]

embedding:
  base-url: https://api.openai.com/v1
  model: text-embedding-3-small
  api-key=[已脱敏]
  dimensions: 1536
  revision: "1"
```
### 片段 6(powershell)
```powershell
ollama pull qwen3-embedding:0.6b
```
### 片段 7(yaml)
```yaml
embedding:
  base-url: http://127.0.0.1:11434/v1
  model: qwen3-embedding:0.6b
  api-key=[已脱敏]
  dimensions: 1024
  revision: "1"
  price-basis: "本机推理，无云端调用账单；硬件和电费未估算"
```
### 片段 8(sql)
```sql
SELECT
    v.title,
    v.sequence_no AS document_version,
    p.model,
    p.dimensions,
    i.status,
    i.chunk_count,
    i.error,
    i.completed_at
FROM atlas_vector_index i
JOIN atlas_document_version v ON v.id = i.version_id
JOIN atlas_embedding_profile p ON p.id = i.profile_id
ORDER BY i.started_at DESC;
```
### 片段 9(sql)
```sql
SELECT
    v.title,
    c.ordinal,
    c.section_path,
    p.model,
    vector_dims(e.embedding) AS dimensions,
    left(e.embedding::text, 160) AS vector_preview
FROM atlas_chunk_embedding e
JOIN atlas_chunk c ON c.id = e.chunk_id
JOIN atlas_document_version v ON v.id = c.version_id
JOIN atlas_embedding_profile p ON p.id = e.profile_id
LIMIT 20;
```
### 片段 10(powershell)
```powershell
.\mvnw.cmd spring-boot:run "-Dspring-boot.run.arguments=--logging.level.com.codeatlas.service.RagService=DEBUG"
```

---

*本页由 [summarize.py](https://github.com/zhaiming86326/my-blog) 自动生成*
