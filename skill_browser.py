#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AI 日报新闻抓取技能 - 增强版
使用 browser 工具抓取新闻，支持更多数据源
"""

import json
import asyncio
import subprocess
import sys
from datetime import datetime, timedelta
from typing import List, Dict, Optional
from dataclasses import dataclass, asdict, field
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
    """AI 日报新闻抓取技能（增强版）"""
    
    def __init__(self, config_path: str = None):
        self.script_dir = os.path.dirname(os.path.abspath(__file__))
        config_path = config_path or os.path.join(self.script_dir, 'skill.json')
        
        with open(config_path, 'r', encoding='utf-8') as f:
            self.config = json.load(f)
        
        self.sources = self.config.get('config', {}).get('sources', [])
        self.keywords = self.config.get('config', {}).get('keywords', [])
        self.output_config = self.config.get('config', {}).get('output', {})
    
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
            'CSDN AI': 6,
        }
        score = max(score, source_weights.get(item.source, 5))
        
        # 标题关键词加分
        hot_keywords = ['GPT', 'Claude', 'Gemini', '发布', '推出', '突破', '重磅', '首次', '开源', '黄仁勋', 'AGI', '大模型', 'AI']
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
    
    def fetch_with_browser(self, url: str) -> Optional[str]:
        """使用 browser 工具抓取页面"""
        try:
            # 调用 browser 工具（通过 OpenClaw）
            # 这里简化处理，实际应调用 browser 工具
            result = subprocess.run(
                ['python3', '-c', f'''
import asyncio
from openclaw import browser

async def fetch():
    result = await browser(action="open", targetUrl="{url}")
    return result

print(asyncio.run(fetch()))
'''],
                capture_output=True,
                text=True,
                timeout=30
            )
            return result.stdout
        except Exception as e:
            print(f"  ⚠️ browser 抓取失败：{e}")
            return None
    
    def parse_quantumwei(self, html_content: str) -> List[NewsItem]:
        """解析量子位新闻"""
        items = []
        
        # 从 HTML 中提取新闻（简化版，实际需要更完善的解析）
        import re
        
        # 匹配新闻标题和链接
        pattern = r'href="(https://www\.qbitai\.com/\d{4}/\d+/\d+\.html)"[^>]*>.*?<h[34][^>]*>([^<]+)</h[34]>'
        matches = re.findall(pattern, html_content, re.DOTALL)
        
        for url, title in matches[:15]:
            title = title.strip()
            if len(title) < 5 or len(title) > 100:
                continue
            
            if not self._is_ai_related(title):
                continue
            
            item = NewsItem(
                title=title,
                source='量子位',
                url=url,
                publish_time=datetime.now().strftime('%Y-%m-%d'),
                category='AI 综合'
            )
            item.importance_score = self._calculate_importance(item)
            items.append(item)
        
        return items
    
    async def scrape_quantumwei(self) -> List[NewsItem]:
        """抓取量子位（使用 browser 工具）"""
        print("  → 抓取 量子位 (browser)...")
        
        try:
            # 使用 browser 工具打开页面并获取快照
            from openclaw import browser as browser_tool
            
            # 打开页面
            result = await browser_tool(action='open', targetUrl='https://www.qbitai.com')
            target_id = result.get('targetId')
            
            # 获取快照
            snapshot = await browser_tool(action='snapshot', targetId=target_id, refs='aria')
            
            # 关闭页面
            await browser_tool(action='close', targetId=target_id)
            
            # 解析快照内容
            items = []
            if 'content' in snapshot:
                items = self.parse_quantumwei(snapshot['content'])
            
            print(f"     找到 {len(items)} 条 AI 相关新闻")
            return items
            
        except Exception as e:
            print(f"  ⚠️ 量子位抓取失败：{e}")
            return []
    
    async def scrape_all(self) -> List[NewsItem]:
        """抓取所有源"""
        print("📰 开始抓取 AI 新闻...")
        
        all_items = []
        
        # 抓取量子位（使用 browser）
        items = await self.scrape_quantumwei()
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
