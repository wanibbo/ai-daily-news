#!/bin/bash
# AI 日报 - 一键部署到 Vercel/Netlify

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "======================================"
echo "🚀 AI 日报 - 外网部署"
echo "======================================"
echo ""

# 检查 Git
if ! command -v git &> /dev/null; then
    echo "❌ Git 未安装，请先安装 Git"
    exit 1
fi

# 初始化 Git 仓库
if [ ! -d ".git" ]; then
    echo "📦 初始化 Git 仓库..."
    git init
    git config user.email "ai@example.com"
    git config user.name "AI Assistant"
fi

# 添加文件
echo "📝 添加文件..."
git add -A
git commit -m "AI Daily News - $(date +%Y-%m-%d)" || echo "没有新更改"

echo ""
echo "======================================"
echo "✅ 部署准备完成！"
echo "======================================"
echo ""
echo "请选择部署方式："
echo ""
echo "1️⃣  Vercel 部署（推荐）"
echo "   访问：https://vercel.com/new"
echo "   步骤："
echo "   1. 用 GitHub 登录"
echo "   2. 点击 'Import Git Repository'"
echo "   3. 选择你的仓库"
echo "   4. 点击 'Deploy'"
echo ""
echo "2️⃣  Netlify 部署（拖拽）"
echo "   访问：https://app.netlify.com/drop"
echo "   步骤："
echo "   1. 拖拽文件夹到页面"
echo "   2. 完成！"
echo ""
echo "3️⃣  Cloudflare Pages"
echo "   访问：https://pages.cloudflare.com"
echo "   步骤："
echo "   1. 连接 GitHub"
echo "   2. 选择仓库"
echo "   3. 部署"
echo ""
echo "======================================"
echo ""
echo "📁 项目文件位置："
echo "$SCRIPT_DIR"
echo ""
echo "📊 包含文件："
ls -la *.html *.json 2>/dev/null | awk '{print "   " $9 " (" $5 " bytes)"}'
echo ""
