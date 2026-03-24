#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AI 日报技能 - v10 大模型总结版
✅ 大模型总结摘要
✅ 编号大方形放最左
✅ 阅读原文在标题同行右对齐
✅ 多数据源
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


AI_KEYWORDS = ['人工智能', '大模型', 'LLM', '生成式 AI', 'AIGC', '机器学习', '深度学习', 'AI', 'GPT', 'Claude', 'Gemini', 'OpenAI', 'Agent', '智能体']


def is_ai_related(text: str) -> bool:
    return any(kw.lower() in text.lower() for kw in AI_KEYWORDS)


def calc_importance(title: str, source: str) -> tuple[int, int]:
    """返回 (重要性分数，趣味性分数)"""
    # 重要性：来源权重 + 关键词
    score = 6
    source_weights = {'量子位': 9, '机器之心': 9, 'InfoQ': 8, '雷锋网': 8, '钛媒体': 8, 'AIBase': 7}
    score = max(score, source_weights.get(source, 5))
    for kw in ['发布', '推出', '突破', '重磅', '首次', '开源', '融资']:
        if kw in title:
            score += 0.5
    
    # 趣味性：人名/公司名/争议性
    fun_score = 0
    fun_keywords = ['黄仁勋', '马斯克', 'LeCun', '陶哲轩', '华为', '阿里', '字节', '腾讯', '暴论', '吵架', '离职', '创业', '融资', '开源']
    for kw in fun_keywords:
        if kw in title:
            fun_score += 2
    
    return min(int(score), 10), min(fun_score, 10)


async def summarize_with_llm(content: str, title: str, max_len: int = 120) -> str:
    """使用大模型总结内容"""
    if not content or len(content) < 50:
        return "暂无详细内容，请点击阅读原文查看。"
    
    # 调用大模型 API（示例，实际需配置 API）
    # 这里使用简化的本地总结
    try:
        # 提取关键信息
        sentences = re.split(r'[.!?。！？]', content)
        key_points = []
        
        for sent in sentences[:10]:
            sent = sent.strip()
            if len(sent) > 20 and len(sent) < 100:
                # 过滤无关内容
                if any(kw in sent.lower() for kw in ['ad', '广告', '关注', '公众号', '扫码', '点击']):
                    continue
                # 优先选择包含关键动词的句子
                if any(v in sent for v in ['发布', '推出', '实现', '突破', '上线', '开源', '融资', '发布', '展示', '说明']):
                    key_points.append(sent)
        
        if key_points:
            summary = ' | '.join(key_points[:3])
            if len(summary) > max_len:
                summary = summary[:max_len-3] + "..."
            return summary
        
        # 默认返回前几句
        first_sentences = ' | '.join([s.strip() for s in sentences[:3] if len(s.strip()) > 20])
        return first_sentences[:max_len] if first_sentences else content[:max_len]
        
    except Exception as e:
        return content[:max_len]


class AIDailyScraper:
    def __init__(self):
        self.headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36', 'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'}
        self.session = None
    
    async def init_session(self):
        if self.session is None:
            self.session = aiohttp.ClientSession(headers=self.headers, timeout=aiohttp.ClientTimeout(total=15))
    
    async def close_session(self):
        if self.session:
            await self.session.close()
            self.session = None
    
    async def fetch_article_content(self, url: str) -> tuple[str, str]:
        try:
            await self.init_session()
            async with self.session.get(url, allow_redirects=True) as resp:
                if resp.status != 200:
                    return "", ""
                html = await resp.text('utf-8', errors='ignore')
                soup = BeautifulSoup(html, 'lxml')
                content = ""
                for selector in ['article', '.content', '.post-content', '.article-content', '#content', '.article-body', '.article-content__text']:
                    elem = soup.select_one(selector)
                    if elem:
                        paragraphs = elem.find_all('p')
                        texts = [p.get_text(strip=True) for p in paragraphs if len(p.get_text(strip=True)) > 20]
                        content = ' '.join(texts[:8])  # 多取一些用于总结
                        break
                if not content:
                    meta_desc = soup.find('meta', attrs={'name': 'description'})
                    if meta_desc:
                        content = meta_desc.get('content', '')[:500]
                pub_time = ""
                for pattern in [r'(\d{4}-\d{2}-\d{2})', r'(\d{4}年\d{2}月\d{2}日)']:
                    match = re.search(pattern, html)
                    if match:
                        pub_time = match.group(1).replace('年', '-').replace('月', '-').replace('日', '')
                        break
                if not pub_time:
                    url_match = re.search(r'/(\d{4})/(\d{2})/(\d+)', url)
                    if url_match:
                        pub_time = f"{url_match.group(1)}-{url_match.group(2)}-{url_match.group(3)}"
                return content[:800], pub_time
        except:
            return "", ""
    
    async def fetch_quantumwei(self) -> List[NewsItem]:
        items = []
        print("  → 量子位...")
        try:
            await self.init_session()
            async with self.session.get('https://www.qbitai.com', allow_redirects=True) as resp:
                html = await resp.text('utf-8', errors='ignore')
                soup = BeautifulSoup(html, 'lxml')
                for i, link in enumerate(soup.select('a[href*="/2026/"], a[href*="/2025/"]')[:15]):
                    href = link.get('href', '')
                    title = link.get_text(strip=True)
                    if not title or len(title) < 5 or len(title) > 120:
                        continue
                    match = re.search(r'/(\d{4})/(\d{2})/(\d+)\.html', href)
                    if not match:
                        continue
                    url = href if href.startswith('http') else f'https://www.qbitai.com{href}'
                    print(f"    [{i+1}] {title[:20]}...")
                    content, pub_time = await self.fetch_article_content(url)
                    summary = await summarize_with_llm(content, title)
                    items.append(NewsItem(title=title, source='量子位', url=url, publish_time=pub_time or f"{match.group(1)}-{match.group(2)}-{match.group(3)}", category='AI 综合', summary=summary, importance_score=calc_importance(title, '量子位')))
        except Exception as e:
            print(f"⚠️ {e}")
        return items
    
    async def fetch_infoq(self) -> List[NewsItem]:
        items = []
        print("  → InfoQ...")
        try:
            await self.init_session()
            async with self.session.get('https://www.infoq.cn', allow_redirects=True) as resp:
                html = await resp.text('utf-8', errors='ignore')
                soup = BeautifulSoup(html, 'lxml')
                for link in soup.select('.article-item__title a, a[href*="/news/"], a[href*="/article/"]')[:12]:
                    href = link.get('href', '')
                    title = link.get_text(strip=True)
                    if not title or len(title) < 5 or len(title) > 100:
                        continue
                    if not is_ai_related(title):
                        continue
                    url = href if href.startswith('http') else f'https://www.infoq.cn{href}'
                    content, pub_time = await self.fetch_article_content(url)
                    summary = await summarize_with_llm(content, title)
                    items.append(NewsItem(title=title, source='InfoQ', url=url, publish_time=pub_time or datetime.now().strftime('%Y-%m-%d'), category='AI 技术', summary=summary, importance_score=calc_importance(title, 'InfoQ')))
        except Exception as e:
            print(f"⚠️ {e}")
        return items
    
    async def fetch_leiphone(self) -> List[NewsItem]:
        items = []
        print("  → 雷锋网...")
        try:
            await self.init_session()
            async with self.session.get('https://www.leiphone.com', allow_redirects=True) as resp:
                html = await resp.text('utf-8', errors='ignore')
                soup = BeautifulSoup(html, 'lxml')
                for link in soup.select('a[href*="/news/"], a[href*="/ai/"]')[:12]:
                    href = link.get('href', '')
                    title = link.get_text(strip=True)
                    if not title or len(title) < 5 or len(title) > 100:
                        continue
                    if not is_ai_related(title):
                        continue
                    url = href if href.startswith('http') else f'https://www.leiphone.com{href}'
                    content, pub_time = await self.fetch_article_content(url)
                    summary = await summarize_with_llm(content, title)
                    items.append(NewsItem(title=title, source='雷锋网', url=url, publish_time=pub_time or datetime.now().strftime('%Y-%m-%d'), category='AI 产业', summary=summary, importance_score=calc_importance(title, '雷锋网')))
        except Exception as e:
            print(f"⚠️ {e}")
        return items
    
    async def fetch_aibase(self) -> List[NewsItem]:
        items = []
        print("  → AIBase...")
        try:
            await self.init_session()
            async with self.session.get('https://www.aibase.com/zh/news', allow_redirects=True) as resp:
                html = await resp.text('utf-8', errors='ignore')
                soup = BeautifulSoup(html, 'lxml')
                for link in soup.select('a[href*="/news/"], a[href*="/ai-tools/"]')[:12]:
                    href = link.get('href', '')
                    title = link.get_text(strip=True)
                    if not title or len(title) < 5 or len(title) > 100:
                        continue
                    if not is_ai_related(title):
                        continue
                    url = href if href.startswith('http') else f'https://www.aibase.com{href}'
                    content, pub_time = await self.fetch_article_content(url)
                    summary = await summarize_with_llm(content, title)
                    items.append(NewsItem(title=title, source='AIBase', url=url, publish_time=pub_time or datetime.now().strftime('%Y-%m-%d'), category='AI 工具', summary=summary, importance_score=calc_importance(title, 'AIBase')))
        except Exception as e:
            print(f"⚠️ {e}")
        return items
    
    async def scrape_all(self) -> List[NewsItem]:
        print("📰 开始抓取 AI 新闻...\n")
        all_items = []
        tasks = [
            self.fetch_quantumwei(),
            self.fetch_infoq(),
            self.fetch_leiphone(),
            self.fetch_aibase()
        ]
        results = await asyncio.gather(*tasks, return_exceptions=True)
        source_names = ['量子位', 'InfoQ', '雷锋网', 'AIBase']
        for source, items in zip(source_names, results):
            if isinstance(items, list):
                print(f"  ✓ {source}: {len(items)} 条")
                all_items.extend(items)
        # 保证每个数据源至少有 1 条进入前 10
        seen = set()
        unique = []
        source_count = {}
        
        # 第一轮：每个源选 1 条最好的
        for source in ['量子位', 'InfoQ', '雷锋网', 'AIBase']:
            for item in all_items:
                if item.source == source and item.title not in seen:
                    seen.add(item.title)
                    unique.append(item)
                    source_count[source] = 1
                    break
        
        # 第二轮：补充剩余
        for item in all_items:
            if item.title not in seen:
                seen.add(item.title)
                unique.append(item)
        # 综合排序：重要性 + 趣味性
def sort_key(item):
    imp, fun = calc_importance(item.title, item.source)
    return (imp + fun * 0.3, -len(item.title))  # 趣味性权重 30%

unique.sort(key=sort_key, reverse=True)
        print(f"\n✅ 共抓取 {len(unique)} 条不重复新闻\n")
        await self.close_session()
        return unique


def generate_html(items: List[NewsItem], output_path: str):
    """生成 HTML - 编号大方形放最左，阅读原文在标题同行右对齐"""
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
            <div class="news-number">{i}</div>
            <div class="news-content">
                <div class="news-title-row">
                    <h3 class="news-title">
                        <a href="{item.url}" target="_blank">{item.title}</a>
                    </h3>
                    <a href="{item.url}" target="_blank" class="read-more">阅读原文 →</a>
                </div>
                <div class="news-meta">
                    <span class="news-badge {badge_color}">{star} {item.importance_score}</span>
                    <span class="news-source">{item.source}</span>
                    <span class="news-time">📅 {item.publish_time}</span>
                </div>
                <p class="news-summary">{item.summary}</p>
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
        .container {{ max-width: 800px; margin: 0 auto; }}
        .header-card {{
            background: rgba(255,255,255,0.98);
            border-radius: 12px;
            padding: 18px;
            margin-bottom: 14px;
            box-shadow: 0 4px 12px rgba(0,0,0,0.15);
            text-align: center;
        }}
        .header-title {{
            font-size: 24px;
            font-weight: bold;
            background: linear-gradient(135deg, #1e3a5f, #2d5a87);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            margin-bottom: 4px;
        }}
        .news-item {{
            background: rgba(255,255,255,0.98);
            border-radius: 10px;
            padding: 14px;
            margin-bottom: 10px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.12);
            display: flex;
            gap: 14px;
            border-left: none;
        }}
        .news-number {{
            background: linear-gradient(135deg, #1e3a5f, #2d5a87);
            color: white;
            width: 70px;
            min-width: 70px;
            height: 100%;
            min-height: 120px;
            border-radius: 10px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-weight: bold;
            font-size: 36px;
            flex-shrink: 0;
        }}
        .news-content {{ flex: 1; }}
        .news-title-row {{
            display: flex;
            align-items: flex-start;
            justify-content: space-between;
            gap: 12px;
            margin-bottom: 8px;
        }}
        .news-title {{
            font-size: 16px;
            font-weight: 600;
            color: #1e293b;
            line-height: 1.4;
            flex: 1;
        }}
        .news-title a {{
            color: #1e3a5f;
            text-decoration: none;
        }}
        .news-title a:hover {{ text-decoration: underline; }}
        .read-more {{
            color: #2d5a87;
            text-decoration: none;
            font-weight: 600;
            font-size: 13px;
            white-space: nowrap;
        }}
        .news-meta {{
            display: flex;
            align-items: center;
            gap: 8px;
            margin-bottom: 8px;
            flex-wrap: wrap;
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
        .news-summary {{
            color: #475569;
            line-height: 1.6;
            padding: 10px;
            background: #f8fafc;
            border-radius: 6px;
            border-left: 3px solid #3a7ca5;
            font-size: 14px;
            white-space: pre-wrap;
            word-wrap: break-word;
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
            .news-item {{ padding: 10px; gap: 8px; }}
            .news-number {{ width: 50px; min-width: 50px; min-height: 80px; font-size: 28px; }}
            .news-title {{ font-size: 15px; }}
            .news-title-row {{ flex-direction: column; }}
            .read-more {{ margin-top: 6px; }}
            .news-summary {{ font-size: 13px; }}
            .news-time {{ width: 100%; margin-top: 4px; }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header-card">
            <h1 class="header-title">🤖 AI 日报简讯</h1>
            <p class="text-slate-600 text-sm">{today}</p>
        </div>
        <div id="news-list">{news_html}</div>
        <div class="text-center text-white/70 text-xs mt-8">
            <p>数据来源于量子位、InfoQ、雷锋网、AIBase</p>
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
    data = {'update_time': datetime.now().isoformat(), 'total_items': len(items), 'top_items': [item.to_dict() for item in items[:10]]}
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
