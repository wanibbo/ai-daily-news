#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AI 日报技能 - 最终版 v8
✅ 多数据源（量子位 + 开源中国 + InfoQ + 雷锋网）
✅ 从内容提取摘要
✅ 原始发布时间
✅ 编号放大放最前，阅读原文在摘要后
✅ 摘要多行展示
✅ 紧凑布局 + 手机适配
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
    
    def to_dict(self) -> Dict:
        return asdict(self)


AI_KEYWORDS = [
    '人工智能', '大模型', 'LLM', '生成式 AI', 'AIGC', '机器学习',
    '深度学习', '神经网络', '自然语言处理', '计算机视觉', '强化学习',
    'AI 应用', 'AGI', 'transformer', 'diffusion', 'GPT', 'Claude',
    'Gemini', 'OpenAI', 'Anthropic', '智谱', '百川', '通义千问',
    '文心一言', '讯飞星火', 'Kimi', '阶跃星辰', '月之暗面', 'MiniMax',
    'Agent', '智能体', '具身智能', '机器人', '自动驾驶', '大语言模型'
]


def is_ai_related(text: str) -> bool:
    text_lower = text.lower()
    return any(kw.lower() in text_lower for kw in AI_KEYWORDS)


def calc_importance(title: str, source: str) -> int:
    score = 5
    source_weights = {'量子位': 9, '机器之心': 9, 'InfoQ': 8, '开源中国': 8, '雷锋网': 8, '钛媒体': 7}
    score = max(score, source_weights.get(source, 5))
    hot_words = ['发布', '推出', '突破', '重磅', '首次', '开源', '融资', '创业']
    for kw in hot_words:
        if kw in title:
            score += 0.5
    return min(int(score), 10)


def summarize_content(content: str, max_len: int = 150) -> str:
    """从内容生成摘要"""
    if not content:
        return "暂无详细内容，请点击阅读原文查看。"
    
    # 清理 HTML 标签和多余空格
    text = re.sub(r'\s+', ' ', content).strip()
    
    # 提取关键句
    sentences = re.split(r'[.!?。！？]', text)
    summary_parts = []
    
    for sent in sentences:
        sent = sent.strip()
        if len(sent) > 15 and len(sent) < 80:
            # 过滤无关内容
            if any(kw in sent for kw in ['广告', '关注', '公众号', '扫码', '点击']):
                continue
            summary_parts.append(sent)
            if len(' | '.join(summary_parts)) >= max_len:
                break
    
    if not summary_parts:
        return text[:max_len]
    
    return ' | '.join(summary_parts)


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
            self.session = aiohttp.ClientSession(headers=self.headers, timeout=aiohttp.ClientTimeout(total=20))
    
    async def close_session(self):
        if self.session:
            await self.session.close()
            self.session = None
    
    async def fetch_article_content(self, url: str) -> tuple[str, str]:
        """抓取文章详情页，返回（内容，发布时间）"""
        try:
            await self.init_session()
            async with self.session.get(url, allow_redirects=True) as resp:
                if resp.status != 200:
                    return "", ""
                
                html = await resp.text('utf-8', errors='ignore')
                soup = BeautifulSoup(html, 'lxml')
                
                # 提取正文内容
                content = ""
                for selector in ['article', '.content', '.post-content', '.article-content', '#content', '.entry-content', '.article-body']:
                    elem = soup.select_one(selector)
                    if elem:
                        paragraphs = elem.find_all('p')
                        texts = [p.get_text(strip=True) for p in paragraphs if len(p.get_text(strip=True)) > 20]
                        content = ' '.join(texts[:5])
                        break
                
                if not content:
                    meta_desc = soup.find('meta', attrs={'name': 'description'})
                    if meta_desc:
                        content = meta_desc.get('content', '')[:300]
                
                # 提取发布时间
                pub_time = ""
                time_patterns = [
                    r'(\d{4}-\d{2}-\d{2}\s+\d{2}:\d{2})',
                    r'(\d{4}年\d{2}月\d{2}日\s*\d{2}:\d{2})',
                    r'(\d{4}-\d{2}-\d{2})',
                    r'(\d{4}年\d{2}月\d{2}日)',
                ]
                
                for pattern in time_patterns:
                    match = re.search(pattern, html)
                    if match:
                        pub_time = match.group(1).replace('年', '-').replace('月', '-').replace('日', ' ')
                        break
                
                if not pub_time:
                    url_match = re.search(r'/(\d{4})/(\d{2})/(\d+)\.html', url)
                    if url_match:
                        pub_time = f"{url_match.group(1)}-{url_match.group(2)}-{url_match.group(3)}"
                
                return content[:500], pub_time
                
        except Exception as e:
            return "", ""
    
    async def fetch_quantumwei(self) -> List[NewsItem]:
        items = []
        print("  → 抓取 量子位...")
        
        try:
            await self.init_session()
            async with self.session.get('https://www.qbitai.com', allow_redirects=True) as resp:
                html = await resp.text('utf-8', errors='ignore')
                soup = BeautifulSoup(html, 'lxml')
                
                links = soup.select('a[href*="/2026/"], a[href*="/2025/"]')[:25]
                
                for i, link in enumerate(links):
                    href = link.get('href', '')
                    title = link.get_text(strip=True)
                    
                    if not title or len(title) < 5 or len(title) > 120:
                        continue
                    
                    match = re.search(r'/(\d{4})/(\d{2})/(\d+)\.html', href)
                    if not match:
                        continue
                    
                    url = href if href.startswith('http') else f'https://www.qbitai.com{href}'
                    
                    print(f"    [{i+1}] {title[:25]}...")
                    
                    content, pub_time = await self.fetch_article_content(url)
                    
                    if pub_time:
                        publish_time = pub_time
                    else:
                        year, month = match.group(1), match.group(2)
                        publish_time = f"{year}-{month}-{datetime.now().strftime('%d')}"
                    
                    item = NewsItem(
                        title=title,
                        source='量子位',
                        url=url,
                        publish_time=publish_time,
                        category='AI 综合',
                        summary=summarize_content(content),
                        importance_score=calc_importance(title, '量子位')
                    )
                    items.append(item)
                    
        except Exception as e:
            print(f"⚠️ 量子位：{e}")
        
        return items
    
    async def fetch_oschina(self) -> List[NewsItem]:
        items = []
        print("  → 抓取 开源中国...")
        
        try:
            await self.init_session()
            async with self.session.get('https://www.oschina.net/news/topic/ai', allow_redirects=True) as resp:
                html = await resp.text('utf-8', errors='ignore')
                soup = BeautifulSoup(html, 'lxml')
                
                for link in soup.select('.news-item .title a, .news-item a[href*="/news/"]')[:15]:
                    href = link.get('href', '')
                    title = link.get_text(strip=True)
                    
                    if not title or len(title) < 5 or len(title) > 100:
                        continue
                    if not is_ai_related(title):
                        continue
                    
                    url = href if href.startswith('http') else f'https://www.oschina.net{href}'
                    content, pub_time = await self.fetch_article_content(url)
                    
                    item = NewsItem(
                        title=title,
                        source='开源中国',
                        url=url,
                        publish_time=pub_time or datetime.now().strftime('%Y-%m-%d'),
                        category='AI 技术',
                        summary=summarize_content(content),
                        importance_score=calc_importance(title, '开源中国')
                    )
                    items.append(item)
                    
        except Exception as e:
            print(f"⚠️ 开源中国：{e}")
        
        return items
    
    async def fetch_infoq(self) -> List[NewsItem]:
        items = []
        print("  → 抓取 InfoQ...")
        
        try:
            await self.init_session()
            async with self.session.get('https://www.infoq.cn', allow_redirects=True) as resp:
                html = await resp.text('utf-8', errors='ignore')
                soup = BeautifulSoup(html, 'lxml')
                
                for link in soup.select('.article-item__title a, a[href*="/news/"], a[href*="/article/"]')[:15]:
                    href = link.get('href', '')
                    title = link.get_text(strip=True)
                    
                    if not title or len(title) < 5 or len(title) > 100:
                        continue
                    if not is_ai_related(title):
                        continue
                    
                    url = href if href.startswith('http') else f'https://www.infoq.cn{href}'
                    content, pub_time = await self.fetch_article_content(url)
                    
                    item = NewsItem(
                        title=title,
                        source='InfoQ',
                        url=url,
                        publish_time=pub_time or datetime.now().strftime('%Y-%m-%d'),
                        category='AI 技术',
                        summary=summarize_content(content),
                        importance_score=calc_importance(title, 'InfoQ')
                    )
                    items.append(item)
                    
        except Exception as e:
            print(f"⚠️ InfoQ: {e}")
        
        return items
    
    async def fetch_leiphone(self) -> List[NewsItem]:
        """抓取雷锋网"""
        items = []
        print("  → 抓取 雷锋网...")
        
        try:
            await self.init_session()
            async with self.session.get('https://www.leiphone.com', allow_redirects=True) as resp:
                html = await resp.text('utf-8', errors='ignore')
                soup = BeautifulSoup(html, 'lxml')
                
                for link in soup.select('a[href*="/news/"], a[href*="/ai/"]')[:15]:
                    href = link.get('href', '')
                    title = link.get_text(strip=True)
                    
                    if not title or len(title) < 5 or len(title) > 100:
                        continue
                    if not is_ai_related(title):
                        continue
                    
                    url = href if href.startswith('http') else f'https://www.leiphone.com{href}'
                    content, pub_time = await self.fetch_article_content(url)
                    
                    item = NewsItem(
                        title=title,
                        source='雷锋网',
                        url=url,
                        publish_time=pub_time or datetime.now().strftime('%Y-%m-%d'),
                        category='AI 产业',
                        summary=summarize_content(content),
                        importance_score=calc_importance(title, '雷锋网')
                    )
                    items.append(item)
                    
        except Exception as e:
            print(f"⚠️ 雷锋网：{e}")
        
        return items
    
    async def scrape_all(self) -> List[NewsItem]:
        print("📰 开始抓取 AI 新闻...\n")
        
        all_items = []
        
        # 抓取多个源
        tasks = [
            self.fetch_quantumwei(),
            self.fetch_oschina(),
            self.fetch_infoq(),
            self.fetch_leiphone()
        ]
        
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        source_names = ['量子位', '开源中国', 'InfoQ', '雷锋网']
        for source, items in zip(source_names, results):
            if isinstance(items, list) and items:
                print(f"  ✓ {source}: {len(items)} 条\n")
                all_items.extend(items)
            elif isinstance(items, list):
                print(f"  ✓ {source}: 0 条\n")
        
        # 去重
        seen = set()
        unique = []
        for item in all_items:
            if item.title not in seen:
                seen.add(item.title)
                unique.append(item)
        
        # 按重要性排序
        unique.sort(key=lambda x: x.importance_score, reverse=True)
        
        print(f"✅ 共抓取 {len(unique)} 条不重复新闻\n")
        
        await self.close_session()
        return unique


def generate_html(items: List[NewsItem], output_path: str):
    """生成 HTML - 编号放大放最前，阅读原文在摘要后"""
    
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
                <span class="news-number">{i}</span>
                <div class="news-meta">
                    <span class="news-badge {badge_color}">{star} {item.importance_score}</span>
                    <span class="news-source">{item.source}</span>
                    <span class="news-time">📅 {item.publish_time}</span>
                </div>
            </div>
            <h3 class="news-title">
                <a href="{item.url}" target="_blank">{item.title}</a>
            </h3>
            <p class="news-summary">{item.summary}</p>
            <div class="news-footer">
                <a href="{item.url}" target="_blank" class="read-more">阅读原文 →</a>
            </div>
        </div>
        '''
    
    html = f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AI 日报简讯</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{
            background: linear-gradient(135deg, #1e3a5f 0%, #2d5a87 100%);
            min-height: 100vh;
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "PingFang SC", "Microsoft YaHei", sans-serif;
            padding: 10px;
        }}
        .container {{ max-width: 750px; margin: 0 auto; }}
        .header-card {{
            background: rgba(255,255,255,0.98);
            border-radius: 12px;
            padding: 18px;
            margin-bottom: 14px;
            box-shadow: 0 4px 12px rgba(0,0,0,0.15);
        }}
        .news-item {{
            background: rgba(255,255,255,0.98);
            border-radius: 10px;
            padding: 14px;
            margin-bottom: 10px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.12);
            border-left: 3px solid #2d5a87;
        }}
        .news-header {{
            display: flex;
            align-items: center;
            gap: 10px;
            margin-bottom: 8px;
        }}
        .news-number {{
            background: linear-gradient(135deg, #1e3a5f, #2d5a87);
            color: white;
            width: 36px;
            height: 36px;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            font-weight: bold;
            font-size: 18px;
            flex-shrink: 0;
        }}
        .news-meta {{
            display: flex;
            align-items: center;
            gap: 8px;
            flex-wrap: wrap;
            flex: 1;
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
        .news-summary {{
            color: #475569;
            line-height: 1.6;
            margin-bottom: 10px;
            padding: 10px;
            background: #f8fafc;
            border-radius: 6px;
            border-left: 2px solid #3a7ca5;
            font-size: 14px;
            white-space: pre-wrap;
            word-wrap: break-word;
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
        .stat-item {{ text-align: center; }}
        .stat-value {{ font-size: 22px; font-weight: bold; color: #1e3a5f; }}
        .stat-label {{ font-size: 11px; color: #64748b; }}
        @media (max-width: 640px) {{
            body {{ padding: 6px; }}
            .header-card {{ padding: 14px; }}
            .news-item {{ padding: 12px; }}
            .news-number {{ width: 32px; height: 32px; font-size: 16px; }}
            .news-title {{ font-size: 15px; }}
            .news-summary {{ font-size: 13px; }}
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
        <div id="news-list">{news_html}</div>
        <div class="text-center text-white/70 text-xs mt-8">
            <p>数据来源于量子位、开源中国、InfoQ、雷锋网</p>
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
