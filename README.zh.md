# 技能

技能是指令、脚本和资源的集合，Claude会动态加载这些内容以提高在专业任务上的表现。技能教会Claude如何以可重复的方式完成特定任务，无论是使用您公司的品牌指南创建文档、使用组织特定的工作流程分析数据，还是自动化个人任务。

更多信息，请查看：
- [什么是技能？](https://support.claude.com/en/articles/12512176-what-are-skills)
- [在Claude中使用技能](https://support.claude.com/en/articles/12512180-using-skills-in-claude)
- [如何创建自定义技能](https://support.claude.com/en/articles/12512198-creating-custom-skills)
- [为现实世界配备代理技能](https://anthropic.com/engineering/equipping-agents-for-the-real-world-with-agent-skills)

# 关于此仓库

此仓库包含展示Claude技能系统可能性的示例技能。这些示例涵盖从创意应用（艺术、音乐、设计）到技术任务（测试Web应用、MCP服务器生成）再到企业工作流程（通信、品牌等）的各个方面。

每个技能都自包含在各自的目录中，包含一个`SKILL.md`文件，其中包含Claude使用的指令和元数据。浏览这些示例以获得您自己技能的灵感，或了解不同的模式和方法。

此仓库中的示例技能是开源的（Apache 2.0）。我们还包含了驱动[Claude的文档功能](https://www.anthropic.com/news/create-files)底层功能的文档创建和编辑技能，位于[`document-skills/`](./document-skills/)文件夹中。这些是源码可用的，不是开源的，但我们希望与开发者分享这些作为在生产AI应用中积极使用的更复杂技能的参考。

**注意：**这些是用于灵感和学习的参考示例。它们展示了通用功能，而不是组织特定的工作流程或敏感内容。

## 免责声明

**这些技能仅供演示和教育目的提供。**虽然Claude中可能提供其中一些功能，但您从Claude获得的实现和行为可能与这些示例中显示的不同。这些示例旨在说明模式和可能性。在依赖这些技能完成关键任务之前，请务必在您自己的环境中彻底测试技能。

# 示例技能

此仓库包含展示不同能力的多样化示例技能集合：

## 创意与设计
- **algorithmic-art** - 使用p5.js通过种子随机性、流场和粒子系统创建生成艺术
- **canvas-design** - 使用设计理念在.png和.pdf格式中设计美丽的视觉艺术
- **slack-gif-creator** - 创建针对Slack大小约束优化的动画GIF

## 开发与技术
- **artifacts-builder** - 使用React、Tailwind CSS和shadcn/ui组件构建复杂的claude.ai HTML artifacts
- **mcp-server** - 创建高质量MCP服务器以集成外部API和服务的指南
- **webapp-testing** - 使用Playwright测试本地Web应用程序，用于UI验证和调试

## 企业与通信
- **brand-guidelines** - 将Anthropic的官方品牌颜色和字体应用于artifacts
- **internal-comms** - 编写内部通信，如状态报告、新闻通讯和常见问题
- **theme-factory** - 使用10个预设专业主题为artifacts添加样式，或即时生成自定义主题

## 元技能
- **skill-creator** - 创建扩展Claude能力的高效技能指南
- **template-skill** - 用作新技能起点的基础模板

# 文档技能

`document-skills/`子目录包含Anthropic开发的帮助Claude创建各种文档文件格式的技能。这些技能展示了处理复杂文件格式和二进制数据的高级模式：

- **docx** - 创建、编辑和分析Word文档，支持跟踪更改、评论、格式保持和文本提取
- **pdf** - 全面的PDF操作工具包，用于提取文本和表格、创建新PDF、合并/拆分文档以及处理表单
- **pptx** - 创建、编辑和分析PowerPoint演示文稿，支持布局、模板、图表和自动幻灯片生成
- **xlsx** - 创建、编辑和分析Excel电子表格，支持公式、格式化、数据分析和可视化

**重要免责声明：**这些文档技能是时间点快照，未被积极维护或更新。Claude预装了这些技能的版本。它们主要作为参考示例来说明Anthropic如何开发处理二进制文件格式和文档结构的更复杂技能。

# 在Claude Code、Claude.ai和API中试用

## Claude Code
您可以通过在Claude Code中运行以下命令将此仓库注册为Claude Code插件市场：
```
/plugin marketplace add anthropics/skills
```

然后，安装特定的技能集：
1. 选择`浏览和安装插件`
2. 选择`anthropic-agent-skills`
3. 选择`document-skills`或`example-skills`
4. 选择`立即安装`

或者，直接通过以下方式安装任一插件：
```
/plugin install document-skills@anthropic-agent-skills
/plugin install example-skills@anthropic-agent-skills
```

安装插件后，您只需提及技能即可使用它。例如，如果您从市场安装了`document-skills`插件，您可以要求Claude Code执行类似操作："使用PDF技能从path/to/some-file.pdf提取表单字段"

## Claude.ai

这些示例技能在Claude.ai的付费计划中都已可用。

要使用此仓库中的任何技能或上传自定义技能，请按照[在Claude中使用技能](https://support.claude.com/en/articles/12512180-using-skills-in-claude#h_a4222fa77b)中的说明操作。

## Claude API

您可以通过Claude API使用Anthropic的预构建技能并上传自定义技能。查看[技能API快速入门](https://docs.claude.com/en/api/skills-guide#creating-a-skill)了解更多信息。

# 创建基础技能

技能创建很简单 - 只需一个包含`SKILL.md`文件的文件夹，该文件包含YAML frontmatter和指令。您可以使用此仓库中的**template-skill**作为起点：

```markdown
---
name: my-skill-name
description: 清晰描述此技能的功能和使用时机
---

# 我的技能名称

[在此处添加Claude在此技能激活时将遵循的指令]

## 示例
- 示例用法 1
- 示例用法 2

## 指南
- 指南 1
- 指南 2
```

frontmatter只需要两个字段：
- `name` - 技能的唯一标识符（小写，空格用连字符）
- `description` - 技能功能和何时使用的完整描述

下面的markdown内容包含Claude将遵循的指令、示例和指南。更多详情，请查看[如何创建自定义技能](https://support.claude.com/en/articles/12512198-creating-custom-skills)。

# 合作伙伴技能

技能是教会Claude如何更好地使用特定软件的好方法。当我们看到来自合作伙伴的精彩示例技能时，我们可能会在此处重点介绍其中一些：

- **Notion** - [Claude的Notion技能](https://www.notion.so/notiondevs/Notion-Skills-for-Claude-28da4445d27180c7af1df7d8615723d0)
