/**
 * WeChat Article List Export Script
 *
 * Run this script in the browser console on a WeChat Official Account article list page
 * to export the article information as a JSON file.
 *
 * Usage:
 * 1. Open the WeChat Official Account article list page in your browser
 * 2. Open Developer Tools (F12 or Cmd+Option+I)
 * 3. Go to the Console tab
 * 4. Paste this entire script and press Enter
 * 5. The browser will automatically download a JSON file
 */

(function() {
    console.log('Starting WeChat article export...');

    const articles = [];

    // Method 1: Try to extract from article list items
    const listItems = document.querySelectorAll('.album__list-item, .appmsg-item, .weui-media-box');

    if (listItems.length > 0) {
        listItems.forEach((item, index) => {
            const titleEl = item.querySelector('.album__list-item-title, .appmsg-title, .weui-media-box__title');
            const linkEl = item.querySelector('a');
            const digestEl = item.querySelector('.appmsg-desc, .weui-media-box__desc');
            const authorEl = item.querySelector('.appmsg-author');
            const dateEl = item.querySelector('.appmsg-time, .publish_time');

            if (titleEl && linkEl) {
                const article = {
                    title: titleEl.innerText?.trim() || `Article ${index + 1}`,
                    url: linkEl.href,
                    content_url: linkEl.href,
                    digest: digestEl?.innerText?.trim() || '',
                    author: authorEl?.innerText?.trim() || '',
                    publish_date: dateEl?.innerText?.trim() || ''
                };

                articles.push(article);
            }
        });
    }

    // Method 2: If Method 1 fails, try alternative selectors
    if (articles.length === 0) {
        const altItems = document.querySelectorAll('[data-link], [data-url]');

        altItems.forEach((item, index) => {
            const url = item.getAttribute('data-link') || item.getAttribute('data-url');
            const title = item.getAttribute('data-title') ||
                         item.querySelector('[class*="title"]')?.innerText?.trim() ||
                         `Article ${index + 1}`;

            if (url) {
                articles.push({
                    title: title,
                    url: url,
                    content_url: url,
                    digest: '',
                    author: '',
                    publish_date: ''
                });
            }
        });
    }

    if (articles.length === 0) {
        alert('No articles found. Please make sure you are on a WeChat Official Account article list page.');
        console.error('Export failed: No articles found on the page');
        return;
    }

    // Create the export data
    const exportData = {
        export_time: new Date().toISOString(),
        total_count: articles.length,
        articles: articles
    };

    // Create and download the JSON file
    const blob = new Blob([JSON.stringify(exportData, null, 2)], {
        type: 'application/json;charset=utf-8'
    });

    const url = URL.createObjectURL(blob);
    const link = document.createElement('a');
    link.href = url;
    link.download = `wechat_articles_${new Date().toISOString().split('T')[0]}.json`;

    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);

    URL.revokeObjectURL(url);

    console.log(`✅ Export successful! ${articles.length} articles exported.`);
    console.log('File name:', link.download);
    alert(`✅ Successfully exported ${articles.length} articles!\nFile: ${link.download}`);
})();
