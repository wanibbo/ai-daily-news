# AI 日报新闻抓取技能

## 描述

自动从各大主流媒体获取 AI 相关的最新技术或应用进展，以日报简讯的形式总结出来，每天推送最重要的 5-10 条信息，并注明来源和总结分析。

## 触发条件

用户提到以下关键词时触发：
- "AI 日报"
- "新闻抓取"
- "AI 资讯"
- "技术简报"
- "daily report"
- "AI news"
- "帮我收集 AI 新闻"
- "今天 AI 圈有什么动态"

## 使用方法

### 1. 直接运行（推荐）

```bash
cd /home/admin/openclaw/workspace/skills/ai-daily-news
python3 skill_rss.py
```

### 2. 作为技能调用

```python
from skill_rss import scrape_all, generate_report

items = await scrape_all()
report = generate_report(items)
print(report)
```

### 2. 作为技能调用

```python
from skill import AIDailyNewsSkill

skill = AIDailyNewsSkill()
result = await skill.run()
print(result)
```

### 3. 抓取并保存

```python
skill = AIDailyNewsSkill()
items = await skill.fetch_and_save(limit=10)
```

## 数据源

当前支持的数据源：
- 量子位 (qbitai.com)
- 机器之心 (jiqizhixin.com)
- 36Kr AI
- InfoQ AI

可在 `skill.json` 的 `config.sources` 中添加更多数据源。

## 输出格式

### 文本格式（控制台输出）

```
============================================================
🤖 AI 日报简讯
📅 日期：2026-03-24
📊 精选：10 条
============================================================

1. [9⭐] 黄仁勋暴论核弹：AGI 已经实现，Ilya 错了，程序员有 10 亿
   来源：量子位 | 分类：AI 综合
   链接：https://www.qbitai.com/2026/03/391750.html

2. [8⭐] OpenAI 发布 GPT-5，性能提升 10 倍
   来源：机器之心 | 分类：AI 综合
   链接：https://www.jiqizhixin.com/...

============================================================
数据来源于各大主流媒体 · 由 AI 自动整理
```

### JSON 格式（news_data.json）

```json
{
  "update_time": "2026-03-24T17:59:02.551598",
  "total_items": 15,
  "top_items": [
    {
      "title": "新闻标题",
      "source": "来源",
      "url": "链接",
      "publish_time": "2026-03-24",
      "category": "AI 综合",
      "importance_score": 9
    }
  ]
}
```

## 配置说明

编辑 `skill.json` 修改配置：

### 添加数据源

```json
{
  "sources": [
    {
      "name": "媒体名称",
      "url": "https://example.com",
      "category": "分类",
      "language": "zh",
      "selector": "h2 a"
    }
  ]
}
```

### 修改关键词

```json
{
  "keywords": ["人工智能", "大模型", "LLM", ...]
}
```

### 调整输出配置

```json
{
  "output": {
    "daily_limit": 10,
    "min_importance_score": 5
  }
}
```

## 定时任务

### 使用 cron

```bash
crontab -e
# 每天早上 8 点执行
0 8 * * * cd /home/admin/openclaw/workspace/skills/ai-daily-news && python3 skill.py >> /var/log/ai_daily.log 2>&1
```

### 使用 Python 调度器

参考 `ai_daily/scheduler.py`

## 依赖

```bash
pip3 install aiohttp beautifulsoup4 lxml
```

## 文件结构

```
ai-daily-news/
├── skill.json          # 技能配置
├── skill.py            # 技能主程序
├── SKILL.md            # 说明文档
├── news_data.json      # 输出数据（运行时生成）
└── README.md           # 扩展文档
```

## 扩展功能

### 1. 添加 AI 总结

集成大模型 API 对每条新闻进行摘要：

```python
async def summarize(self, item: NewsItem) -> str:
    # 调用大模型 API
    pass
```

### 2. 推送通知

集成微信、钉钉、邮件等推送方式。

### 3. 网页展示

生成 HTML 页面，参考 `ai_daily/template.html`

## 注意事项

1. 部分网站有反爬机制，建议设置合理的请求间隔
2. 确保服务器可以访问配置的新闻源
3. 定期更新数据源配置，移除失效的源

## 常见问题

**Q: 抓取不到新闻？**
A: 检查网络连接，确认数据源网站可访问；调整 CSS selector。

**Q: 如何添加新数据源？**
A: 在 `skill.json` 的 `sources` 数组中添加，指定 `url` 和 `selector`。

**Q: 如何修改抓取数量？**
A: 修改 `output.daily_limit` 配置，或在调用时传入 `limit` 参数。

## 许可证

MIT License
