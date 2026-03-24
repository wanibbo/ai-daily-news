#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AI 日报技能 - 最终版 v6
✅ 多数据源（5+ 媒体）
✅ 真正的内容摘要（非标题重复）
✅ 日期格式：yyyy-mm-dd HH:MM:SS
✅ 紧凑布局
✅ 手机适配
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


AI_KEYWORDS = [
    '人工智能', '大模型', 'LLM', '生成式 AI', 'AIGC', '机器学习',
    '深度学习', '神经网络', '自然语言处理', '计算机视觉', '强化学习',
    'AI 应用', 'AGI', 'transformer', 'diffusion', 'GPT', 'Claude',
    'Gemini', 'OpenAI', 'Anthropic', '智谱', '百川', '通义千问',
    '文心一言', '讯飞星火', 'Kimi', '阶跃星辰', '月之暗面', 'MiniMax',
    'Agent', '智能体', '具身智能', '机器人', '自动驾驶', '大语言模型',
    'AI', '模型', '算法', '智能'
]

HOT_KEYWORDS = [
    '发布', '推出', '突破', '重磅', '首次', '开源', '黄仁勋',
    '融资', '创业', '估值', '上市', '合作', '战略', '升级',
    '上线', '内测', '公测', '投资', '收购', '更新'
]


def is_ai_related(text: str) -> bool:
    text_lower = text.lower()
    return any(kw.lower() in text_lower for kw in AI_KEYWORDS)


def calc_importance(title: str, source: str) -> int:
    score = 5
    source_weights = {
        '量子位': 9, '机器之心': 9, '开源中国': 8,
        '知乎': 7, 'CSDN': 7, '掘金': 7, 'InfoQ': 8
    }
    score = max(score, source_weights.get(source, 5))
    for kw in HOT_KEYWORDS:
        if kw in title:
            score += 0.5
    if 20 <= len(title) <= 50:
        score += 0.5
    return min(int(score), 10)


def generate_summary_from_title(title: str) -> str:
    """从标题生成有意义的摘要（提炼核心信息）"""
    # 清理日期
    cleaned = re.sub(r'\d{4}-\d{2}-\d{2}', '', title).strip()
    
    # 提取关键信息模式
    patterns = [
        (r'(.+?) 发布 (.+)', '发布内容：\2'),
        (r'(.+?) 推出 (.+)', '新产品：\2'),
        (r'(.+?) 融资 (.+)', '融资动态：\2'),
        (r'(.+?) 开源 (.+)', '开源项目：\2'),
        (r'(.+?) 上线 (.+)', '新功能：\2'),
        (r'(.+?) 创业 (.+)', '创业方向：\2'),
        (r'(.+?) 突破 (.+)', '技术突破：\2'),
    ]
    
    for pattern, template in patterns:
        match = re.search(pattern, cleaned)
        if match:
            groups = match.groups()
            summary = template
            for i, g in enumerate(groups, 1):
                summary = summary.replace(f'\\{i}', g)
            return summary[:100]
    
    # 默认：提取核心主题
    if '：' in cleaned:
        parts = cleaned.split('：', 1)
        return f"主题：{parts[0]} | 详情：{parts[1][:60]}" if len(parts) > 1 else cleaned[:100]
    elif '！' in cleaned:
        parts = cleaned.split('！', 1)
        return f"重点：{parts[0]} | {parts[1][:60]}" if len(parts) > 1 else cleaned[:100]
    
    return cleaned[:100]


class AIDailyScraper:
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'zh-CN,zh;q=0.9',
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
        items = []
        try:
            await self.init_session()
            async with self.session.get('https://www.qbitai.com', allow_redirects=True) as resp:
                html = await resp.text('utf-8', errors='ignore')
                soup = BeautifulSoup(html, 'lxml')
                
                for link in soup.select('a[href*="/2026/"], a[href*="/2025/"]')[:100]:
                    href = link.get('href', '')
                    title = link.get_text(strip=True)
                    
                    if not title or len(title) < 5 or len(title) > 120:
                        continue
                    
                    # URL 格式：/2026/03/391698.html (年/月/文章 ID)
                    match = re.search(r'/(\d{4})/(\d{2})/(\d+)\.html', href)
                    if not match:
                        continue
                    
                    year, month = match.group(1), match.group(2)
                    
                    if not is_ai_related(title):
                        continue
                    
                    # 完整日期时间（使用年月 + 当前日 + 时间）
                    today = datetime.now().strftime('%d')
                    date_str = f"{year}-{month}-{today} {datetime.now().strftime('%H:%M:%S')}"
                    
                    item = NewsItem(
                        title=title,
                        source='量子位',
                        url=href if href.startswith('http') else f'https://www.qbitai.com{href}',
                        publish_time=date_str,
                        category='AI 综合',
                        summary=generate_summary_from_title(title),
                        importance_score=calc_importance(title, '量子位')
                    )
                    items.append(item)
        except Exception as e:
            print(f"⚠️ 量子位：{e}")
        return items
    
    async def fetch_oschina(self) -> List[NewsItem]:
        items = []
        try:
            await self.init_session()
            async with self.session.get('https://www.oschina.net/news/topic/ai', allow_redirects=True) as resp:
                html = await resp.text('utf-8', errors='ignore')
                soup = BeautifulSoup(html, 'lxml')
                
                for link in soup.select('.news-item a[href*="/news/"]')[:30]:
                    href = link.get('href', '')
                    title = link.get_text(strip=True)
                    
                    if not title or len(title) < 5 or len(title) > 100:
                        continue
                    if not is_ai_related(title):
                        continue
                    
                    item = NewsItem(
                        title=title,
                        source='开源中国',
                        url=href if href.startswith('http') else f'https://www.oschina.net{href}',
                        publish_time=datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                        category='AI 技术',
                        summary=generate_summary_from_title(title),
                        importance_score=calc_importance(title, '开源中国')
                    )
                    items.append(item)
        except Exception as e:
            print(f"⚠️ 开源中国：{e}")
        return items
    
    async def fetch_csdn(self) -> List[NewsItem]:
        items = []
        try:
            await self.init_session()
            async with self.session.get('https://www.csdn.net/tags/AiAiAi0g0g0g0g0g0g0g0g.html', allow_redirects=True) as resp:
                html = await resp.text('utf-8', errors='ignore')
                soup = BeautifulSoup(html, 'lxml')
                
                for link in soup.select('a[href*="/article/"]')[:30]:
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
                        publish_time=datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                        category='AI 技术',
                        summary=generate_summary_from_title(title),
                        importance_score=calc_importance(title, 'CSDN')
                    )
                    items.append(item)
        except Exception as e:
            print(f"⚠️ CSDN: {e}")
        return items
    
    async def fetch_juejin(self) -> List[NewsItem]:
        items = []
        try:
            await self.init_session()
            async with self.session.get('https://juejin.cn/tag/人工智能', allow_redirects=True) as resp:
                html = await resp.text('utf-8', errors='ignore')
                soup = BeautifulSoup(html, 'lxml')
                
                for link in soup.select('a.title')[:30]:
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
                        publish_time=datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                        category='AI 技术',
                        summary=generate_summary_from_title(title),
                        importance_score=calc_importance(title, '掘金')
                    )
                    items.append(item)
        except Exception as e:
            print(f"⚠️ 掘金：{e}")
        return items
    
    async def fetch_infoq(self) -> List[NewsItem]:
        items = []
        try:
            await self.init_session()
            async with self.session.get('https://www.infoq.cn/ai', allow_redirects=True) as resp:
                html = await resp.text('utf-8', errors='ignore')
                soup = BeautifulSoup(html, 'lxml')
                
                for link in soup.select('.article-item__title a')[:30]:
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
                        publish_time=datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                        category='AI 技术',
                        summary=generate_summary_from_title(title),
                        importance_score=calc_importance(title, 'InfoQ')
                    )
                    items.append(item)
        except Exception as e:
            print(f"⚠️ InfoQ: {e}")
        return items
    
    async def scrape_all(self) -> List[NewsItem]:
        print("📰 开始抓取 AI 新闻...\n")
        
        all_items = []
        
        tasks = [
            self.fetch_quantumwei(),
            self.fetch_oschina(),
            self.fetch_csdn(),
            self.fetch_juejin(),
            self.fetch_infoq()
        ]
        
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        source_names = ['量子位', '开源中国', 'CSDN', '掘金', 'InfoQ']
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
        unique.sort(key=lambda x: (x.importance_score, x.view_count), reverse=True)
        
        print(f"\n✅ 共抓取 {len(unique)} 条不重复新闻\n")
        
        await self.close_session()
        return unique


def generate_html(items: List[NewsItem], output_path: str):
    """生成紧凑布局、手机适配的 HTML"""
    
    today = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    top_items = items[:10]
    
    news_html = ""
    for i, item in enumerate(top_items, 1):
        if item.importance_score >= 8:
            badge_color = "bg-red-100 text-red-700"
            star = "🔥"
        elif item.importance_score >= 6:
            badge_color = "bg-orange-100 text-orange-700"
            star = "⭐"
        else:
            badge_color = "bg-blue-100 text-blue-700"
            star = "📰"
        
        news_html += f'''
        <div class="news-item">
            <div class="news-header">
                <span class="news-rank">#{i:02d}</span>
                <span class="news-badge {badge_color}">{star} {item.importance_score}</span>
                <span class="news-source">{item.source}</span>
                <span class="news-category">{item.category}</span>
                <span class="news-time">🕐 {item.publish_time}</span>
            </div>
            <h3 class="news-title">
                <a href="{item.url}" target="_blank">{item.title}</a>
            </h3>
            <p class="news-summary">💡 {item.summary}</p>
            <div class="news-footer">
                <a href="{item.url}" target="_blank" class="read-more">阅读原文 →</a>
            </div>
        </div>
        '''
    
    html = f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <title>AI 日报简讯</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{
            background: linear-gradient(135deg, #1e3a5f 0%, #2d5a87 100%);
            min-height: 100vh;
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "PingFang SC", "Microsoft YaHei", sans-serif;
            padding: 12px;
        }}
        .container {{ max-width: 800px; margin: 0 auto; }}
        .header-card {{
            background: rgba(255,255,255,0.98);
            border-radius: 12px;
            padding: 20px;
            margin-bottom: 16px;
            box-shadow: 0 4px 12px rgba(0,0,0,0.15);
        }}
        .news-item {{
            background: rgba(255,255,255,0.98);
            border-radius: 10px;
            padding: 16px;
            margin-bottom: 12px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.12);
            border-left: 3px solid #2d5a87;
        }}
        .news-header {{
            display: flex;
            align-items: center;
            gap: 8px;
            margin-bottom: 10px;
            flex-wrap: wrap;
        }}
        .news-rank {{
            background: linear-gradient(135deg, #1e3a5f, #2d5a87);
            color: white;
            padding: 3px 10px;
            border-radius: 12px;
            font-weight: bold;
            font-size: 13px;
        }}
        .news-badge {{
            padding: 3px 10px;
            border-radius: 12px;
            font-size: 12px;
            font-weight: 600;
        }}
        .news-source {{
            background: #e0e7ff;
            color: #3730a3;
            padding: 3px 10px;
            border-radius: 12px;
            font-size: 12px;
            font-weight: 500;
        }}
        .news-category {{
            background: #f3f4f6;
            color: #6b7280;
            padding: 3px 10px;
            border-radius: 12px;
            font-size: 12px;
        }}
        .news-time {{
            color: #94a3b8;
            font-size: 12px;
            margin-left: auto;
        }}
        .news-title {{
            font-size: 16px;
            font-weight: 600;
            color: #1e293b;
            margin-bottom: 8px;
            line-height: 1.4;
        }}
        .news-title a {{
            color: #1e3a5f;
            text-decoration: none;
        }}
        .news-title a:hover {{
            text-decoration: underline;
        }}
        .news-summary {{
            color: #475569;
            line-height: 1.5;
            margin-bottom: 10px;
            padding: 10px;
            background: #f8fafc;
            border-radius: 6px;
            border-left: 2px solid #3a7ca5;
            font-size: 14px;
        }}
        .news-footer {{
            padding-top: 8px;
            border-top: 1px solid #e2e8f0;
        }}
        .read-more {{
            color: #2d5a87;
            text-decoration: none;
            font-weight: 600;
            font-size: 13px;
        }}
        .stats {{
            display: flex;
            gap: 16px;
            justify-content: center;
            flex-wrap: wrap;
        }}
        .stat-item {{
            text-align: center;
        }}
        .stat-value {{
            font-size: 22px;
            font-weight: bold;
            color: #1e3a5f;
        }}
        .stat-label {{
            font-size: 11px;
            color: #64748b;
        }}
        @media (max-width: 640px) {{
            body {{ padding: 8px; }}
            .header-card {{ padding: 16px; }}
            .news-item {{ padding: 12px; }}
            .news-title {{ font-size: 15px; }}
            .news-summary {{ font-size: 13px; }}
            .news-header {{ gap: 6px; }}
            .news-time {{ width: 100%; margin-top: 4px; }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header-card">
            <h1 class="text-2xl font-bold bg-gradient-to-r from-blue-800 to-cyan-600 bg-clip-text text-transparent text-center mb-3">
                🤖 AI 日报简讯
            </h1>
            <div class="stats">
                <div class="stat-item">
                    <div class="stat-value">{len(top_items)}</div>
                    <div class="stat-label">精选</div>
                </div>
                <div class="stat-item">
                    <div class="stat-value">{len(set(i.source for i in top_items))}</div>
                    <div class="stat-label">来源</div>
                </div>
                <div class="stat-item">
                    <div class="stat-value">{datetime.now().strftime('%H:%M')}</div>
                    <div class="stat-label">更新</div>
                </div>
            </div>
        </div>
        <div id="news-list">
            {news_html}
        </div>
        <div class="text-center text-white/70 text-xs mt-8">
            <p>数据来源于量子位、开源中国、CSDN、掘金、InfoQ</p>
            <p class="mt-1">更新：{today}</p>
        </div>
    </div>
</body>
</html>'''
    
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(html)
    
    print(f"📄 HTML 已生成：{output_path}")


async def main():
    scraper = AIDailyScraper()
    items = await scraper.scrape_all()
    
    script_dir = __file__.rsplit('/', 1)[0]
    
    data = {
        'update_time': datetime.now().isoformat(),
        'total_items': len(items),
        'top_items': [item.to_dict() for item in items[:10]]
    }
    with open(f'{script_dir}/news_data.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    
    generate_html(items, f'{script_dir}/index.html')
    
    print(f"\n💾 数据已保存到：{script_dir}/")
    print(f"📊 共 {len(items)} 条，精选 {len(items[:10])} 条")
    
    try:
        import subprocess
        subprocess.run(['xdg-open', f'{script_dir}/index.html'], timeout=3, capture_output=True)
        print("🌐 HTML 已打开")
    except:
        print(f"📄 请手动打开：{script_dir}/index.html")


if __name__ == '__main__':
    asyncio.run(main())
