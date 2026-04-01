# 🔧 推送错误解决方案

## ❌ 错误原因

```
refusing to allow a Personal Access Token to create or update workflow 
`.github/workflows/auto-deploy-all.yml` without `workflow` scope
```

**原因**: 当前使用的 GitHub Token 缺少 `workflow` 权限

---

## ✅ 解决方案：重新创建 Token

### 步骤 1：创建新的 Personal Access Token

1. 访问：https://github.com/settings/tokens

2. 找到旧的 Token 并删除（可选）

3. 点击 **"Generate new token (classic)"**

4. 填写信息：
   - **Note**: `AI Daily News Deploy`
   - **Expiration**: `No expiration`
   - **Scopes**（权限）**: 勾选以下所有：
     - ✅ **`repo`** (Full control of private repositories)
     - ✅ **`workflow`** (Update GitHub Action workflows) ← 关键！
     - ✅ `admin:repo_hook` (可选，用于管理 webhooks)

5. 点击 **"Generate token"**

6. **立即复制 Token**（格式：`ghp_xxxxxxxxxxxx`）

---

### 步骤 2：使用新 Token 推送

```bash
cd /home/admin/openclaw/workspace/skills/ai-daily-news

# 将 <NEW_TOKEN> 替换为新的 Token
git remote set-url origin https://ghp_<NEW_TOKEN>@github.com/wanibbo/ai-daily-news.git

# 强制推送（因为本地历史更完整）
git push --force --set-upstream origin main
```

---

### 步骤 3：验证推送

推送成功后，访问：
- 仓库：https://github.com/wanibbo/ai-daily-news
- 提交历史：https://github.com/wanibbo/ai-daily-news/commits/main
- Actions: https://github.com/wanibbo/ai-daily-news/actions

应该能看到最新提交：`b99d96f 添加自动部署脚本`

---

## 🎯 快速命令（复制粘贴）

```bash
# 1. 创建 Token 后，替换 <NEW_TOKEN> 并执行
cd /home/admin/openclaw/workspace/skills/ai-daily-news
git remote set-url origin https://ghp_<NEW_TOKEN>@github.com/wanibbo/ai-daily-news.git
git push --force --set-upstream origin main

# 2. 推送成功后，访问 Actions 触发部署
# https://github.com/wanibbo/ai-daily-news/actions
```

---

## 📋 Token 权限检查清单

创建 Token 时确保勾选：

- [ ] ✅ `repo` (必须)
- [ ] ✅ `workflow` (必须 - 用于推送 Actions 工作流)
- [ ] ⬜ `admin:repo_hook` (可选)
- [ ] ⬜ `delete_repo` (可选)

---

## ⚠️ 安全提示

1. **Token 只在自己电脑使用**
2. **不要提交到代码仓库**
3. **使用后立即保存好**
4. **如果泄露，立即删除并重新创建**

---

## 🔗 快速链接

- 创建 Token: https://github.com/settings/tokens
- GitHub 仓库：https://github.com/wanibbo/ai-daily-news
- Actions: https://github.com/wanibbo/ai-daily-news/actions

---

**下一步**: 创建带有 `workflow` 权限的新 Token，然后执行推送命令！
