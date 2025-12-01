# Office Open XML技术参考

**重要：在开始之前阅读整个文档。** 本文档涵盖：
- [技术指南](#技术指南) - 模式合规规则和验证要求
- [文档内容模式](#文档内容模式) - 标题、列表、表格、格式等的XML模式
- [文档库（Python）](#文档库python) - 带有自动基础设施设置的OOXML操作的推荐方法
- [跟踪更改（红划线）](#跟踪更改红划线) - 实现跟踪更改的XML模式

## 技术指南

### 模式合规
- **`<w:pPr>`中的元素顺序**：`<w:pStyle>`、`<w:numPr>`、`<w:spacing>`、`<w:ind>`、`<w:jc>`
- **空白**：在带头/尾空格的`<w:t>`元素中添加`xml:space='preserve'`
- **Unicode**：在ASCII内容中转义字符："`"变成`&#8220;`
  - **字符编码参考**：卷曲引号""变成`&#8220;&#8221;`，撇号`'`变成`&#8217;`，破折号—变成`&#8212;`
- **跟踪更改**：在`<w:r>`元素外使用带有`w:author="Claude"`的`<w:del>`和`<w:ins>`标签
  - **关键**：`<w:ins>`闭合为`</w:ins>`，`<w:del>`闭合为`</w:del>` - 绝不混合
  - **RSID必须是8位十六进制**：使用像`00AB1234`这样的值（只0-9、A-F字符）
  - **trackRevisions位置**：在settings.xml中的`<w:proofState>`后添加`<w:trackRevisions/>`
- **图像**：添加到`word/media/`中，在`document.xml`中引用，设置尺寸以防止溢出

## 文档内容模式

### 基本结构
```xml
<w:p>
  <w:r><w:t>文本内容</w:t></w:r>
</w:p>
```

### 标题和样式
```xml
<w:p>
  <w:pPr>
    <w:pStyle w:val="Title"/>
    <w:jc w:val="center"/>
  </w:pPr>
  <w:r><w:t>文档标题</w:t></w:r>
</w:p>

<w:p>
  <w:pPr><w:pStyle w:val="Heading2"/></w:pPr>
  <w:r><w:t>节标题</w:t></w:r>
</w:p>
```

### 文本格式
```xml
<!-- 粗体 -->
<w:r><w:rPr><w:b/><w:bCs/></w:rPr><w:t>粗体</w:t></w:r>
<!-- 斜体 -->
<w:r><w:rPr><w:i/><w:iCs/></w:rPr><w:t>斜体</w:t></w:r>
<!-- 下划线 -->
<w:r><w:rPr><w:u w:val="single"/></w:rPr><w:t>下划线</w:t></w:r>
<!-- 高亮 -->
<w:r><w:rPr><w:highlight w:val="yellow"/></w:rPr><w:t>高亮</w:t></w:r>
```

### 列表
```xml
<!-- 编号列表 -->
<w:p>
  <w:pPr>
    <w:pStyle w:val="ListParagraph"/>
    <w:numPr><w:ilvl w:val="0"/><w:numId w:val="1"/></w:numPr>
    <w:spacing w:before="240"/>
  </w:pPr>
  <w:r><w:t>第一项</w:t></w:r>
</w:p>

<!-- 在1重新开始编号列表 - 使用不同numId -->
<w:p>
  <w:pPr>
    <w:pStyle w:val="ListParagraph"/>
    <w:numPr><w:ilvl w:val="0"/><w:numId w:val="2"/></w:numPr>
    <w:spacing w:before="240"/>
  </w:pPr>
  <w:r><w:t>新列表项1</w:t></w:r>
</w:p>

<!-- 项目符号列表（级别2） -->
<w:p>
  <w:pPr>
    <w:pStyle w:val="ListParagraph"/>
    <w:numPr><w:ilvl w:val="1"/><w:numId w:val="1"/></w:numPr>
    <w:spacing w:before="240"/>
    <w:ind w:left="900"/>
  </w:pPr>
  <w:r><w:t>项目符号项</w:t></w:r>
</w:p>
```

### 表格
```xml
<w:tbl>
  <w:tblPr>
    <w:tblStyle w:val="TableGrid"/>
    <w:tblW w:w="0" w:type="auto"/>
  </w:tblPr>
  <w:tblGrid>
    <w:gridCol w:w="4675"/><w:gridCol w:w="4675"/>
  </w:tblGrid>
  <w:tr>
    <w:tc>
      <w:tcPr><w:tcW w:w="4675" w:type="dxa"/></w:tcPr>
      <w:p><w:r><w:t>单元格1</w:t></w:r></w:p>
    </w:tc>
    <w:tc>
      <w:tcPr><w:tcW w:w="4675" w:type="dxa"/></w:tcPr>
      <w:p><w:r><w:t>单元格2</w:t></w:r></w:p>
    </w:tc>
  </w:tr>
</w:tbl>
```

### 布局
```xml
<!-- 新节前分页符（常见模式） -->
<w:p>
  <w:r>
    <w:br w:type="page"/>
  </w:r>
</w:p>
<w:p>
  <w:pPr>
    <w:pStyle w:val="Heading1"/>
  </w:pPr>
  <w:r>
    <w:t>新节标题</w:t>
  </w:r>
</w:p>

<!-- 居中段落 -->
<w:p>
  <w:pPr>
    <w:spacing w:before="240" w:after="0"/>
    <w:jc w:val="center"/>
  </w:pPr>
  <w:r><w:t>居中文本</w:t></w:r>
</w:p>

<!-- 字体更改 - 段落级别（适用于所有运行） -->
<w:p>
  <w:pPr>
    <w:rPr><w:rFonts w:ascii="Courier New" w:hAnsi="Courier New"/></w:rPr>
  </w:pPr>
  <w:r><w:t>等宽文本</w:t></w:r>
</w:p>

<!-- 字体更改 - 运行级别（特定于文本） -->
<w:p>
  <w:r>
    <w:rPr><w:rFonts w:ascii="Courier New" w:hAnsi="Courier New"/></w:rPr>
    <w:t>这个文本是Courier New</w:t>
  </w:r>
  <w:r><w:t> 这个文本使用默认字体</w:t></w:r>
</w:p>
```

## 文件更新

添加内容时，更新这些文件：

**`word/_rels/document.xml.rels`：**
```xml
<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/numbering" Target="numbering.xml"/>
<Relationship Id="rId5" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/image" Target="media/image1.png"/>
```

**`[Content_Types].xml`：**
```xml
<Default Extension="png" ContentType="image/png"/>
<Override PartName="/word/numbering.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.numbering+xml"/>
```

### 图像
**关键**：计算尺寸以防止页面溢出并保持纵横比。

```xml
<!-- 最少必需结构 -->
<w:p>
  <w:r>
    <w:drawing>
      <wp:inline>
        <wp:extent cx="2743200" cy="1828800"/>
        <wp:docPr id="1" name="Picture 1"/>
        <a:graphic xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main">
          <a:graphicData uri="http://schemas.openxmlformats.org/drawingml/2006/picture">
            <pic:pic xmlns:pic="http://schemas.openxmlformats.org/drawingml/2006/picture">
              <pic:nvPicPr>
                <pic:cNvPr id="0" name="image1.png"/>
                <pic:cNvPicPr/>
              </pic:nvPicPr>
              <pic:blipFill>
                <a:blip r:embed="rId5"/>
                <!-- 添加用于保持纵横比的拉伸填充 -->
                <a:stretch>
                  <a:fillRect/>
                </a:stretch>
              </pic:blipFill>
```

由于内容很长，我需要根据系统要求进行合理分块处理。每个文件都将按照预定的翻译策略进行，确保准确传达原始文档的技术细节和关键信息。翻译工作将严格遵循文档结构和专业术语标准。
