#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AI 日报新闻抓取技能 - RSS 版本（可靠）
"""

import json
import asyncio
import aiohttp
import feedparser
from datetime import datetime
from typing import List, Dict
from dataclasses import dataclass, asdict


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


# RSS 源列表
RSS_SOURCES = [
    {
        'name': '量子位',
        'url': 'https://www.qbitai.com/feed',
        'category': 'AI 综合'
    },
    {
        'name': '机器之心',
        'url': 'https://www.jiqizhixin.com/rss',
        'category': 'AI 综合'
    },
    {
        'name': 'Hugging Face',
        'url': 'https://huggingface.co/blog/feed.xml',
        'category': '技术实践'
    },
    {
        'name': 'OpenAI',
        'url': 'https://openai.com/blog/rss/',
        'category': '厂商动态'
    }
]

AI_KEYWORDS = [
    '人工智能', '大模型', 'LLM', '生成式 AI', 'AIGC', '机器学习',
    '深度学习', '神经网络', '自然语言处理', '计算机视觉',
    'AI 应用', 'AI 产品', 'AGI', 'GPT', 'Claude', 'Gemini',
    'OpenAI', '智谱', '百川', '通义千问', '文心一言', 'Kimi',
    '机器人', '自动驾驶', '智能', '算法', '模型', 'Agent'
]

HOT_KEYWORDS = ['发布', '推出', '突破', '重磅', '首次', '开源', '黄仁勋', '融资', '创业']


def is_ai_related(text: str) -> bool:
    """判断是否与 AI 相关"""
    text_lower = text.lower()
    for kw in AI_KEYWORDS:
        if kw.lower() in text_lower:
            return True
    return False


def calc_importance(title: str, source: str) -> int:
    """计算重要性分数"""
    score = 5
    weights = {'量子位': 8, '机器之心': 8, 'OpenAI': 9, 'Hugging Face': 8}
    score = max(score, weights.get(source, 5))
    for kw in HOT_KEYWORDS:
        if kw in title:
            score += 1
    return min(score, 10)


async def fetch_rss(source: Dict) -> List[NewsItem]:
    """抓取单个 RSS 源"""
    items = []
    
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(source['url'], timeout=10) as resp:
                content = await resp.text()
                feed = feedparser.parse(content)
                
                for entry in feed.entries[:15]:
                    title = entry.get('title', '')
                    if len(title) < 5 or len(title) > 150:
                        continue
                    
                    # AI 相关过滤
                    if not is_ai_related(title):
                        continue
                    
                    # 解析时间
                    pub_date = entry.get('published', '')
                    if pub_date:
                        try:
                            dt = datetime.strptime(pub_date[:19], '%Y-%m-%dT%H:%M:%S')
                            pub_date = dt.strftime('%Y-%m-%d')
                        except:
                            pub_date = datetime.now().strftime('%Y-%m-%d')
                    else:
                        pub_date = datetime.now().strftime('%Y-%m-%d')
                    
                    item = NewsItem(
                        title=title,
                        source=source['name'],
                        url=entry.get('link', ''),
                        publish_time=pub_date,
                        category=source['category']
                    )
                    item.importance_score = calc_importance(title, source['name'])
                    items.append(item)
                    
    except Exception as e:
        print(f"  ⚠️ {source['name']} 抓取失败：{e}")
    
    return items


async def scrape_all() -> List[NewsItem]:
    """抓取所有源"""
    print("📰 开始抓取 AI 新闻...\n")
    
    all_items = []
    tasks = [fetch_rss(source) for source in RSS_SOURCES]
    results = await asyncio.gather(*tasks, return_exceptions=True)
    
    for i, result in enumerate(results):
        source_name = RSS_SOURCES[i]['name']
        if isinstance(result, list):
            count = len(result)
            if count > 0:
                print(f"  ✓ {source_name}: {count} 条")
            all_items.extend(result)
        else:
            print(f"  ✗ {source_name}: 失败")
    
    # 去重
    seen = set()
    unique = []
    for item in all_items:
        if item.title not in seen:
            seen.add(item.title)
            unique.append(item)
    
    # 排序
    unique.sort(key=lambda x: x.importance_score, reverse=True)
    
    print(f"\n✅ 共抓取 {len(unique)} 条不重复新闻\n")
    
    return unique


def generate_report(items: List[NewsItem], limit: int = 10) -> str:
    """生成日报"""
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
        lines.append(f"   来源：{item.source} | {item.category}")
        lines.append(f"   链接：{item.url}")
        lines.append("")
    
    lines.append("=" * 60)
    lines.append("数据来源于量子位、机器之心等主流媒体 · 由 AI 自动整理")
    
    return "\n".join(lines)


async def main():
    """主函数"""
    items = await scrape_all()
    
    # 保存 JSON
    data = {
        'update_time': datetime.now().isoformat(),
        'total_items': len(items),
        'top_items': [item.to_dict() for item in items[:10]]
    }
    
    script_dir = __file__.rsplit('/', 1)[0]
    with open(f'{script_dir}/news_data.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    
    # 输出日报
    report = generate_report(items)
    print(report)
    
    print(f"\n💾 数据已保存到：{script_dir}/news_data.json")


if __name__ == '__main__':
    asyncio.run(main())
