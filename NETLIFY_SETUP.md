# 🌐 Netlify 部署配置指南

**更新时间**: 2026-04-01 11:07

---

## ⚠️ 当前问题

**症状**: Netlify 上还是昨天的日报，没有更新

**原因**: GitHub Secrets 未配置，导致部署失败

---

## ✅ 解决方案

### 步骤 1：创建 Netlify 账号（如果没有）

访问：https://app.netlify.com

使用 **GitHub 账号登录**（推荐）

---

### 步骤 2：创建站点

1. 登录后点击 **"Add new site"**
2. 选择 **"Import an existing project"**
3. 选择 **GitHub**
4. 搜索并授权 `wanibbo/ai-daily-news` 仓库
5. 点击 **"Deploy site"**

**无需配置构建设置**（已有 netlify.toml）

---

### 步骤 3：获取 Site ID

1. 进入站点 **Site settings**
2. 在 **General** → **Site details** 中找到
3. **Site ID** 格式：`xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx`
4. 复制保存

---

### 步骤 4：创建 Personal Access Token

1. 访问：https://app.netlify.com/user/applications#personal-access-tokens
2. 点击 **"New personal access token"**
3. 填写：
   - Description: `AI Daily News Deploy`
   - Expiration: `No expiration`
   - Scopes: 勾选 `sites:write`, `sites:read`, `deploys:write`
4. 点击 **"Generate token"**
5. **立即复制 Token**（格式：`nfp_xxxxxxxxxxxx`）

---

### 步骤 5：添加到 GitHub Secrets

访问：https://github.com/wanibbo/ai-daily-news/settings/secrets/actions

添加两个 Secrets：

| Name | Value |
|------|-------|
| `NETLIFY_AUTH_TOKEN` | 步骤 4 创建的 Token（`nfp_xxx...`） |
| `NETLIFY_SITE_ID` | 步骤 3 获取的 Site ID |

---

### 步骤 6：测试部署

1. 访问：https://github.com/wanibbo/ai-daily-news/actions/workflows/auto-deploy-all.yml
2. 点击 "Run workflow"
3. 等待 3-5 分钟
4. 访问：https://ai-daily-daily.netlify.app/
5. 确认显示今日日报

---

## 🔧 验证配置

### 检查部署状态

访问：https://app.netlify.com/sites/ai-daily-daily/deploys

应该能看到：
- ✅ 最近的部署记录
- ✅ 状态为 "Published"
- ✅ 部署时间对应 GitHub Actions 运行时间

### 检查访问 URL

默认 URL 格式：
```
https://ai-daily-daily.netlify.app/
```

可以在 Netlify 控制台自定义域名。

---

## 📊 部署流程

```
GitHub 代码推送
    ↓
auto-deploy-all.yml 触发
    ↓
等待 2 分钟（确保代码同步）
    ↓
Netlify CLI 安装
    ↓
netlify deploy --prod
    ↓
部署完成（约 2-3 分钟）
    ↓
网站可访问
```

---

## 🛡️ 故障排查

### 问题 1: 部署失败 "Invalid token"

**原因**: Token 错误或过期

**解决**:
1. 重新创建 Token
2. 确认 Scopes 正确
3. 更新 GitHub Secret

### 问题 2: 部署失败 "Site not found"

**原因**: Site ID 错误

**解决**:
1. 确认站点已创建
2. 重新复制 Site ID
3. 更新 GitHub Secret

### 问题 3: 部署成功但内容未更新

**原因**: 缓存问题

**解决**:
1. 访问 Netlify 控制台
2. 点击 "Clear cache and deploy site"
3. 或手动触发工作流

---

## 📋 配置检查清单

- [ ] Netlify 账号已创建
- [ ] 站点已创建（ai-daily-daily）
- [ ] Site ID 已获取
- [ ] Personal Access Token 已创建
- [ ] GitHub Secrets 已添加：
  - [ ] `NETLIFY_AUTH_TOKEN`
  - [ ] `NETLIFY_SITE_ID`
- [ ] 手动测试部署成功
- [ ] 访问 URL 显示最新日报

---

## 🔗 快速链接

| 功能 | 链接 |
|------|------|
| **Netlify 登录** | https://app.netlify.com |
| **创建 Token** | https://app.netlify.com/user/applications#personal-access-tokens |
| **GitHub Secrets** | https://github.com/wanibbo/ai-daily-news/settings/secrets/actions |
| **部署工作流** | https://github.com/wanibbo/ai-daily-news/actions/workflows/auto-deploy-all.yml |
| **Netlify 控制台** | https://app.netlify.com/sites/ai-daily-daily/deploys |
| **访问 URL** | https://ai-daily-daily.netlify.app/ |

---

## 💡 提示

1. **Netlify 免费额度**: 每月 100GB 带宽，足够日常使用
2. **自动部署**: 每次 push 到 main 分支都会触发
3. **部署历史**: Netlify 保留所有部署版本，可随时回滚
4. **自定义域名**: 可在 Netlify 控制台配置

---

**配置完成后，每天 07:08 自动部署最新日报！** 🎉
