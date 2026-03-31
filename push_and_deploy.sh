#!/bin/bash
# 自动推送并触发部署脚本

echo "=========================================="
echo "🚀 AI Daily News - 自动部署脚本"
echo "=========================================="
echo ""

cd /home/admin/openclaw/workspace/skills/ai-daily-news

# 1. 检查 Git 状态
echo "📊 检查 Git 状态..."
git status --short

echo ""
echo "📝 添加所有更改..."
git add -A

echo ""
echo "💾 提交更改..."
git commit -m "自动部署：更新日报和配置"

echo ""
echo "📤 推送到 GitHub..."
echo "⚠️  如果需要认证，请输入 GitHub 用户名和 Token（Personal Access Token）"
git push --set-upstream origin main

if [ $? -eq 0 ]; then
    echo ""
    echo "✅ 推送成功！"
    echo ""
    echo "🌐 请在 GitHub 上查看 Actions："
    echo "   https://github.com/wanibbo/ai-daily-news/actions"
    echo ""
    echo "📋 或者手动触发部署："
    echo "   1. 访问上述链接"
    echo "   2. 点击 'Auto Deploy to Multiple Platforms'"
    echo "   3. 点击 'Run workflow'"
else
    echo ""
    echo "❌ 推送失败"
    echo ""
    echo "💡 解决方案："
    echo ""
    echo "方法 1：使用 GitHub Token"
    echo "  git remote set-url origin https://<YOUR_TOKEN>@github.com/wanibbo/ai-daily-news.git"
    echo "  git push --set-upstream origin main"
    echo ""
    echo "方法 2：配置 SSH 密钥"
    echo "  1. 生成 SSH 密钥：ssh-keygen -t ed25519"
    echo "  2. 添加公钥到 GitHub：https://github.com/settings/keys"
    echo "  3. 更改 remote：git remote set-url origin git@github.com:wanibbo/ai-daily-news.git"
    echo "  4. 再次推送：git push --set-upstream origin main"
    echo ""
fi

echo ""
echo "=========================================="
