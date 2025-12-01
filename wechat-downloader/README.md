# WeChat Article Downloader Skill

High-performance batch downloading of WeChat Official Account articles with intelligent error handling and progress tracking.

## Quick Start

### 1. Export Article List

Run this script in your browser console on a WeChat Official Account article list page:

```javascript
// Open Developer Tools (F12) and paste this in the Console tab
// See references/export_script.js for the full script
```

This will download a JSON file with all article information.

### 2. Download Articles

```bash
# Place the downloaded JSON file in the same directory as the script
# Run the download script
uv run scripts/download_articles.py
```

### 3. Check Results

```
📊 共找到 354 篇文章
🚀 使用 20 线程并行下载...
✅ 下载成功: 338 篇
❌ 下载失败: 16 篇
📊 成功率: 95.5%
⏱️  总耗时: 342.2 秒
⚡ 平均速度: 1.0 篇/秒
```

## Features

- **High Performance**: 20 parallel threads, 1.0 article/second average
- **Smart Retry**: Automatic retry with exponential backoff
- **Error Classification**: Distinguishes deleted articles from network issues
- **Progress Tracking**: Real-time progress bar with statistics
- **Resume Support**: Skips already downloaded files

## Performance

| Metric | Target | Achieved |
|--------|--------|----------|
| Success Rate | >90% | 95.5% |
| Download Speed | >0.5/sec | 1.0/sec |
| Concurrent Threads | 10-30 | 20 |

## File Structure

```
wechat-downloader/
├── SKILL.md                        # Skill instructions (English)
├── SKILL.zh.md                     # Skill instructions (Chinese)
├── README.md                       # This file
├── LICENSE.txt                     # MIT License
├── scripts/
│   ├── download_articles.py        # Main download script
│   └── retry_failed.py             # Retry failed downloads
├── references/
│   ├── export_script.js            # Browser console export script
│   ├── conversion_guide.md         # Convert HTML to other formats
│   └── troubleshooting.md          # Detailed troubleshooting guide
└── assets/
    └── example_articles.json       # Example JSON format
```

## Configuration

Adjust these parameters based on your network:

```python
# High-speed network (100Mbps+)
max_workers = 30
timeout = 10

# Medium-speed network (default)
max_workers = 15
timeout = 15

# Low-speed network
max_workers = 5
timeout = 30
```

## Requirements

- Python 3.11+
- uv package manager
- Dependencies (auto-installed via PEP 723):
  - requests
  - tqdm

## Troubleshooting

Common issues and solutions:

### High Failure Rate
- Reduce `max_workers` to 10
- Increase `timeout` to 25
- Check network stability

### Slow Downloads
- Increase `max_workers` to 25-30
- Use wired connection
- Avoid peak hours

### Memory Issues
- Reduce `max_workers` to 5
- Process in batches of 100
- Close other applications

See `references/troubleshooting.md` for detailed solutions.

## Advanced Usage

### Convert to Markdown

```python
import html2text

h = html2text.HTML2Text()
markdown = h.handle(html_content)
```

### Download Images

```python
from bs4 import BeautifulSoup

soup = BeautifulSoup(html_content, 'html.parser')
for img in soup.find_all('img'):
    download_image(img['data-src'])
```

### Integration with Knowledge Base

- **Obsidian**: Convert to Markdown with frontmatter
- **Notion**: Import HTML directly
- **Logseq**: Convert to Markdown with tags

See `references/conversion_guide.md` for detailed guides.

## License

MIT License - See LICENSE.txt for details

## Disclaimer

This skill is for personal backup and educational purposes only. Please:
- Respect WeChat's Terms of Service
- Use for personal backup only
- Don't redistribute commercially
- Respect original authors' copyright

## Credits

Created with Claude Code by Anthropic
Based on real-world testing with 350+ articles
