# MCP服务器开发最佳实践和指南

## 概述

本文档汇编了构建模型上下文协议（MCP）服务器的基本最佳实践和指南。它涵盖命名约定、工具设计、响应格式、分页、错误处理、安全性和合规要求。

---

## 快速参考

### 服务器命名
- **Python**：`{service}_mcp`（例如，`slack_mcp`）
- **Node/TypeScript**：`{service}-mcp-server`（例如，`slack-mcp-server`）

### 工具命名
- 使用带服务前缀的snake_case
- 格式：`{service}_{action}_{resource}`
- 示例：`slack_send_message`、`github_create_issue`

### 响应格式
- 支持JSON和Markdown两种格式
- JSON用于程序化处理
- Markdown用于人类可读性

### 分页
- 始终尊重`limit`参数
- 返回`has_more`、`next_offset`、`total_count`
- 默认20-50项

### 字符限制
- 设置CHARACTER_LIMIT常量（通常25,000）
- 优雅截断并提供清晰消息
- 提供过滤指导

---

## 目录
1. 服务器命名约定
2. 工具命名和设计
3. 响应格式指南
4. 分页最佳实践
5. 字符限制和截断
6. 工具开发最佳实践
7. 传输最佳实践
8. 测试要求
9. OAuth和安全最佳实践
10. 资源管理最佳实践
11. 提示管理最佳实践
12. 错误处理标准
13. 文档要求
14. 合规性和监控

---

## 1. 服务器命名约定

为MCP服务器遵循这些标准化命名模式：

**Python**：使用`{service}_mcp`格式（小写下划线）
- 示例：`slack_mcp`、`github_mcp`、`jira_mcp`、`stripe_mcp`

**Node/TypeScript**：使用`{service}-mcp-server`格式（小写连字符）
- 示例：`slack-mcp-server`、`github-mcp-server`、`jira-mcp-server`

名称应该是：
- 一般的（不绑定到特定功能）
- 描述要集成/服务的
- 从任务描述中易于推断
- 没有版本号或日期

---

## 2. 工具命名和设计

### 工具命名最佳实践

1. **使用snake_case**：`search_users`、`create_project`、`get_channel_info`
2. **包含服务前缀**：预期您的MCP服务器可能与其他MCP服务器一起使用
   - 使用`slack_send_message`而不仅仅是`send_message`
   - 使用`github_create_issue`而不仅仅是`create_issue`
   - 使用`asana_list_tasks`而不仅仅是`list_tasks`
3. **以行动为导向**：以动词开头（get、list、search、create等）
4. **要具体**：避免可能与其他服务器冲突的通用名称
5. **保持一致**：在服务器内使用一致的命名模式

### 工具设计指南

- 工具描述必须狭窄且明确描述功能
- 描述必须精确匹配实际功能
- 不应与其他MCP服务器造成混淆
- 应提供工具注释（readOnlyHint、destructiveHint、idempotentHint、openWorldHint）
- 保持工具操作聚焦和原子性

---

## 3. 响应格式指南

所有返回数据的工具应支持多种格式以获得灵活性：

### JSON格式（`response_format="json"`）
