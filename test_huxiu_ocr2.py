#!/usr/bin/env python3
"""虎嗅 OCR 测试脚本"""

import asyncio
import aiohttp
import base64
import json
import re
import subprocess

async def test_ocr():
    # 1. 打开页面
    result = subprocess.run(['openclaw', 'browser', 'open', 'https://www.huxiu.com'], capture_output=True, text=True, timeout=30)
    print('打开页面:', result.stdout[:200])
    
    # 提取 target_id
    target_id = None
    for line in result.stdout.split('\n'):
        if line.startswith('id:'):
            target_id = line.split(':', 1)[1].strip()
            break
    
    if not target_id:
        print('无法获取 target_id')
        return
    
    print(f'target_id: {target_id}')
    
    # 2. 等待
    await asyncio.sleep(3)
    
    # 3. 截图
    screenshot_result = subprocess.run(['openclaw', 'browser', 'screenshot', target_id, '--full-page'], capture_output=True, text=True, timeout=30)
    print('截图结果:', screenshot_result.stdout[:200])
    
    # 解析图片路径
    if screenshot_result.stdout.startswith('MEDIA:'):
        image_path = screenshot_result.stdout[6:].strip()
        # 处理 $OPENCLAW_HOME (实际是 /home/admin)
        image_path = image_path.replace('$OPENCLAW_HOME', '/home/admin')
        print(f'图片路径：{image_path}')
        
        # 4. 读取图片
        with open(image_path, 'rb') as f:
            image_data = base64.b64encode(f.read()).decode('utf-8')
        print(f'图片大小：{len(image_data)} bytes')
        
        # 5. 调用 API
        api_key = 'sk-668bbaeb841b44b1a0a9bf62668d4024'
        api_url = 'https://dashscope.aliyuncs.com/compatible-mode/v1/chat/completions'
        
        prompt = """你是专业的新闻内容识别助手。请仔细识别这张虎嗅网（huxiu.com）首页截图中的所有新闻条目。

## 识别要求：

1. **标题识别**：识别页面中所有新闻文章的主标题，保持原文
2. **摘要识别**：识别标题下方的副标题、导语或摘要文字（30-80 字）
3. **链接识别**：格式 https://www.huxiu.com/article/XXXXXX.html

## 输出格式：

严格按以下 JSON 数组返回（不要其他文字）：
[{"title": "标题", "summary": "摘要 30-80 字", "url": "链接"}]

识别 15-20 条最新新闻，忽略导航和广告。"""
        
        payload = {
            'model': 'qwen3-max-2026-01-23',
            'messages': [{
                'role': 'user',
                'content': [
                    {'type': 'text', 'text': prompt},
                    {'type': 'image_url', 'image_url': {'url': f'data:image/png;base64,{image_data}'}}
                ]
            }],
            'max_tokens': 4000
        }
        
        headers = {
            'Authorization': f'Bearer {api_key}',
            'Content-Type': 'application/json'
        }
        
        print('正在调用大模型 API...')
        async with aiohttp.ClientSession() as session:
            async with session.post(api_url, json=payload, headers=headers, timeout=aiohttp.ClientTimeout(total=90)) as resp:
                result = await resp.json()
                print(f'API 状态码：{resp.status}')
                
                if resp.status == 200:
                    content = result.get('choices', [{}])[0].get('message', {}).get('content', '')
                    print('\n=== OCR 识别结果 ===')
                    print(content[:3000])
                    print('\n=== 解析 JSON ===')
                    json_match = re.search(r'\[.*\]', content, re.DOTALL)
                    if json_match:
                        parsed = json.loads(json_match.group())
                        print(f'解析到 {len(parsed)} 条新闻')
                        for i, news in enumerate(parsed[:10], 1):
                            print(f'{i}. {news.get("title", "N/A")}')
                            print(f'   摘要：{news.get("summary", "N/A")[:80]}...')
                    else:
                        print('无法解析 JSON')
                else:
                    print(f'API 错误：{result}')
        
        # 6. 关闭
        subprocess.run(['openclaw', 'browser', 'close', target_id], capture_output=True, timeout=10)

if __name__ == '__main__':
    asyncio.run(test_ocr())
