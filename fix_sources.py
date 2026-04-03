#!/usr/bin/env python3
"""修复 InfoQ 和雷锋网的内容抓取"""

import re

# 读取文件
with open('skill_v12.py', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. 修复 fetch_article_content 函数，增加更多选择器
old_selectors = "for selector in ['article', '.content', '.post-content', '.article-content', '#content', '.article-body']:"
new_selectors = "for selector in ['article', '.content', '.post-content', '.article-content', '#content', '.article-body', '.article-detail', '.main-content', '.news-content', '.article-wrap']:"
content = content.replace(old_selectors, new_selectors)

# 2. 修复 InfoQ 抓取，使用正确的选择器
old_infoq = "soup.select('.article-item__title a, a[href*=\"/news/\"], a[href*=\"/article/\"]')[:12]"
new_infoq = "soup.select('.article-item__title a, .article-item a[href*=\"/article/\"]')[:15]"
content = content.replace(old_infoq, new_infoq)

# 3. 修复雷锋网抓取
old_leiphone = "soup.select('a[href*=\"/news/\"], a[href*=\"/ai/\"]')[:12]"
new_leiphone = "soup.select('.news-item a, a[href*=\"/news/\"]')[:15]"
content = content.replace(old_leiphone, new_leiphone)

# 保存
with open('skill_v12.py', 'w', encoding='utf-8') as f:
    f.write(content)

print("✅ 修复完成")
