#!/bin/bash
# Netlify 部署诊断脚本

echo "=========================================="
echo "🔍 Netlify 部署诊断"
echo "=========================================="
echo ""

cd /home/admin/openclaw/workspace/skills/ai-daily-news

# 检查 1: Netlify CLI
echo "检查 1/6: Netlify CLI"
if command -v netlify &> /dev/null; then
    echo "✅ Netlify CLI 已安装：$(netlify --version)"
else
    echo "❌ Netlify CLI 未安装"
fi
echo ""

# 检查 2: 工作流文件
echo "检查 2/6: GitHub Actions 工作流"
if [ -f ".github/workflows/auto-deploy-all.yml" ]; then
    echo "✅ 工作流文件存在"
    if grep -q "NETLIFY_AUTH_TOKEN" .github/workflows/auto-deploy-all.yml; then
        echo "✅ 工作流配置正确"
    else
        echo "❌ 工作流配置可能有问题"
    fi
else
    echo "❌ 工作流文件不存在"
fi
echo ""

# 检查 3: netlify.toml
echo "检查 3/6: Netlify 配置文件"
if [ -f "netlify.toml" ]; then
    echo "✅ netlify.toml 存在"
else
    echo "❌ netlify.toml 不存在"
fi
echo ""

# 检查 4: 本地配置
echo "检查 4/6: 本地 Netlify 配置"
if [ -f ".netlify" ]; then
    echo "✅ .netlify 配置文件存在"
    cat .netlify
elif [ -n "$NETLIFY_AUTH_TOKEN" ] && [ -n "$NETLIFY_SITE_ID" ]; then
    echo "✅ 环境变量已设置"
    echo "   NETLIFY_AUTH_TOKEN: ${NETLIFY_AUTH_TOKEN:0:10}..."
    echo "   NETLIFY_SITE_ID: $NETLIFY_SITE_ID"
else
    echo "❌ 本地未配置 Netlify"
    echo ""
    echo "提示：GitHub Secrets 在 GitHub 服务器端，本地无法检查"
    echo "请访问：https://github.com/wanibbo/ai-daily-news/settings/secrets/actions"
fi
echo ""

# 检查 5: 最近的提交
echo "检查 5/6: 最近的 Git 提交"
git log --oneline -3
echo ""

# 检查 6: 网站文件
echo "检查 6/6: 网站文件"
if [ -f "index.html" ]; then
    echo "✅ index.html 存在"
else
    echo "❌ index.html 不存在"
fi

if [ -d "history" ] && [ "$(ls -A history/*.html 2>/dev/null)" ]; then
    echo "✅ 历史报告存在"
    ls -la history/*.html | tail -3
else
    echo "❌ 历史报告目录为空"
fi
echo ""

# 总结
echo "=========================================="
echo "📊 诊断总结"
echo "=========================================="
echo ""
echo "GitHub Secrets 配置检查:"
echo "  访问：https://github.com/wanibbo/ai-daily-news/settings/secrets/actions"
echo ""
echo "需要配置的 Secrets:"
echo "  - NETLIFY_AUTH_TOKEN (格式：nfp_xxx)"
echo "  - NETLIFY_SITE_ID (格式：xxx-xxx-xxx)"
echo ""
echo "查看 GitHub Actions 日志:"
echo "  访问：https://github.com/wanibbo/ai-daily-news/actions"
echo ""
echo "=========================================="
