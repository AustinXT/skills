# PowerPoint的Office Open XML技术参考

**重要：在开始之前阅读整个文档。** 整个文档涵盖关键XML模式规则和格式要求。错误实现会创建PowerPoint无法打开的无效PPTX文件。

## 技术指南

### 模式合规
- **`<p:txBody>`中的元素顺序**：`<a:bodyPr>`、`<a:lstStyle>`、`<a:p>`
- **空白**：在带头/尾空格的`<a:t>`元素中添加`xml:space='preserve'`
- **Unicode**：在ASCII内容中转义字符："`"变成`&#8220;`
- **图像**：添加到`ppt/media/`中，在幻灯片XML中引用，设置尺寸以适应幻灯片边界
- **关系**：为每个幻灯片的资源更新`ppt/slides/_rels/slideN.xml.rels`
- **脏属性**：在`<a:rPr>`和`<a:endParaRPr>`元素中添加`dirty="0"`以指示清洁状态

## 演示文稿结构

### 基本幻灯片结构
```xml
<!-- ppt/slides/slide1.xml -->
<p:sld>
  <p:cSld>
    <p:spTree>
      <p:nvGrpSpPr>...</p:nvGrpSpPr>
      <p:grpSpPr>...</p:grpSpPr>
      <!-- 形状在这里 -->
    </p:spTree>
  </p:cSld>
</p:sld>
```

### 带文本的文本框/形状
```xml
<p:sp>
  <p:nvSpPr>
    <p:cNvPr id="2" name="Title"/>
    <p:cNvSpPr>
      <a:spLocks noGrp="1"/>
    </p:cNvSpPr>
    <p:nvPr>
      <p:ph type="ctrTitle"/>
    </p:nvPr>
  </p:nvSpPr>
  <p:spPr>
    <a:xfrm>
      <a:off x="838200" y="365125"/>
      <a:ext cx="7772400" cy="1470025"/>
    </a:xfrm>
  </p:spPr>
  <p:txBody>
    <a:bodyPr/>
