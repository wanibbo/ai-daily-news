# 🚀 手动触发自动部署

**更新时间**: 2026-04-01 11:13

---

## ✅ 当前状态

- ✅ 今日日报已生成：`report_2026-04-01.html`
- ✅ 代码已推送到 GitHub
- ⏳ Netlify 部署待触发

---

## 📋 触发方式

### 方式 1：GitHub 网页触发（推荐 ⭐）

**步骤**:

1. **访问工作流页面**
   ```
   https://github.com/wanibbo/ai-daily-news/actions/workflows/auto-deploy-all.yml
   ```

2. **点击 "Run workflow" 按钮**
   - 在页面右侧

3. **选择分支**
   - Branch: `main`

4. **点击 "Run workflow"**

5. **等待部署完成**
   - 约 3-5 分钟
   - 绿色勾表示成功

6. **验证部署**
   ```
   https://ai-daily-daily.netlify.app/
   ```

---

### 方式 2：使用 GitHub CLI（如果已安装）

```bash
# 触发工作流
gh workflow run auto-deploy-all.yml --ref main

# 查看运行状态
gh run list --workflow=auto-deploy-all.yml --limit 1

# 查看详细日志
gh run view <RUN_ID> --log
```

---

### 方式 3：使用 curl 命令（需要 Token）

```bash
# 替换 <YOUR_GITHUB_TOKEN> 为你的 GitHub Personal Access Token
curl -X POST \
  -H "Accept: application/vnd.github.v3+json" \
  -H "Authorization: token <YOUR_GITHUB_TOKEN>" \
  https://api.github.com/repos/wanibbo/ai-daily-news/actions/workflows/auto-deploy-all.yml/dispatches \
  -d '{"ref":"main"}'
```

---

## 🔍 验证部署

### 1. 检查 GitHub Actions

访问：https://github.com/wanibbo/ai-daily-news/actions

**查看**:
- ✅ 最近的运行记录
- ✅ 状态为绿色（成功）
- ✅ 运行时间 < 5 分钟

---

### 2. 检查 Netlify

访问：https://app.netlify.com/sites/ai-daily-daily/deploys

**查看**:
- ✅ 最近的部署记录
- ✅ 状态为 "Published"
- ✅ 部署时间对应 Actions 运行时间

---

### 3. 访问网站

访问：https://ai-daily-daily.netlify.app/

**验证**:
- ✅ 显示今日日报（2026-04-01）
- ✅ 页面正常加载
- ✅ 新闻内容正确

---

## ⚠️ 常见问题

### 问题 1: 部署失败 "Invalid token"

**原因**: Netlify Token 错误或未配置

**解决**:
1. 访问：https://github.com/wanibbo/ai-daily-news/settings/secrets/actions
2. 检查 `NETLIFY_AUTH_TOKEN` 是否正确
3. 重新创建 Token 并更新

---

### 问题 2: 部署失败 "Site not found"

**原因**: Site ID 错误或站点未创建

**解决**:
1. 访问 Netlify 创建站点
2. 获取正确的 Site ID
3. 更新 `NETLIFY_SITE_ID` Secret

---

### 问题 3: 部署成功但内容未更新

**原因**: 缓存问题

**解决**:
1. 访问 Netlify 控制台
2. 点击 "Clear cache and deploy site"
3. 或重新触发工作流

---

## 📊 部署流程

```
触发工作流
    ↓
等待 2 分钟（代码同步）
    ↓
安装 Netlify CLI
    ↓
netlify deploy --prod
    ↓
部署完成（2-3 分钟）
    ↓
网站可访问
```

---

## 🔗 快速链接

| 功能 | 链接 |
|------|------|
| **触发部署** | https://github.com/wanibbo/ai-daily-news/actions/workflows/auto-deploy-all.yml |
| **Actions 历史** | https://github.com/wanibbo/ai-daily-news/actions |
| **Netlify 控制台** | https://app.netlify.com/sites/ai-daily-daily/deploys |
| **访问 URL** | https://ai-daily-daily.netlify.app/ |
| **配置 Secrets** | https://github.com/wanibbo/ai-daily-news/settings/secrets/actions |

---

## 🎯 立即执行

**推荐方式**: 访问 GitHub 网页手动触发

```
1. 打开：https://github.com/wanibbo/ai-daily-news/actions/workflows/auto-deploy-all.yml
2. 点击 "Run workflow"
3. 选择 main 分支
4. 再次点击 "Run workflow"
5. 等待 3-5 分钟
6. 访问：https://ai-daily-daily.netlify.app/
```

---

**部署完成后，网站将显示今日日报（2026-04-01）！** 🎉
