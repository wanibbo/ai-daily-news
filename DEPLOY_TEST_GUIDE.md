# 🚀 测试部署 - 完整指南

**当前状态**: 代码已准备好，需要推送到 GitHub 触发部署

---

## 📊 当前本地状态

```bash
✅ 最新提交：b99d96f 添加自动部署脚本
✅ 工作区：干净
✅ 分支：main
✅ 远程：origin (https://github.com/wanibbo/ai-daily-news.git)
```

---

## 🔧 推送代码到 GitHub（3 种方法）

### 方法 1：使用 GitHub Token（推荐 ⭐）

**步骤 1：创建 Personal Access Token**

1. 访问：https://github.com/settings/tokens
2. 点击 **"Generate new token (classic)"**
3. 填写：
   - Note: `AI Daily News Deploy`
   - Expiration: `No expiration`
   - Scopes: 勾选 **`repo`** (Full control of private repositories)
4. 点击 **"Generate token"**
5. **立即复制 Token**（格式：`ghp_xxxxxxxxxxxx`）

**步骤 2：使用 Token 推送**

```bash
cd /home/admin/openclaw/workspace/skills/ai-daily-news

# 将 <YOUR_TOKEN> 替换为实际的 Token
git remote set-url origin https://ghp_xxxxxxxxxxxx@github.com/wanibbo/ai-daily-news.git

# 推送
git push --set-upstream origin main
```

---

### 方法 2：配置 SSH 密钥

**步骤 1：生成 SSH 密钥**

```bash
ssh-keygen -t ed25519 -C "your_email@example.com"
# 连续按回车使用默认设置
```

**步骤 2：添加公钥到 GitHub**

1. 复制公钥：
   ```bash
   cat ~/.ssh/id_ed25519.pub
   ```

2. 访问：https://github.com/settings/keys
3. 点击 **"New SSH key"**
4. 粘贴公钥，保存

**步骤 3：更改 remote 为 SSH**

```bash
cd /home/admin/openclaw/workspace/skills/ai-daily-news
git remote set-url origin git@github.com:wanibbo/ai-daily-news.git
git push --set-upstream origin main
```

---

### 方法 3：使用 Git Credential Manager（桌面用户）

```bash
cd /home/admin/openclaw/workspace/skills/ai-daily-news
git push --set-upstream origin main
```

系统会弹出浏览器窗口，登录 GitHub 授权即可。

---

## ✅ 推送成功后

### 1. 验证推送

访问：https://github.com/wanibbo/ai-daily-news/commits/main

应该能看到最新提交：`b99d96f 添加自动部署脚本`

### 2. 手动触发部署

访问：https://github.com/wanibbo/ai-daily-news/actions

1. 点击左侧 **"Auto Deploy to Multiple Platforms"**
2. 点击 **"Run workflow"** 按钮
3. 选择分支 `main`
4. 点击 **"Run workflow"**

### 3. 查看部署进度

- 工作流运行时间：约 2-5 分钟
- 实时日志：点击运行中的任务查看
- 部署成功：显示绿色 ✅

### 4. 访问部署的站点

部署成功后，Netlify 会生成一个临时域名：

```
https://ai-daily-news-xxxxx.netlify.app
```

可以在 Netlify 控制台自定义域名。

---

## 🔍 故障排查

### 问题 1：推送失败 "could not read Username"

**原因**: Git 需要认证

**解决**: 使用方法 1（Token）或方法 2（SSH）

---

### 问题 2：GitHub Actions 没有运行

**原因**: 可能未配置 Secrets 或工作流被禁用

**检查**:
1. 访问：https://github.com/wanibbo/ai-daily-news/actions
2. 确认工作流未被禁用（绿色圆点）
3. 检查 Secrets 是否已配置

---

### 问题 3：Netlify 部署失败

**常见原因**:
- `NETLIFY_AUTH_TOKEN` 错误
- `NETLIFY_SITE_ID` 错误
- Netlify 站点未创建

**解决**:
1. 检查 GitHub Secrets 是否正确
2. 确认 Netlify 站点已创建
3. 查看 Actions 日志获取详细错误

---

## 📋 快速检查清单

- [ ] GitHub 账号已登录
- [ ] 仓库 `wanibbo/ai-daily-news` 存在
- [ ] Personal Access Token 已创建（方法 1）
   - 或 SSH 密钥已配置（方法 2）
- [ ] 代码已推送到 GitHub
- [ ] GitHub Actions 工作流已触发
- [ ] Netlify 站点已创建（可选，用于生产部署）
- [ ] GitHub Secrets 已配置（可选，用于自动部署）

---

## 🎯 最简测试流程（5 分钟）

```bash
# 1. 创建 Token（https://github.com/settings/tokens）
#    勾选 repo 权限，复制 ghp_xxx...

# 2. 配置 remote
cd /home/admin/openclaw/workspace/skills/ai-daily-news
git remote set-url origin https://ghp_xxxxxxxxxxxx@github.com/wanibbo/ai-daily-news.git

# 3. 推送
git push --set-upstream origin main

# 4. 访问 Actions
# https://github.com/wanibbo/ai-daily-news/actions

# 5. 手动触发工作流
# 点击 "Auto Deploy to Multiple Platforms" → "Run workflow"
```

---

## 📞 需要帮助？

推送完成后告诉我，我可以帮你：
- 检查 GitHub Actions 状态
- 查看部署日志
- 验证部署结果
- 配置 Netlify 自动部署

---

**下一步**: 选择一种方法推送代码到 GitHub，然后触发 Actions 工作流！
