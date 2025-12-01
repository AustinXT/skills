## Troubleshooting Guide

Comprehensive solutions for common issues when using the WeChat Article Downloader skill.

### Problem: High Failure Rate (>10%)

**Symptoms:**
- Many articles failing to download
- Success rate below 90%
- Frequent error messages

**Diagnosis:**
Check the `failed_articles.json` file to identify failure patterns:
```bash
cat articles/failed_articles.json | grep "error" | sort | uniq -c
```

**Solutions:**

1. **Reduce Concurrency**
   ```python
   max_workers = 10  # Lower from default 20
   ```

2. **Increase Timeout**
   ```python
   timeout = 25  # Increase from default 15
   ```

3. **Add More Retries**
   ```python
   max_retries = 3  # Increase from default 2
   retry_delay = 1.0  # Increase from default 0.5
   ```

4. **Check Network**
   ```bash
   # Test WeChat connectivity
   curl -I https://mp.weixin.qq.com/

   # Check DNS resolution
   nslookup mp.weixin.qq.com
   ```

### Problem: Slow Download Speed (<0.5 articles/sec)

**Symptoms:**
- Progress bar moving slowly
- Downloads taking much longer than expected
- Low articles per second rate

**Solutions:**

1. **Increase Concurrency**
   ```python
   max_workers = 30  # Increase from default 20
   ```

2. **Check Network Bandwidth**
   ```bash
   # Run speed test
   speedtest-cli

   # Check other bandwidth usage
   nethogs  # Linux
   nettop   # macOS
   ```

3. **Optimize Connection Pool**
   ```python
   session.mount('https://', requests.adapters.HTTPAdapter(
       pool_connections=30,
       pool_maxsize=30,
       max_retries=2
   ))
   ```

4. **Use Wired Connection**
   - Switch from WiFi to ethernet
   - Reduce distance from router
   - Check for network interference

### Problem: Memory Issues

**Symptoms:**
- Python process using excessive RAM (>2GB)
- System slowdown during downloads
- "MemoryError" exceptions

**Solutions:**

1. **Reduce Concurrency**
   ```python
   max_workers = 5  # Significantly reduce threads
   ```

2. **Process in Batches**
   ```python
   def process_in_batches(articles, batch_size=100):
       for i in range(0, len(articles), batch_size):
           batch = articles[i:i+batch_size]
           download_batch(batch)
           gc.collect()  # Force garbage collection
           time.sleep(5)  # Pause between batches
   ```

3. **Immediate File Writing**
   ```python
   # Write files immediately, don't store in memory
   with open(filepath, 'w', encoding='utf-8') as f:
       f.write(content)
   # Don't keep content in variables
   ```

4. **Close Other Applications**
   - Close browser tabs
   - Exit unnecessary applications
   - Check Activity Monitor/Task Manager

### Problem: File System Errors

**Symptoms:**
- "OSError: [Errno 22] Invalid argument"
- "Permission denied" errors
- Files not being saved

**Solutions:**

1. **Check Disk Space**
   ```bash
   df -h  # Check available disk space
   ```
   Ensure at least 1GB free space.

2. **Verify Permissions**
   ```bash
   # Check write permissions
   touch articles/test.txt
   rm articles/test.txt

   # Fix permissions if needed
   chmod -R u+w articles/
   ```

3. **Fix Filename Issues**
   ```python
   def sanitize_filename(filename: str, max_length: int = 100) -> str:
       # Remove all illegal characters
       illegal_chars = r'[<>:"/\\|?*\x00-\x1f]'
       filename = re.sub(illegal_chars, '_', filename)

       # Remove leading/trailing spaces and dots
       filename = filename.strip(' .')

       # Limit length
       if len(filename) > max_length:
           filename = filename[:max_length]

       # Ensure not empty
       if not filename:
           filename = 'unnamed'

       return filename
   ```

4. **Check Path Length**
   ```python
   # On Windows, total path must be <260 characters
   # Use shorter output directory names
   output_dir = Path('art')  # Instead of 'downloaded_wechat_articles'
   ```

### Problem: Connection Pool Errors

**Symptoms:**
- "urllib3.exceptions.MaxRetryError"
- "Connection pool is full"
- "HTTPSConnectionPool... Max retries exceeded"

**Solutions:**

1. **Increase Pool Size**
   ```python
   session.mount('https://', requests.adapters.HTTPAdapter(
       pool_connections=40,  # Increase
       pool_maxsize=40,      # Increase
       max_retries=3
   ))
   ```

2. **Add Connection Cleanup**
   ```python
   # Close session periodically
   if downloaded_count % 100 == 0:
       session.close()
       session = requests.Session()
       setup_session(session)
   ```

3. **Reduce Concurrency**
   ```python
   max_workers = 10  # Match or be less than pool_connections
   ```

### Problem: Timeout Errors

**Symptoms:**
- Many "Read timed out" errors
- "Connection timed out" messages
- Articles timing out consistently

**Solutions:**

1. **Increase Timeout**
   ```python
   timeout = 30  # Increase from 15
   ```

2. **Add Retry Logic**
   ```python
   for attempt in range(3):
       try:
           response = session.get(url, timeout=30)
           break
       except Timeout:
           if attempt < 2:
               time.sleep(2 ** attempt)  # Exponential backoff
               continue
           raise
   ```

3. **Check Time of Day**
   - Avoid peak hours (evening in China timezone)
   - Try early morning or late night
   - WeChat servers may be slower during peak times

4. **Use VPN/Proxy** (if applicable)
   ```python
   proxies = {
       'https': 'http://proxy.example.com:8080'
   }
   response = session.get(url, proxies=proxies, timeout=30)
   ```

### Problem: All Articles Show as Deleted

**Symptoms:**
- Most/all articles marked as "deleted or violated"
- High number of "此内容因违规无法查看" messages

**Diagnosis:**
1. Manually check a few article URLs in browser
2. Verify the JSON file URLs are correct
3. Check if account was suspended

**Solutions:**

1. **Verify URLs**
   - Ensure URLs in JSON are complete and valid
   - Test URLs manually in browser
   - Check for URL encoding issues

2. **Check Account Status**
   - Visit the official account in WeChat
   - Verify account is still active
   - Check if content was legitimately removed

3. **Update Export Script**
   - Re-export article list with latest script
   - Verify export script is getting correct selectors
   - WeChat may have changed their HTML structure

### Problem: Download Stops/Hangs

**Symptoms:**
- Progress bar stops updating
- Script appears frozen
- No error messages

**Solutions:**

1. **Check Process Status**
   ```bash
   # Check if Python process is running
   ps aux | grep python

   # Check system resources
   top  # or htop
   ```

2. **Add Timeout to Thread Pool**
   ```python
   try:
       future.result(timeout=60)  # 60 second timeout per task
   except TimeoutError:
       print(f"Task timed out: {article['title']}")
       continue
   ```

3. **Add Heartbeat Logging**
   ```python
   last_update = time.time()

   for future in as_completed(futures):
       if time.time() - last_update > 30:
           print(f"Still running... {success_count}/{total} complete")
           last_update = time.time()
   ```

4. **Restart with Resume**
   - The script automatically skips downloaded files
   - Simply run the script again
   - It will continue from where it stopped

### Problem: JSON File Format Error

**Symptoms:**
- "JSONDecodeError" when running script
- "No articles found" message
- Script exits immediately

**Solutions:**

1. **Validate JSON**
   ```bash
   # Check if JSON is valid
   python -m json.tool wechat_articles.json > /dev/null

   # Or use jq
   jq . wechat_articles.json > /dev/null
   ```

2. **Check Required Fields**
   ```python
   import json

   with open('wechat_articles.json') as f:
       data = json.load(f)

   # Verify structure
   assert 'articles' in data, "Missing 'articles' key"
   assert isinstance(data['articles'], list), "'articles' must be a list"
   assert len(data['articles']) > 0, "Articles list is empty"

   # Check first article
   article = data['articles'][0]
   assert 'title' in article, "Article missing 'title'"
   assert 'url' in article or 'content_url' in article, "Article missing URL"
   ```

3. **Re-Export Articles**
   - Run the export script again
   - Verify you're on the correct page
   - Check browser console for errors

### Problem: Chinese Characters Garbled

**Symptoms:**
- Downloaded files show question marks or boxes
- Chinese text appears as gibberish
- Encoding errors

**Solutions:**

1. **Force UTF-8 Encoding**
   ```python
   with open(filepath, 'w', encoding='utf-8') as f:
       f.write(content)
   ```

2. **Check Response Encoding**
   ```python
   response = session.get(url)
   response.encoding = 'utf-8'  # Force UTF-8
   content = response.text
   ```

3. **Set System Locale**
   ```bash
   # macOS/Linux
   export LANG=en_US.UTF-8
   export LC_ALL=en_US.UTF-8
   ```

### Getting Additional Help

If none of these solutions work:

1. **Enable Debug Logging**
   ```python
   import logging
   logging.basicConfig(level=logging.DEBUG)
   ```

2. **Capture Full Error**
   ```python
   try:
       # download code
   except Exception as e:
       import traceback
       traceback.print_exc()
       with open('error.log', 'a') as f:
           f.write(traceback.format_exc())
   ```

3. **Check System Resources**
   ```bash
   # CPU usage
   top

   # Memory usage
   free -h  # Linux
   vm_stat  # macOS

   # Disk I/O
   iostat
   ```

4. **Test with Minimal Example**
   ```python
   # Test downloading just one article
   test_article = articles[0]
   result = download_article(test_article, output_dir, 1)
   print(result)
   ```
