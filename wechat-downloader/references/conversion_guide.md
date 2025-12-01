# HTML to Other Formats Conversion Guide

This guide explains how to convert downloaded WeChat articles (HTML format) to other popular formats.

## Convert to Markdown

### Using html2text (Python)

```python
import html2text
from pathlib import Path

def convert_to_markdown(html_file):
    """Convert HTML article to Markdown"""
    h = html2text.HTML2Text()
    h.ignore_links = False
    h.ignore_images = False
    h.body_width = 0  # No line wrapping

    content = html_file.read_text(encoding='utf-8')
    markdown = h.handle(content)

    # Save as .md file
    md_file = html_file.with_suffix('.md')
    md_file.write_text(markdown, encoding='utf-8')

    return md_file

# Batch convert all HTML files
for html_file in Path('articles').glob('*.html'):
    md_file = convert_to_markdown(html_file)
    print(f"✅ {html_file.name} -> {md_file.name}")
```

### Using pandoc (Command Line)

```bash
# Install pandoc
brew install pandoc  # macOS
# or
sudo apt-get install pandoc  # Linux

# Convert single file
pandoc article.html -o article.md

# Batch convert all HTML files
for file in articles/*.html; do
    pandoc "$file" -o "${file%.html}.md"
done
```

## Convert to PDF

### Using weasyprint (Python)

```python
from weasyprint import HTML
from pathlib import Path

def convert_to_pdf(html_file):
    """Convert HTML article to PDF"""
    pdf_file = html_file.with_suffix('.pdf')
    HTML(filename=str(html_file)).write_pdf(pdf_file)
    return pdf_file

# Batch convert
for html_file in Path('articles').glob('*.html'):
    pdf_file = convert_to_pdf(html_file)
    print(f"✅ {html_file.name} -> {pdf_file.name}")
```

### Using wkhtmltopdf (Command Line)

```bash
# Install wkhtmltopdf
brew install wkhtmltopdf  # macOS

# Convert single file
wkhtmltopdf article.html article.pdf

# Batch convert
for file in articles/*.html; do
    wkhtmltopdf "$file" "${file%.html}.pdf"
done
```

## Extract Plain Text

### Using BeautifulSoup (Python)

```python
from bs4 import BeautifulSoup
from pathlib import Path

def extract_text(html_file):
    """Extract plain text from HTML"""
    content = html_file.read_text(encoding='utf-8')
    soup = BeautifulSoup(content, 'html.parser')

    # Remove script and style elements
    for script in soup(['script', 'style']):
        script.decompose()

    # Get text
    text = soup.get_text()

    # Clean up whitespace
    lines = (line.strip() for line in text.splitlines())
    chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
    text = '\n'.join(chunk for chunk in chunks if chunk)

    # Save as .txt
    txt_file = html_file.with_suffix('.txt')
    txt_file.write_text(text, encoding='utf-8')

    return txt_file

# Batch extract
for html_file in Path('articles').glob('*.html'):
    txt_file = extract_text(html_file)
    print(f"✅ {html_file.name} -> {txt_file.name}")
```

## Extract Metadata

### Using BeautifulSoup (Python)

```python
from bs4 import BeautifulSoup
from pathlib import Path
import csv
import re

def extract_metadata(html_file):
    """Extract metadata from HTML comments and content"""
    content = html_file.read_text(encoding='utf-8')

    # Extract from HTML comments
    metadata = {}
    comment_pattern = r'<!--\s*文章标题:\s*(.+?)\s*文章URL:\s*(.+?)\s*下载时间:\s*(.+?)\s*-->'
    match = re.search(comment_pattern, content, re.DOTALL)

    if match:
        metadata['title'] = match.group(1).strip()
        metadata['url'] = match.group(2).strip()
        metadata['download_time'] = match.group(3).strip()

    # Parse HTML
    soup = BeautifulSoup(content, 'html.parser')

    # Try to extract additional metadata
    title_tag = soup.find('h1')
    if title_tag and not metadata.get('title'):
        metadata['title'] = title_tag.get_text().strip()

    author_tag = soup.find(class_=re.compile('author'))
    if author_tag:
        metadata['author'] = author_tag.get_text().strip()

    publish_time_tag = soup.find(id='publish_time')
    if publish_time_tag:
        metadata['publish_time'] = publish_time_tag.get_text().strip()

    metadata['filename'] = html_file.name

    return metadata

# Extract metadata from all files
all_metadata = []
for html_file in Path('articles').glob('*.html'):
    metadata = extract_metadata(html_file)
    all_metadata.append(metadata)

# Save to CSV
csv_file = Path('articles') / 'metadata.csv'
if all_metadata:
    keys = set()
    for m in all_metadata:
        keys.update(m.keys())

    with open(csv_file, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=sorted(keys))
        writer.writeheader()
        writer.writerows(all_metadata)

    print(f"✅ Metadata extracted to {csv_file}")
```

## Integration with Obsidian

### Convert and Organize for Obsidian

```python
from pathlib import Path
import html2text
import shutil

def prepare_for_obsidian(articles_dir, obsidian_vault):
    """Convert articles and organize for Obsidian"""
    h = html2text.HTML2Text()
    h.ignore_links = False
    h.ignore_images = False
    h.body_width = 0

    # Create target directory
    target_dir = Path(obsidian_vault) / 'WeChat Articles'
    target_dir.mkdir(exist_ok=True)

    for html_file in Path(articles_dir).glob('*.html'):
        # Convert to Markdown
        content = html_file.read_text(encoding='utf-8')
        markdown = h.handle(content)

        # Add frontmatter
        frontmatter = """---
tags: [wechat, article]
source: WeChat Official Account
---

"""
        # Save to Obsidian vault
        md_file = target_dir / html_file.with_suffix('.md').name
        md_file.write_text(frontmatter + markdown, encoding='utf-8')

        print(f"✅ {html_file.name} -> {md_file.name}")

# Usage
prepare_for_obsidian('articles', '/path/to/obsidian/vault')
```

## Integration with Notion

Notion can import HTML files directly:

1. In Notion, create a new page or database
2. Use the "Import" option
3. Select "HTML" as the format
4. Upload the HTML files
5. Notion will automatically convert them

For batch import via API:

```python
import requests
from pathlib import Path

def upload_to_notion(html_file, notion_token, database_id):
    """Upload HTML article to Notion via API"""
    headers = {
        "Authorization": f"Bearer {notion_token}",
        "Content-Type": "application/json",
        "Notion-Version": "2022-06-28"
    }

    # Read HTML and convert to Notion blocks
    # (Simplified - actual implementation needs proper HTML -> Notion blocks conversion)

    data = {
        "parent": {"database_id": database_id},
        "properties": {
            "Name": {
                "title": [
                    {"text": {"content": html_file.stem}}
                ]
            }
        }
    }

    response = requests.post(
        "https://api.notion.com/v1/pages",
        headers=headers,
        json=data
    )

    return response.json()
```

## Download Images

Extract and download images from articles:

```python
from bs4 import BeautifulSoup
from pathlib import Path
import requests
from urllib.parse import urljoin

def download_images(html_file, images_dir):
    """Download all images from an article"""
    content = html_file.read_text(encoding='utf-8')
    soup = BeautifulSoup(content, 'html.parser')

    images_dir = Path(images_dir)
    images_dir.mkdir(exist_ok=True)

    # Create subdirectory for this article
    article_images = images_dir / html_file.stem
    article_images.mkdir(exist_ok=True)

    downloaded = []

    for img in soup.find_all('img'):
        img_url = img.get('data-src') or img.get('src')

        if not img_url:
            continue

        try:
            # Download image
            response = requests.get(img_url, timeout=10)
            response.raise_for_status()

            # Generate filename
            img_name = img_url.split('/')[-1].split('?')[0]
            if not img_name:
                img_name = f"image_{len(downloaded)+1}.jpg"

            img_path = article_images / img_name

            # Save image
            img_path.write_bytes(response.content)
            downloaded.append(img_path)

            print(f"✅ Downloaded: {img_name}")

        except Exception as e:
            print(f"❌ Failed to download {img_url}: {e}")

    return downloaded

# Batch download images
for html_file in Path('articles').glob('*.html'):
    images = download_images(html_file, 'images')
    print(f"📁 {html_file.name}: {len(images)} images downloaded")
```

## Tips

1. **Batch Processing**: Use loops to process multiple files efficiently
2. **Error Handling**: Always include try-except blocks for robust conversion
3. **Encoding**: Use UTF-8 encoding for Chinese content
4. **Validation**: Check converted files for completeness
5. **Backup**: Keep original HTML files as backup
