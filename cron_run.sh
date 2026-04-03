#!/bin/bash
# AI 日报 - 定时任务脚本
# 添加到 crontab: crontab -e
# 0 8 * * * /home/admin/openclaw/workspace/skills/ai-daily-news/cron_run.sh >> /var/log/ai_daily.log 2>&1

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "======================================"
echo "🤖 AI 日报 - 自动更新"
echo "时间：$(date '+%Y-%m-%d %H:%M:%S')"
echo "======================================"

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
