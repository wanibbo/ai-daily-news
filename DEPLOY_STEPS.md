# 🚀 Vercel 部署 - 完整步骤

## 你的 GitHub 用户名：wanibbo

---

## 📝 步骤 1：创建 GitHub 仓库

**浏览器已打开**：https://github.com/new

**操作**：
1. **Repository name**: `ai-daily-news`
2. **Description**: `AI Daily News - 自动抓取 AI 新闻并生成日报`
3. **Public**: ✅ 保持默认
4. **Add README**: ❌ 不勾选
5. 点击 **"Create repository"**

---

## 📤 步骤 2：上传代码到 GitHub

### 方法 A：使用 GitHub 网页上传（最简单）

创建仓库后，在 GitHub 页面：

1. 点击 **"uploading an existing file"**
2. 拖拽以下文件到页面：
   - `index.html`
   - `news_data.json`
   - `history/` 文件夹
   - `vercel.json`
   - `skill.json`
3. 点击 **"Commit changes"**

### 方法 B：使用命令行（需要配置 SSH）

```bash
cd /home/admin/openclaw/workspace/skills/ai-daily-news

# 配置 SSH（如果未配置）
ssh-keygen -t ed25519 -C "your_email@example.com"
# 将 ~/.ssh/id_ed25519.pub 添加到 GitHub Settings → SSH Keys

# 添加远程仓库
git remote add origin git@github.com:wanibbo/ai-daily-news.git

# 推送
git branch -M main
git push -u origin main
```

---

## 🚀 步骤 3：Vercel 部署

### 访问 Vercel

**浏览器打开**：https://vercel.com/new

### 操作步骤

1. **点击**："Continue with GitHub"
2. **授权** Vercel 访问你的 GitHub
3. **点击**："Import Git Repository"
4. **找到**：`wanibbo/ai-daily-news`
5. **点击**："Import"
6. **配置**：保持默认
7. **点击**："Deploy"

---

## 🎉 步骤 4：获得外网 URL

部署完成后（约 1-2 分钟）：

```
🎉 Congratulations! Your deployment is ready.

https://ai-daily-news-xxxx.vercel.app
```

**访问你的网站**：
```
https://ai-daily-news-xxxx.vercel.app
```

---

## 📱 网站功能

- ✅ 今日 AI 日报（10 条精选）
- ✅ 多数据源（量子位、InfoQ、雷锋网）
- ✅ 智能摘要（120 字以内）
- ✅ 热度 + 趣味性排序
- ✅ 右侧历史日报栏
- ✅ 手机适配
- ✅ 自动 HTTPS
- ✅ 全球 CDN

---

## 🔄 自动更新

### 方式 1：GitHub 自动部署

每次 push 到 GitHub，Vercel 会自动重新部署：

```bash
# 更新日报
cd /home/admin/openclaw/workspace/skills/ai-daily-news
python3 skill_v12.py

# 推送到 GitHub
git add -A
git commit -m "更新日报 $(date +%Y-%m-%d)"
git push

# Vercel 会自动重新部署！
```

### 方式 2：手动上传

在 GitHub 仓库页面：
1. 点击 "Add file" → "Upload files"
2. 上传更新的文件
3. Vercel 会自动检测并重新部署

---

## ⏰ 定时任务

**已配置**：每天早上 8:00 自动执行

```bash
# 查看 cron 配置
crontab -l

# 应该看到：
0 8 * * * /home/admin/openclaw/workspace/skills/ai-daily-news/cron_run.sh
```

**自动执行**：
1. 抓取最新 AI 新闻
2. 生成 HTML 日报
3. 保存到 history/
4. 推送到 GitHub（需要配置 SSH）
5. Vercel 自动部署

---

## 📊 部署检查清单

- [ ] 1. 创建 GitHub 仓库（https://github.com/new）
- [ ] 2. 上传代码文件
- [ ] 3. Vercel 部署（https://vercel.com/new）
- [ ] 4. 获得外网 URL
- [ ] 5. 测试访问
- [ ] 6. 配置自动更新（可选）

---

## 🎯 现在开始

### 第 1 步：创建仓库

**访问**：https://github.com/new

**仓库名**：`ai-daily-news`

**点击**："Create repository"

---

### 第 2 步：上传文件

**在 GitHub 仓库页面**：
1. 点击 "uploading an existing file"
2. 上传以下文件：
   - `index.html`
   - `news_data.json`
   - `vercel.json`
   - `skill.json`
   - `history/` 文件夹（如果有）
3. 点击 "Commit changes"

---

### 第 3 步：Vercel 部署

**访问**：https://vercel.com/new

**操作**：
1. GitHub 登录
2. Import Git Repository
3. 选择 `wanibbo/ai-daily-news`
4. Deploy

---

## 📞 需要帮助？

**部署问题**：
- 查看 Vercel 文档：https://vercel.com/docs
- 查看部署日志：Vercel Dashboard → Deployments

**本地问题**：
- 检查状态：`./check_status.sh`
- 重新生成：`python3 skill_v12.py`

---

**状态**: ⏳ 等待创建仓库  
**GitHub**: https://github.com/wanibbo  
**仓库名**: ai-daily-news  
**预计时间**: 5 分钟
