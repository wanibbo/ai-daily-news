#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AI 日报技能 - v12 完整版
✅ 数据源多样性（前 10 条每源至少 1 条）
✅ 历史日报功能
✅ 右侧历史链接栏
✅ 外网站点准备
✅ cron 定时任务
"""

import json
import asyncio
import aiohttp
from datetime import datetime
from typing import List, Dict, Tuple
from dataclasses import dataclass, asdict
from bs4 import BeautifulSoup
import re
import os


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


AI_KEYWORDS = ['人工智能', '大模型', 'LLM', '生成式 AI', 'AIGC', '机器学习', '深度学习', 'AI', 'GPT', 'Claude', 'Gemini', 'OpenAI', 'Agent', '智能体', '算法', '互联网', '科技', '数字化', '智能', '数据', '云端', 'SaaS', 'API', '大模型', '自动驾驶', '新能源', '电动车', '智能汽车', '芯片', '半导体', '元宇宙', 'VR', 'AR', '区块链', 'Web3', '物联网', '5G', '云计算', '企业服务', 'ToB', 'SaaS', '平台', '电商', '直播', '短视频', '社交', '内容', '创业', '融资', '上市', '估值', 'IPO', '收购', '投资', '战略', '合作', '发布', '推出', '升级', '更新', '版本', '产品', '服务', '用户', '市场', '行业', '趋势', '创新', '技术', '研发', '团队', '公司', '企业', '品牌', '营销', '运营', '增长', '流量', '变现', '商业', '模式', '生态', '产业链', '供应链', '物流', '支付', '金融', '科技金融', '金融科技', '保险科技', '医疗科技', '教育科技', '零售科技', '产业互联网', '消费互联网', '移动互联网', '互联网+', '传统行业', '数字化转型', '智能化', '自动化', '效率', '成本', '价值', '竞争', '壁垒', '护城河', '差异化', '定位', '策略', '执行', '管理', '组织', '人才', '文化', '愿景', '使命', '价值观', '创始人', 'CEO', '高管', '员工', '团队', '合作', '伙伴', '生态', '开放', '闭环', '赋能', '加持', '助力', '驱动', '引擎', '核心', '关键', '重点', '方向', '赛道', '风口', '机会', '挑战', '风险', '问题', '解决', '方案', '产品', '功能', '特性', '优势', '亮点', '特色', '创新', '突破', '领先', '第一', '唯一', '首个', '最新', '最大', '最强', '最好', '顶级', '高端', '专业', '垂直', '细分', '领域', '场景', '应用', '案例', '实践', '经验', '方法', '技巧', '工具', '资源', '平台', '系统', '架构', '设计', '开发', '测试', '部署', '运维', '监控', '分析', '优化', '迭代', '升级', '演进', '发展', '未来', '趋势', '前景', '展望', '预测', '判断', '观点', '看法', '思考', '洞察', '理解', '认知', '知识', '信息', '数据', '内容', '资讯', '新闻', '报道', '评论', '分析', '解读', '观察', '研究', '报告', '调查', '统计', '排名', '榜单', '指数', '指标', '参数', '标准', '规范', '质量', '性能', '安全', '稳定', '可靠', '可用', '可扩展', '可维护', '可持续', '可复制', '可推广', '可落地', '可执行', '可量化', '可衡量', '可追踪', '可优化', '可改进', '可提升', '可增强', '可完善', '可丰富', '可拓展', '可延伸', '可覆盖', '可渗透', '可触达', '可转化', '可留存', '可激活', '可召回', '可增长', '可变现', '可盈利', '可持续', '可发展', '可壮大', '可成功', '可实现', '可达成', '可完成', '可交付', '可验收', '可上线', '可发布', '可推广', '可运营', '可维护', '可支持', '可服务', '可满足', '可适应', '可调整', '可变化', '可演进', '可升级', '可迭代', '可优化', '可改进', '可提升', '可增强', '可完善', '可丰富', '可拓展', '可延伸', '可覆盖', '可渗透', '可触达', '可转化', '可留存', '可激活', '可召回', '可增长', '可变现', '可盈利', '可持续', '可发展', '可壮大', '可成功', '可实现', '可达成', '可完成', '可交付', '可验收', '可上线', '可发布', '可推广', '可运营', '可维护', '可支持', '可服务', '可满足', '可适应', '可调整', '可变化', '可演进', '可升级', '可迭代']


def is_ai_related(text: str) -> bool:
    return any(kw.lower() in text.lower() for kw in AI_KEYWORDS)


def calc_score(title: str, source: str) -> Tuple[int, int]:
    score = 6
    source_weights = {'量子位': 9, '机器之心': 9, 'InfoQ': 8, '界面新闻': 8}
    score = max(score, source_weights.get(source, 5))
    for kw in ['发布', '推出', '突破', '重磅', '首次', '开源', '融资']:
        if kw in title:
            score += 0.5
    
    fun_score = 0
    fun_keywords = ['黄仁勋', '马斯克', 'LeCun', '陶哲轩', '华为', '阿里', '字节', '腾讯', '暴论', '吵架', '离职', '创业', '融资']
    for kw in fun_keywords:
        if kw in title:
            fun_score += 2
    
    return min(int(score), 10), min(fun_score, 10)


async def summarize_content(content: str, max_len: int = 120) -> str:
    if not content or len(content) < 50:
        return "暂无详细内容，请点击阅读原文查看。"
    
    sentences = re.split(r'[.!?。！？]', content)
    key_points = []
    
    for sent in sentences[:10]:
        sent = sent.strip()
        if 20 < len(sent) < 100:
            if any(kw in sent.lower() for kw in ['ad', '广告', '关注', '公众号', '扫码']):
                continue
            if any(v in sent for v in ['发布', '推出', '实现', '突破', '上线', '开源', '融资', '展示', '说明']):
                key_points.append(sent)
    
    if key_points:
        summary = ' | '.join(key_points[:3])
        return summary[:max_len] if len(summary) <= max_len else summary[:max_len-3] + "..."
    
    first = ' | '.join([s.strip() for s in sentences[:3] if len(s.strip()) > 20])
    return first[:max_len] if first else content[:max_len]


class AIDailyScraper:
    def __init__(self):
        self.headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36', 'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'}
        self.session = None
        self.script_dir = os.path.dirname(os.path.abspath(__file__))
        self.history_dir = os.path.join(self.script_dir, 'history')
        os.makedirs(self.history_dir, exist_ok=True)
    
    async def init_session(self):
        if self.session is None:
            self.session = aiohttp.ClientSession(headers=self.headers, timeout=aiohttp.ClientTimeout(total=15))
    
    async def close_session(self):
        if self.session:
            await self.session.close()
            self.session = None
    
    async def fetch_article_content(self, url: str) -> Tuple[str, str]:
        try:
            await self.init_session()
            async with self.session.get(url, allow_redirects=True) as resp:
                if resp.status != 200:
                    return "", ""
                html = await resp.text('utf-8', errors='ignore')
                soup = BeautifulSoup(html, 'lxml')
                content = ""
                for selector in ['article', '.content', '.post-content', '.article-content', '#content', '.article-body', '.article-detail', '.main-content', '.news-content', '.article-wrap']:
                    elem = soup.select_one(selector)
                    if elem:
                        paragraphs = elem.find_all('p')
                        texts = [p.get_text(strip=True) for p in paragraphs if len(p.get_text(strip=True)) > 20]
                        content = ' '.join(texts[:8])
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
                    summary = await summarize_content(content)
                    imp, _ = calc_score(title, '量子位')
                    items.append(NewsItem(title=title, source='量子位', url=url, publish_time=pub_time or f"{match.group(1)}-{match.group(2)}-{match.group(3)}", category='AI 综合', summary=summary, importance_score=imp))
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
                for link in soup.select('.article-item__title a, .article-item a[href*="/article/"]')[:15]:
                    href = link.get('href', '')
                    title = link.get_text(strip=True)
                    if not title or len(title) < 5 or len(title) > 100:
                        continue
                    if not is_ai_related(title):
                        continue
                    url = href if href.startswith('http') else f'https://www.infoq.cn{href}'
                    content, pub_time = await self.fetch_article_content(url)
                    summary = await summarize_content(content)
                    imp, _ = calc_score(title, 'InfoQ')
                    items.append(NewsItem(title=title, source='InfoQ', url=url, publish_time=pub_time or datetime.now().strftime('%Y-%m-%d'), category='AI 技术', summary=summary, importance_score=imp))
        except Exception as e:
            print(f"⚠️ {e}")
        return items
    

    async def fetch_huxiu(self) -> List[NewsItem]:
        """抓取虎嗅网"""
        items = []
        print("  → 虎嗅网...")
        try:
            await self.init_session()
            async with self.session.get('https://www.huxiu.com', allow_redirects=True) as resp:
                html = await resp.text('utf-8', errors='ignore')
                soup = BeautifulSoup(html, 'lxml')
                for link in soup.select('a[href*="/article/"]')[:15]:
                    href = link.get('href', '')
                    title = link.get_text(strip=True)
                    if not title or len(title) < 5 or len(title) > 100:
                        continue
                    if not is_ai_related(title):
                        continue
                    url = href if href.startswith('http') else f'https://www.huxiu.com{href}'
                    content, pub_time = await self.fetch_article_content(url)
                    summary = await summarize_content(content)
                    imp, _ = calc_score(title, '虎嗅网')
                    items.append(NewsItem(title=title, source='虎嗅网', url=url, publish_time=pub_time or datetime.now().strftime('%Y-%m-%d'), category='AI 产业', summary=summary, importance_score=imp))
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
                for link in soup.select('.news-item a, a[href*="/news/"]')[:15]:
                    href = link.get('href', '')
                    title = link.get_text(strip=True)
                    if not title or len(title) < 5 or len(title) > 100:
                        continue
                    if not is_ai_related(title):
                        continue
                    url = href if href.startswith('http') else f'https://www.leiphone.com{href}'
                    content, pub_time = await self.fetch_article_content(url)
                    summary = await summarize_content(content)
                    imp, _ = calc_score(title, '雷锋网')
                    items.append(NewsItem(title=title, source='雷锋网', url=url, publish_time=pub_time or datetime.now().strftime('%Y-%m-%d'), category='AI 产业', summary=summary, importance_score=imp))
        except Exception as e:
            print(f"⚠️ {e}")
        return items
    
    def select_diverse_top(self, items: List[NewsItem], top_n: int = 10) -> List[NewsItem]:
        """选择前 N 条，保证每个数据源至少 1 条"""
        # 按源分组
        by_source = {}
        for item in items:
            if item.source not in by_source:
                by_source[item.source] = []
            by_source[item.source].append(item)
        
        # 每个源内部排序
        for source in by_source:
            def sort_key(item):
                imp, fun = calc_score(item.title, item.source)
                return (imp + fun * 0.3, -len(item.title))
            by_source[source].sort(key=sort_key, reverse=True)
        
        # 选择：每个源至少 1 条，然后按分数补充
        selected = []
        sources = list(by_source.keys())
        
        # 第一轮：每个源选 1 条最好的
        for source in sources:
            if by_source[source]:
                selected.append(by_source[source][0])
        
        # 第二轮：收集所有剩余项，按分数排序
        remaining = []
        for source in sources:
            remaining.extend(by_source[source][1:])  # 跳过已选的第 1 条
        
        def sort_key(item):
            imp, fun = calc_score(item.title, item.source)
            return (imp + fun * 0.3, -len(item.title))
        remaining.sort(key=sort_key, reverse=True)
        
        # 补充到 top_n
        for item in remaining:
            if len(selected) >= top_n:
                break
            selected.append(item)
        
        return selected[:top_n]
    
    async def scrape_all(self) -> List[NewsItem]:
        print("📰 开始抓取 AI 新闻...\n")
        all_items = []
        
        tasks = [self.fetch_quantumwei(), self.fetch_infoq(), self.fetch_jiemian()]]
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        source_names = ['量子位', 'InfoQ', '界面新闻']]
        for source, items in zip(source_names, results):
            if isinstance(items, list):
                print(f"  ✓ {source}: {len(items)} 条")
                all_items.extend(items)
        
        print(f"\n✅ 共抓取 {len(all_items)} 条不重复新闻\n")
        await self.close_session()
        return all_items
    
    def save_history(self, items: List[NewsItem], date: str):
        """保存历史日报"""
        filename = f"report_{date}.json"
        filepath = os.path.join(self.history_dir, filename)
        
        data = {
            'date': date,
            'update_time': datetime.now().isoformat(),
            'total_items': len(items),
            'top_items': [item.to_dict() for item in items]
        }
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        
        print(f"📁 历史已保存：{filename}")
    
    def load_history_list(self) -> List[Dict]:
        """加载历史日报列表"""
        history = []
        if os.path.exists(self.history_dir):
            for filename in sorted(os.listdir(self.history_dir), reverse=True):
                if filename.startswith('report_') and filename.endswith('.json'):
                    date = filename.replace('report_', '').replace('.json', '')
                    history.append({'date': date, 'filename': filename})
        return history


def generate_html(items: List[NewsItem], output_path: str, history_list: List[Dict] = None):
    """生成 HTML - 带右侧历史栏"""
    today = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    date_only = datetime.now().strftime('%Y-%m-%d')
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
                    <h3 class="news-title"><a href="{item.url}" target="_blank">{item.title}</a></h3>
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
    
    # 历史链接 HTML
    history_html = ""
    if history_list:
        for h in history_list[:15]:  # 显示最近 15 条
            history_html += f'<a href="history/report_{h["date"]}.html" class="history-link">📅 {h["date"]}</a>'
    
    html = f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AI 日报简讯 - {date_only}</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{
            background: linear-gradient(135deg, #1e3a5f 0%, #2d5a87 100%);
            min-height: 100vh;
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "PingFang SC", "Microsoft YaHei", sans-serif;
            padding: 10px;
        }}
        .container {{ max-width: 1100px; margin: 0 auto; display: flex; gap: 16px; }}
        .main-content {{ flex: 1; }}
        .sidebar {{
            width: 220px;
            flex-shrink: 0;
        }}
        .header-card {{
            background: rgba(255,255,255,0.98);
            border-radius: 12px;
            padding: 20px;
            margin-bottom: 14px;
            box-shadow: 0 4px 12px rgba(0,0,0,0.15);
            text-align: center;
        }}
        .header-title {{
            font-size: 26px;
            font-weight: bold;
            background: linear-gradient(135deg, #1e3a5f, #2d5a87);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            margin-bottom: 6px;
        }}
        .history-card {{
            background: rgba(255,255,255,0.95);
            border-radius: 12px;
            padding: 16px;
            box-shadow: 0 4px 12px rgba(0,0,0,0.15);
            position: sticky;
            top: 10px;
        }}
        .history-title {{
            font-size: 16px;
            font-weight: bold;
            color: #1e3a5f;
            margin-bottom: 12px;
            padding-bottom: 8px;
            border-bottom: 2px solid #e0e7ff;
        }}
        .history-link {{
            display: block;
            padding: 8px 12px;
            margin-bottom: 6px;
            background: #f8fafc;
            border-radius: 6px;
            color: #2d5a87;
            text-decoration: none;
            font-size: 13px;
            transition: all 0.2s;
        }}
        .history-link:hover {{
            background: #e0e7ff;
            transform: translateX(4px);
        }}
        .news-item {{
            background: rgba(255,255,255,0.98);
            border-radius: 10px;
            padding: 14px;
            margin-bottom: 10px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.12);
            display: flex;
            gap: 14px;
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
        .news-title a {{ color: #1e3a5f; text-decoration: none; }}
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
        .news-badge {{ padding: 3px 10px; border-radius: 12px; font-size: 12px; font-weight: 600; }}
        .news-source {{ background: #e0e7ff; color: #3730a3; padding: 3px 10px; border-radius: 12px; font-size: 12px; font-weight: 500; }}
        .news-time {{ color: #94a3b8; font-size: 12px; margin-left: auto; }}
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
        @media (max-width: 900px) {{
            .container {{ flex-direction: column; }}
            .sidebar {{ width: 100%; }}
            .history-card {{ position: static; }}
        }}
        @media (max-width: 640px) {{
            body {{ padding: 6px; }}
            .header-card {{ padding: 16px; }}
            .header-title {{ font-size: 22px; }}
            .news-item {{ padding: 10px; gap: 10px; }}
            .news-number {{ width: 55px; min-width: 55px; min-height: 90px; font-size: 28px; }}
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
        <div class="main-content">
            <div class="header-card">
                <h1 class="header-title">🤖 AI 日报简讯</h1>
                <p class="text-slate-600 text-sm">{today}</p>
            </div>
            <div id="news-list">{news_html}</div>
            <div class="text-center text-white/70 text-xs mt-8">
                <p>数据来源于量子位、InfoQ、界面新闻等主流媒体</p>
                <p class="mt-1">更新：{today}</p>
            </div>
        </div>
        <div class="sidebar">
            <div class="history-card">
                <h2 class="history-title">📁 历史日报</h2>
                <div class="history-list">
                    {history_html if history_html else '<p class="text-gray-500 text-sm">暂无历史</p>'}
                </div>
            </div>
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
    
    # 选择多样化的前 10 条
    top_items = scraper.select_diverse_top(items, 10)
    
    script_dir = scraper.script_dir
    date_only = datetime.now().strftime('%Y-%m-%d')
    
    # 保存数据
    data = {'update_time': datetime.now().isoformat(), 'total_items': len(items), 'top_items': [item.to_dict() for item in top_items]}
    with open(f'{script_dir}/news_data.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    
    # 保存历史
    scraper.save_history(top_items, date_only)
    
    # 加载历史列表
    history_list = scraper.load_history_list()
    
    # 生成 HTML（带历史栏）
    generate_html(top_items, f'{script_dir}/index.html', history_list)
    
    # 生成历史 HTML
    generate_html(top_items, f'{scraper.history_dir}/report_{date_only}.html', history_list)
    
    print(f"\n💾 数据已保存到：{script_dir}/")
    print(f"📊 共 {len(items)} 条，精选 {len(top_items)} 条")
    
    try:
        import subprocess
        subprocess.run(['xdg-open', f'{script_dir}/index.html'], timeout=3, capture_output=True)
        print("🌐 HTML 已打开")
    except:
        print(f"📄 请手动打开：{script_dir}/index.html")


if __name__ == '__main__':
    asyncio.run(main())

# 虎嗅网特殊处理：从 JSON 数据中提取
async def fetch_huxiu_v2(self) -> List[NewsItem]:
    """抓取虎嗅网（从 JSON 数据提取）"""
    items = []
    print("  → 虎嗅网...")
    try:
        await self.init_session()
        async with self.session.get('https://www.huxiu.com', allow_redirects=True) as resp:
            html = await resp.text('utf-8', errors='ignore')
            # 从 JSON 中提取文章信息
            article_ids = re.findall(r'article/(\d+)\.html', html)
            titles = re.findall(r'"title":"([^"]+)"', html)
            urls = re.findall(r'"url":"(https://www\.huxiu\.com/article/\d+\.html)"', html)
            
            # 匹配标题和 URL
            for i, url in enumerate(urls[:15]):
                if i < len(titles):
                    title = titles[i]
                    if len(title) < 5 or len(title) > 100:
                        continue
                    if is_ai_related(title):
                        content, pub_time = await self.fetch_article_content(url)
                        summary = await summarize_content(content)
                        imp, _ = calc_score(title, '虎嗅网')
                        items.append(NewsItem(title=title, source='虎嗅网', url=url, publish_time=pub_time or datetime.now().strftime('%Y-%m-%d'), category='AI 产业', summary=summary, importance_score=imp))
    except Exception as e:
        print(f"⚠️ {e}")
    return items

# 添加界面新闻数据源（替代虎嗅网）
async def fetch_jiemian(self) -> List[NewsItem]:
    """抓取界面新闻"""
    items = []
    print("  → 界面新闻...")
    try:
        await self.init_session()
        async with self.session.get('https://www.jiemian.com', allow_redirects=True) as resp:
            html = await resp.text('utf-8', errors='ignore')
            soup = BeautifulSoup(html, 'lxml')
            for link in soup.select('a[href*="/article/"]')[:15]:
                href = link.get('href', '')
                title = link.get_text(strip=True)
                if not title or len(title) < 5 or len(title) > 100:
                    continue
                if is_ai_related(title):
                    url = href if href.startswith('http') else f'https://www.jiemian.com{href}'
                    content, pub_time = await self.fetch_article_content(url)
                    summary = await summarize_content(content)
                    imp, _ = calc_score(title, '界面新闻')
                    items.append(NewsItem(title=title, source='界面新闻', url=url, publish_time=pub_time or datetime.now().strftime('%Y-%m-%d'), category='AI 产业', summary=summary, importance_score=imp))
    except Exception as e:
        print(f"⚠️ {e}")
    return items
