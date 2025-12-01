---
name: artifacts-builder
description: 用于使用现代前端Web技术（React、Tailwind CSS、shadcn/ui）创建复杂多组件claude.ai HTML artifacts的工具套件。用于需要状态管理、路由或shadcn/ui组件的复杂artifact - 不用于简单的单文件HTML/JSX artifacts。
license: Complete terms in LICENSE.txt
---

# Artifacts构建器

要构建强大的前端claude.ai artifacts，请遵循以下步骤：
1. 使用`scripts/init-artifact.sh`初始化前端仓库
2. 通过编辑生成的代码开发您的artifact
3. 使用`scripts/bundle-artifact.sh`将所有代码捆绑成单个HTML文件
4. 向用户显示artifact
5. （可选）测试artifact

**技术栈**：React 18 + TypeScript + Vite + Parcel（打包）+ Tailwind CSS + shadcn/ui

## 设计样式指南

非常重要：为了避免通常被称为"AI垃圾"的东西，避免使用过度的居中布局、紫色渐变、统一圆角和Inter字体。

## 快速开始

### 步骤1：初始化项目

运行初始化脚本创建新的React项目：
```bash
bash scripts/init-artifact.sh <project-name>
cd <project-name>
```

这创建一个完全配置的项目：
- ✅ React + TypeScript（通过Vite）
- ✅ Tailwind CSS 3.4.1与shadcn/ui主题系统
- ✅ 配置路径别名（`@/`）
- ✅ 预安装40+个shadcn/ui组件
- ✅ 包含所有Radix UI依赖
- ✅ 配置Parcel用于打包（通过.parcelrc）
- ✅ Node 18+兼容性（自动检测并固定Vite版本）

### 步骤2：开发您的Artifact

要构建artifact，编辑生成的文件。见下面的**常见开发任务**以获取指导。

### 步骤3：打包为单个HTML文件

要将React应用捆绑成单个HTML artifact：
```bash
bash scripts/bundle-artifact.sh
```

这创建`bundle.html` - 一个自包含artifact，所有JavaScript、CSS和依赖都内联。此文件可以直接在Claude对话中作为artifact分享。

**要求**：您的项目必须在根目录有`index.html`。

**脚本做什么**：
- 安装打包依赖（parcel、@parcel/config-default、parcel-resolver-tspaths、html-inline）
- 创建带有路径别名支持的`.parcelrc`配置
- 使用Parcel构建（无源映射）
- 使用html-inline将所有资源内联到单个HTML

### 步骤4：与用户分享Artifact

最后，在对话中与用户分享捆绑的HTML文件，以便他们可以将其作为artifact查看。

### 步骤5：测试/可视化Artifact（可选）

注意：这是完全可选的步骤。仅在必要或请求时执行。

要测试/可视化artifact，使用可用工具（包括其他技能或内置工具如Playwright或Puppeteer）。通常，避免提前测试artifact，因为它在请求和看到完成的artifact之间增加了延迟。如果请求或出现问题，在呈现artifact之后测试。

## 参考

- **shadcn/ui组件**：https://ui.shadcn.com/docs/components
