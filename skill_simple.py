#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AI 日报新闻抓取技能 - 简洁可用版
直接运行，输出日报
"""

import json
import asyncio
import aiohttp
from datetime import datetime
from typing import List, Dict
from dataclasses import dataclass, asdict, field
import re


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


# AI 关键词
AI_KEYWORDS = [
    '人工智能', '大模型', 'LLM', '生成式 AI', 'AIGC', '机器学习',
    '深度学习', '神经网络', '自然语言处理', '计算机视觉', '强化学习',
    'AI 应用', 'AI 产品', 'AGI', 'transformer', 'diffusion',
    'GPT', 'Claude', 'Gemini', 'OpenAI', 'Anthropic', '智谱', '百川',
    '通义千问', '文心一言', '讯飞星火', 'Kimi', '阶跃星辰', '月之暗面'
]

# 热门关键词（加分）
HOT_KEYWORDS = [
    '发布', '推出', '突破', '重磅', '首次', '开源', '黄仁勋',
    '融资', '创业', '估值', '上市', '合作', '战略'
]


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
    
    # 来源权重
    weights = {'量子位': 8, '机器之心': 8, '36Kr': 7}
    score = max(score, weights.get(source, 5))
    
    # 热门词加分
    for kw in HOT_KEYWORDS:
        if kw in title:
            score += 1
    
    return min(score, 10)


async def fetch_quantumwei() -> List[NewsItem]:
    """抓取量子位"""
    items = []
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    }
    
    try:
        async with aiohttp.ClientSession(headers=headers) as session:
            async with session.get('https://www.qbitai.com', timeout=15) as resp:
                html = await resp.text('utf-8', errors='ignore')
                
                # 提取标题和链接
                pattern = r'href="(https://www\.qbitai\.com/(\d{4})/(\d+)/(\d+)\.html)"[^>]*>.*?<h[34][^>]*>([^<]+)</h[34]>'
                matches = re.findall(pattern, html, re.DOTALL)
                
                for match in matches[:20]:
                    url, year, month, day, title = match
                    title = title.strip()
                    
                    if len(title) < 5 or len(title) > 100:
                        continue
                    
                    if not is_ai_related(title):
                        continue
                    
                    item = NewsItem(
                        title=title,
                        source='量子位',
                        url=url,
                        publish_time=f"{year}-{month}-{day}",
                        category='AI 综合'
                    )
                    item.importance_score = calc_importance(title, '量子位')
                    items.append(item)
                    
    except Exception as e:
        print(f"⚠️ 量子位抓取失败：{e}")
    
    return items


async def scrape_all() -> List[NewsItem]:
    """抓取所有源"""
    print("📰 开始抓取 AI 新闻...\n")
    
    all_items = []
    
    # 抓取量子位
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
        lines.append(f"   来源：{item.source}")
        lines.append(f"   链接：{item.url}")
        lines.append("")
    
    lines.append("=" * 60)
    lines.append("数据来源于量子位等主流媒体 · 由 AI 自动整理")
    
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
