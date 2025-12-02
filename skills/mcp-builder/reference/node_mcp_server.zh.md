# Node/TypeScript MCP服务器实现指南

## 概述

本文档提供使用MCP TypeScript SDK实现MCP服务器的Node/TypeScript特定最佳实践和示例。它涵盖项目结构、服务器设置、工具注册模式、使用Zod进行输入验证、错误处理和完整工作示例。

---

## 快速参考

### 关键导入
```typescript
import { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import { z } from "zod";
import axios, { AxiosError } from "axios";
```

### 服务器初始化
```typescript
const server = new McpServer({
  name: "service-mcp-server",
  version: "1.0.0"
});
```

### 工具注册模式
```typescript
server.registerTool("tool_name", {...config}, async (params) => {
  // 实现
});
```

---

## MCP TypeScript SDK

官方MCP TypeScript SDK提供：
- `McpServer`类用于服务器初始化
- `registerTool`方法用于工具注册
- Zod模式集成用于运行时输入验证
- 类型安全的工具处理器实现

有关完整详细信息，请参阅参考中的MCP SDK文档。

## 服务器命名约定

Node/TypeScript MCP服务器必须遵循此命名模式：
- **格式**：`{service}-mcp-server`（小写连字符）
- **示例**：`github-mcp-server`、`jira-mcp-server`、`stripe-mcp-server`
