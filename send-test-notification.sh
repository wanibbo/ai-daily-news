#!/bin/bash
# 发送测试通知

echo "======================================"
echo "📢 发送日报通知测试"
echo "时间：$(date +'%Y-%m-%d %H:%M:%S')"
echo "======================================"

# 检查 GitHub Secrets
if [ -z "$DINGTALK_WEBHOOK" ]; then
    echo "⚠️  DINGTALK_WEBHOOK 未配置"
    echo ""
    echo "请在 GitHub Secrets 中配置:"
    echo "  1. 访问：https://github.com/wanibbo/ai-daily-news/settings/secrets/actions"
    echo "  2. 添加 Secret: DINGTALK_WEBHOOK"
    echo "  3. Value: 钉钉机器人 Webhook URL"
    exit 1
fi

TITLE="✅ AI 日报生成成功（测试）"
TEXT="今日 AI 日报已自动生成并部署！\n\n📊 数据来源：量子位、InfoQ、界面新闻、虎嗅网\n📁 报告：history/report_2026-04-03.html\n🌐 部署：GitHub Pages 已完成\n🔗 查看：https://wanibbo.github.io/ai-daily-news/\n\n⏰ 生成时间：$(date +'%Y-%m-%d %H:%M')\n📰 新闻数量：24 条"

echo "📤 发送钉钉通知..."
curl -X POST "$DINGTALK_WEBHOOK" \
  -H 'Content-Type: application/json' \
  -d "{
    \"msgtype\": \"markdown\",
    \"markdown\": {
      \"title\": \"$TITLE\",
      \"text\": \"$TITLE\n\n$TEXT\n\n⏰ 时间：$(date +'%Y-%m-%d %H:%M:%S')\n🤖 自动发送\"
    }
  }"

if [ $? -eq 0 ]; then
    echo ""
    echo "✅ 钉钉通知发送成功"
else
    echo ""
    echo "❌ 钉钉通知发送失败"
fi

echo "======================================"
