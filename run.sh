#!/bin/bash
# AI 日报技能 - 快捷运行脚本（最终版）

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "======================================"
echo "🤖 AI 日报技能 v5"
echo "======================================"
echo ""

# 检查依赖
python3 -c "import aiohttp, bs4" 2>/dev/null || {
    echo "📦 安装依赖..."
    pip3 install -q aiohttp beautifulsoup4 lxml
}

# 运行技能
python3 skill_v12.py

echo ""
echo "======================================"
echo "✅ 完成！"
echo "======================================"
echo ""
echo "📄 HTML 文件：$SCRIPT_DIR/index.html"
echo "📊 JSON 数据：$SCRIPT_DIR/news_data.json"
echo ""
