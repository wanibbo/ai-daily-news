#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AI 日报新闻抓取技能
自动从主流媒体获取 AI 相关最新技术/应用进展，生成日报简讯
"""

import json
import asyncio
import aiohttp
from datetime import datetime, timedelta
from bs4 import BeautifulSoup
from typing import List, Dict, Optional
from dataclasses import dataclass, asdict, field
import re
import os


@dataclass
class NewsItem:
    """新闻条目数据结构"""
    title: str
    source: str
    url: str
    publish_time: str
    category: str
    content: str = ""
    summary: str = ""
    importance_score: int = 5
    keywords: List[str] = field(default_factory=list)
    
    def to_dict(self) -> Dict:
        return asdict(self)


class AIDailyNewsSkill:
    """AI 日报新闻抓取技能"""
    
    def __init__(self, config_path: str = None):
        self.script_dir = os.path.dirname(os.path.abspath(__file__))
        config_path = config_path or os.path.join(self.script_dir, 'skill.json')
        
        with open(config_path, 'r', encoding='utf-8') as f:
            self.config = json.load(f)
        
        self.sources = self.config.get('config', {}).get('sources', [])
        self.keywords = self.config.get('config', {}).get('keywords', [])
        self.output_config = self.config.get('config', {}).get('output', {})
        self.session = None
    
    async def init_session(self):
        """初始化 HTTP 会话"""
        if self.session is None:
            self.session = aiohttp.ClientSession(
                headers={
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
                },
                timeout=aiohttp.ClientTimeout(total=15)
            )
    
    async def close_session(self):
        """关闭 HTTP 会话"""
        if self.session:
            await self.session.close()
            self.session = None
    
    def _is_ai_related(self, text: str) -> bool:
        """判断内容是否与 AI 相关"""
        text_lower = text.lower()
        for keyword in self.keywords:
            if keyword.lower() in text_lower:
                return True
        return False
    
    def _calculate_importance(self, item: NewsItem) -> int:
        """计算新闻重要性分数 (1-10)"""
        score = 5  # 基础分
        
        # 来源权重
        source_weights = {
            '量子位': 8,
            '机器之心': 8,
            '36Kr AI': 7,
            'InfoQ AI': 7,
        }
        score = max(score, source_weights.get(item.source, 5))
        
        # 标题关键词加分
        hot_keywords = ['GPT', 'Claude', 'Gemini', '发布', '推出', '突破', '重磅', '首次', '开源', '黄仁勋', 'AGI']
        for kw in hot_keywords:
            if kw in item.title:
                score += 1
        
        # 时效性加分（24 小时内）
        try:
            pub_time = datetime.strptime(item.publish_time, '%Y-%m-%d')
            if datetime.now() - pub_time < timedelta(hours=24):
                score += 1
        except:
            pass
        
        return min(score, 10)
    
    async def fetch_source(self, source: Dict) -> List[NewsItem]:
        """抓取单个源"""
        items = []
        
        try:
            await self.init_session()
            async with self.session.get(source['url'], allow_redirects=True) as response:
                if response.status != 200:
                    print(f"⚠️ {source['name']} 访问失败：HTTP {response.status}")
                    return items
                
                html = await response.text('utf-8', errors='ignore')
                soup = BeautifulSoup(html, 'lxml')
                
                # 尝试找标题链接
                selector = source.get('selector', 'h2 a, h3 a')
                links = soup.select(selector, limit=15)
                
                for link in links:
                    title = link.get_text(strip=True)
                    if len(title) < 8 or len(title) > 80:
                        continue
                    
                    # AI 相关过滤
                    if not self._is_ai_related(title):
                        continue
                    
                    # 获取 URL
                    url = link.get('href', '')
                    if url and not url.startswith('http'):
                        base_url = source['url'].rsplit('/', 1)[0]
                        url = base_url + url if url.startswith('/') else source['url']
                    
                    if not url:
                        url = source['url']
                    
                    item = NewsItem(
                        title=title,
                        source=source['name'],
                        url=url,
                        publish_time=datetime.now().strftime('%Y-%m-%d'),
                        category=source.get('category', 'AI 综合')
                    )
                    item.importance_score = self._calculate_importance(item)
                    items.append(item)
                    
        except Exception as e:
            print(f"⚠️ {source['name']} 抓取失败：{e}")
        
        return items
    
    async def scrape_all(self) -> List[NewsItem]:
        """抓取所有源"""
        print("📰 开始抓取 AI 新闻...")
        
        all_items = []
        
        for source in self.sources:
            print(f"  → 抓取 {source['name']}...")
            items = await self.fetch_source(source)
            if items:
                print(f"     找到 {len(items)} 条 AI 相关新闻")
            all_items.extend(items)
        
        # 去重（基于标题）
        seen = set()
        unique_items = []
        for item in all_items:
            if item.title not in seen:
                seen.add(item.title)
                unique_items.append(item)
        
        # 按重要性排序
        unique_items.sort(key=lambda x: x.importance_score, reverse=True)
        
        print(f"\n✅ 共抓取 {len(unique_items)} 条不重复新闻")
        
        await self.close_session()
        return unique_items
    
    def generate_summary(self, items: List[NewsItem], limit: int = 10) -> str:
        """生成文本格式的日报摘要"""
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
            lines.append(f"   来源：{item.source} | 分类：{item.category}")
            lines.append(f"   链接：{item.url}")
            lines.append("")
        
        lines.append("=" * 60)
        lines.append("数据来源于各大主流媒体 · 由 AI 自动整理")
        
        return "\n".join(lines)
    
    async def fetch_and_save(self, output_path: str = None, limit: int = 10) -> List[NewsItem]:
        """抓取并保存数据"""
        items = await self.scrape_all()
        top_items = items[:limit]
        
        if output_path is None:
            output_path = os.path.join(self.script_dir, 'news_data.json')
        
        data = {
            'update_time': datetime.now().isoformat(),
            'total_items': len(items),
            'top_items': [item.to_dict() for item in top_items]
        }
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        
        print(f"\n💾 数据已保存到：{output_path}")
        
        return top_items
    
    async def run(self) -> str:
        """运行技能，返回日报文本"""
        try:
            items = await self.fetch_and_save()
            summary = self.generate_summary(items)
            return summary
        except Exception as e:
            return f"❌ 抓取失败：{e}"


async def main():
    """主函数"""
    skill = AIDailyNewsSkill()
    result = await skill.run()
    print("\n" + result)


if __name__ == '__main__':
    asyncio.run(main())
