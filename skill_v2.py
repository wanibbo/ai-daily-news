#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AI 日报技能 - 增强版
- 多数据源（5+ 主流媒体）
- 每条带摘要（<100 字）
- 商务风格 HTML 输出
- 按热度排序
"""

import json
import asyncio
import aiohttp
from datetime import datetime
from typing import List, Dict
from dataclasses import dataclass, asdict
from bs4 import BeautifulSoup
import re


@dataclass
class NewsItem:
    title: str
    source: str
    url: str
    publish_time: str
    category: str
    summary: str = ""
    importance_score: int = 5
    view_count: int = 0
    
    def to_dict(self) -> Dict:
        return asdict(self)


# AI 关键词
AI_KEYWORDS = [
    '人工智能', '大模型', 'LLM', '生成式 AI', 'AIGC', '机器学习',
    '深度学习', '神经网络', '自然语言处理', '计算机视觉', '强化学习',
    'AI 应用', 'AGI', 'transformer', 'diffusion', 'GPT', 'Claude',
    'Gemini', 'OpenAI', 'Anthropic', '智谱', '百川', '通义千问',
    '文心一言', '讯飞星火', 'Kimi', '阶跃星辰', '月之暗面', 'MiniMax'
]

# 热门关键词（加分）
HOT_KEYWORDS = [
    '发布', '推出', '突破', '重磅', '首次', '开源', '黄仁勋',
    '融资', '创业', '估值', '上市', '合作', '战略', '升级',
    '发布', '上线', '内测', '公测', '融资', '投资', '收购'
]


def is_ai_related(text: str) -> bool:
    """判断是否与 AI 相关"""
    text_lower = text.lower()
    return any(kw.lower() in text_lower for kw in AI_KEYWORDS)


def calc_importance(title: str, source: str, content: str = "") -> int:
    """计算重要性分数 (1-10)"""
    score = 5
    
    # 来源权重
    source_weights = {
        '量子位': 9,
        '机器之心': 9,
        '36Kr': 8,
        'InfoQ': 8,
        'CSDN': 7,
        '掘金': 7,
        '知乎': 6,
    }
    score = max(score, source_weights.get(source, 5))
    
    # 热门词加分
    full_text = title + content
    for kw in HOT_KEYWORDS:
        if kw in full_text:
            score += 0.5
    
    # 标题长度适中加分
    if 20 <= len(title) <= 50:
        score += 0.5
    
    return min(int(score), 10)


def generate_summary(title: str, content: str = "", max_len: int = 100) -> str:
    """生成精炼摘要（<100 字）"""
    if content:
        # 从内容提取第一句
        summary = content.split('.')[0].split('。')[0].strip()
        if len(summary) > max_len:
            summary = summary[:max_len-3] + "..."
        return summary
    else:
        # 从标题生成
        if len(title) <= max_len:
            return title
        return title[:max_len-3] + "..."


class AIDailyScraper:
    """AI 新闻爬虫"""
    
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
        }
        self.session = None
    
    async def init_session(self):
        if self.session is None:
            self.session = aiohttp.ClientSession(headers=self.headers, timeout=aiohttp.ClientTimeout(total=15))
    
    async def close_session(self):
        if self.session:
            await self.session.close()
            self.session = None
    
    async def fetch_quantumwei(self) -> List[NewsItem]:
        """抓取量子位"""
        items = []
        try:
            await self.init_session()
            async with self.session.get('https://www.qbitai.com', allow_redirects=True) as resp:
                html = await resp.text('utf-8', errors='ignore')
                soup = BeautifulSoup(html, 'lxml')
                
                for link in soup.select('a[href*="/2026/"]')[:30]:
                    href = link.get('href', '')
                    title = link.get_text(strip=True)
                    
                    if not title or len(title) < 5 or len(title) > 100:
                        continue
                    if '/2026/' not in href:
                        continue
                    if not is_ai_related(title):
                        continue
                    
                    parts = href.split('/')
                    date_str = '2026-03-24'
                    
                    item = NewsItem(
                        title=title,
                        source='量子位',
                        url=href if href.startswith('http') else f'https://www.qbitai.com{href}',
                        publish_time=date_str,
                        category='AI 综合',
                        summary=generate_summary(title),
                        importance_score=calc_importance(title, '量子位')
                    )
                    items.append(item)
        except Exception as e:
            print(f"⚠️ 量子位：{e}")
        return items
    
    async def fetch_36kr(self) -> List[NewsItem]:
        """抓取 36Kr AI"""
        items = []
        try:
            await self.init_session()
            async with self.session.get('https://36kr.com/topics/766044145815937', allow_redirects=True) as resp:
                html = await resp.text('utf-8', errors='ignore')
                soup = BeautifulSoup(html, 'lxml')
                
                for link in soup.select('a[href*="/p/"]')[:20]:
                    href = link.get('href', '')
                    title = link.get_text(strip=True)
                    
                    if not title or len(title) < 5 or len(title) > 100:
                        continue
                    if not is_ai_related(title):
                        continue
                    
                    item = NewsItem(
                        title=title,
                        source='36Kr',
                        url=href if href.startswith('http') else f'https://36kr.com{href}',
                        publish_time='2026-03-24',
                        category='AI 产业',
                        summary=generate_summary(title),
                        importance_score=calc_importance(title, '36Kr')
                    )
                    items.append(item)
        except Exception as e:
            print(f"⚠️ 36Kr: {e}")
        return items
    
    async def fetch_csdn(self) -> List[NewsItem]:
        """抓取 CSDN AI"""
        items = []
        try:
            await self.init_session()
            async with self.session.get('https://www.csdn.net/tags/AiAiAi0g0g0g0g0g0g0g0g.html', allow_redirects=True) as resp:
                html = await resp.text('utf-8', errors='ignore')
                soup = BeautifulSoup(html, 'lxml')
                
                for link in soup.select('.articleItemBox__title a')[:20]:
                    href = link.get('href', '')
                    title = link.get_text(strip=True)
                    
                    if not title or len(title) < 5 or len(title) > 100:
                        continue
                    if not is_ai_related(title):
                        continue
                    
                    item = NewsItem(
                        title=title,
                        source='CSDN',
                        url=href if href.startswith('http') else f'https://www.csdn.net{href}',
                        publish_time='2026-03-24',
                        category='AI 技术',
                        summary=generate_summary(title),
                        importance_score=calc_importance(title, 'CSDN')
                    )
                    items.append(item)
        except Exception as e:
            print(f"⚠️ CSDN: {e}")
        return items
    
    async def fetch_infoq(self) -> List[NewsItem]:
        """抓取 InfoQ AI"""
        items = []
        try:
            await self.init_session()
            async with self.session.get('https://www.infoq.cn/ai', allow_redirects=True) as resp:
                html = await resp.text('utf-8', errors='ignore')
                soup = BeautifulSoup(html, 'lxml')
                
                for link in soup.select('.article-item__title a')[:20]:
                    href = link.get('href', '')
                    title = link.get_text(strip=True)
                    
                    if not title or len(title) < 5 or len(title) > 100:
                        continue
                    if not is_ai_related(title):
                        continue
                    
                    item = NewsItem(
                        title=title,
                        source='InfoQ',
                        url=href if href.startswith('http') else f'https://www.infoq.cn{href}',
                        publish_time='2026-03-24',
                        category='AI 技术',
                        summary=generate_summary(title),
                        importance_score=calc_importance(title, 'InfoQ')
                    )
                    items.append(item)
        except Exception as e:
            print(f"⚠️ InfoQ: {e}")
        return items
    
    async def fetch_juejin(self) -> List[NewsItem]:
        """抓取掘金 AI"""
        items = []
        try:
            await self.init_session()
            async with self.session.get('https://juejin.cn/tag/人工智能', allow_redirects=True) as resp:
                html = await resp.text('utf-8', errors='ignore')
                soup = BeautifulSoup(html, 'lxml')
                
                for link in soup.select('a.title')[:20]:
                    href = link.get('href', '')
                    title = link.get_text(strip=True)
                    
                    if not title or len(title) < 5 or len(title) > 100:
                        continue
                    if not is_ai_related(title):
                        continue
                    
                    item = NewsItem(
                        title=title,
                        source='掘金',
                        url=href if href.startswith('http') else f'https://juejin.cn{href}',
                        publish_time='2026-03-24',
                        category='AI 技术',
                        summary=generate_summary(title),
                        importance_score=calc_importance(title, '掘金')
                    )
                    items.append(item)
        except Exception as e:
            print(f"⚠️ 掘金：{e}")
        return items
    
    async def scrape_all(self) -> List[NewsItem]:
        """抓取所有源"""
        print("📰 开始抓取 AI 新闻...\n")
        
        all_items = []
        
        # 并发抓取多个源
        tasks = [
            self.fetch_quantumwei(),
            self.fetch_36kr(),
            self.fetch_csdn(),
            self.fetch_infoq(),
            self.fetch_juejin()
        ]
        
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        source_names = ['量子位', '36Kr', 'CSDN', 'InfoQ', '掘金']
        for source, items in zip(source_names, results):
            if isinstance(items, list):
                print(f"  ✓ {source}: {len(items)} 条")
                all_items.extend(items)
        
        # 去重
        seen = set()
        unique = []
        for item in all_items:
            if item.title not in seen:
                seen.add(item.title)
                unique.append(item)
        
        # 按重要性排序
        unique.sort(key=lambda x: x.importance_score, reverse=True)
        
        print(f"\n✅ 共抓取 {len(unique)} 条不重复新闻\n")
        
        await self.close_session()
        return unique


def generate_html(items: List[NewsItem], output_path: str):
    """生成商务风格 HTML"""
    
    today = datetime.now().strftime('%Y-%m-%d')
    
    # 取前 10 条
    top_items = items[:10]
    
    news_html = ""
    for i, item in enumerate(top_items, 1):
        # 根据分数设置颜色
        if item.importance_score >= 8:
            badge_color = "bg-red-100 text-red-800"
            star = "🔥"
        elif item.importance_score >= 6:
            badge_color = "bg-orange-100 text-orange-800"
            star = "⭐"
        else:
            badge_color = "bg-blue-100 text-blue-800"
            star = "📰"
        
        news_html += f'''
        <div class="news-item">
            <div class="news-header">
                <span class="news-rank">#{i:02d}</span>
                <span class="news-badge {badge_color}">{star} {item.importance_score}分</span>
                <span class="news-source">{item.source}</span>
                <span class="news-category">{item.category}</span>
            </div>
            <h3 class="news-title">
                <a href="{item.url}" target="_blank" rel="noopener">{item.title}</a>
            </h3>
            <p class="news-summary">{item.summary}</p>
            <div class="news-footer">
                <span class="news-date">📅 {item.publish_time}</span>
                <a href="{item.url}" target="_blank" rel="noopener" class="read-more">阅读原文 →</a>
            </div>
        </div>
        '''
    
    html = f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AI 日报简讯 - {today}</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <style>
        body {{
            background: linear-gradient(135deg, #1e3a5f 0%, #2d5a87 50%, #3a7ca5 100%);
            min-height: 100vh;
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
        }}
        .container {{ max-width: 1000px; }}
        .header-card {{
            background: rgba(255, 255, 255, 0.98);
            border-radius: 16px;
            padding: 40px;
            margin-bottom: 32px;
            box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.2);
            border: 1px solid rgba(255, 255, 255, 0.3);
        }}
        .news-item {{
            background: rgba(255, 255, 255, 0.98);
            border-radius: 12px;
            padding: 28px;
            margin-bottom: 20px;
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.15);
            transition: all 0.3s ease;
            border-left: 4px solid #2d5a87;
        }}
        .news-item:hover {{
            transform: translateX(8px);
            box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.2);
        }}
        .news-header {{
            display: flex;
            align-items: center;
            gap: 12px;
            margin-bottom: 16px;
            flex-wrap: wrap;
        }}
        .news-rank {{
            background: linear-gradient(135deg, #1e3a5f, #2d5a87);
            color: white;
            padding: 6px 16px;
            border-radius: 20px;
            font-weight: bold;
            font-size: 14px;
        }}
        .news-badge {{
            padding: 6px 16px;
            border-radius: 20px;
            font-size: 13px;
            font-weight: 600;
        }}
        .news-source {{
            background: #e0e7ff;
            color: #3730a3;
            padding: 6px 16px;
            border-radius: 20px;
            font-size: 13px;
            font-weight: 500;
        }}
        .news-category {{
            background: #f3f4f6;
            color: #6b7280;
            padding: 6px 16px;
            border-radius: 20px;
            font-size: 13px;
        }}
        .news-title {{
            font-size: 20px;
            font-weight: 600;
            color: #1e293b;
            margin-bottom: 12px;
            line-height: 1.5;
        }}
        .news-title a {{
            color: #1e3a5f;
            text-decoration: none;
            transition: color 0.2s;
        }}
        .news-title a:hover {{
            color: #3a7ca5;
            text-decoration: underline;
        }}
        .news-summary {{
            color: #475569;
            line-height: 1.7;
            margin-bottom: 16px;
            padding: 16px;
            background: #f8fafc;
            border-radius: 8px;
            border-left: 3px solid #3a7ca5;
        }}
        .news-footer {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding-top: 16px;
            border-top: 1px solid #e2e8f0;
        }}
        .news-date {{
            color: #94a3b8;
            font-size: 13px;
        }}
        .read-more {{
            color: #2d5a87;
            text-decoration: none;
            font-weight: 600;
            font-size: 14px;
            transition: color 0.2s;
        }}
        .read-more:hover {{
            color: #3a7ca5;
        }}
        .stats {{
            display: flex;
            gap: 24px;
            justify-content: center;
            flex-wrap: wrap;
        }}
        .stat-item {{
            text-align: center;
        }}
        .stat-value {{
            font-size: 28px;
            font-weight: bold;
            color: #1e3a5f;
        }}
        .stat-label {{
            font-size: 13px;
            color: #64748b;
            margin-top: 4px;
        }}
    </style>
</head>
<body>
    <div class="py-12 px-4">
        <div class="container mx-auto">
            <!-- 头部 -->
            <div class="header-card text-center">
                <h1 class="text-4xl font-bold bg-gradient-to-r from-blue-800 to-cyan-600 bg-clip-text text-transparent mb-4">
                    🤖 AI 日报简讯
                </h1>
                <p class="text-xl text-slate-600 mb-8">📅 {today}</p>
                
                <div class="stats">
                    <div class="stat-item">
                        <div class="stat-value">{len(top_items)}</div>
                        <div class="stat-label">精选新闻</div>
                    </div>
                    <div class="stat-item">
                        <div class="stat-value">{len(set(i.source for i in top_items))}</div>
                        <div class="stat-label">数据源</div>
                    </div>
                    <div class="stat-item">
                        <div class="stat-value">{len(set(i.category for i in top_items))}</div>
                        <div class="stat-label">类别</div>
                    </div>
                </div>
            </div>

            <!-- 新闻列表 -->
            <div id="news-list">
                {news_html}
            </div>

            <!-- 底部 -->
            <div class="text-center mt-12 text-white/80 text-sm">
                <p>数据来源于量子位、36Kr、CSDN、InfoQ、掘金等主流媒体</p>
                <p class="mt-2">更新时间：{today} · 由 AI 自动整理</p>
            </div>
        </div>
    </div>
</body>
</html>'''
    
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(html)
    
    print(f"📄 HTML 已生成：{output_path}")


async def main():
    """主函数"""
    scraper = AIDailyScraper()
    items = await scraper.scrape_all()
    
    script_dir = __file__.rsplit('/', 1)[0]
    
    # 保存 JSON
    data = {
        'update_time': datetime.now().isoformat(),
        'total_items': len(items),
        'top_items': [item.to_dict() for item in items[:10]]
    }
    with open(f'{script_dir}/news_data.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    
    # 生成 HTML
    generate_html(items, f'{script_dir}/index.html')
    
    print(f"\n💾 数据已保存到：{script_dir}/")
    print(f"📊 共 {len(items)} 条，精选 {len(items[:10])} 条")


if __name__ == '__main__':
    asyncio.run(main())
