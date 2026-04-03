# 🚀 Netlify 自动部署指南

## 为什么选择 Netlify？

- ✅ 完全免费
- ✅ 自动 HTTPS
- ✅ 全球 CDN
- ✅ 自动部署
- ✅ 支持表单、函数等高级功能
- ✅ 比 Vercel 更稳定

---

## 📋 部署步骤

### 方法 1：Netlify 官网拖拽（最简单）

1. **访问** https://app.netlify.com/drop
2. **登录/注册**（支持 GitHub 登录）
3. **拖拽文件夹**到页面
   - 拖拽 `/home/admin/openclaw/workspace/skills/ai-daily-news/` 整个文件夹
4. **完成！**

**获得 URL**: `https://ai-daily-news-xxxx.netlify.app`

---

### 方法 2：GitHub + Netlify 自动部署（推荐）

#### 第 1 步：推送到 GitHub

```bash
cd /home/admin/openclaw/workspace/skills/ai-daily-news

git init
git add -A
git commit -m "AI Daily News with Netlify auto-deploy"

git remote add origin https://github.com/wanibbo/ai-daily-news.git
git branch -M main
git push -u origin main
```

#### 第 2 步：连接 Netlify

1. **访问** https://app.netlify.com
2. **GitHub 登录**
3. **点击** "Add new site" → "Import an existing project"
4. **选择** "Deploy with GitHub"
5. **授权** Netlify 访问 GitHub
6. **选择** `ai-daily-news` 仓库
7. **配置**：
   - Build command: 留空（无需构建）
   - Publish directory: 留空（当前目录）
8. **点击** "Deploy site"

#### 第 3 步：获得外网 URL

部署成功后获得：
```
https://ai-daily-news-xxxx.netlify.app
```

---

### 方法 3：Netlify CLI（高级）

#### 安装 CLI

```bash
npm install -g netlify-cli
```

#### 登录

```bash
netlify login
```

#### 部署

```bash
cd /home/admin/openclaw/workspace/skills/ai-daily-news
netlify init
netlify deploy --prod
```

---

## ⏰ 自动更新流程

```
每天早上 8:00 (北京时间)
    ↓
GitHub Actions 触发
    ↓
抓取新闻 + 生成 HTML
    ↓
Commit & Push
    ↓
Netlify 自动检测变化
    ↓
自动重新部署
    ↓
外网可访问
```

---

## 🔧 配置说明

### netlify.toml

```toml
[build]
  command = "echo 'No build needed'"
  publish = "."

[[redirects]]
  from = "/*"
  to = "/index.html"
  status = 200
```

### GitHub Actions

`.github/workflows/daily-update.yml` 已配置：
- 每天 UTC 0 点（北京时间 8 点）执行
- 自动抓取新闻
- 自动 Commit & Push
- Netlify 自动部署

---

## 🌐 访问地址

部署成功后：

1. **Netlify**: `https://ai-daily-news-xxxx.netlify.app`
2. **自定义域名**（可选）: 在 Netlify 后台配置

---

## 📊 Netlify vs Vercel

| 特性 | Netlify | Vercel |
|------|---------|--------|
| 免费额度 | 100GB/月 | 100GB/月 |
| 构建分钟 | 300/月 | 6000/月 |
| 带宽 | 100GB/月 | 100GB/月 |
| 自动 HTTPS | ✅ | ✅ |
| 全球 CDN | ✅ | ✅ |
| 表单处理 | ✅ | ❌ |
| 函数支持 | ✅ | ✅ |
| 稳定性 | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ |

**结论**: Netlify 更适合静态网站部署！

---

## 🎯 推荐方案

**使用 Netlify 官网拖拽**（最快）：
1. 访问 https://app.netlify.com/drop
2. 拖拽文件夹
3. 完成！

**或使用 GitHub 自动部署**（最方便）：
1. 推送代码到 GitHub
2. Netlify 连接仓库
3. 自动部署

---

**预计时间**: 5-10 分钟  
**难度**: ⭐⭐（简单）
