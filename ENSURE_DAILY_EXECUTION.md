# ✅ 确保每日自动执行检查清单

## 📊 当前配置状态

### GitHub Actions 工作流

**文件**: `.github/workflows/daily-update.yml`

```yaml
name: Daily AI News Update

on:
  schedule:
    - cron: '0 0 * * *'  # 每天 UTC 0 点（北京时间 8 点）
  workflow_dispatch:  # 允许手动触发
```

**状态**: ✅ 配置正确

---

## ✅ 验证步骤

### 步骤 1：确认工作流已启用

访问：https://github.com/wanibbo/ai-daily-news/actions

**检查项**:
- [ ] 工作流列表中有 "Daily AI News Update"
- [ ] 工作流状态是启用（绿色圆点，不是禁用）
- [ ] 最近有运行记录

**如果工作流被禁用**:
- 点击工作流名称
- 点击 "Enable workflow" 按钮

---

### 步骤 2：验证 Cron 调度

**当前配置**: `cron: '0 0 * * *'`

**执行时间**:
- UTC 时间：每天 0:00
- 北京时间：每天 8:00（UTC+8）

**如果需要修改时间**:

编辑 `.github/workflows/daily-update.yml`:

```yaml
# 北京时间早上 8 点（推荐）
- cron: '0 0 * * *'

# 北京时间早上 9 点
- cron: '0 1 * * *'

# 北京时间晚上 8 点
- cron: '0 12 * * *'
```

---

### 步骤 3：检查 GitHub Secrets

访问：https://github.com/wanibbo/ai-daily-news/settings/secrets/actions

**必需配置**（用于 Netlify 部署）:
- [ ] `NETLIFY_AUTH_TOKEN` - Netlify Personal Access Token
- [ ] `NETLIFY_SITE_ID` - Netlify Site ID

**可选配置**（其他平台）:
- [ ] `CLOUDFLARE_API_TOKEN`
- [ ] `CLOUDFLARE_ACCOUNT_ID`
- [ ] `VERCEL_TOKEN`
- [ ] `VERCEL_ORG_ID`
- [ ] `VERCEL_PROJECT_ID`

---

### 步骤 4：测试手动触发

访问：https://github.com/wanibbo/ai-daily-news/actions/workflows/daily-update.yml

1. 点击 **"Run workflow"** 按钮
2. 选择分支 `main`
3. 点击 **"Run workflow"**
4. 等待 2-5 分钟
5. 检查运行结果

**预期结果**:
- ✅ 工作流运行成功（绿色勾）
- ✅ 生成了新的日报文件
- ✅ 代码已推送到仓库
- ✅ Netlify 部署成功（如果配置了）

---

### 步骤 5：验证自动推送权限

访问：https://github.com/wanibbo/ai-daily-news/settings/actions

**检查项**:
- [ ] **Workflow permissions** 设置为 "Read and write permissions"
- [ ] 勾选 "Allow GitHub Actions to create and approve pull requests"（可选）

**如果权限不足**:
- 工作流会失败在 `git push` 步骤
- 错误信息：`! [remote rejected] main -> main`

---

## 🔍 故障排查

### 问题 1：工作流不运行

**可能原因**:
- 工作流被禁用
- Cron 表达式错误
- 仓库长时间无活动

**解决方案**:
1. 手动触发一次工作流激活
2. 检查 `.github/workflows/daily-update.yml` 语法
3. 提交一次代码激活仓库

---

### 问题 2：推送失败

**错误信息**:
```
! [remote rejected] main -> main (refusing to allow a Personal Access Token to create or update workflow without `workflow` scope)
```

**原因**: GitHub Token 缺少 `workflow` 权限

**解决方案**:
1. 重新创建 Personal Access Token
2. 确保勾选 `workflow` 权限
3. 更新 GitHub Secrets

---

### 问题 3：Netlify 部署失败

**错误信息**:
```
Error: Invalid NETLIFY_AUTH_TOKEN or NETLIFY_SITE_ID
```

**解决方案**:
1. 检查 Netlify Token 是否过期
2. 验证 Site ID 是否正确
3. 确认 Netlify 站点已创建

---

## 📋 日常监控

### 每周检查（建议）

**检查频率**: 每周一早上

**检查项**:
1. 访问：https://github.com/wanibbo/ai-daily-news/actions
2. 查看上周运行记录
3. 确认没有失败的运行
4. 检查 `history/` 目录文件完整性

### 配置通知（推荐）

**GitHub 邮件通知**:
1. 访问：https://github.com/notifications
2. 点击 "Customize notifications"
3. 勾选 "Actions" 通知

**仓库通知**:
1. 访问：https://github.com/wanibbo/ai-daily-news
2. 点击右上角 🔔 图标
3. 选择 "Watching" 或 "Custom"

---

## 🛡️ 预防措施

### 1. 添加状态徽章

在 README.md 中添加：

```markdown
![Daily Update](https://github.com/wanibbo/ai-daily-news/actions/workflows/daily-update.yml/badge.svg)
```

这样可以直观看到工作流状态。

---

### 2. 配置失败通知

编辑 `.github/workflows/daily-update.yml`:

```yaml
on:
  schedule:
    - cron: '0 0 * * *'
  workflow_dispatch:

jobs:
  update:
    runs-on: ubuntu-latest
    # 添加失败通知
    env:
      SLACK_WEBHOOK: ${{ secrets.SLACK_WEBHOOK }}  # 可选
    steps:
      # ... 现有步骤 ...
      
      - name: Notify on failure
        if: failure()
        run: |
          # 发送通知（Slack/Discord/邮件等）
          curl -X POST $SLACK_WEBHOOK -d '{"text":"日报生成失败！"}'
```

---

### 3. 定期备份

**每月检查**:
- 下载 `history/` 目录备份
- 检查 Netlify 部署状态
- 验证访问 URL 正常

---

## 📊 完整检查清单

### 初次配置

- [ ] 工作流文件存在且语法正确
- [ ] 工作流已启用（绿色圆点）
- [ ] GitHub Secrets 已配置
- [ ] Netlify 站点已创建
- [ ] 手动触发测试成功
- [ ] 自动推送权限已授予

### 每周检查

- [ ] 访问 Actions 页面查看运行历史
- [ ] 确认最近 7 天都有成功运行
- [ ] 检查 `history/` 目录文件完整性
- [ ] 验证 Netlify 访问正常

### 每月维护

- [ ] 检查 Token 是否过期
- [ ] 备份历史数据
- [ ] 更新依赖包版本
- [ ] 检查 AI 关键词列表

---

## 🔗 快速链接

| 功能 | 链接 |
|------|------|
| **Actions 首页** | https://github.com/wanibbo/ai-daily-news/actions |
| **工作流配置** | https://github.com/wanibbo/ai-daily-news/blob/main/.github/workflows/daily-update.yml |
| **Secrets 设置** | https://github.com/wanibbo/ai-daily-news/settings/secrets/actions |
| **权限设置** | https://github.com/wanibbo/ai-daily-news/settings/actions |
| **Netlify 控制台** | https://app.netlify.com |
| **运行历史** | https://github.com/wanibbo/ai-daily-news/actions/workflows/daily-update.yml |

---

## 🎯 总结

**当前状态**: ✅ 配置正确，已就绪

**关键点**:
1. ✅ Cron 调度：每天 UTC 0 点（北京时间 8 点）
2. ✅ 工作流：已启用
3. ⏳ 需要配置：GitHub Secrets（Netlify Token）
4. ⏳ 需要验证：手动触发测试

**下一步**:
1. 手动触发一次工作流测试
2. 配置 Netlify Secrets（如需部署）
3. 设置通知提醒
4. 建立每周检查习惯

---

**记住**: GitHub Actions 免费额度充足（每月 2000 分钟），每日运行完全够用！
