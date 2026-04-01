#!/bin/bash
# 触发 GitHub Actions 自动部署

echo "=========================================="
echo "🚀 触发 GitHub Actions 自动部署"
echo "=========================================="
echo ""

# 检查是否有 git 远程
if git remote -v | grep -q origin; then
    echo "✅ Git 远程仓库已配置"
else
    echo "❌ 未配置 Git 远程仓库"
    exit 1
fi

# 创建触发文件
echo "📝 创建触发文件..."
touch .trigger-deploy
echo "Deploy triggered at $(date)" > .trigger-deploy

# 提交并推送
echo "📤 推送代码触发部署..."
git add .trigger-deploy
git commit -m "chore: trigger auto deploy $(date +%Y-%m-%d %H:%M)"
git push

if [ $? -eq 0 ]; then
    echo ""
    echo "✅ 推送成功！"
    echo ""
    echo "📊 查看部署状态:"
    echo "   https://github.com/wanibbo/ai-daily-news/actions/workflows/auto-deploy-all.yml"
    echo ""
    echo "⏱️  部署时间：约 3-5 分钟"
    echo ""
    echo "🌐 部署完成后访问:"
    echo "   https://ai-daily-daily.netlify.app/"
else
    echo ""
    echo "❌ 推送失败"
    exit 1
fi
