# 🔧 Netlify 部署配置检查清单

## ✅ 本地配置检查

### 1. GitHub 仓库配置
- ✅ 仓库地址：`https://github.com/wanibbo/ai-daily-news`
- ✅ 当前分支：`main`
- ✅ 最新提交：`cf732e7 更新虎嗅 OCR 和界面新闻关键词`
- ✅ 工作区干净：无未提交更改

### 2. GitHub Actions 工作流
- ✅ `auto-deploy-all.yml` - 多平台部署
- ✅ `daily-update.yml` - 每日自动更新
- ✅ `deploy-to-netlify.yml` - Netlify 专用部署
- ✅ `deploy-to-vercel.yml` - Vercel 部署

### 3. Netlify 配置文件
- ✅ `netlify.toml` 已存在
- ✅ 构建配置正确（无需构建命令）
- ✅ 发布目录：当前目录 `.`

---

## ⏳ 需要在 Netlify 配置的事项

### 步骤 1：创建 Netlify 站点

1. 访问：https://app.netlify.com
2. 点击 **"Add new site"** → **"Import an existing project"**
3. 选择 **GitHub**
4. 搜索并选择 `wanibbo/ai-daily-news` 仓库
5. 点击 **"Deploy site"**

**无需配置构建设置**（已有 netlify.toml）

---

### 步骤 2：获取 Site ID

部署完成后：

1. 进入站点 **Site settings**
2. 在 **General** → **Site details** 中找到
3. **Site ID** 格式：`xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx`

---

### 步骤 3：创建 Personal Access Token

1. 访问：https://app.netlify.com/user/applications#personal-access-tokens
2. 点击 **"New personal access token"**
3. 填写：
   - Description: `AI Daily News Deploy`
   - Expiration: `No expiration`
   - Scopes: 勾选 `sites:write`, `sites:read`, `deploys:write`
4. 点击 **"Generate token"**
5. **立即复制 Token**（只会显示一次）

Token 格式：`nfp_xxxxxxxxxxxxxxxxxxxx`

---

### 步骤 4：添加 GitHub Secrets

访问：https://github.com/wanibbo/ai-daily-news/settings/secrets/actions

添加以下两个 Repository secrets：

| Name | Value |
|------|-------|
| `NETLIFY_AUTH_TOKEN` | 步骤 3 创建的 Token |
| `NETLIFY_SITE_ID` | 步骤 2 获取的 Site ID |

---

## ✅ 验证部署

### 方法 1：手动触发工作流

1. 访问：https://github.com/wanibbo/ai-daily-news/actions
2. 点击 **"Auto Deploy to Multiple Platforms"**
3. 点击 **"Run workflow"** → **"Run workflow"**
4. 等待 2-3 分钟

### 方法 2：推送代码触发

```bash
cd /home/admin/openclaw/workspace/skills/ai-daily-news
echo "# 测试部署" >> README.md
git add README.md
git commit -m "test deploy"
git push
```

---

## 📊 配置状态总结

| 项目 | 状态 | 说明 |
|------|------|------|
| GitHub 仓库 | ✅ 已配置 | `wanibbo/ai-daily-news` |
| 工作流文件 | ✅ 已创建 | 4 个 workflow 文件 |
| netlify.toml | ✅ 已配置 | 静态站点配置 |
| Netlify 站点 | ⏳ 待创建 | 需要登录 Netlify |
| Personal Access Token | ⏳ 待创建 | 需要 Netlify 账户 |
| GitHub Secrets | ⏳ 待配置 | 需要 Token 和 Site ID |

---

## 🎯 下一步操作

**按顺序执行**：

1. **登录 Netlify** → https://app.netlify.com
2. **创建站点** → 导入 GitHub 仓库
3. **获取 Site ID** → 从站点设置复制
4. **创建 Token** → Personal access tokens
5. **配置 Secrets** → GitHub 仓库设置
6. **测试部署** → 手动触发工作流

**预计时间**：10 分钟

---

## 🔗 快速链接

- Netlify 登录：https://app.netlify.com
- Netlify Tokens：https://app.netlify.com/user/applications#personal-access-tokens
- GitHub Secrets：https://github.com/wanibbo/ai-daily-news/settings/secrets/actions
- GitHub Actions：https://github.com/wanibbo/ai-daily-news/actions
