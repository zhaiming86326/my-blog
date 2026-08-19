---
title: "2026-08-18 AI 知识库日报"
date: 2026-08-18T06:00:00+08:00
tags: [AI知识库, daily]
summary: "AI 对话知识提炼:共 120 条对话,提炼 104 条,含代码片段"
---

> 由本机 AI 自动总结,数据来源:当日 AI 对话记录(104/120 条有效)。
> 信息来源分布:DeepSeek API(103条)、DeepSeek Harness(1条)

## 今日知识要点

### PAC配置问题
- **核心结论**：当前 PAC 配置将所有流量指向 v2rayN，导致 v2rayN 退出后无法上网。
- **关键要点**
  - 当前 PAC 配置：AI 域名 → 8080(mitmproxy) → 10809(v2rayN)，其他流量 → 10809(v2rayN)。
  - 问题根源：PAC 将非 AI 流量也指向了 10809(v2rayN)，v2rayN 退出后，10809 端口失效，所有流量指向死端口，导致全网断网。
  - 更好的设计：AI 域名 → 8080(mitmproxy 直连)，其他流量 → DIRECT(直连)；需要翻墙的流量 → 8080 → 10809。
  - 解决方案：修改 PAC 配置，使非 AI 流量直接走直连，AI 流量走 mitmproxy，需要翻墙的流量走 mitmproxy → v2rayN。
- **信息来源**：DeepSeek API

### 修复启动失败问题
- **核心结论**：启动失败的原因是 `LangChainConfig.java` 中未解析的 `@Value` 占位符导致 Spring 启动失败。
- **关键要点**
  - `LangChainConfig.java` 中保留了三个 `@Value` 注入字段，但对应的 `@Bean` 被注释掉。
  - 由于环境变量未定义，Spring 在实例化 `LangChainConfig` Bean 时抛出异常，导致应用启动失败。
  - 解决方案：删除无用的 `@Value` 注入字段和对应的注释代码，保留纯 Ollama 配置。
  - 修复后的 `LangChainConfig.java`：
    ```java
    @Configuration
    public class LangChainConfig {
        @Bean
        public ChatModel chatModel() {
            return OllamaChatModel.builder()
                .baseUrl("http://localhost:11434")
                .modelName("qwen2.5:14b-instruct")
                .temperature(0.7)
                .build();
        }
    }
    ```
  - 验证编译和启动，确保应用能正常启动。
- **信息来源**：DeepSeek API

### 构建 IntelliJ 插件
- **核心结论**：创建一个 IntelliJ 插件，实现右键选中文本后，出现“翻譯此段”菜单，将选中的文字翻译为中文简体。
- **关键要点**
  - 项目结构：
    ```
    idea-trans/
    ├── build.gradle.kts
    ├── settings.gradle.kts
    ├── gradle.properties
    ├── src/main/kotlin/...  (插件代码)
    ├── src/main/resources/META-INF/plugin.xml
    ```
  - 插件功能：
    - 右键菜单“翻譯此段”
    - 使用 Google 免费翻译接口 `https://translate.googleapis.com/translate_a/single`
    - 显示翻译结果在 tooltip 或对话框中
  - 实现细节：
    - `AnAction` 子类，注册在编辑器的右键菜单中
    - 获取选中文本：`Editor.getSelectionModel().getSelectedText()`
    - 调用翻译 API（使用 `java.net.http.HttpClient`）
    - 显示结果：使用 `Notifications.Bus` 或自定义 `JBPopup`
  - 构建验证：`gradle buildPlugin`
- **信息来源**：DeepSeek API

### 使用本地 LLM 模型进行翻译
- **核心结论**：修改 IntelliJ 插件，使用本地 LLM 模型（Qwen14B）进行翻译。
- **关键要点**
  - 修改 `Translator.kt`，调用 Ollama API：
    ```kotlin
    object Translator {
        private const val ENDPOINT = "http://localhost:11434/api/generate"
        private const val MODEL = "qwen:14b"

        private val client: HttpClient = HttpClient.newBuilder()
            .connectTimeout(Duration.ofSeconds(10))
            .build()

        fun translate(text: String): String {
            val payload = JsonObject().apply {
                addProperty("model", MODEL)
                addProperty("prompt", "Translate to Simplified Chinese: $text")
                addProperty("stream", false)
            }
            val request = HttpRequest.newBuilder()
                .uri(URI.create(ENDPOINT))
                .header("Content-Type", "application/json")
                .POST(HttpRequest.BodyPublishers.ofString(payload.toString()))
                .build()
            val response = client.send(request, HttpResponse.BodyHandlers.ofString())
            val json = JsonParser.parseString(response.body()).asJsonObject
            return json.get("response").asString
        }
    }
    ```
  - 更新 `plugin.xml` 和 README，移除 Google 翻译相关描述。
- **信息来源**：DeepSeek API

## 排查涉及的代码片段
> 从当日对话中提取,供快速参考。
### 片段 1(javascript)
```javascript
AI 域名 → PROXY 127.0.0.1:8080   (mitmproxy → 10809)
其他所有流量 → PROXY 127.0.0.1:10809   (v2rayN)  ← 问题在这
```
### 片段 2
```
deepseek.com ──► 8080  mitmproxy(直连出站)          ──► DeepSeek 服务器
chatgpt/grok ──► 8082  mitmproxy(upstream 10809)   ──► v2rayN 翻墙
其他流量     ──► 直连(不经任何代理)
```
### 片段 3
```

虽然把 Azure的 `@Bean`注释掉了，改用 Ollama，但**这三个 `@Value`字段仍然存在**。Spring在创建 `LangChainConfig`这个 `@Configuration` Bean时，会对这三个字段进行占位符解析。如果环境变量 `AZURE_OPENAI_ENDPOINT`、`AZURE_OPENAI_API_KEY`、`AZURE_OPENAI_DEPLOYMENT`没有定义，Spring启动会直接抛异常：

> `Could not resolve placeholder 'AZURE_OPENAI_ENDPOINT' in value "${AZURE_OPENAI_ENDPOINT}"`

这会导致应用**启动失败**，即使你用的是 Ollama而不是 Azure。

另外还有一个连带的启动问题：`OllamaChatModel.builder()`指定了模型 `qwen2.5:14b-instruct`，如果本地 Ollama没下载这个模型，会在运行时报错（但这不会阻止启动，因为 builder只是构建配置）。不过主因是 `@Value`占位符。

让我先确认一下这个模块是否在根 pom中被启用了。注意根 pom中 `01-introduction`被注释掉了：
```
### 片段 4(JAVA)
```JAVA
package com.example.langchain4j.config;

import dev.langchain4j.model.chat.ChatModel;
import dev.langchain4j.model.ollama.OllamaChatModel;
/*import dev.langchain4j.model.openaiofficial.OpenAiOfficialChatModel;*/
import org.springframework.beans.factory.annotation.Value;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;

import java.time.Duration;

/**
 * Configuration for LangChain4j with Azure OpenAI using the OpenAI Official client.
 * 
 * The OpenAI Official client supports Azure OpenAI endpoints, providing a unified
 * interface for both OpenAI and Azure OpenAI services.
 */
@Configuration
public class LangChainConfig {

    @Value("${AZURE_OPENAI_ENDPOINT}")
    private String azureEndpoint;

    @Value("${AZURE_OPENAI_API_KEY}")
    private String azureApiKey;

    @Value("${AZURE_OPENAI_DEPLOYMENT}")
    private String deploymentName; // Azure deployment name, used as modelName

    /**
     * Creates the OpenAI Official chat model configured for Azure OpenAI.
     * 
     * @return configured OpenAiOfficialChatModel
     */
    /*@Bean*/
/*    public OpenAiOfficialChatModel openAiOfficialChatModel() {
        return OpenAiOfficialChatModel.builder()
                .baseUrl(azureEndpoint)
                .apiKey(azureApiKey)
                .modelName(deploymentName)
                .timeout(Duration.ofMinutes(5))
                .maxRetries(3)
                .build();
    }*/

    @Bean
    public ChatModel chatModel() {
        // 直接创建一个 OllamaChatModel 的 Bean
        return OllamaChatModel.builder()
                .baseUrl("http://localhost:11434") // Ollama 服务地址，默认就是这个
                .modelName("qwen2.5:14b-instruct") // 务必和下载的模型名一致
                .temperature(0.7) // 可选：控制回答的随机性
                .build();
    }
}
```
### 片段 5
```
package com.example.langchain4j.config;

import dev.langchain4j.model.chat.ChatModel;
import dev.langchain4j.model.ollama.OllamaChatModel;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;

/**
 * Configuration for LangChain4j chat model using a local Ollama instance.
 *
 * The app talks to a locally running Ollama server (http://localhost:11434)
 * with the "qwen2.5:14b-instruct" model already pulled.
 */
@Configuration
public class LangChainConfig {

    /**
     * Creates the chat model backed by a local Ollama server.
     *
     * @return configured OllamaChatModel
     */
    @Bean
    public ChatModel chatModel() {
        return OllamaChatModel.builder()
                .baseUrl("http://localhost:11434") // Ollama 服务地址，默认就是这个
                .modelName("qwen2.5:14b-instruct") // 务必和下载的模型名一致
                .temperature(0.7) // 可选：控制回答的随机性
                .build();
    }
}
```
### 片段 6
```

由于 `application.yaml`中没有这些配置，环境变量也没有定义，Spring在实例化这个 `@Configuration` Bean做占位符解析时就会抛异常：

> `Could not resolve placeholder 'AZURE_OPENAI_ENDPOINT' in value "${AZURE_OPENAI_ENDPOINT}"`

**这导致应用一启动就失败**——即便你实际上用的是 Ollama而不是 Azure。

###所做的修改清理了 `LangChainConfig.java`，删除所有无用的 Azure `@Value`字段和对应注释代码，保留一个干净的纯 Ollama配置：
```
### 片段 7(XML)
```XML
<project xmlns="http://maven.apache.org/POM/4.0.0"
         xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
         xsi:schemaLocation="http://maven.apache.org/POM/4.0.0
                             https://maven.apache.org/xsd/maven-4.0.0.xsd">
  <modelVersion>4.0.0</modelVersion>

  <groupId>com.example.langchain4j</groupId>
  <artifactId>langchain4j-for-beginners</artifactId>
  <version>1.0.0</version>
  <packaging>pom</packaging>

  <modules>
    <!--<module>01-introduction</module>-->
    <module>02-prompt-engineering</module>
    <module>03-rag</module>
    <module>04-tools</module>
    <module>05-mcp</module>
  </modules>

  <properties>
    <!-- Use Java 21 by default.  Override by setting the
         JAVA_HOME environment variable or the `java.version` property -->
    <java.version>21</java.version>
    <spring.boot.version>4.0.1</spring.boot.version>
    <!-- Set the LangChain4j version to a recent stable release -->
    <langchain4j.version>1.18.1</langchain4j.version>
    <!-- MCP support requires beta version -->
    <langchain4j.mcp.version>1.18.1-beta28</langchain4j.mcp.version>
    <!-- Test dependency versions - JUnit version managed by Spring Boot BOM -->
    <assertj.version>3.27.7</assertj.version>
    <testcontainers.version>2.0.2</testcontainers.version>
    <!-- Logging versions - aligned with Spring Boot 4.0.0 -->
    <slf4j.version>2.0.17</slf4j.version>
    <logback.version>1.5.18</logback.version>
    <!-- Other dependency versions -->
    <pdfbox.version>2.0.31</pdfbox.version>
    <!-- Maven plugin versions -->
    <maven.surefire.version>3.5.4</maven.surefire.version>
    <maven.compiler.plugin.version>3.13.0</maven.compiler.plugin.version>
    <!-- Encoding -->
    <project.build.sourceEncoding>UTF-8</project.build.sourceEncoding>
    <project.reporting.outputEncoding>UTF-8</project.reporting.outputEncoding>
    <maven.compiler.encoding>UTF-8</maven.compiler.encoding>
  </properties>

  <dependencyManagement>
    <dependencies>
      <!-- LangChain4j dependency versions -->
      <dependency>
        <groupId>dev.langchain4j</groupId>
        <artifactId>langchain4j-bom</artifactId>
        <version>${langchain4j.version}</version>
        <type>pom</type>
        <scope>import</scope>
      </dependency>
      
      <!-- Import Spring Boot dependency versions -->
      <dependency>
        <groupId>org.springframework.boot</groupId>
        <artifactId>spring-boot-dependencies</artifactId>
        <version>${spring.boot.version}</version>
        <type>pom</type>
        <scope>import</scope>
      </dependency>
      
      <!-- Testing dependencies - JUnit managed by Spring Boot BOM -->
      <dependency>
        <groupId>org.assertj</groupId>
        <artifactId>assertj-core</artifactId>
        <version>${assertj.version}</version>
        <scope>test</scope>
      </dependency>
      <dependency>
        <groupId>org.testcontainers</groupId>
        <artifactId>testcontainers</artifactId>
        <version>${testcontainers.version}</version>
        <scope>test</scope>
      </dependency>
      <dependency>
        <groupId>org.testcontainers</groupId>
        <artifactId>testcontainers-junit-jupiter</artifactId>
        <version>${testcontainers.version}</version>
        <scope>test</scope>
      </dependency>
      
      <!-- Logging dependencies - aligned with Spring Boot 4.0.0 -->
      <dependency>
        <groupId>org.slf4j</groupId>
        <artifactId>slf4j-simple</artifactId>
        <version>${slf4j.version}</version>
      </dependency>
      <dependency>
        <groupId>ch.qos.logback</groupId>
        <artifactId>logback-classic</artifactId>
        <version>${logback.version}</version>
      </dependency>
      
      <!-- Other dependencies -->
      <dependency>
        <groupId>org.apache.pdfbox</groupId>
        <artifactId>pdfbox</artifactId>
        <version>${pdfbox.version}</version>
      </dependency>
    </dependencies>
  </dependencyManagement>

  <build>
    <pluginManagement>
      <plugins>
        <plugin>
          <groupId>org.apache.maven.plugins</groupId>
          <artifactId>maven-compiler-plugin</artifactId>
          <version>${maven.compiler.plugin.version}</version>
          <configuration>
            <source>${java.version}</source>
            <target>${java.version}</target>
            <release>${java.version}</release>
            <parameters>true</parameters>
          </configuration>
        </plugin>
        <plugin>
          <groupId>org.springframework.boot</groupId>
          <artifactId>spring-boot-maven-plugin</artifactId>
          <version>${spring.boot.version}</version>
        </plugin>
        <plugin>
          <groupId>org.apache.maven.plugins</groupId>
          <artifactId>maven-surefire-plugin</artifactId>
          <version>${maven.surefire.version}</version>
        </plugin>
      </plugins>
    </pluginManagement>
  </build>
</project>
```
### 片段 8
```
  <modules>
    <module>01-introduction</module>
    <module>02-prompt-engineering</module>
    <module>03-rag</module>
    <module>04-tools</module>
    <module>05-mcp</module>
  </modules>
```
### 片段 9(JAVA)
```JAVA
package com.example.langchain4j.service;

import dev.langchain4j.data.message.AiMessage;
import dev.langchain4j.data.message.ChatMessage;
import dev.langchain4j.model.chat.response.ChatResponse;
import dev.langchain4j.model.openaiofficial.OpenAiOfficialChatModel;

import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.Mock;
import org.mockito.junit.jupiter.MockitoExtension;
import org.mockito.junit.jupiter.MockitoSettings;
import org.mockito.quality.Strictness;

import java.util.List;

import static org.assertj.core.api.Assertions.assertThat;
import static org.mockito.ArgumentMatchers.anyList;
import static org.mockito.Mockito.when;

/**
 * Simple tests for ConversationService demonstrating conversation management and memory.
 * These tests validate conversation lifecycle, memory management, and context preservation.
 * 
 * Testing Philosophy for Beginners:
 * - Uses Mockito to mock OpenAiOfficialChatModel (simplest way!)
 * - @Mock annotation creates a mock instance
 * - when().thenReturn() defines the mock behavior
 * - Tests the conversation management logic without real LLM calls
 * - Keeps tests fast, deterministic, and independent
 */
@ExtendWith(MockitoExtension.class)
@MockitoSettings(strictness = Strictness.LENIENT)
@DisplayName("Conversation Service Tests")
class SimpleConversationTest {

    private ConversationService conversationService;
    
    @Mock
    private OpenAiOfficialChatModel mockChatModel;

    @BeforeEach
    void setUp() {
        // Set up default mock behavior - return a simple response
        ChatResponse mockResponse = ChatResponse.builder()
            .aiMessage(AiMessage.from("This is a test response"))
            .build();
        when(mockChatModel.chat(anyList())).thenReturn(mockResponse);
        
        conversationService = new ConversationService(mockChatModel);
    }

    @Test
    @DisplayName("Should create a new conversation with unique ID")
    void shouldStartConversation() {
        // When
        String conversationId = conversationService.startConversation();

        // Then
        assertThat(conversationId)
            .isNotNull()
            .isNotEmpty();
        assertThat(conversationService.conversationExists(conversationId)).isTrue();
    }

    @Test
    @DisplayName("Should generate different conversation IDs for each new conversation")
    void shouldGenerateUniqueConversationIds() {
        // When
        String id1 = conversationService.startConversation();
        String id2 = conversationService.startConversation();

        // Then
        assertThat(id1).isNotEqualTo(id2);
    }

    @Test
    @DisplayName("Should maintain conversation history across multiple messages")
    void shouldMaintainConversationHistory() {
        // Given
        String conversationId = conversationService.startConversation();
        
        // Configure mock to return different responses
        ChatResponse mockResponse1 = ChatResponse.builder()
            .aiMessage(AiMessage.from("Response 1"))
            .build();
        ChatResponse mockResponse2 = ChatResponse.builder()
            .aiMessage(AiMessage.from("Response 2"))
            .build();
        ChatResponse mockResponse3 = ChatResponse.builder()
            .aiMessage(AiMessage.from("Response 3"))
            .build();
        
        when(mockChatModel.chat(anyList()))
            .thenReturn(mockResponse1)
            .thenReturn(mockResponse2)
            .thenReturn(mockResponse3);

        // When
        conversationService.chat(conversationId, "First message");
        conversationService.chat(conversationId, "Second message");
        conversationService.chat(conversationId, "Third message");

        // Then
        List<ChatMessage> history = conversationService.getHistory(conversationId);
        assertThat(history).hasSize(6); // 3 user messages + 3 AI responses
    }

    @Test
    @DisplayName("Should include previous messages as context in new prompts")
    void shouldIncludeContextInPrompt() {
        // Given
        String conversationId = conversationService.startConversation();
        
        ChatResponse mockResponse = ChatResponse.builder()
            .aiMessage(AiMessage.from("Response"))
            .build();
        when(mockChatModel.chat(anyList())).thenReturn(mockResponse);

        // When
        conversationService.chat(conversationId, "Tell me about Java");
        conversationService.chat(conversationId, "What about Spring Boot?");

        // Then
        List<ChatMessage> history = conversationService.getHistory(conversationId);
        assertThat(history).hasSize(4); // 2 user + 2 AI messages
        // Conversation service builds context from all messages
    }

    @Test
    @DisplayName("Should isolate conversations by ID")
    void shouldIsolateConversationsByid() {
        // Given
        String conv1 = conversationService.startConversation();
        String conv2 = conversationService.startConversation();
        
        ChatResponse mockResponse = ChatResponse.builder()
            .aiMessage(AiMessage.from("Response"))
            .build();
        when(mockChatModel.chat(anyList())).thenReturn(mockResponse);

        // When
        conversationService.chat(conv1, "Message for conversation 1");
        conversationService.chat(conv2, "Message for conversation 2");

        // Then
        List<ChatMessage> history1 = conversationService.getHistory(conv1);
        List<ChatMessage> history2 = conversationService.getHistory(conv2);
        
        assertThat(history1).hasSize(2); // 1 user + 1 AI
        assertThat(history2).hasSize(2); // 1 user + 1 AI
        // Each conversation maintains its own separate history
    }

    @Test
    @DisplayName("Should clear conversation history")
    void shouldClearConversation() {
        // Given
        String conversationId = conversationService.startConversation();
        ChatResponse mockResponse = ChatResponse.builder()
            .aiMessage(AiMessage.from("Response"))
            .build();
        when(mockChatModel.chat(anyList())).thenReturn(mockResponse);
        conversationService.chat(conversationId, "Test message");

        // When
        conversationService.clearConversation(conversationId);

        // Then
        assertThat(conversationService.conversationExists(conversationId)).isFalse();
    }

    @Test
    @DisplayName("Should auto-create conversation if ID doesn't exist")
    void shouldAutoCreateConversationIfNotExists() {
        // Given
        String nonExistentId = "non-existent-conversation-id";
        ChatResponse mockResponse = ChatResponse.builder()
            .aiMessage(AiMessage.from("Response"))
            .build();
        when(mockChatModel.chat(anyList())).thenReturn(mockResponse);

        // When
        String response = conversationService.chat(nonExistentId, "Test message");

        // Then
        assertThat(response).isNotNull();
        assertThat(conversationService.conversationExists(nonExistentId)).isTrue();
    }

    @Test
    @DisplayName("Should respect maximum message window of 10 messages")
    void shouldRespectMaxMessageWindow() {
        // Given
        String conversationId = conversationService.startConversation();
        ChatResponse mockResponse = ChatResponse.builder()
            .aiMessage(AiMessage.from("Response"))
            .build();
…(截断)
```
### 片段 10
```
import dev.langchain4j.data.message.AiMessage;
import dev.langchain4j.data.message.ChatMessage;
import dev.langchain4j.model.chat.ChatModel;
import dev.langchain4j.model.chat.response.ChatResponse;
```

---

*本页由 [summarize.py](https://github.com/zhaiming86326/my-blog) 自动生成*
