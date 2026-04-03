#!/usr/bin/env python3
"""虎嗅 OCR 测试脚本 - 简化版"""

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
    
    target_id = None
    for line in result.stdout.split('\n'):
        if line.startswith('id:'):
            target_id = line.split(':', 1)[1].strip()
            break
    
    if not target_id:
        print('无法获取 target_id')
        return
    
    print(f'target_id: {target_id}')
    await asyncio.sleep(3)
    
    # 3. 截图
    screenshot_result = subprocess.run(['openclaw', 'browser', 'screenshot', target_id, '--full-page'], capture_output=True, text=True, timeout=30)
    
    if screenshot_result.stdout.startswith('MEDIA:'):
        image_path = screenshot_result.stdout[6:].strip().replace('$OPENCLAW_HOME', '/home/admin')
        print(f'图片路径：{image_path}')
        
        with open(image_path, 'rb') as f:
            image_data = base64.b64encode(f.read()).decode('utf-8')
        print(f'图片大小：{len(image_data)} bytes')
        
        # 简化的提示词
        prompt = """请识别这张虎嗅网首页截图中的所有文章标题和摘要。

按以下 JSON 格式返回：
[{"title": "文章标题", "summary": "文章摘要或副标题", "url": "https://www.huxiu.com/article/1.html"}]

识别 15 条最新新闻。只返回 JSON，不要其他内容。"""
        
        api_key = 'sk-668bbaeb841b44b1a0a9bf62668d4024'
        api_url = 'https://dashscope.aliyuncs.com/compatible-mode/v1/chat/completions'
        
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
        
        headers = {'Authorization': f'Bearer {api_key}', 'Content-Type': 'application/json'}
        
        print('正在调用大模型 API...')
        async with aiohttp.ClientSession() as session:
            async with session.post(api_url, json=payload, headers=headers, timeout=aiohttp.ClientTimeout(total=90)) as resp:
                result = await resp.json()
                print(f'API 状态码：{resp.status}')
                
                if resp.status == 200:
                    content = result.get('choices', [{}])[0].get('message', {}).get('content', '')
                    print('\n=== 原始响应 ===')
                    print(content[:2000])
                    
                    json_match = re.search(r'\[.*\]', content, re.DOTALL)
                    if json_match:
                        try:
                            parsed = json.loads(json_match.group())
                            print(f'\n解析到 {len(parsed)} 条新闻')
                            for i, news in enumerate(parsed[:10], 1):
                                print(f'{i}. {news.get("title", "N/A")}')
                                print(f'   摘要：{news.get("summary", "N/A")[:60]}...')
                        except json.JSONDecodeError as e:
                            print(f'JSON 解析错误：{e}')
                    else:
                        print('无法找到 JSON 数组')
                else:
                    print(f'API 错误：{result}')
        
        subprocess.run(['openclaw', 'browser', 'close', target_id], capture_output=True, timeout=10)

if __name__ == '__main__':
    asyncio.run(test_ocr())
