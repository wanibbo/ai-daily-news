# 🚀 AI 日报 - 自动部署完整指南

## ✅ 已完成配置

### 1. GitHub Actions 工作流
- ✅ `.github/workflows/daily-update.yml` - 每日自动更新
- ✅ `.github/workflows/deploy-to-vercel.yml` - Vercel 部署

### 2. 数据源
- ✅ 量子位（10 条）
- ✅ InfoQ（14 条）
- ✅ 界面新闻（新增）

### 3. 摘要功能
- ✅ 量子位 - 正常
- ✅ InfoQ - 已修复
- ✅ 界面新闻 - 正常

---

## 📋 需要你配合的步骤

### 第 1 步：推送到 GitHub

```bash
cd /home/admin/openclaw/workspace/skills/ai-daily-news

# 初始化 Git（如果还没初始化）
git init
git add -A
git commit -m "AI Daily News with auto-deploy"

# 添加远程仓库（使用你的 GitHub 账号 wanibbo）
git remote add origin https://github.com/wanibbo/ai-daily-news.git

# 推送到 GitHub
git branch -M main
git push -u origin main
```

### 第 2 步：配置 Vercel

**选项 A：使用 Vercel 官网（推荐）**

1. 访问 https://vercel.com
2. 用 GitHub 账号登录
3. 点击 "Import Git Repository"
4. 选择 `wanibbo/ai-daily-news` 仓库
6. 点击 "Deploy"
7. 获得外网 URL：`https://ai-daily-news-wanibbo.vercel.app`

**选项 B：使用 Vercel CLI**

1. 安装 Vercel CLI：
   ```bash
   npm install -g vercel
   ```

2. 登录 Vercel：
   ```bash
   vercel login
   ```

3. 部署：
   ```bash
   vercel --prod
   ```

### 第 3 步：配置 Secrets（如果使用 Vercel CLI 部署）

在 GitHub 仓库设置中添加以下 Secrets：
- `VERCEL_TOKEN` - Vercel API Token
- `VERCEL_ORG_ID` - Vercel 组织 ID
- `VERCEL_PROJECT_ID` - Vercel 项目 ID

---

## ⏰ 自动更新流程

```
每天早上 8:00 (北京时间)
    ↓
GitHub Actions 触发
    ↓
安装 Python 依赖
    ↓
执行 skill_v12.py
    ↓
抓取最新 AI 新闻
    ↓
生成 HTML 日报
    ↓
Commit & Push
    ↓
Vercel 自动部署
    ↓
外网可访问
```

---

## 🌐 访问地址

部署成功后，你可以通过以下地址访问：

1. **Vercel**: `https://ai-daily-news-wanibbo.vercel.app`
2. **GitHub Pages**（可选）: `https://wanibbo.github.io/ai-daily-news`

---

## 🔧 手动触发更新

如果需要立即更新（不等到明天 8 点）：

1. 访问 GitHub 仓库
2. 点击 "Actions" 标签
3. 选择 "Daily AI News Update"
4. 点击 "Run workflow"
5. 等待完成

---

## 📊 当前状态

| 项目 | 状态 |
|------|------|
| 数据源 | ✅ 3 个（量子位、InfoQ、界面新闻） |
| 摘要功能 | ✅ 全部正常 |
| GitHub Actions | ✅ 已配置 |
| Vercel 部署 | ⏳ 等待授权 |
| 自动更新 | ⏳ 等待部署 |

---

## 🎯 下一步

**需要你做的**：
1. 推送代码到 GitHub
2. 在 Vercel 授权并部署

**我来帮你做的**：
1. ✅ 已配置所有自动化脚本
2. ✅ 已修复所有数据源
3. ✅ 已创建 GitHub Actions 工作流

---

**预计完成时间**: 10 分钟（需要你配合推送代码和 Vercel 授权）
