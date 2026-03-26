# 🚀 全自动部署方案 - 完整指南

## 需求确认
- ✅ **完全自动化**（无需人工干预）
- ✅ 每天早上 8 点自动抓取
- ✅ 自动 Commit & Push
- ✅ 自动触发部署
- ✅ 外网可访问

---

## 📋 方案对比（纯自动化）

### 方案 1：Netlify（⭐最推荐）

**自动化流程**:
```
GitHub Actions (每天 8:00)
    ↓
抓取新闻 + 生成 HTML
    ↓
自动 Commit & Push
    ↓
Netlify 自动检测变化
    ↓
自动重新部署
    ↓
外网可访问
```

**配置步骤**:
1. **获取 Netlify Token**
   - 访问 https://app.netlify.com/account/applications
   - 创建 Personal Access Token
   - 复制 Token

2. **获取 Site ID**
   - 在 Netlify 创建站点（首次需要手动）
   - 复制 Site ID

3. **添加 GitHub Secrets**
   ```
   NETLIFY_AUTH_TOKEN = 你的 Token
   NETLIFY_SITE_ID = 你的 Site ID
   ```

4. **完成！**
   - 之后完全自动化
   - 无需人工干预

**优点**:
- ✅ 配置简单
- ✅ 部署速度快
- ✅ 稳定性高
- ✅ 完全自动化

**缺点**:
- ⚠️ 首次需要手动创建站点（5 分钟）

---

### 方案 2：Cloudflare Pages

**自动化流程**:
```
GitHub Actions (每天 8:00)
    ↓
抓取新闻 + 生成 HTML
    ↓
自动 Commit & Push
    ↓
Cloudflare Pages 自动部署
    ↓
外网可访问
```

**配置步骤**:
1. **获取 Cloudflare API Token**
   - 访问 https://dash.cloudflare.com/profile/api-tokens
   - 创建 Token（Pages 权限）
   - 复制 Token

2. **获取 Account ID**
   - 在 Cloudflare Dashboard 查看
   - 复制 Account ID

3. **添加 GitHub Secrets**
   ```
   CLOUDFLARE_API_TOKEN = 你的 Token
   CLOUDFLARE_ACCOUNT_ID = 你的 Account ID
   ```

4. **完成！**

**优点**:
- ✅ 带宽无限制
- ✅ Cloudflare CDN
- ✅ 完全自动化

**缺点**:
- ⚠️ 首次需要创建 Project（5 分钟）
- ⚠️ 构建次数有限（500 次/月）

---

### 方案 3：Vercel

**自动化流程**:
类似 Netlify

**配置步骤**:
1. **获取 Vercel Token**
   - 访问 https://vercel.com/account/tokens
   - 创建 Token
   - 复制 Token

2. **获取 Org ID 和 Project ID**
   - 在 Vercel Dashboard 查看

3. **添加 GitHub Secrets**
   ```
   VERCEL_TOKEN = 你的 Token
   VERCEL_ORG_ID = 你的 Org ID
   VERCEL_PROJECT_ID = 你的 Project ID
   ```

**优点**:
- ✅ 自动 HTTPS
- ✅ 全球 CDN

**缺点**:
- ⚠️ 之前遇到认证问题
- ⚠️ 首次需要创建 Project

---

## 🎯 推荐方案：Netlify

### 为什么推荐？
1. **配置最简单**
2. **稳定性最高**
3. **部署速度最快**
4. **免费额度足够**

### 需要你配合的事项

**必须项（一次性配置，5 分钟）**:
1. ✅ GitHub 账号（已有：wanibbo）
2. ⏳ Netlify 账号（可用 GitHub 登录，1 分钟）
3. ⏳ 创建 Personal Access Token（2 分钟）
4. ⏳ 添加 GitHub Secrets（2 分钟）

**之后完全自动化**:
- ✅ 每天 8:00 自动抓取
- ✅ 自动 Commit & Push
- ✅ 自动部署
- ✅ 无需人工干预

---

## 📋 完整配置步骤

### 第 1 步：推送代码到 GitHub
```bash
cd /home/admin/openclaw/workspace/skills/ai-daily-news

git init
git add -A
git commit -m "AI Daily News with auto-deploy"

git remote add origin https://github.com/wanibbo/ai-daily-news.git
git branch -M main
git push -u origin main
```

### 第 2 步：创建 Netlify 站点（首次）
1. 访问 https://app.netlify.com
2. GitHub 登录
3. Add new site → Import with GitHub
4. 选择 `ai-daily-news` 仓库
5. Deploy
6. 获得 Site ID

### 第 3 步：获取 Netlify Token
1. 访问 https://app.netlify.com/account/applications
2. Create new personal access token
3. 复制 Token

### 第 4 步：添加 GitHub Secrets
1. 访问 https://github.com/wanibbo/ai-daily-news/settings/secrets/actions
2. 添加以下 Secrets:
   - `NETLIFY_AUTH_TOKEN` = 你的 Token
   - `NETLIFY_SITE_ID` = 你的 Site ID

### 第 5 步：测试部署
1. 访问 https://github.com/wanibbo/ai-daily-news/actions
2. 查看 "Auto Deploy to Multiple Platforms" 工作流
3. 确认部署成功

---

## ⏰ 自动化流程

**每天执行**:
```
00:00 UTC (08:00 北京时间)
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
Git Commit & Push
    ↓
Netlify 自动检测变化
    ↓
自动重新部署
    ↓
外网可访问
```

---

## 📊 方案对比总结

| 特性 | Netlify | Cloudflare | Vercel |
|------|---------|------------|--------|
| 配置难度 | ⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐ |
| 部署速度 | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ |
| 稳定性 | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ |
| 免费额度 | 100GB/月 | 500 次构建 | 100GB/月 |
| 推荐度 | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐ |

---

## 🚀 立即执行

**需要你配合的步骤**:
1. ⏳ 推送代码到 GitHub（我可以帮你执行）
2. ⏳ Netlify 登录（1 分钟）
3. ⏳ 创建 Token（2 分钟）
4. ⏳ 添加 Secrets（2 分钟）

**总计时间**: 5-10 分钟（一次性配置）

**配置完成后**:
- ✅ 完全自动化
- ✅ 无需人工干预
- ✅ 每天自动更新

---

**状态**: ⏳ 等待你确认方案  
**推荐**: Netlify  
**需要你**: 5 分钟配置时间
