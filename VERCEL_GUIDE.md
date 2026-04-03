# 🚀 Vercel 部署完整指南

## 方式 1：通过 GitHub 部署（推荐）

### 第 1 步：创建 GitHub 仓库

1. 访问 https://github.com/new
2. 仓库名：`ai-daily-news`
3. 设置为 Public
4. 点击 "Create repository"

### 第 2 步：推送代码到 GitHub

```bash
cd /home/admin/openclaw/workspace/skills/ai-daily-news

# 添加远程仓库（替换 YOUR_USERNAME 为你的 GitHub 用户名）
git remote add origin https://github.com/YOUR_USERNAME/ai-daily-news.git

# 推送代码
git push -u origin master
```

### 第 3 步：在 Vercel 部署

1. 访问 https://vercel.com/new
2. 点击 **"Continue with GitHub"**
3. 授权 Vercel 访问 GitHub
4. 点击 **"Import Git Repository"**
5. 找到 `ai-daily-news` 仓库
6. 点击 **"Import"**
7. 配置保持默认
8. 点击 **"Deploy"**

### 第 4 步：获得外网 URL

部署完成后获得：
```
https://ai-daily-news-xxxx.vercel.app
```

---

## 方式 2：Vercel CLI 部署（需要登录）

```bash
cd /home/admin/openclaw/workspace/skills/ai-daily-news

# 1. 登录 Vercel
vercel login

# 2. 部署
vercel --prod
```

---

## 方式 3：Vercel 官网拖拽（无需 Git）

1. 访问 https://vercel.com/new
2. 用 GitHub 登录
3. 选择 "Add New Project"
4. 选择 "Import Third Party Git" 或创建空项目
5. 手动上传文件

---

## ⚡ 快速部署脚本

```bash
#!/bin/bash
# 快速部署到 Vercel

cd /home/admin/openclaw/workspace/skills/ai-daily-news

# 检查是否已登录
if ! vercel whoami &>/dev/null; then
    echo "🔐 请先登录 Vercel"
    vercel login
fi

# 部署
echo "🚀 开始部署..."
vercel --prod

echo "✅ 部署完成！"
```

---

## 📊 部署配置

**Vercel 配置**（vercel.json 已创建）：

```json
{
  "buildCommand": null,
  "devCommand": null,
  "installCommand": null,
  "outputDirectory": ".",
  "public": true
}
```

**说明**：
- 无需构建（纯静态文件）
- 直接部署当前目录
- 自动识别 index.html

---

## 🎯 推荐流程

**最快方式**（5 分钟）：

1. **创建 GitHub 仓库**
   - 访问 https://github.com/new
   - 仓库名：`ai-daily-news`
   - 创建

2. **推送代码**
   ```bash
   cd /home/admin/openclaw/workspace/skills/ai-daily-news
   git remote add origin https://github.com/YOUR_USERNAME/ai-daily-news.git
   git push -u origin master
   ```

3. **Vercel 部署**
   - 访问 https://vercel.com/new
   - GitHub 登录
   - 选择仓库
   - Deploy

4. **完成！**
   - 获得 URL：`https://ai-daily-news-xxxx.vercel.app`

---

## 📱 访问部署后的网站

部署成功后访问：
```
https://ai-daily-news-xxxx.vercel.app
```

**功能**：
- ✅ 今日 AI 日报（10 条精选）
- ✅ 多数据源（量子位、InfoQ、雷锋网）
- ✅ 智能摘要
- ✅ 历史日报栏
- ✅ 手机适配
- ✅ 自动 HTTPS
- ✅ 全球 CDN

---

## 🔄 自动更新

### 连接 GitHub 后

每次 push 到 GitHub 仓库，Vercel 会自动重新部署！

```bash
# 更新日报后
cd /home/admin/openclaw/workspace/skills/ai-daily-news
python3 skill_v12.py
git add -A
git commit -m "更新日报 $(date +%Y-%m-%d)"
git push
```

Vercel 会自动检测并重新部署！

---

## 📞 需要帮助？

1. **查看部署状态**：https://vercel.com/dashboard
2. **查看日志**：https://vercel.com/[project]/activity
3. **自定义域名**：Vercel 设置 → Domains

---

**状态**: ⏳ 等待部署  
**推荐**: GitHub + Vercel  
**时间**: 约 5 分钟  
**结果**: 永久外网 URL
