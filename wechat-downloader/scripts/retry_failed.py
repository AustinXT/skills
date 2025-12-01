#!/usr/bin/env python3
# /// script
# requires-python = ">=3.11"
# dependencies = [
#     "requests",
#     "tqdm",
# ]
# ///

"""
重新核查失败文章的脚本

使用 10 个并发任务核查失败的文章,验证是否真的失败。
"""

import json
import re
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from typing import Dict, Tuple

import requests
from tqdm import tqdm


# 全局会话对象
session = requests.Session()
session.mount('https://', requests.adapters.HTTPAdapter(
    pool_connections=10,
    pool_maxsize=10,
    max_retries=3
))


def sanitize_filename(filename: str, max_length: int = 100) -> str:
    """清理文件名"""
    filename = re.sub(r'[<>:"/\\|?*]', '_', filename)
    filename = filename.strip()
    if len(filename) > max_length:
        filename = filename[:max_length]
    return filename


def check_article(failed_item: Dict, articles: list, output_dir: Path) -> Tuple[str, str, str]:
    """
    核查单篇文章

    Returns:
        (标题, 状态, 详细信息)
    """
    index = failed_item['index']
    title = failed_item['title']
    original_error = failed_item['error']

    # 获取文章URL
    article = articles[index - 1]  # 索引从1开始,列表从0开始
    url = article.get('content_url') or article.get('url')

    if not url:
        return title, "❌ 失败", "缺少URL"

    # 检查是否已经下载成功
    safe_title = sanitize_filename(title)
    filename = f"{index:04d}_{safe_title}.html"
    filepath = output_dir / filename

    if filepath.exists():
        return title, "✅ 已存在", "文件已下载"

    # 设置请求头
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
        'Connection': 'keep-alive',
    }

    # 尝试多次重试(最多3次)
    max_retries = 3
    for attempt in range(max_retries):
        try:
            # 使用更长的超时时间进行核查
            response = session.get(url, headers=headers, timeout=30)
            response.raise_for_status()

            content = response.text

            # 检查是否是被删除的文章
            if '此内容因违规无法查看' in content:
                return title, "🚫 已违规", "内容因违规无法查看"

            if '该内容已被发布者删除' in content:
                return title, "🗑️  已删除", "内容已被发布者删除"

            if '该内容已被投诉' in content:
                return title, "⚠️  已投诉", "内容已被投诉"

            if len(content) < 500:
                return title, "❓ 内容异常", f"内容过短({len(content)}字符)"

            # 如果可以成功下载,保存文件
            metadata = f"""<!--
文章标题: {title}
文章URL: {url}
下载时间: {time.strftime('%Y-%m-%d %H:%M:%S')}
重试次数: {attempt + 1}
原错误: {original_error}
-->
"""
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(metadata + content)

            return title, "✅ 重试成功", f"第{attempt + 1}次重试成功"

        except requests.exceptions.Timeout:
            if attempt < max_retries - 1:
                time.sleep(2)  # 等待2秒后重试
                continue
            return title, "⏱️  超时", f"尝试{max_retries}次后仍超时"

        except requests.exceptions.RequestException as e:
            if attempt < max_retries - 1:
                time.sleep(2)
                continue
            return title, "❌ 网络错误", str(e)[:50]

        except Exception as e:
            return title, "❌ 未知错误", str(e)[:50]

    return title, "❌ 失败", "超过最大重试次数"


def main():
    """主函数"""
    # 文件路径
    json_file = Path(__file__).parent.parent / 'task05_wechat' / 'wechat_articles_2025-11-29.json'
    failed_file = Path(__file__).parent / 'articles' / 'failed_articles.json'
    output_dir = Path(__file__).parent / 'articles'

    # 读取原始文章列表
    print("📖 读取原始文章列表...")
    with open(json_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    articles = data.get('articles', [])

    # 读取失败文章列表
    print("📋 读取失败文章列表...")
    with open(failed_file, 'r', encoding='utf-8') as f:
        failed_articles = json.load(f)

    total = len(failed_articles)
    print(f"🔍 共需核查 {total} 篇失败文章")

    # 分类统计
    timeout_count = sum(1 for item in failed_articles if 'timeout' in item['error'].lower())
    deleted_count = total - timeout_count

    print(f"   - 网络超时: {timeout_count} 篇")
    print(f"   - 已删除/违规: {deleted_count} 篇")
    print(f"\n🚀 使用 10 线程并发核查...\n")

    # 结果统计
    results = {
        "retry_success": [],
        "already_exists": [],
        "deleted": [],
        "timeout": [],
        "other_error": []
    }

    # 使用线程池并发核查
    with ThreadPoolExecutor(max_workers=10) as executor:
        futures = {
            executor.submit(check_article, item, articles, output_dir): item
            for item in failed_articles
        }

        with tqdm(total=total, desc="核查进度", unit="篇") as pbar:
            for future in as_completed(futures):
                item = futures[future]
                try:
                    title, status, detail = future.result()

                    # 分类统计
                    if "重试成功" in status:
                        results["retry_success"].append({
                            "index": item['index'],
                            "title": title,
                            "detail": detail
                        })
                    elif "已存在" in status:
                        results["already_exists"].append({
                            "index": item['index'],
                            "title": title
                        })
                    elif "删除" in status or "违规" in status or "投诉" in status:
                        results["deleted"].append({
                            "index": item['index'],
                            "title": title,
                            "reason": detail
                        })
                    elif "超时" in status:
                        results["timeout"].append({
                            "index": item['index'],
                            "title": title,
                            "detail": detail
                        })
                    else:
                        results["other_error"].append({
                            "index": item['index'],
                            "title": title,
                            "error": detail
                        })

                    pbar.set_postfix_str(f"{status}: {title[:30]}...")

                except Exception as e:
                    results["other_error"].append({
                        "index": item['index'],
                        "title": item['title'],
                        "error": str(e)
                    })

                pbar.update(1)

    # 打印详细统计
    print(f"\n{'='*70}")
    print("📊 核查结果统计\n")

    print(f"✅ 重试成功: {len(results['retry_success'])} 篇")
    for item in results['retry_success']:
        print(f"   [{item['index']:04d}] {item['title'][:40]} - {item['detail']}")

    print(f"\n📁 已存在文件: {len(results['already_exists'])} 篇")
    for item in results['already_exists']:
        print(f"   [{item['index']:04d}] {item['title'][:40]}")

    print(f"\n🗑️  确认已删除/违规: {len(results['deleted'])} 篇")
    for item in results['deleted'][:10]:
        print(f"   [{item['index']:04d}] {item['title'][:40]} - {item['reason']}")
    if len(results['deleted']) > 10:
        print(f"   ... 还有 {len(results['deleted']) - 10} 篇")

    print(f"\n⏱️  仍然超时: {len(results['timeout'])} 篇")
    for item in results['timeout']:
        print(f"   [{item['index']:04d}] {item['title'][:40]} - {item['detail']}")

    print(f"\n❌ 其他错误: {len(results['other_error'])} 篇")
    for item in results['other_error']:
        print(f"   [{item['index']:04d}] {item['title'][:40]} - {item['error']}")

    # 保存详细结果
    result_file = output_dir / 'retry_results.json'
    with open(result_file, 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=2)

    print(f"\n{'='*70}")
    print(f"📄 详细结果已保存到: {result_file}")

    # 更新失败列表
    still_failed = results['deleted'] + results['timeout'] + results['other_error']
    if still_failed:
        with open(failed_file, 'w', encoding='utf-8') as f:
            failed_data = [
                {
                    "index": item['index'],
                    "title": item['title'],
                    "error": item.get('reason') or item.get('detail') or item.get('error', '未知错误')
                }
                for item in still_failed
            ]
            json.dump(failed_data, f, ensure_ascii=False, indent=2)

        print(f"🔄 更新后的失败列表: {len(still_failed)} 篇")
    else:
        print(f"🎉 所有文章核查完成,无失败文章!")

    # 最终统计
    final_success = len(results['retry_success']) + len(results['already_exists'])
    print(f"\n✨ 最终成功: {final_success}/{total} 篇")
    print(f"❌ 最终失败: {len(still_failed)}/{total} 篇")


if __name__ == '__main__':
    main()
