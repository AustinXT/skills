# Python MCP服务器实现指南

## 概述

本文档提供使用MCP Python SDK实现MCP服务器的Python特定最佳实践和示例。它涵盖服务器设置、工具注册模式、使用Pydantic进行输入验证、错误处理和完整工作示例。

---

## 快速参考

### 关键导入
```python
from mcp.server.fastmcp import FastMCP
from pydantic import BaseModel, Field, field_validator, ConfigDict
from typing import Optional, List, Dict, Any
from enum import Enum
import httpx
```

### 服务器初始化
```python
mcp = FastMCP("service_mcp")
```

### 工具注册模式
```python
@mcp.tool(name="tool_name", annotations={...})
async def tool_function(params: InputModel) -> str:
    # 实现
    pass
```

---

## MCP Python SDK和FastMCP

官方MCP Python SDK提供FastMCP，这是构建MCP服务器的高级框架。它提供：
- 从函数签名和文档字符串自动生成描述和inputSchema
- Pydantic模型集成用于输入验证
- 基于装饰器的工具注册与`@mcp.tool`

**有关完整SDK文档，使用WebFetch加载：**
`https://raw.githubusercontent.com/modelcontextprotocol/python-sdk/main/README.md`

## 服务器命名约定

Python MCP服务器必须遵循此命名模式：
- **格式**：`{service}_mcp`（小写下划线）
- **示例**：`github_mcp`、`jira_mcp`、`stripe_mcp`
