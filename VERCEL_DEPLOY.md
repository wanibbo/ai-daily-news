# 🚀 Vercel 部署指南

## 方式 1：Vercel 官网部署（推荐）

### 步骤

1. **访问 Vercel 官网**
   ```
   https://vercel.com
   ```

2. **注册/登录**
   - 使用 GitHub 账号登录（推荐）
   - 或使用邮箱注册

3. **导入项目**
   - 点击 "Add New Project"
   - 选择 "Import Git Repository"
   - 如果没有 GitHub 仓库，选择 "Import Third Party Git"

4. **本地上传（无需 Git）**
   
   访问：https://vercel.com/new
   
   或者使用 Vercel CLI：
   ```bash
   cd /home/admin/openclaw/workspace/skills/ai-daily-news
   vercel login
   vercel --prod
   ```

### 配置

- **Build Command**: 留空（无需构建）
- **Output Directory**: 留空（当前目录）
- **Install Command**: 留空

### 获得 URL

部署成功后获得：
```
https://ai-daily-xxxx.vercel.app
```

---

## 方式 2：Netlify 部署（同样推荐）

### 步骤

1. **访问 Netlify**
   ```
   https://app.netlify.com
   ```

2. **注册/登录**
   - 使用 GitHub 账号登录

3. **拖拽部署**
   - 将 `ai-daily-news` 文件夹拖到 Netlify
   - 或连接 GitHub 仓库

### 获得 URL

```
https://ai-daily-xxxx.netlify.app
```

---

## 方式 3：Cloudflare Pages（免费）

### 步骤

1. **访问 Cloudflare**
   ```
   https://pages.cloudflare.com
   ```

2. **连接 GitHub**
   - 选择仓库
   - 配置构建设置（无需构建）

### 获得 URL

```
https://ai-daily.pages.dev
```

---

## 📁 当前文件已准备好

```
ai-daily-news/
├── index.html          ✅ 首页
├── news_data.json      ✅ 数据
├── history/            ✅ 历史目录
├── vercel.json         ✅ Vercel 配置
└── ...
```

---

## 🎯 最快的部署方式

### 使用 Vercel 官网（无需 CLI）

1. 打开 https://vercel.com/new
2. 用 GitHub 登录
3. 创建新仓库并上传文件
4. 自动部署

**5 分钟搞定！**

---

**状态**: ⏳ 等待部署  
**推荐**: Vercel 官网部署  
**时间**: 约 5 分钟
