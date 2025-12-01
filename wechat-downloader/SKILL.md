---
name: wechat-downloader
description: High-performance batch downloading of WeChat Official Account articles with parallel processing, smart retry, and comprehensive error handling. This skill should be used when users need to backup, archive, or migrate WeChat public account articles in bulk, requiring efficient parallel downloads with progress tracking and failure recovery.
---

# WeChat Article Downloader

Download WeChat Official Account articles in batch with high-performance parallel processing, intelligent error handling, and comprehensive progress tracking.

## When to Use This Skill

Use this skill when the user needs to:
- Backup WeChat public account articles for offline reading
- Archive content from followed accounts
- Migrate WeChat content to personal blogs or knowledge bases
- Collect articles for data analysis or research
- Download large quantities of articles (10+ articles) efficiently

## Core Capabilities

### 1. High-Performance Parallel Download
- Multi-threaded concurrent downloads (default: 20 threads)
- Connection pool reuse for optimal network performance
- Configurable concurrency based on network conditions
- Average speed: 1.0 article/second for typical use cases

### 2. Intelligent Error Handling
- Automatic classification of failure types:
  - Deleted/violated articles
  - Network timeouts
  - Connection errors
- Smart retry mechanism with exponential backoff
- Detailed failure reports with categorized reasons

### 3. Progress Tracking
- Real-time progress bar with completion percentage
- Live success rate calculation
- Estimated time remaining
- Detailed statistics upon completion

### 4. Resume Capability
- Skip already downloaded files (resume interrupted downloads)
- Separate retry script for failed articles
- Maintains download state across sessions

## Usage Workflow

### Step 1: Prepare Article List

The user needs to provide a JSON file containing the article list. The JSON format should be:

```json
{
  "export_time": "2025-11-29T10:06:06.152Z",
  "total_count": 354,
  "articles": [
    {
      "title": "Article Title",
      "url": "https://mp.weixin.qq.com/s/xxxxx",
      "content_url": "https://mp.weixin.qq.com/s/xxxxx",
      "digest": "Article summary",
      "author": "Author name",
      "publish_date": "2025-01-01"
    }
  ]
}
```

If the user doesn't have this JSON file, provide them with a browser console script (located in `references/export_script.js`) to export the article list from WeChat's web interface.

### Step 2: Download Articles

Use the main download script (`scripts/download_articles.py`) to perform the batch download:

```bash
uv run scripts/download_articles.py
```

The script will:
1. Read the article list from JSON
2. Create output directory for downloaded articles
3. Download articles with 20 parallel threads
4. Display real-time progress with tqdm
5. Save successful downloads as HTML files with metadata
6. Generate a failure report for any unsuccessful downloads

### Step 3: Handle Failures (If Needed)

If there are failed downloads, use the retry script (`scripts/retry_failed.py`) to:
- Re-attempt downloads with longer timeout
- Verify if articles are truly deleted/unavailable
- Provide detailed categorization of failures
- Update the failure list

```bash
uv run scripts/retry_failed.py
```

### Step 4: Verify Results

Check the download statistics:
- Success rate (target: >95%)
- Total articles downloaded
- Categorized failure reasons
- Average download speed

## Performance Optimization

### Network-Based Tuning

Adjust the `max_workers` parameter based on network conditions:

**High-speed network (100Mbps+)**:
```python
max_workers = 30
timeout = 10
```

**Medium-speed network (10-100Mbps)**:
```python
max_workers = 15  # Default
timeout = 15
```

**Low-speed network (<10Mbps)**:
```python
max_workers = 5
timeout = 30
max_retries = 3
```

### Configuration Parameters

Key parameters that can be adjusted in the scripts:

- `max_workers`: Number of concurrent download threads (5-30)
- `timeout`: Request timeout in seconds (10-30)
- `max_retries`: Maximum retry attempts per article (2-5)
- `retry_delay`: Delay between retries in seconds (0.5-2.0)
- `pool_connections`: HTTP connection pool size (match max_workers)

## Output Structure

```
output_directory/
├── 0001_Article_Title.html
├── 0002_Article_Title.html
├── ...
├── failed_articles.json      # List of failed downloads
└── retry_results.json        # Results from retry attempts
```

Each HTML file includes:
- Article content
- Metadata comments (title, URL, download time)
- Original formatting and images

## Error Classification

The skill categorizes failures into distinct types:

**🗑️ Deleted/Violated Articles**
- Article removed by publisher
- Content violated platform rules
- Article reported and taken down
- **Action**: No further action possible

**⏱️ Network Timeouts**
- Request exceeded timeout limit
- Slow server response
- Network instability
- **Action**: Retry with longer timeout

**❌ Other Errors**
- Connection refused
- Invalid URL
- File system errors
- **Action**: Investigate specific error message

## Best Practices

### Before Starting
1. Verify JSON file format and content
2. Check available disk space (estimate: ~50KB per article)
3. Ensure stable network connection
4. Test with small batch first (10-20 articles)

### During Download
1. Monitor progress bar for anomalies
2. Check success rate (should be >90%)
3. Don't interrupt the process
4. Note any system resource issues

### After Download
1. Review success rate and failure reasons
2. Run retry script for timeout failures
3. Verify random sample of downloaded articles
4. Back up downloaded content
5. Clean up old article list and failed articles

### Performance Tips
1. Start with default settings (20 threads)
2. Adjust based on observed performance
3. Avoid downloading during peak hours
4. Use wired connection for large batches
5. Close unnecessary applications to free resources

## Troubleshooting

### High Failure Rate (>10%)
- Reduce `max_workers` to 10
- Increase `timeout` to 25
- Check network stability
- Verify JSON file URLs are valid

### Slow Download Speed (<0.5 articles/sec)
- Increase `max_workers` to 25-30
- Check network bandwidth usage
- Verify no rate limiting from WeChat
- Consider time of day (avoid peak hours)

### Memory Issues
- Reduce `max_workers` to 5-10
- Process in batches of 100 articles
- Clear browser cache and close other apps
- Ensure sufficient RAM available

### File System Errors
- Check disk space
- Verify write permissions
- Ensure file names are valid
- Check path length limits

## Advanced Usage

### Batch Processing Multiple Accounts
Process multiple JSON files sequentially with delays:

```python
import time
import glob

for json_file in glob.glob('*.json'):
    process_articles(json_file)
    time.sleep(60)  # 60 second delay between accounts
```

### Custom Output Format
Modify the save function to export in different formats (Markdown, PDF, etc.). See `references/conversion_guide.md` for details.

### Integration with Knowledge Base
Downloaded articles can be integrated with:
- Obsidian (convert to Markdown)
- Notion (import HTML)
- Logseq (convert to Markdown)
- Custom knowledge management systems

## Technical Details

### Dependencies
- Python 3.11+
- requests (HTTP library)
- tqdm (progress bars)
- uv (package manager, using PEP 723 inline metadata)

### Implementation Highlights
- **Session Reuse**: HTTP session with connection pooling for performance
- **PEP 723 Compliance**: Inline script metadata for dependency management
- **Unicode Handling**: Proper UTF-8 encoding for Chinese content
- **Filename Sanitization**: Automatic cleaning of illegal characters
- **Metadata Preservation**: HTML comments with article information

## Success Metrics

Expected performance benchmarks:

| Metric | Target | Excellent |
|--------|--------|-----------|
| Success Rate | >90% | >95% |
| Download Speed | >0.5/sec | >1.0/sec |
| Retry Effectiveness | >50% | >80% |
| Network Efficiency | Stable | Optimal |

## References

For detailed implementation guides, consult:
- `references/export_script.js` - Browser console script for exporting article lists
- `references/conversion_guide.md` - Converting downloaded HTML to other formats
- `references/troubleshooting.md` - Detailed troubleshooting scenarios

## Notes

- Respect WeChat's terms of service
- Use for personal backup only, not commercial redistribution
- Downloaded content retains original copyright
- Be mindful of server load (avoid excessive concurrent requests)
- Some articles may be legitimately unavailable due to deletion or violation
