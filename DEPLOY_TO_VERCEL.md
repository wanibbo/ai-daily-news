# 🚀 迁移到 Vercel 部署

**原因**: Netlify 额度用完，项目暂停

---

## ✅ Vercel 优势

| 特性 | Vercel | Netlify |
|------|--------|---------|
| **免费带宽** | 100GB/月 | 100GB/月 |
| **免费构建** | 6000 分钟/月 | 300 分钟/月 |
| **部署速度** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ |
| **自动 HTTPS** | ✅ | ✅ |
| **自定义域名** | ✅ | ✅ |

---

## 📋 配置步骤（5 分钟）

### 步骤 1: 创建 Vercel 账号

1. **访问**: https://vercel.com/signup
2. **选择**: "Continue with GitHub"
3. **授权**: 允许访问 GitHub 仓库

---

### 步骤 2: 导入项目

1. **点击**: "Add New Project"
2. **选择**: "Import Git Repository"
3. **搜索**: `ai-daily-news`
4. **点击**: "Import"

---

### 步骤 3: 配置部署

**无需修改配置**，Vercel 会自动识别静态网站：

- **Build Command**: 留空（无需构建）
- **Output Directory**: 留空（当前目录）
- **Install Command**: 留空

**点击**: "Deploy"

---

### 步骤 4: 获取访问 URL

部署完成后，会生成访问 URL：
```
https://ai-daily-news-xxxx.vercel.app
```

**可以自定义**:
- 项目设置 → Domains
- 添加自定义域名

---

## 🔧 配置 GitHub Actions 自动部署

### 修改工作流文件

编辑 `.github/workflows/daily-update.yml`:

```yaml
# 添加 Vercel 部署步骤
- name: Deploy to Vercel
  if: ${{ success() }}
  env:
    VERCEL_TOKEN: ${{ secrets.VERCEL_TOKEN }}
    VERCEL_ORG_ID: ${{ secrets.VERCEL_ORG_ID }}
    VERCEL_PROJECT_ID: ${{ secrets.VERCEL_PROJECT_ID }}
  run: |
    npm install -g vercel
    vercel --prod --token=$VERCEL_TOKEN
```

### 获取 Vercel Secrets

1. **访问 Vercel 控制台**
   ```
   https://vercel.com/dashboard
   ```

2. **获取 Token**
   ```
   Settings → Tokens → Create Token
   复制：xxxxxxxxxxxxx
   ```

3. **获取 Org ID 和 Project ID**
   ```
   项目设置 → General
   复制：Org ID 和 Project ID
   ```

4. **添加到 GitHub Secrets**
   ```
   https://github.com/wanibbo/ai-daily-news/settings/secrets/actions
   
   添加:
   - VERCEL_TOKEN
   - VERCEL_ORG_ID
   - VERCEL_PROJECT_ID
   ```

---

## 🎯 快速部署（无需配置 Actions）

### 方式 1: Vercel 自动部署

**Vercel 会自动监听 GitHub push**:
1. 推送代码到 GitHub
2. Vercel 自动触发部署
3. 2-3 分钟后网站更新

**无需配置 GitHub Actions！**

---

### 方式 2: Vercel CLI 本地部署

```bash
# 安装 Vercel CLI
npm install -g vercel

# 登录
vercel login

# 部署
cd /home/admin/openclaw/workspace/skills/ai-daily-news
vercel --prod
```

---

## 📊 部署对比

| 平台 | 状态 | 免费额度 | 建议 |
|------|------|---------|------|
| **Netlify** | ❌ 暂停 | 100GB/月 | 等待下月恢复 |
| **Vercel** | ✅ 可用 | 100GB/月 | **推荐使用** |
| **Cloudflare Pages** | ✅ 可用 | 无限带宽 | 备选方案 |
| **GitHub Pages** | ✅ 可用 | 100GB/月 | 简单方案 |

---

## 🌐 其他替代方案

### Cloudflare Pages

**优势**:
- ✅ 无限带宽
- ✅ 无限构建次数
- ✅ 全球 CDN

**配置**:
```
访问：https://pages.cloudflare.com/
连接 GitHub → 选择仓库 → 自动部署
```

---

### GitHub Pages

**优势**:
- ✅ 完全免费
- ✅ 无需额外配置
- ✅ 与 GitHub 集成

**配置**:
```
仓库 Settings → Pages
Source: Deploy from branch
Branch: main
Folder: / (root)
```

**劣势**:
- ❌ 无自动部署（需配置 Actions）
- ❌ URL 较长

---

## 🎯 推荐方案

### 立即方案：Vercel

1. **现在配置 Vercel**（5 分钟）
2. **修改钉钉/微信通知链接**
3. **恢复自动部署**

### 长期方案：多平台部署

1. **Vercel**（主用）
2. **Cloudflare Pages**（备用）
3. **Netlify**（5 月 1 日恢复）

---

## 🔗 快速链接

| 功能 | 链接 |
|------|------|
| **Vercel 注册** | https://vercel.com/signup |
| **Vercel 控制台** | https://vercel.com/dashboard |
| **创建 Token** | https://vercel.com/settings/tokens |
| **Cloudflare Pages** | https://pages.cloudflare.com/ |
| **GitHub Pages** | https://pages.github.com/ |

---

## 📝 下一步

**立即执行**:

1. **注册 Vercel**（2 分钟）
   ```
   https://vercel.com/signup
   GitHub 登录
   ```

2. **导入项目**（2 分钟）
   ```
   Add New Project → Import Git Repository
   选择 ai-daily-news
   点击 Deploy
   ```

3. **获取访问 URL**（1 分钟）
   ```
   复制：https://ai-daily-news-xxxx.vercel.app
   ```

4. **更新通知链接**
   ```
   修改工作流中的 URL
   或使用 Vercel 自定义域名
   ```

---

**需要我帮您配置 Vercel 吗？** 🚀
