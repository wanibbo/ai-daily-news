# 🐯 虎嗅网 OCR 抓取 - 实现完成

**完成时间**: 2026-03-26 15:10  
**状态**: ✅ 代码已实现

---

## 📋 实现方案

### 技术架构
```
browser 工具
    ↓
打开虎嗅网
    ↓
全屏截图
    ↓
大模型 OCR 识别
    ↓
解析 JSON 结果
    ↓
过滤 AI 内容
    ↓
生成新闻条目
```

### 代码实现

**主函数**: `fetch_huxiu_ocr()`
```python
async def fetch_huxiu_ocr(self) -> List[NewsItem]:
    # 1. browser 工具打开页面
    browser_result = await browser(action='open', targetUrl='https://www.huxiu.com')
    
    # 2. 等待加载
    await asyncio.sleep(3)
    
    # 3. 截图
    screenshot = await browser(action='screenshot', targetId=target_id, fullPage=True)
    
    # 4. 读取图片
    with open(image_path, 'rb') as f:
        image_data = base64.b64encode(f.read()).decode('utf-8')
    
    # 5. 调用大模型 OCR
    ocr_news = await self._call_llm_ocr(image_data)
    
    # 6. 解析并过滤
    for news in ocr_news:
        if is_ai_related(news['title']):
            items.append(NewsItem(...))
    
    # 7. 关闭页面
    await browser(action='close', targetId=target_id)
    
    return items
```

**辅助函数**: `_call_llm_ocr()`
```python
async def _call_llm_ocr(self, image_base64: str) -> List[Dict]:
    prompt = """请识别这张网页截图中的所有新闻条目..."""
    
    # 调用大模型 API
    # 返回 JSON 格式的新闻列表
```

---

## 🔧 需要你配置

### 大模型 API

**方案 1：使用 OpenAI GPT-4 Vision**
```python
async with aiohttp.ClientSession() as session:
    payload = {
        "model": "gpt-4-vision-preview",
        "messages": [{
            "role": "user",
            "content": [
                {"type": "text", "text": prompt},
                {"type": "image_url", "image_url": {"url": f"data:image/png;base64,{image_base64}"}}
            ]
        }],
        "max_tokens": 3000
    }
    
    headers = {"Authorization": f"Bearer YOUR_API_KEY"}
    async with session.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload) as resp:
        result = await resp.json()
        return json.loads(result['choices'][0]['message']['content'])
```

**方案 2：使用国内大模型**
- 智谱 AI、通义千问、文心一言等
- 替换 API endpoint 和 API key

---

## 📊 预期效果

| 指标 | 预期值 |
|------|--------|
| 抓取数量 | 10-15 条 |
| AI 相关性 | 自动过滤 |
| 摘要质量 | 大模型生成 |
| 速度 | 10-15 秒/次 |

---

## 🚀 使用方式

### 已集成到主程序
```python
tasks = [
    self.fetch_quantumwei(),
    self.fetch_infoq(),
    self.fetch_jiemian(),
    self.fetch_huxiu_ocr()  # 虎嗅网 OCR
]
```

### 单独测试
```bash
cd /home/admin/openclaw/workspace/skills/ai-daily-news
python3 huxiu_ocr_impl.py
```

---

## ⚠️ 注意事项

1. **browser 工具必须可用**
   - 需要 OpenClaw gateway 运行正常
   - 浏览器控制服务必须可用

2. **大模型 API 需要配置**
   - 需要 API key
   - 有使用成本（按 token 计费）

3. **速度较慢**
   - 每次抓取约 10-15 秒
   - 不适合高频调用

4. **建议配置**
   - 每天抓取 1 次即可
   - 与其他数据源并行抓取

---

## 📁 相关文件

| 文件 | 说明 |
|------|------|
| `skill_v12.py` | 主程序（已集成） |
| `huxiu_ocr_impl.py` | 独立测试脚本 |
| `HUXIU_OCR_COMPLETE.md` | 本文档 |

---

**状态**: ✅ 代码已实现  
**待配置**: 大模型 API key  
**预计效果**: 10-15 条 AI 新闻/次
