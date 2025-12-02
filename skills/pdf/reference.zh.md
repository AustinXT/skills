# PDF处理高级参考

本文档包含PDF处理高级功能、详细示例和主技能指令中未涵盖的其他库。

## pypdfium2库（Apache/BSD许可证）

### 概述
pypdfium2是PDFium（Chromium的PDF库）的Python绑定。它对于快速PDF渲染、图像生成非常出色，并可作为PyMuPDF的替代品。

### 将PDF渲染为图像
```python
import pypdfium2 as pdfium
from PIL import Image

# 加载PDF
pdf = pdfium.PdfDocument("document.pdf")

# 将页面渲染为图像
page = pdf[0]  # 第一页
bitmap = page.render(
    scale=2.0,  # 更高分辨率
    rotation=0  # 不旋转
)

# 转换为PIL图像
img = bitmap.to_pil()
img.save("page_1.png", "PNG")

# 处理多页
for i, page in enumerate(pdf):
    bitmap = page.render(scale=1.5)
    img = bitmap.to_pil()
    img.save(f"page_{i+1}.jpg", "JPEG", quality=90)
```

### 使用pypdfium2提取文本
```python
import pypdfium2 as pdfium

pdf = pdfium.PdfDocument("document.pdf")
for i, page in enumerate(pdf):
    text = page.get_text()
    print(f"第{i+1}页文本长度: {len(text)}字符")
```

## JavaScript库

### pdf-lib（MIT许可证）

pdf-lib是在任何JavaScript环境中创建和修改PDF文档的强大JavaScript库。

#### 加载和操作现有PDF
```javascript
import { PDFDocument } from 'pdf-lib';
import fs from 'fs';

async function manipulatePDF() {
    // 加载现有PDF
    const existingPdfBytes = fs.readFileSync('input.pdf');
    const pdfDoc = await PDFDocument.load(existingPdfBytes);

    // 获取页数
    const pageCount = pdfDoc.getPageCount();
    console.log(`文档有${pageCount}页`);

    // 添加新页面
    const newPage = pdfDoc.addPage([600, 400]);
    newPage.drawText('由pdf-lib添加', {
        x: 100,
        y: 300,
        size: 16
    });

    // 保存修改的PDF
    const pdfBytes = await pdfDoc.save();
    fs.writeFileSync('modified.pdf', pdfBytes);
}
```

#### 从零创建复杂PDF
```javascript
import { PDFDocument, rgb, StandardFonts } from 'pdf-lib';
import fs from 'fs';

async function createPDF() {
    const pdfDoc = await PDFDocument.create();

    // 添加字体
    const helveticaFont = await pdfDoc.embedFont(StandardFonts.Helvetica);
    const helveticaBold = await pdfDoc.embedFont(StandardFonts.HelveticaBold);

    // 添加页面
    const page = pdfDoc.addPage([595, 842]); // A4尺寸
    const { width, height } = page.getSize();

    // 添加带样式的文本
    page.drawText('发票 #12345', {
        x: 50,
        y: height - 50,
        size: 18,
