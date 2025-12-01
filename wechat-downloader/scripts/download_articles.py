#!/usr/bin/env python3
# /// script
# requires-python = ">=3.11"
# dependencies = [
#     "requests",
#     "tqdm",
# ]
# ///

"""
微信公众号文章并行下载脚本（优化版）

优化点：
1. 增加线程数到 20
2. 使用会话对象复用连接
3. 减少超时时间
4. 添加失败重试机制
5. 快速失败策略
"""

import json
import os
import re
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from typing import Dict, List, Tuple
from urllib.parse import urlparse

import requests
from tqdm import tqdm


# 全局会话对象，支持连接池复用
session = requests.Session()
session.mount('https://', requests.adapters.HTTPAdapter(
    pool_connections=20,
    pool_maxsize=20,
    max_retries=2
))


def sanitize_filename(filename: str, max_length: int = 100) -> str:
    """清理文件名，移除非法字符"""
    filename = re.sub(r'[<>:"/\\|?*]', '_', filename)
    filename = filename.strip()
    if len(filename) > max_length:
        filename = filename[:max_length]
    return filename


def download_article(article: Dict, output_dir: Path, index: int, max_retries: int = 2) -> Tuple[bool, str, str]:
    """
    下载单篇文章（优化版）

    Args:
        article: 文章信息字典
        output_dir: 输出目录
        index: 文章编号
        max_retries: 最大重试次数

    Returns:
        (是否成功, 文章标题, 错误信息)
    """
    title = article.get('title', f'未命名文章_{index}')
    url = article.get('content_url') or article.get('url')

    if not url:
        return False, title, "缺少URL"

    # 检查文件是否已存在
    safe_title = sanitize_filename(title)
    filename = f"{index:04d}_{safe_title}.html"
    filepath = output_dir / filename

    if filepath.exists():
        return True, title, ""  # 跳过已存在的文件

    # 设置请求头
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
        'Connection': 'keep-alive',
    }

    # 重试逻辑
    for attempt in range(max_retries):
        try:
            # 使用更短的超时时间
            response = session.get(url, headers=headers, timeout=15)
            response.raise_for_status()

            # 快速检查是否是被删除的文章
            content = response.text
            if '此内容因违规无法查看' in content or '该内容已被发布者删除' in content:
                return False, title, "文章已删除或违规"

            # 保存文章
            metadata = f"""<!--
文章标题: {title}
文章URL: {url}
下载时间: {time.strftime('%Y-%m-%d %H:%M:%S')}
-->
"""
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(metadata + content)

            return True, title, ""

        except requests.exceptions.Timeout:
            if attempt < max_retries - 1:
                time.sleep(0.5)  # 短暂延迟后重试
                continue
            return False, title, "请求超时"

        except requests.exceptions.RequestException as e:
            if attempt < max_retries - 1:
                time.sleep(0.5)
                continue
            return False, title, f"网络错误: {str(e)}"

        except Exception as e:
            return False, title, f"未知错误: {str(e)}"

    return False, title, "超过最大重试次数"


def main():
    """主函数"""
    # 文件路径
    json_file = Path(__file__).parent.parent / 'task05_wechat' / 'wechat_articles_2025-11-29.json'
    output_dir = Path(__file__).parent / 'articles'

    # 创建输出目录
    output_dir.mkdir(exist_ok=True)

    # 读取 JSON 文件
    print(f"📖 读取文章列表: {json_file}")
    with open(json_file, 'r', encoding='utf-8') as f:
        data = json.load(f)

    articles = data.get('articles', [])
    total_count = len(articles)

    print(f"📊 共找到 {total_count} 篇文章")
    print(f"💾 保存目录: {output_dir}")
    print(f"🚀 使用 20 线程并行下载（优化版）...\n")

    # 统计信息
    success_count = 0
    failed_count = 0
    failed_articles = []

    start_time = time.time()

    # 使用线程池并行下载（增加到 20 线程）
    with ThreadPoolExecutor(max_workers=20) as executor:
        # 提交所有任务
        futures = {
            executor.submit(download_article, article, output_dir, idx + 1): (idx + 1, article)
            for idx, article in enumerate(articles)
        }

        # 使用 tqdm 显示进度条
        with tqdm(total=total_count, desc="下载进度", unit="篇",
                  bar_format='{l_bar}{bar}| {n_fmt}/{total_fmt} [{elapsed}<{remaining}, {rate_fmt}]') as pbar:

            for future in as_completed(futures):
                idx, article = futures[future]
                try:
                    success, title, error_msg = future.result()

                    if success:
                        success_count += 1
                    else:
                        failed_count += 1
                        failed_articles.append({
                            'index': idx,
                            'title': title,
                            'error': error_msg
                        })

                except Exception as e:
                    failed_count += 1
                    failed_articles.append({
                        'index': idx,
                        'title': article.get('title', '未知'),
                        'error': str(e)
                    })

                pbar.update(1)
                # 实时更新成功率
                current_total = success_count + failed_count
                if current_total > 0:
                    success_rate = success_count / current_total * 100
                    pbar.set_postfix_str(f"成功率: {success_rate:.1f}%")

    elapsed_time = time.time() - start_time

    # 打印统计信息
    print(f"\n{'='*60}")
    print(f"✅ 下载成功: {success_count} 篇")
    print(f"❌ 下载失败: {failed_count} 篇")
    print(f"📊 成功率: {success_count/total_count*100:.1f}%")
    print(f"⏱️  总耗时: {elapsed_time:.1f} 秒")
    print(f"⚡ 平均速度: {total_count/elapsed_time:.1f} 篇/秒")

    # 保存失败列表
    if failed_articles:
        print(f"\n{'='*60}")
        print("失败文章列表:")
        failed_file = output_dir / 'failed_articles.json'
        with open(failed_file, 'w', encoding='utf-8') as f:
            json.dump(failed_articles, f, ensure_ascii=False, indent=2)

        print(f"详细信息已保存到: {failed_file}")

        # 显示前 10 个失败的文章
        for item in failed_articles[:10]:
            print(f"  [{item['index']:04d}] {item['title'][:40]} - {item['error']}")

        if len(failed_articles) > 10:
            print(f"  ... 还有 {len(failed_articles) - 10} 篇失败文章")

    print(f"\n{'='*60}")
    print(f"🎉 下载完成！文章保存在: {output_dir}")


if __name__ == '__main__':
    main()
