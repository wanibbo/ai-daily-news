# 🤖 AI 日报 - 自动部署方案

## 需求
- ✅ 每天早上 8 点自动抓取新闻
- ✅ 自动生成 HTML 日报
- ✅ 自动部署到外网
- ✅ 外网可访问

---

## 方案对比

### 方案 1：GitHub Actions + Vercel（⭐最推荐）

**架构**：
```
GitHub Actions (定时触发)
    ↓
抓取新闻 + 生成 HTML
    ↓
Push 到 GitHub
    ↓
Vercel 自动部署
    ↓
外网可访问
```

**优点**：
- ✅ 完全免费
- ✅ 自动 HTTPS
- ✅ 全球 CDN
- ✅ 永久 URL
- ✅ 无需服务器

**缺点**：
- ⚠️ 需要 GitHub 账号
- ⚠️ 首次配置需要 10 分钟

**配置步骤**：

1. **创建 GitHub 仓库**
   ```bash
   cd /home/admin/openclaw/workspace/skills/ai-daily-news
   git init
   git add -A
   git commit -m "Initial commit"
   git remote add origin https://github.com/wanibbo/ai-daily-news.git
   git push -u origin main
   ```

2. **创建 GitHub Actions 工作流**
   
   创建 `.github/workflows/daily-update.yml`：
   ```yaml
   name: Daily AI News Update
   
   on:
     schedule:
       - cron: '0 0 * * *'  # 每天 UTC 0 点（北京时间 8 点）
     workflow_dispatch:  # 允许手动触发
   
   jobs:
     update:
       runs-on: ubuntu-latest
       steps:
         - uses: actions/checkout@v3
         
         - name: Setup Python
           uses: actions/setup-python@v4
           with:
             python-version: '3.10'
         
         - name: Install dependencies
           run: |
             pip install aiohttp beautifulsoup4 lxml
         
         - name: Generate daily news
           run: python skill_v12.py
         
         - name: Commit and push
           run: |
             git config user.name "AI Assistant"
             git config user.email "ai@example.com"
             git add -A
             git commit -m "Daily update $(date +%Y-%m-%d)" || echo "No changes"
             git push
   ```

3. **连接 Vercel**
   - 访问 https://vercel.com
   - GitHub 登录
   - Import Git Repository
   - 选择 `ai-daily-news` 仓库
   - Deploy

4. **获得外网 URL**
   ```
   https://ai-daily-news-wanibbo.vercel.app
   ```

---

### 方案 2：云服务器 + Nginx + Cron

**架构**：
```
Cron 定时任务 (8:00)
    ↓
执行 Python 脚本
    ↓
生成 HTML 到 /var/www/ai-daily
    ↓
Nginx 提供 Web 服务
    ↓
外网通过公网 IP 访问
```

**优点**：
- ✅ 完全控制
- ✅ 无需第三方服务
- ✅ 数据私有

**缺点**：
- ⚠️ 需要云服务器
- ⚠️ 需要配置 Nginx
- ⚠️ 需要自己管理 HTTPS

**配置步骤**：

1. **安装 Nginx**
   ```bash
   sudo apt update
   sudo apt install nginx -y
   ```

2. **配置 Nginx**
   ```bash
   sudo nano /etc/nginx/sites-available/ai-daily
   ```
   
   添加配置：
   ```nginx
   server {
       listen 80;
       server_name your-domain.com;  # 或公网 IP
       
       location / {
           root /var/www/ai-daily;
           index index.html;
           try_files $uri $uri/ =404;
       }
   }
   ```

3. **启用配置**
   ```bash
   sudo ln -s /etc/nginx/sites-available/ai-daily /etc/nginx/sites-enabled/
   sudo nginx -t
   sudo systemctl restart nginx
   ```

4. **配置 Cron**
   ```bash
   crontab -e
   # 添加：
   0 8 * * * cd /home/admin/openclaw/workspace/skills/ai-daily-news && python3 skill_v12.py && cp index.html history/ && cp -r history/* /var/www/ai-daily/history/
   ```

---

### 方案 3：Cloudflare Pages + GitHub Actions

**类似方案 1**，但使用 Cloudflare Pages 代替 Vercel。

**优点**：
- ✅ 免费额度更大
- ✅ Cloudflare CDN
- ✅ 自动 HTTPS

**步骤**：
1. 创建 GitHub 仓库
2. 配置 GitHub Actions
3. 连接 Cloudflare Pages
4. 获得 URL：`https://ai-daily-news.pages.dev`

---

## 🎯 推荐方案：GitHub Actions + Vercel

### 为什么推荐？

1. **完全免费** - 无需服务器费用
2. **自动部署** - Push 代码后自动部署
3. **自动 HTTPS** - 无需配置证书
4. **全球 CDN** - 访问速度快
5. **永久 URL** - 域名稳定

### 需要你配合的事项

**需要提供的信息**：
1. ✅ GitHub 账号（已有：wanibbo）
2. ⏳ Vercel 账号（需要注册）
3. ⏳ 授权 Vercel 访问 GitHub 仓库

**我来帮你做**：
1. ✅ 创建 GitHub Actions 工作流文件
2. ✅ 配置自动抓取脚本
3. ✅ 配置 Vercel 部署设置
4. ⏳ 需要你点击授权

---

## 📋 执行清单

### 任务 1：虎嗅网替代方案
- [ ] 测试其他新闻源（36 氪、钛媒体等）
- [ ] 选择最佳替代源
- [ ] 集成到代码

### 任务 2：InfoQ/雷锋网摘要
- [ ] 检查摘要函数
- [ ] 修复内容提取
- [ ] 测试验证

### 任务 3：自动部署
- [ ] 创建 GitHub Actions 工作流
- [ ] 配置 Vercel 部署
- [ ] 测试自动更新
- [ ] 配置定时任务

---

## ⏰ 预计时间

- 任务 1：10 分钟
- 任务 2：5 分钟
- 任务 3：15 分钟（需要你配合授权）
- **总计**：30 分钟

---

**状态**: ⏳ 准备执行  
**需要你的帮助**: Vercel 账号授权  
**预计完成**: 30 分钟内
