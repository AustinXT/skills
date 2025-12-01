---
name: mcp-builder
description: 用于创建高质量MCP（模型上下文协议）服务器的指南，使LLM能够通过精心设计的工具与外部服务交互。在构建MCP服务器以集成外部API或服务时使用，无论是在Python（FastMCP）还是Node/TypeScript（MCP SDK）中。
license: Complete terms in LICENSE.txt
---

# MCP服务器开发指南

## 概述

要创建使LLM有效与外部服务交互的高质量MCP（模型上下文协议）服务器，请使用此技能。MCP服务器提供允许LLM访问外部服务和API的工具。MCP服务器的质量通过它使LLM能够使用提供的工具完成现实世界任务的程度来衡量。

---

# 流程

## 🚀 高级工作流程

创建高质量的MCP服务器涉及四个主要阶段：

### 阶段1：深度研究和规划

#### 1.1 理解以代理为中心的设计原则

在深入实现之前，通过审查这些原则了解如何为AI代理设计工具：

**为工作流程而构建，而不仅仅是API端点：**
- 不要简单地包装现有API端点 - 构建深思熟虑、高影响力的工作流程工具
- 整合相关操作（例如既检查可用性又创建事件的`schedule_event`）
- 专注于使完整任务成为可能的工具，而不仅仅是单个API调用
- 考虑代理实际需要完成的工作流程

**针对有限上下文进行优化：**
- 代理有受限的上下文窗口 - 使每个token都有价值
- 返回高信号信息，而不是详尽的数据转储
- 提供"简洁"vs"详细"响应格式选项
- 默认为人类可读标识符而不是技术代码（名称优于ID）
- 将代理的上下文预算视为稀缺资源

**设计可行的错误消息：**
- 错误消息应指导代理采用正确的使用模式
- 建议具体下一步："尝试使用filter='active_only'来减少结果"
- 使错误具有教育性，而不仅仅是诊断性
- 通过清晰反馈帮助代理学习正确的工具使用

**遵循自然任务细分：**
- 工具名称应反映人类对任务的思考方式
- 为可发现性用一致前缀对相关工具进行分组
- 围绕自然工作流程设计工具，而不仅仅是API结构

**使用评估驱动的开发：**
- 尽早创建现实评估场景
- 让代理反馈推动工具改进
- 快速原型化并基于实际代理性能迭代

#### 1.3 研究MCP协议文档

**获取最新的MCP协议文档：**

使用WebFetch加载：`https://modelcontextprotocol.io/llms-full.txt`

这个综合文档包含完整的MCP规范和指南。

#### 1.4 研究框架文档

**加载并阅读以下参考文件：**

- **MCP最佳实践**：[📋 查看最佳实践](./reference/mcp_best_practices.md) - 所有MCP服务器的核心指南

**对于Python实现，也加载：**
- **Python SDK文档**：使用WebFetch加载`https://raw.githubusercontent.com/modelcontextprotocol/python-sdk/main/README.md`
- [🐍 Python实现指南](./reference/python_mcp_server.md) - Python特定的最佳实践和示例

**对于Node/TypeScript实现，也加载：**
- **TypeScript SDK文档**：使用WebFetch加载`https://raw.githubusercontent.com/modelcontextprotocol/typescript-sdk/main/README.md`
- [⚡ TypeScript实现指南](./reference/node_mcp_server.md) - Node/TypeScript特定的最佳实践和示例

#### 1.5 穷尽性研究API文档

要集成服务，阅读**所有**可用的API文档：
- 官方API参考文档
- 身份验证和授权要求
- 速率限制和分页模式
- 错误响应和状态码
- 可用端点及其参数
- 数据模型和模式

**要收集全面信息，根据需要使用网络搜索和WebFetch工具。**

#### 1.6 创建综合实现计划

基于您的研究，创建一个包含以下内容的详细计划：

**工具选择：**
- 列出要实现的最有价值的端点/操作
- 优先考虑能够实现最常见和最重要的用例的工具
- 考虑哪些工具协同工作以实现复杂工作流程

**共享实用程序和助手：**
- 识别常见API请求模式
- 规划分页助手
- 设计过滤和格式化实用程序
- 规划错误处理策略

**输入/输出设计：**
- 定义输入验证模型（Python的Pydantic，TypeScript的Zod）
- 设计一致的响应格式（例如JSON或Markdown），以及可配置的详细级别（例如详细或简洁）
- 规划大规模使用（数千用户/资源）
- 实现字符限制和截断策略（例如25,000个token）

**错误处理策略：**
- 规划优雅的失败模式
- 设计清晰、可行的、对LLM友好的自然语言错误消息，提示进一步行动
- 考虑速率限制和超时场景
- 处理身份验证和授权错误

---

### 阶段2：实现

现在您有了综合计划，遵循特定语言的最佳实践开始实现。

#### 2.1 设置项目结构

**对于Python：**
- 创建单个`.py`文件或如果复杂则组织为模块（见[🐍 Python指南](./reference/python_mcp_server.md)）
- 使用MCP Python SDK进行工具注册
- 定义Pydantic模型进行输入验证

**对于Node/TypeScript：**
- 创建适当的项目结构（见[⚡ TypeScript指南](./reference/node_mcp_server.md)）
- 设置`package.json`和`tsconfig.json`
- 使用MCP TypeScript SDK
- 定义Zod模式进行输入验证

#### 2.2 首先实现核心基础设施

**要开始实现，在实现工具之前创建共享实用程序：**
- API请求助手函数
- 错误处理实用程序
- 响应格式化函数（JSON和Markdown）
- 分页助手
- 身份验证/令牌管理

#### 2.3 系统化实现工具

对于计划中的每个工具：

**定义输入模式：**
- 使用Pydantic（Python）或Zod（TypeScript）进行验证
- 包含适当约束（最小/最大长度、regex模式、最小/最大值、范围）
- 提供清晰、描述性的字段描述
- 在字段描述中包含多样示例

**编写全面的文档字符串/描述：**
- 工具功能的一行摘要
- 目的和功能的详细解释
- 带有示例的显式参数类型
- 完整的返回类型模式
- 使用示例（何时使用、何时不使用）
- 错误处理文档，概述给定特定错误如何继续

**实现工具逻辑：**
- 使用共享实用程序避免代码重复
- 遵循所有I/O的async/await模式
- 实现适当的错误处理
- 支持多种响应格式（JSON和Markdown）
- 尊重分页参数
- 检查字符限制并适当截断

**添加工具注释：**
- `readOnlyHint`: true（用于只读操作）
- `destructiveHint`: false（用于非破坏性操作）
- `idempotentHint`: true（如果重复调用有相同效果）
- `openWorldHint`: true（如果与外部系统交互）

#### 2.4 遵循特定语言的最佳实践

**此时，加载适当的语言指南：**

**对于Python：加载[🐍 Python实现指南](./reference/python_mcp_server.md)并确保以下：**
- 使用带有适当工具注册的MCP Python SDK
- 带有`model_config`的Pydantic v2模型
- 贯穿始终的类型提示
- 所有I/O操作的Async/await
- 适当的导入组织
- 模块级常量（CHARACTER_LIMIT、API_BASE_URL）

**对于Node/TypeScript：加载[⚡ TypeScript实现指南](./reference/node_mcp_server.md)并确保以下：**
- 正确使用`server.registerTool`
- 带有`.strict()`的Zod模式
- 启用TypeScript严格模式
- 没有`any`类型 - 使用适当类型
- 显式Promise<T>返回类型
- 配置构建过程（`npm run build`）

---

### 阶段3：审查和完善

初始实现后：

#### 3.1 代码质量审查

为确保质量，审查代码：
- **DRY原则**：工具间没有重复代码
- **可组合性**：共享逻辑提取为函数
- **一致性**：类似操作返回类似格式
- **错误处理**：所有外部调用都有错误处理
- **类型安全**：完全类型覆盖（Python类型提示，TypeScript类型）
- **文档**：每个工具都有全面的文档字符串/描述

#### 3.2 测试和构建

**重要：**MCP服务器是等待通过stdio/stdin或sse/http接收请求的长期运行进程。直接在主进程中运行它们（例如`python server.py`或`node dist/index.js`）将导致您的进程无限挂起。

**安全测试服务器的方法：**
- 使用评估工具（见阶段4） - 推荐方法
- 在tmux中运行服务器以将其保持在主进程之外
- 测试时使用超时：`timeout 5s python server.py`

**对于Python：**
- 验证Python语法：`python -m py_compile your_server.py`
- 通过审查文件检查导入是否正确工作
- 要手动测试：在tmux中运行服务器，然后在主进程中用评估工具测试
- 或直接使用评估工具（它管理stdio传输的服务器）

**对于Node/TypeScript：**
- 运行`npm run build`并确保它无错误完成
- 验证创建了dist/index.js
- 要手动测试：在tmux中运行服务器，然后在主进程中用评估工具测试
- 或直接使用评估工具（它管理stdio传输的服务器）

#### 3.3 使用质量清单

为验证实现质量，从特定语言指南加载适当的清单：
- Python：见[🐍 Python指南](./reference/python_mcp_server.md)中的"质量清单"
- Node/TypeScript：见[⚡ TypeScript指南](./reference/node_mcp_server.md)中的"质量清单"

---

### 阶段4：创建评估

实现MCP服务器后，创建全面评估来测试其有效性。

**加载[✅ 评估指南](./reference/evaluation.md)获取完整评估指南。**

#### 4.1 理解评估目的

评估测试LLM是否能够有效使用您的MCP服务器来回答现实、复杂的问题。

#### 4.2 创建10个评估问题

要创建有效评估，遵循评估指南中概述的流程：

1. **工具检查**：列出可用工具并了解其能力
2. **内容探索**：使用只读操作探索可用数据
3. **问题生成**：创建10个复杂、现实的问题
4. **答案验证**：自己解决每个问题以验证答案

#### 4.3 评估要求

每个问题必须是：
- **独立**：不依赖于其他问题
- **只读**：只需要非破坏性操作
- **复杂**：需要多个工具调用和深度探索
- **现实**：基于人类关心的真实用例
- **可验证**：可以通过字符串比较验证的单一、清晰答案
- **稳定**：答案不会随时间变化

#### 4.4 输出格式

创建具有此结构的XML文件：

```xml
<evaluation>
  <qa_pair>
    <question>查找有关具有动物代号AI模型发布的讨论。一个模型需要特定的安全指定，其格式为ASL-X。正在为名为斑点野猫的模型确定什么数字X？</question>
    <answer>3</answer>
  </qa_pair>
<!-- 更多qa_pairs... -->
</evaluation>
```

---

# 参考文件

## 📚 文档库

在开发期间根据需要加载这些资源：

### 核心MCP文档（首先加载）
- **MCP协议**：从`https://modelcontextprotocol.io/llms-full.txt`获取 - 完整MCP规范
- [📋 MCP最佳实践](./reference/mcp_best_practices.md) - 通用MCP指南包括：
  - 服务器和工具命名约定
  - 响应格式指南（JSON vs Markdown）
  - 分页最佳实践
  - 字符限制和截断策略
  - 工具开发指南
  - 安全和错误处理标准

### SDK文档（在阶段1/2期间加载）
- **Python SDK**：从`https://raw.githubusercontent.com/modelcontextprotocol/python-sdk/main/README.md`获取
- **TypeScript SDK**：从`https://raw.githubusercontent.com/modelcontextprotocol/typescript-sdk/main/README.md`获取

### 特定语言实现指南（在阶段2期间加载）
- [🐍 Python实现指南](./reference/python_mcp_server.md) - 完整的Python/FastMCP指南包括：
  - 服务器初始化模式
  - Pydantic模型示例
  - 带`@mcp.tool`的工具注册
  - 完整工作示例
  - 质量清单

- [⚡ TypeScript实现指南](./reference/node_mcp_server.md) - 完整TypeScript指南包括：
  - 项目结构
  - Zod模式模式
  - 带`server.registerTool`的工具注册
  - 完整工作示例
  - 质量清单

### 评估指南（在阶段4期间加载）
- [✅ 评估指南](./reference/evaluation.md) - 完整评估创建指南包括：
  - 问题创建指南
  - 答案验证策略
  - XML格式规范
  - 示例问题和答案
  - 使用提供的脚本运行评估
