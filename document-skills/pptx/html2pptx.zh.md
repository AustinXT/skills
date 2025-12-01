# HTML转PowerPoint指南

使用`html2pptx.js`库将HTML幻灯片转换为具有精确定位的PowerPoint演示文稿。

## 目录

1. [创建HTML幻灯片](#创建html幻灯片)
2. [使用html2pptx库](#使用html2pptx库)
3. [使用PptxGenJS](#使用pptxgenjs)

---

## 创建HTML幻灯片

每个HTML幻灯片必须包含适当的正文尺寸：

### 布局尺寸

- **16:9**（默认）：`width: 720pt; height: 405pt`
- **4:3**: `width: 720pt; height: 540pt`
- **16:10**: `width: 720pt; height: 450pt`

### 支持的元素

- `<p>`、`<h1>`-`<h6>` - 带样式的文本
- `<ul>`、`<ol>` - 列表（绝不要使用手动项目符号 •, -, *）
- `<b>`、`<strong>` - 粗体文本（内联格式）
- `<i>`、`<em>` - 斜体文本（内联格式）
- `<u>` - 下划线文本（内联格式）
- `<span>` - 带有CSS样式的内联格式（粗体、斜体、下划线、颜色）
- `<br>` - 换行
- `<div>`带bg/border - 变成形状
- `<img>` - 图像
- `class="placeholder"` - 图表的保留空间（返回`{ id, x, y, w, h }`）

### 关键文本规则

**所有文本必须在`<p>`、`<h1>`-`<h6>`、`<ul>`或`<ol>`标签内：**
- ✅ 正确：`<div><p>这里的文本</p></div>`
- ❌ 错误：`<div>这里的文本</div>` - **文本将不会出现在PowerPoint中**
- ❌ 错误：`<span>文本</span>` - **文本将不会出现在PowerPoint中**
- 没有文本标签的`<div>`或`<span>`中的文本将被静默忽略

**绝不要使用手动项目符号符号（•, -, *等）** - 使用`<ul>`或`<ol>`列表

**仅使用普遍可用的Web安全字体：**
- ✅ Web安全字体：`Arial`、`Helvetica`、`Times New Roman`、`Georgia`、`Courier New`、`Verdana`、`Tahoma`、`Trebuchet MS`、`Impact`、`Comic Sans MS`
- ❌ 错误：`'Segoe UI'`、`'SF Pro'`、`'Roboto'`、自定义字体 - **可能导致渲染问题**

### 样式

- 在body上使用`display: flex`以防止边距折叠破坏溢出验证
- 使用`margin`进行间距（填充包含在大小中）
- 内联格式：使用`<b>`、`<i>`、`<u>`标签或带有CSS样式的`<span>`
  - `<span>`支持：`font-weight: bold`、`font-style: italic`、`text-decoration: underline`、`color: #rrggbb`
  - `<span>`不支持：`margin`、`padding`（PowerPoint文本运行不支持）
  - 示例：`<span style="font-weight: bold; color: #667eea;">粗体蓝色文本</span>`
- Flexbox有效 - 位置从渲染布局计算
- 在CSS中使用带`#`前缀的十六进制颜色
- **文本对齐**：根据需要使用CSS `text-align`（`center`、`right`等）作为PptxGenJS文本格式的提示，如果文本长度略有偏差

### 形状样式（仅DIV元素）

**重要：背景、边框和阴影仅在`<div>`元素上工作，不在文本元素（`<p>`、`<h1>`-`<h6>`、`<ul>`、`<ol>`）上工作**

- **背景**：仅在`<div>`元素上的CSS `background`或`background-color`
  - 示例：`<div style="background: #f0f0f0;">` - 创建带背景的形状
- **边框**：`<div>`元素上的CSS `border`转换为PowerPoint形状边框
  - 支持统一边框：`border: 2px solid #333333`
  - 支持部分边框：`border-left`、`border-right`、`border-top`、`border-bottom`（渲染为线条形状）
  - 示例：`<div style="border-left: 8pt solid #E76F51;">`
- **边框半径**：`<div>`元素上的CSS `border-radius`用于圆角
  - `border-radius: 50%`或更高创建圆形形状
  - <50%的百分比相对于形状的较小维度计算
  - 支持px和pt单位（例如`border-radius: 8pt;`、`border-radius: 12px;`）
  - 示例：100x200px盒子上的`<div style="border-radius: 25%;">` = 100px的25% = 25px半径
- **盒子阴影**：`<div>`元素上的CSS `box-shadow`转换为PowerPoint阴影
  - 仅支持外部阴影（忽略内嵌阴影以防止损坏）
  - 示例：`<div style="box-shadow: 2px 2px 8px rgba(0, 0, 0, 0.3);">`
  - 注意：PowerPoint不支持内嵌/内部阴影，将被跳过

### 图标和渐变

- **关键：绝不要使用CSS渐变（`linear-gradient`、`radial-gradient`）** - 它们不会转换为PowerPoint
- **始终首先使用Sharp创建渐变/图标PNG，然后在HTML中引用**
- 对于渐变：将SVG栅格化为PNG背景图像
- 对于图标：将react-icons SVG栅格化为PNG图像
- 所有视觉效果必须在HTML渲染之前预渲染为栅格图像

**使用Sharp栅格化图标：**

```javascript
const React = require('react');
const ReactDOMServer = require('react-dom/server');
const sharp = require('sharp');
const { FaHome } = require('react-icons/fa');

async function rasterizeIconPng(IconComponent, color, size = "256", filename) {
  const svgString = ReactDOMServer.renderToStaticMarkup(
    React.createElement(IconComponent, { color: `#${color}`, size: size })
  );

  // 使用Sharp将SVG转换为PNG
  await sharp(Buffer.from(svgString))
    .png()
    .toFile(filename);

  return filename;
}

// 用法：在HTML中使用之前栅格化图标
const iconPath = await rasterizeIconPng(FaHome, "4472c4", "256", "home-icon.png");
// 然后在HTML中引用：<img src="home-icon.png" style="width: 40pt; height: 40pt;">
```

**使用Sharp栅格化渐变：**

```javascript
const sharp = require('sharp');

async function createGradientBackground(filename) {
  const svg = `<svg xmlns="http://www.w3.org/2000/svg" width="1000" height="562.5">
    <defs>
      <linearGradient id="g" x1="0%" y1="0%" x2="100%" y2="100%">
        <stop offset="0%" style="stop-color:#COLOR1"/>
        <stop offset="100%" style="stop-color:#COLOR2"/>
      </linearGradient>
    </defs>
    <rect width="100%" height="100%" fill="url(#g)"/>
  </svg>`;

  await sharp(Buffer.from(svg))
    .png()
    .toFile(filename);

  return filename;
}

// 用法：在HTML之前创建渐变背景
const bgPath = await createGradientBackground("gradient-bg.png");
// 然后在HTML中：<body style="background-image: url('gradient-bg.png');">
```

### 示例

```html
<!DOCTYPE html>
<html>
<head>
<style>
html { background: #ffffff; }
body {
  width: 720pt; height: 405pt; margin: 0; padding: 0;
  background: #f5f5f5; font-family: Arial, sans-serif;
  display: flex;
}
.content { margin: 30pt; padding: 40pt; background: #ffffff; border-radius: 8pt; }
h1 { color: #2d3748; font-size: 32pt; }
.box {
  background: #70ad47; padding: 20pt; border: 3px solid #5a8f37;
  border-radius: 12pt; box-shadow: 3px 3px 10px rgba(0, 0, 0, 0.25);
}
</style>
</head>
<body>
<div class="content">
  <h1>配方标题</h1>
  <ul>
    <li><b>项目：</b>描述</li>
  </ul>
  <p>带<b>粗体</b>、<i>斜体</i>、<u>下划线</u>的文本。</p>
  <div id="chart" class="placeholder" style="width: 350pt; height: 200pt;"></div>

  <!-- 文本必须在<p>标签内 -->
  <div class="box">
    <p>5</p>
  </div>
</div>
</body>
</html>
```

## 使用html2pptx库

### 依赖

这些库已全局安装并可以使用：
- `pptxgenjs`
- `playwright`
- `sharp`

### 基本用法

```javascript
const pptxgen = require('pptxgenjs');
const html2pptx = require('./html2pptx');

const pptx = new pptxgen();
pptx.layout = 'LAYOUT_16x9';  // 必须与HTML正文尺寸匹配
