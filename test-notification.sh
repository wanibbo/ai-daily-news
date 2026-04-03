#!/bin/bash
# 测试通知发送脚本

echo "======================================"
echo "📢 测试通知发送"
echo "时间：$(date +'\%Y-\%m-\%d \%H:\%M:\%S')"
echo "======================================"

# 检查是否配置了通知
if [ -z "$DINGTALK_WEBHOOK" ] && [ -z "$WECHAT_WORK_WEBHOOK" ]; then
    echo "⚠️  未配置通知 Webhook"
    echo ""
    echo "请在 GitHub Secrets 中配置:"
    echo "  - DINGTALK_WEBHOOK"
    echo "  - WECHAT_WORK_WEBHOOK"
    exit 1
fi

# 测试数据
TITLE="✅ AI 日报生成成功（测试）"
TEXT="这是一条测试通知\n\n📊 数据来源：量子位、InfoQ、界面新闻、虎嗅网\n📁 报告：history/report_2026-04-03.html\n🌐 部署：GitHub Pages 已完成\n🔗 查看：https://wanibbo.github.io/ai-daily-news/\n\n⏰ 测试时间：$(date +'\%Y-\%m-\%d \%H:\%M:\%S')\n🤖 自动发送"

# 发送钉钉通知
if [ -n "$DINGTALK_WEBHOOK" ]; then
    echo "📤 发送钉钉通知..."
    curl -X POST "$DINGTALK_WEBHOOK" \
      -H 'Content-Type: application/json' \
      -d "{
        \"msgtype\": \"markdown\",
        \"markdown\": {
          \"title\": \"$TITLE\",
          \"text\": \"$TITLE\n\n$TEXT\n\n⏰ 时间：$(date +'\%Y-\%m-\%d \%H:\%M:\%S')\n🤖 自动发送\"
        }
      }"
    echo ""
    if [ $? -eq 0 ]; then
        echo "✅ 钉钉通知发送成功"
    else
        echo "❌ 钉钉通知发送失败"
    fi
else
    echo "⚠️  未配置钉钉 Webhook，跳过"
fi

# 发送企业微信通知
if [ -n "$WECHAT_WORK_WEBHOOK" ]; then
    echo "📤 发送企业微信通知..."
    curl -X POST "$WECHAT_WORK_WEBHOOK" \
      -H 'Content-Type: application/json' \
      -d "{
        \"msgtype\": \"markdown\",
        \"markdown\": {
          \"content\": \"## $TITLE\n\n> $TEXT\n\n_⏰ 时间：$(date +'\%Y-\%m-\%d \%H:\%M:\%S')_\n_🤖 自动发送_\"
        }
      }"
    echo ""
    if [ $? -eq 0 ]; then
        echo "✅ 企业微信通知发送成功"
    else
        echo "❌ 企业微信通知发送失败"
    fi
else
    echo "⚠️  未配置企业微信 Webhook，跳过"
fi

echo ""
echo "======================================"
echo "测试完成"
echo "======================================"
