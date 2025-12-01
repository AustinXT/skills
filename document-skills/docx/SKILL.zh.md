---
name: docx
description: "全面支持跟踪更改、评论、格式保持和文本提取的文档创建、编辑和分析。当Claude需要使用专业文档（.docx文件）进行：(1) 创建新文档，(2) 修改或编辑内容，(3) 处理跟踪更改，(4) 添加评论，或任何其他文档任务时"
license: Proprietary. LICENSE.txt has complete terms
---

# DOCX创建、编辑和分析

## 概述

用户可能要求您创建、编辑或分析.docx文件的内容。.docx文件本质上是包含XML文件和其他资源的ZIP档案，您可以读取或编辑它们。您有不同工具和工作流程可用于不同任务。

## 工作流程决策树

### 读取/分析内容
使用下面的"文本提取"或"原始XML访问"部分

### 创建新文档
使用"创建新Word文档"工作流程

### 编辑现有文档
- **您自己的文档 + 简单更改**
  使用"基本OOXML编辑"工作流程

- **他人的文档**
  使用**"红划线工作流程"**（推荐默认）

- **法律、学术、商业或政府文档**
  使用**"红划线工作流程"**（必需）

## 读取和分析内容

### 文本提取
如果您只需要读取文档的文本内容，您应该使用pandoc将文档转换为markdown。Pandoc对保持文档结构有很好的支持，并且可以显示跟踪的更改：

```bash
# 将文档转换为带跟踪更改的markdown
pandoc --track-changes=all path-to-file.docx -o output.md
# 选项：--track-changes=accept/reject/all
```

### 原始XML访问
您需要原始XML访问：评论、复杂格式、文档结构、嵌入媒体和元数据。对于这些功能中的任何一个，您需要解包文档并读取其原始XML内容。

#### 解包文件
`python ooxml/scripts/unpack.py <office_file> <output_directory>`

#### 关键文件结构
* `word/document.xml` - 主要文档内容
* `word/comments.xml` - 文档中引用的评论
* `word/media/` - 嵌入的图像和媒体文件
* 跟踪更改使用`<w:ins>`（插入）和`<w:del>`（删除）标签

## 创建新Word文档

从零开始创建新Word文档时，使用**docx-js**，它允许您使用JavaScript/TypeScript创建Word文档。

### 工作流程
1. **强制 - 完整阅读文件**：完整阅读[`docx-js.md`](docx-js.md)（~500行）从头到尾。**阅读此文件时绝不要设置任何范围限制。**在继续文档创建之前阅读完整文件内容以获取详细语法、关键格式规则和最佳实践。
2. 使用Document、Paragraph、TextRun组件创建JavaScript/TypeScript文件（您可以假设所有依赖都已安装，但如果没有，请参阅下面的依赖部分）
3. 使用Packer.toBuffer()导出为.docx

## 编辑现有Word文档

编辑现有Word文档时，使用**Document库**（用于OOXML操作的Python库）。库自动处理基础设施设置并提供文档操作方法。对于复杂场景，您可以通过库直接访问底层DOM。

### 工作流程
1. **强制 - 完整阅读文件**：完整阅读[`ooxml.md`](ooxml.md)（~600行）从头到尾。**阅读此文件时绝不要设置任何范围限制。**阅读完整文件内容以获取Document库API和直接编辑文档文件的XML模式。
2. 解包文档：`python ooxml/scripts/unpack.py <office_file> <output_directory>`
3. 使用Document库创建并运行Python脚本（见ooxml.md中的"Document库"部分）
4. 打包最终文档：`python ooxml/scripts/pack.py <input_directory> <office_file>`

Document库既提供常见操作的高级方法，也提供复杂场景的直接DOM访问。

## 文档审阅的红划线工作流程

此工作流程允许您在使用OOXML实现之前使用markdown规划全面的跟踪更改。**关键**：对于完整的跟踪更改，您必须系统地实现所有更改。

**批处理策略**：将相关更改分组为3-10更改的批次。这使调试易于管理，同时保持效率。在进入下一个批次之前测试每个批次。

**原则：最小、精确定位编辑**
实现跟踪更改时，只标记实际更改的文本。重复未更改的文本使编辑更难审阅，显得不专业。将替换分解为：[未更改文本] + [删除] + [插入] + [未更改文本]。通过从原始提取`<w:r>`元素并重新使用它来保留原始运行的RSID用于未更改文本。

示例 - 在句子中将"30天"更改为"60天"：
```python
# 坏 - 替换整个句子
'<w:del><w:r><w:delText>合同期限为30天。</w:delText></w:r></w:del><w:ins><w:r><w:t>合同期限为60天。</w:t></w:r></w:ins>'

# 好 - 只标记更改的内容，为未更改文本保留原始<w:r>
'<w:r w:rsidR="00AB12CD"><w:t>合同期限为</w:t></w:r><w:del><w:r><w:delText>30</w:delText></w:r></w:del><w:ins><w:r><w:t>60</w:t></w:r></w:ins><w:r w:rsidR="00AB12CD"><w:t>天。</w:t></w:r>'
```

### 跟踪更改工作流程

1. **获取markdown表示**：转换文档为保持跟踪更改的markdown：
   ```bash
   pandoc --track-changes=all path-to-file.docx -o current.md
   ```

2. **识别和分组更改**：审阅文档并识别所需的所有更改，将它们组织成逻辑批次：

   **位置方法**（在XML中查找更改）：
   - 节/标题编号（例如，"第3.2节"、"第IV条"）
   - 段落标识符（如果编号）
   - 带有独特周围文本的Grep模式
   - 文档结构（例如，"第一段"、"签名块"）
   - **不要使用markdown行号** - 它们不映射到XML结构

   **批次组织**（每批次分组3-10相关更改）：
   - 按节："第1批：第2节修正案"、"第2批：第5节更新"
   - 按类型："第1批：日期修正"、"第2批：当事方名称更改"
   - 按复杂性：从简单文本替换开始，然后处理复杂结构更改
   - 顺序："第1批：第1-3页"、"第2批：第4-6页"

3. **阅读文档和解包**：
   - **强制 - 完整阅读文件**：完整阅读[`ooxml.md`](ooxml.md)（~600行）从头到尾。**阅读此文件时绝不要设置任何范围限制。**特别关注"Document库"和"跟踪更改模式"部分。
   - **解包文档**：`python ooxml/scripts/unpack.py <file.docx> <dir>`
   - **注意建议的RSID**：解包脚本将建议用于您的跟踪更改的RSID。复制此RSID在步骤4b中使用。

4. **批次实现更改**：将更改逻辑分组（按节、按类型或按邻近性）并在单个脚本中一起实现它们。这种方法：
   - 使调试更容易（更小的批次 = 更容易隔离错误）
   - 允许增量进展
   - 保持效率（3-10更改的批次效果很好）

   **建议的批次分组**：
   - 按文档节（例如，"第3节更改"、"定义"、"终止条款"）
   - 按更改类型（例如，"日期更改"、"当事方名称更新"、"法律术语替换"）
   - 按邻近性（例如，"第1-3页更改"、"文档前半部分更改"）

   对于每批相关更改：

   **a. 将文本映射到XML**：Grep`word/document.xml`中的文本以验证文本如何跨`<w:r>`元素拆分。

   **b. 创建并运行脚本**：使用`get_node`查找节点，实现更改，然后`doc.save()`。见ooxml.md中的**"Document库"**部分了解模式。

   **注意**：在编写脚本之前总是立即grep`word/document.xml`以获取当前行号并验证文本内容。每次脚本运行后行号都会更改。

5. **打包文档**：所有批次完成后，将解包目录转换回.docx：
   ```bash
   python ooxml/scripts/pack.py unpacked reviewed-document.docx
   ```

6. **最终验证**：对完整文档进行全面检查：
   - 将最终文档转换为markdown：
     ```bash
     pandoc --track-changes=all reviewed-document.docx -o verification.md
     ```
   - 验证所有更改都正确应用：
     ```bash
     grep "原始短语" verification.md  # 不应该找到
     grep "替换短语" verification.md  # 应该找到
     ```
   - 检查没有引入意外更改

## 将文档转换为图像

要视觉分析Word文档，使用两步过程将它们转换为图像：

1. **将DOCX转换为PDF**：
   ```bash
   soffice --headless --convert-to pdf document.docx
   ```

2. **将PDF页面转换为JPEG图像**：
   ```bash
   pdftoppm -jpeg -r 150 document.pdf page
   ```
   这创建`page-1.jpg`、`page-2.jpg`等文件。

选项：
- `-r 150`：将分辨率设置为150 DPI（调整质量/大小平衡）
- `-jpeg`：输出JPEG格式（如果首选，使用`-png`表示PNG）
- `-f N`：要转换的第一页（例如，`-f 2`从第2页开始）
- `-l N`：要转换的最后一页（例如，`-l 5`在第5页停止）
- `page`：输出文件的前缀

特定范围示例：
```bash
pdftoppm -jpeg -r 150 -f 2 -l 5 document.pdf page  # 只转换第2-5页
```

## 代码风格指南
**重要**：为DOCX操作生成代码时：
- 编写简洁的代码
- 避免冗长变量名和冗余操作
- 避免不必要的打印语句

## 依赖

所需依赖（如果不可用则安装）：

- **pandoc**：`sudo apt-get install pandoc`（用于文本提取）
- **docx**：`npm install -g docx`（用于创建新文档）
- **LibreOffice**：`sudo apt-get install libreoffice`（用于PDF转换）
- **Poppler**：`sudo apt-get install poppler-utils`（用于pdftoppm将PDF转换为图像）
- **defusedxml**：`pip install defusedxml`（用于安全XML解析）
