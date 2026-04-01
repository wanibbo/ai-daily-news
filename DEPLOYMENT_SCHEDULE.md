# 📅 日报自动化时间表

**更新时间**: 2026-03-31 17:11

---

## ⏰ 每日执行时间表（北京时间）

| 时间 | 事件 | 工作流 | 耗时 |
|------|------|--------|------|
| **08:00** | 🤖 自动生成日报 | `daily-update.yml` 触发 | - |
| **08:00-08:02** | 📝 运行 Python 脚本抓取新闻 | `Generate daily news` | ~2 分钟 |
| **08:02-08:03** | ⏳ 等待（确保文件完整） | `Wait for 2 minutes` | 1 分钟 |
| **08:03-08:05** | 📤 提交并推送代码 | `Commit and push` | ~2 分钟 |
| **08:05** | 🚀 触发自动部署 | `auto-deploy-all.yml` 触发 | - |
| **08:05-08:06** | ⏳ 等待（确保代码同步） | `Wait for 1 minute` | 1 分钟 |
| **08:06-08:08** | 🌐 Netlify 部署 | `Deploy to Netlify` | ~2 分钟 |
| **08:08** | ✅ 网站可访问 | - | - |

---

## 📊 完整流程时序图

```
08:00 ──┬─────────────────────────────────────────────
        │ daily-update.yml 触发（Cron: 0 0 * * *）
        ↓
08:00 ──┼── [Checkout] 检出代码
        │
        ↓
08:00 ──┼── [Setup Python] 配置 Python 环境
        │
        ↓
08:00 ──┼── [Install] 安装依赖包
        │
        ↓
08:00 ──┼── [Generate] 生成日报 ⭐
        │   - 量子位、InfoQ、界面新闻、虎嗅 OCR
        │   - 生成 report_YYYY-MM-DD.html/json
        │
        ↓
08:02 ──┼── [Wait 2min] 等待 2 分钟
        │   - 确保所有文件写入完成
        │
        ↓
08:03 ──┼── [Commit & Push] 提交并推送 ⭐
        │   - git add -A
        │   - git commit -m "Daily update ..."
        │   - git push
        │
        ↓
08:05 ──┴─────────────────────────────────────────────
        │
        │ push 事件触发 auto-deploy-all.yml
        ↓
08:05 ──┬─────────────────────────────────────────────
        │ auto-deploy-all.yml 触发（Push 事件）
        ↓
08:05 ──┼── [Checkout] 检出代码
        │
        ↓
08:05 ──┼── [Wait 1min] 等待 1 分钟
        │   - 确保 GitHub 代码已同步
        │
        ↓
08:06 ──┼── [Setup Node] 配置 Node.js
        │
        ↓
08:06 ──┼── [Install Netlify] 安装 Netlify CLI
        │
        ↓
08:06 ──┼── [Deploy] Netlify 部署 ⭐
        │   - netlify deploy --prod --dir=.
        │
        ↓
08:08 ──┴── ✅ 部署完成，网站可访问
```

---

## 🔧 工作流配置详情

### 1. `daily-update.yml` - 每日生成

**触发时间**: UTC 0:00 = 北京时间 8:00

**关键步骤**:

```yaml
- name: Generate daily news
  run: python skill_v12.py
  timeout-minutes: 5  # 最多 5 分钟

- name: Wait for 2 minutes
  run: sleep 120  # 等待 2 分钟
  continue-on-error: true  # 即使失败也继续

- name: Commit and push
  run: |
    git config user.name "AI Assistant"
    git config user.email "ai@example.com"
    git add -A
    git commit -m "Daily update $(date +%Y-%m-%d %H:%M)" || echo "No changes"
    git push
  timeout-minutes: 3  # 最多 3 分钟
```

**总耗时**: 约 5 分钟（08:00 - 08:05）

---

### 2. `auto-deploy-all.yml` - 自动部署

**触发条件**: push 到 main 分支

**关键步骤**:

```yaml
- name: Wait for 1 minute after push
  run: sleep 60  # 等待 1 分钟
  continue-on-error: true

- name: Deploy to Netlify
  run: |
    netlify deploy --prod --dir=.
  env:
    NETLIFY_AUTH_TOKEN: ${{ secrets.NETLIFY_AUTH_TOKEN }}
    NETLIFY_SITE_ID: ${{ secrets.NETLIFY_SITE_ID }}
  timeout-minutes: 5  # 最多 5 分钟
```

**总耗时**: 约 3 分钟（08:05 - 08:08）

---

## 📋 时间间隔调整说明

### 调整前

| 时间 | 事件 |
|------|------|
| 08:00 | 生成日报 |
| 08:02 | 推送代码 |
| 08:03 | 部署开始 |
| 08:05 | 部署完成 |

**问题**: 时间间隔太短，可能导致：
- 文件未完全写入就提交
- GitHub 代码未同步就部署

---

### 调整后（优化版）

| 时间 | 事件 | 说明 |
|------|------|------|
| **08:00** | 生成日报开始 | 运行 Python 脚本 |
| **08:02** | 生成完成，等待 2 分钟 | 确保文件完整写入 |
| **08:03** | 提交并推送代码 | git commit & push |
| **08:05** | 推送完成，触发部署 | push 事件触发 |
| **08:06** | 等待 1 分钟 | 确保 GitHub 代码同步 |
| **08:08** | 部署完成 | Netlify 部署完成 |

**优势**:
- ✅ 文件写入更充分（2 分钟等待）
- ✅ GitHub 代码同步更可靠（1 分钟等待）
- ✅ 部署失败率更低

---

## 🎯 关键时间节点

### ⭐ 三个关键时间点

1. **08:00** - 生成开始
   - Cron 触发
   - Python 脚本运行

2. **08:03** - 推送代码
   - 生成完成后等待 2 分钟
   - 确保文件完整

3. **08:05** - 开始部署
   - push 事件触发
   - 等待 1 分钟后部署

---

## 🔍 监控建议

### 每日检查（自动化）

**GitHub Actions 会自动执行**:

| 时间 | 检查项 |
|------|--------|
| 08:02 | 生成步骤是否成功 |
| 08:05 | 推送步骤是否成功 |
| 08:08 | 部署步骤是否成功 |

### 每周检查（人工）

**建议每周一早上检查**:

1. 访问：https://github.com/wanibbo/ai-daily-news/actions
2. 查看上周运行历史
3. 确认没有失败的运行
4. 验证 Netlify 访问正常

---

## 🛡️ 故障处理

### 如果某天 08:10 还未完成

**检查步骤**:

1. **访问 Actions 页面**
   - https://github.com/wanibbo/ai-daily-news/actions

2. **查看运行中的工作流**
   - 检查卡在哪个步骤
   - 查看日志输出

3. **常见问题**:
   - Python 脚本超时 → 检查网络或 API
   - git push 失败 → 检查权限配置
   - Netlify 部署失败 → 检查 Secrets

4. **手动触发**
   - 点击 "Run workflow" 重新运行

---

## 📊 预期运行日志

### daily-update.yml 日志

```
✅ [08:00:00] Job started: update
✅ [08:00:15] Checkout completed
✅ [08:00:30] Setup Python completed
✅ [08:01:00] Install dependencies completed
✅ [08:02:30] Generate daily news completed (10 items)
✅ [08:03:30] Wait for 2 minutes completed
✅ [08:05:00] Commit and push completed
✅ [08:05:01] Job completed successfully
```

### auto-deploy-all.yml 日志

```
✅ [08:05:05] Job started: deploy-netlify
✅ [08:05:20] Checkout completed
✅ [08:06:20] Wait for 1 minute completed
✅ [08:06:40] Setup Node completed
✅ [08:07:00] Install Netlify CLI completed
✅ [08:08:30] Deploy to Netlify completed
✅ [08:08:31] Job completed successfully
✅ [08:08:32] Site URL: https://ai-daily-news-xxxxx.netlify.app
```

---

## 🔗 快速链接

| 功能 | 链接 |
|------|------|
| **Actions 首页** | https://github.com/wanibbo/ai-daily-news/actions |
| **日报生成工作流** | https://github.com/wanibbo/ai-daily-news/actions/workflows/daily-update.yml |
| **自动部署工作流** | https://github.com/wanibbo/ai-daily-news/actions/workflows/auto-deploy-all.yml |
| **Netlify 控制台** | https://app.netlify.com |

---

## 📝 总结

### 时间安排

| 时间段 | 活动 | 状态 |
|--------|------|------|
| **08:00-08:02** | 生成日报 | ✅ 已配置 |
| **08:02-08:03** | 等待文件写入 | ✅ 已配置 |
| **08:03-08:05** | 推送代码 | ✅ 已配置 |
| **08:05-08:06** | 等待代码同步 | ✅ 已配置 |
| **08:06-08:08** | Netlify 部署 | ✅ 已配置 |
| **08:08+** | 网站可访问 | ✅ 就绪 |

### 配置状态

- ✅ 工作流文件已更新
- ✅ 时间间隔已优化
- ✅ 等待步骤已添加
- ✅ 超时保护已配置

**明天（2026-04-01）早上 08:00 开始自动执行！** 🎉
