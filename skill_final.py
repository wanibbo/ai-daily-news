#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AI 日报新闻抓取技能 - 最终可用版
"""

import json
import asyncio
import aiohttp
from datetime import datetime
from typing import List, Dict
from dataclasses import dataclass, asdict
from bs4 import BeautifulSoup


@dataclass
class NewsItem:
    title: str
    source: str
    url: str
    publish_time: str
    category: str
    importance_score: int = 5
    
    def to_dict(self) -> Dict:
        return asdict(self)


AI_KEYWORDS = [
    '人工智能', '大模型', 'LLM', '生成式 AI', 'AIGC', '机器学习',
    '深度学习', '神经网络', '自然语言处理', '计算机视觉',
    'AI 应用', 'AGI', 'GPT', 'Claude', 'Gemini', 'OpenAI',
    '智谱', '通义千问', '文心一言', 'Kimi', '月之暗面'
]

HOT_KEYWORDS = ['发布', '推出', '突破', '重磅', '首次', '开源', '黄仁勋', '融资']


def is_ai_related(text: str) -> bool:
    text_lower = text.lower()
    return any(kw.lower() in text_lower for kw in AI_KEYWORDS)


def calc_importance(title: str, source: str) -> int:
    score = 6
    if source in ['量子位', '机器之心']:
        score = 8
    for kw in HOT_KEYWORDS:
        if kw in title:
            score += 1
    return min(score, 10)


async def fetch_quantumwei() -> List[NewsItem]:
    """抓取量子位"""
    items = []
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'zh-CN,zh;q=0.9',
    }
    
    try:
        async with aiohttp.ClientSession(headers=headers) as session:
            async with session.get('https://www.qbitai.com', timeout=15, allow_redirects=True) as resp:
                html = await resp.text('utf-8', errors='ignore')
                soup = BeautifulSoup(html, 'lxml')
                
                # 找所有文章链接
                for link in soup.select('a[href*="/2026/"]')[:25]:
                    href = link.get('href', '')
                    title = link.get_text(strip=True)
                    
                    if not title or len(title) < 5 or len(title) > 100:
                        continue
                    
                    if '/2026/' not in href:
                        continue
                    
                    # AI 相关过滤
                    if not is_ai_related(title):
                        continue
                    
                    # 提取日期
                    parts = href.split('/')
                    date_str = '2026-03-24'
                    if len(parts) >= 5:
                        try:
                            date_str = f"{parts[-3]}-{parts[-2]}-{parts[-1].replace('.html', '')}"
                        except:
                            pass
                    
                    item = NewsItem(
                        title=title,
                        source='量子位',
                        url=href if href.startswith('http') else f'https://www.qbitai.com{href}',
                        publish_time=date_str,
                        category='AI 综合'
                    )
                    item.importance_score = calc_importance(title, '量子位')
                    items.append(item)
                    
    except Exception as e:
        print(f"⚠️ 量子位抓取失败：{e}")
    
    return items


async def scrape_all() -> List[NewsItem]:
    print("📰 开始抓取 AI 新闻...\n")
    
    all_items = []
    items = await fetch_quantumwei()
    if items:
        print(f"  ✓ 量子位：{len(items)} 条")
    all_items.extend(items)
    
    # 去重
    seen = set()
    unique = []
    for item in all_items:
        if item.title not in seen:
            seen.add(item.title)
            unique.append(item)
    
    unique.sort(key=lambda x: x.importance_score, reverse=True)
    print(f"\n✅ 共抓取 {len(unique)} 条不重复新闻\n")
    
    return unique


def generate_report(items: List[NewsItem], limit: int = 10) -> str:
    if not items:
        return "今日暂无 AI 相关新闻"
    
    lines = [
        "=" * 60,
        "🤖 AI 日报简讯",
        f"📅 日期：{datetime.now().strftime('%Y-%m-%d')}",
        f"📊 精选：{min(len(items), limit)} 条",
        "=" * 60,
        ""
    ]
    
    for i, item in enumerate(items[:limit], 1):
        lines.append(f"{i}. [{item.importance_score}⭐] {item.title}")
        lines.append(f"   来源：{item.source}")
        lines.append(f"   链接：{item.url}")
        lines.append("")
    
    lines.append("=" * 60)
    lines.append("数据来源于量子位等主流媒体 · 由 AI 自动整理")
    
    return "\n".join(lines)


async def main():
    items = await scrape_all()
    
    data = {
        'update_time': datetime.now().isoformat(),
        'total_items': len(items),
        'top_items': [item.to_dict() for item in items[:10]]
    }
    
    script_dir = __file__.rsplit('/', 1)[0]
    with open(f'{script_dir}/news_data.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    
    report = generate_report(items)
    print(report)
    print(f"\n💾 数据已保存到：{script_dir}/news_data.json")


if __name__ == '__main__':
    asyncio.run(main())
