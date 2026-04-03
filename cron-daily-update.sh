#!/bin/bash
# AI 日报每日自动生成脚本
# 配置为每天北京时间 08:00 执行

set -e

echo "======================================"
echo "📰 AI 日报自动生成"
echo "时间：$(date '+%Y-%m-%d %H:%M:%S')"
echo "======================================"

# 进入工作目录
cd /home/admin/openclaw/workspace/skills/ai-daily-news

# 生成日报
echo "📝 步骤 1/3: 生成 AI 日报..."
python3 skill_v12.py

# 检查生成结果
if [ ! -f "history/report_$(date +%Y-%m-%d).html" ]; then
    echo "❌ 日报生成失败！"
    exit 1
fi

echo "✅ 日报生成成功"

# 推送代码
echo "📤 步骤 2/3: 推送代码到 GitHub..."
git add -A
git commit -m "Daily update $(date +%Y-%m-%d) [auto]" || echo "No changes"
git push

if [ $? -eq 0 ]; then
    echo "✅ 代码推送成功"
else
    echo "⚠️  代码推送失败，但日报已生成"
fi

# 完成
echo "======================================"
echo "✅ 日报生成完成"
echo "访问：https://wanibbo.github.io/ai-daily-news/"
echo "======================================"
