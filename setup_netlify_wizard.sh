#!/bin/bash
# Netlify 配置向导脚本

echo "=========================================="
echo "🌐 Netlify 自动部署配置向导"
echo "=========================================="
echo ""

cd /home/admin/openclaw/workspace/skills/ai-daily-news

# 检查 CLI
echo "步骤 1/4: 检查 Netlify CLI"
if command -v netlify &> /dev/null; then
    echo "✅ Netlify CLI 已安装：$(netlify --version)"
else
    echo "❌ Netlify CLI 未安装"
    echo "正在安装..."
    npm install -g netlify-cli
fi
echo ""

# 检查登录
echo "步骤 2/4: 检查 Netlify 登录状态"
if netlify status 2>&1 | grep -q "Logged in"; then
    echo "✅ 已登录 Netlify"
else
    echo "⚠️  未登录 Netlify"
    echo ""
    echo "请选择登录方式:"
    echo "1. 使用访问令牌（推荐）"
    echo "2. 浏览器登录"
    echo "3. 跳过（稍后配置 GitHub Secrets）"
    read -p "请选择 [1-3]: " login_choice
    
    case $login_choice in
        1)
            read -p "请输入访问令牌： " token
            if [ -n "$token" ]; then
                netlify login --access-token "$token"
            fi
            ;;
        2)
            netlify login
            ;;
        3)
            echo "跳过登录"
            ;;
    esac
fi
echo ""

# 检查站点配置
echo "步骤 3/4: 检查站点配置"
if [ -f ".netlify" ]; then
    site_id=$(cat .netlify | grep -o '"siteId": "[^"]*"' | cut -d'"' -f4)
    echo "✅ 站点已配置：$site_id"
elif [ -n "$NETLIFY_SITE_ID" ]; then
    echo "✅ 使用环境变量：$NETLIFY_SITE_ID"
else
    echo "⚠️  站点未配置"
    echo ""
    echo "请提供 Site ID（从 Netlify 控制台获取）:"
    echo "访问：https://app.netlify.com → 选择站点 → Site settings → General"
    read -p "Site ID: " site_id
    
    if [ -n "$site_id" ]; then
        echo "{\"siteId\": \"$site_id\"}" > .netlify
        echo "✅ 站点配置已保存：.netlify"
    else
        echo "跳过站点配置"
    fi
fi
echo ""

# 测试部署
echo "步骤 4/4: 测试部署"
read -p "是否立即测试部署？[y/N]: " deploy_choice

if [ "$deploy_choice" = "y" ] || [ "$deploy_choice" = "Y" ]; then
    echo ""
    echo "🚀 开始部署..."
    
    if [ -n "$NETLIFY_AUTH_TOKEN" ]; then
        echo "使用环境变量 NETLIFY_AUTH_TOKEN"
        netlify deploy --prod --dir=. --message "Test deploy from wizard"
    elif [ -f ".netlify" ]; then
        echo "使用本地配置"
        netlify deploy --prod --dir=. --message "Test deploy from wizard"
    else
        echo "⚠️  未配置认证信息，无法部署"
        echo ""
        echo "请配置 GitHub Secrets:"
        echo "1. 访问：https://github.com/wanibbo/ai-daily-news/settings/secrets/actions"
        echo "2. 添加 secrets:"
        echo "   - NETLIFY_AUTH_TOKEN"
        echo "   - NETLIFY_SITE_ID"
    fi
else
    echo "跳过部署测试"
fi
echo ""

# 完成
echo "=========================================="
echo "✅ 配置完成！"
echo "=========================================="
echo ""
echo "下一步:"
echo "1. 配置 GitHub Secrets（如果还未配置）"
echo "   https://github.com/wanibbo/ai-daily-news/settings/secrets/actions"
echo ""
echo "2. 手动触发部署测试"
echo "   https://github.com/wanibbo/ai-daily-news/actions/workflows/auto-deploy-all.yml"
echo ""
echo "3. 访问部署后的网站"
echo "   https://ai-daily-daily.netlify.app/"
echo ""
echo "4. 查看完整配置指南"
echo "   cat NETLIFY_AUTO_SETUP.md"
echo ""
