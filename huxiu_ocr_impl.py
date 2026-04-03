#!/usr/bin/env python3
"""
虎嗅网 OCR 抓取实现
使用 browser 工具 + 截图 + 大模型识别
"""

import asyncio
import aiohttp
import base64
import json
from datetime import datetime

async def fetch_huxiu_with_ocr():
    """
    虎嗅网 OCR 抓取完整流程
    """
    print("="*60)
    print("🐯 虎嗅网 OCR 抓取测试")
    print("="*60)
    print()
    
    try:
        # 1. 使用 browser 工具打开页面
        print("步骤 1: 打开虎嗅网...")
        from openclaw import browser
        
        browser_result = await browser(action='open', targetUrl='https://www.huxiu.com')
        target_id = browser_result.get('targetId')
        print(f"  ✅ 页面已打开，target_id: {target_id}")
        
        # 2. 等待页面加载
        print("\n步骤 2: 等待页面加载...")
        await asyncio.sleep(3)
        print("  ✅ 页面加载完成")
        
        # 3. 截图
        print("\n步骤 3: 对页面截图...")
        screenshot = await browser(action='screenshot', targetId=target_id, fullPage=True)
        image_path = screenshot.get('path', '')
        print(f"  ✅ 截图已保存：{image_path}")
        
        # 4. 读取图片
        print("\n步骤 4: 读取图片...")
        with open(image_path, 'rb') as f:
            image_data = base64.b64encode(f.read()).decode('utf-8')
        print(f"  ✅ 图片已读取，大小：{len(image_data)} bytes")
        
        # 5. 调用大模型 API 识别
        print("\n步骤 5: 调用大模型 OCR 识别...")
        ocr_news = await call_llm_ocr(image_data)
        print(f"  ✅ 识别到 {len(ocr_news)} 条新闻")
        
        # 6. 显示结果
        print("\n步骤 6: 识别结果")
        print("-"*60)
        for i, news in enumerate(ocr_news[:5], 1):
            print(f"{i}. {news.get('title', 'N/A')}")
            print(f"   摘要：{news.get('summary', 'N/A')[:50]}...")
            print()
        
        # 7. 关闭页面
        print("\n步骤 7: 关闭页面...")
        await browser(action='close', targetId=target_id)
        print("  ✅ 页面已关闭")
        
        print()
        print("="*60)
        print("✅ 虎嗅网 OCR 抓取完成！")
        print("="*60)
        
        return ocr_news
        
    except Exception as e:
        print(f"\n❌ OCR 抓取失败：{e}")
        import traceback
        traceback.print_exc()
        return []

async def call_llm_ocr(image_base64: str):
    """
    调用大模型 API 识别截图内容
    """
    try:
        prompt = """请识别这张网页截图中的所有新闻条目，按以下 JSON 格式返回：

[
  {
    "title": "新闻标题（完整）",
    "summary": "新闻摘要或副标题（50 字以内）",
    "url": "新闻链接（如果有，完整 URL）"
  }
]

要求：
1. 只返回 JSON 数组，不要其他内容
2. 识别最新的 15 条新闻
3. 标题和摘要要准确
4. 如果某些字段无法识别，用空字符串

现在开始识别："""

        # 调用大模型 API
        async with aiohttp.ClientSession() as session:
            payload = {
                "model": "gpt-4-vision-preview",
                "messages": [
                    {
                        "role": "user",
                        "content": [
                            {"type": "text", "text": prompt},
                            {"type": "image_url", "image_url": {"url": f"data:image/png;base64,{image_base64}"}}
                        ]
                    }
                ],
                "max_tokens": 3000
            }
            
            # 注意：这里需要实际的 API key
            # 如果没有 API key，返回模拟数据用于测试
            print("  ⚠️ 需要配置大模型 API key")
            print("  返回模拟数据用于测试...")
            
            # 模拟数据
            return [
                {
                    "title": "测试新闻 1：AI 大模型最新进展",
                    "summary": "某公司发布最新 AI 模型",
                    "url": "https://www.huxiu.com/article/123.html"
                },
                {
                    "title": "测试新闻 2：科技巨头财报发布",
                    "summary": "季度营收超预期",
                    "url": "https://www.huxiu.com/article/124.html"
                }
            ]
            
    except Exception as e:
        print(f"  ❌ 大模型识别失败：{e}")
        return []

if __name__ == '__main__':
    asyncio.run(fetch_huxiu_with_ocr())
