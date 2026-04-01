# 🔔 钉钉通知配置指南

**更新时间**: 2026-04-01 10:45

---

## ✅ 功能说明

每天 AI 日报自动生成后（北京时间 08:00），会自动发送钉钉消息通知你。

**消息内容**:
- ✅ 生成成功：包含数据来源、报告文件、部署状态
- ⚠️ 生成失败：包含错误提示和排查链接

---

## 📋 配置步骤

### 步骤 1：创建钉钉机器人

1. **打开钉钉群聊**
   - 选择一个群（或创建新群）
   - 点击右上角「群设置」图标

2. **添加机器人**
   - 选择「智能群助手」
   - 点击「添加机器人」
   - 选择「自定义」机器人

3. **配置机器人**
   - **机器人名字**: `AI Daily News`
   - **头像**: 可选
   - **安全设置**: 选择「自定义关键词」
     - 添加关键词：`AI 日报`、`生成成功`、`生成失败`

4. **获取 Access Token**
   - 复制 Webhook 地址
   - 格式：`https://oapi.dingtalk.com/robot/send?access_token=xxxxxxxx`
   - 提取 `access_token` 参数值（`xxxxxxxx` 部分）

---

### 步骤 2：添加到 GitHub Secrets

1. **访问 Secrets 页面**
   - https://github.com/wanibbo/ai-daily-news/settings/secrets/actions

2. **添加 Secret**
   - 点击 "New repository secret"
   - Name: `DINGTALK_ACCESS_TOKEN`
   - Value: 步骤 1 获取的 Token
   - 点击 "Add secret"

---

### 步骤 3：测试通知

1. **手动触发工作流**
   - 访问：https://github.com/wanibbo/ai-daily-news/actions/workflows/daily-update.yml
   - 点击 "Run workflow"
   - 等待完成

2. **检查钉钉消息**
   - 应该在 1-2 分钟内收到通知
   - 消息格式：
     ```
     ✅ AI 日报生成成功

     今日 AI 日报已自动生成并部署！

     📊 数据来源：量子位、InfoQ、界面新闻、虎嗅网
     📁 报告：history/report_2026-04-01.html
     🌐 部署：Netlify 已完成

     ⏰ 时间：2026-04-01 08:05:30
     🤖 自动发送
     ```

---

## 📊 消息示例

### 成功通知

```markdown
✅ AI 日报生成成功

今日 AI 日报已自动生成并部署！

📊 数据来源：量子位、InfoQ、界面新闻、虎嗅网
📁 报告：history/report_2026-04-01.html
🌐 部署：Netlify 已完成

⏰ 时间：2026-04-01 08:05:30
🤖 自动发送
```

### 失败通知

```markdown
⚠️ AI 日报生成失败

今日 AI 日报生成失败，请检查 GitHub Actions 日志！

🔗 查看：https://github.com/wanibbo/ai-daily-news/actions

⏰ 时间：2026-04-01 08:05:30
🤖 自动发送
```

---

## 🔧 工作流配置

**文件**: `.github/workflows/daily-update.yml`

**新增步骤**:

```yaml
- name: Send DingTalk notification
  if: always()  # 无论成功失败都发送
  run: |
    STATUS="${{ job.status }}"
    if [ "$STATUS" == "success" ]; then
      # 成功消息
    else
      # 失败消息
    fi
    
    curl -X POST 'https://oapi.dingtalk.com/robot/send?access_token=${{ secrets.DINGTALK_ACCESS_TOKEN }}' \
      -H 'Content-Type: application/json' \
      -d '{...}'
```

---

## 🛡️ 安全提示

### 关键词设置（必须）

钉钉机器人需要设置关键词才能发送消息：

**推荐关键词**:
- `AI 日报`
- `生成成功`
- `生成失败`
- `自动发送`

**设置位置**: 机器人设置 → 安全设置 → 自定义关键词

---

### Token 保护

- ✅ 使用 GitHub Secrets 存储 Token
- ✅ 不在代码中硬编码 Token
- ✅ 定期更换 Token（建议每年）
- ❌ 不要分享 Token 给他人

---

## 📋 配置检查清单

- [ ] 钉钉群已创建
- [ ] 机器人已添加到群
- [ ] 安全设置已配置（关键词）
- [ ] Access Token 已复制
- [ ] GitHub Secret 已添加（`DINGTALK_ACCESS_TOKEN`）
- [ ] 工作流文件已推送
- [ ] 手动测试通知成功

---

## 🔗 快速链接

| 功能 | 链接 |
|------|------|
| **GitHub Secrets** | https://github.com/wanibbo/ai-daily-news/settings/secrets/actions |
| **工作流文件** | https://github.com/wanibbo/ai-daily-news/blob/main/.github/workflows/daily-update.yml |
| **钉钉机器人文档** | https://open.dingtalk.com/document/robots/custom-robot-access |
| **Actions 运行历史** | https://github.com/wanibbo/ai-daily-news/actions |

---

## 🎯 下一步

1. **立即配置**:
   - 创建钉钉机器人
   - 获取 Access Token
   - 添加到 GitHub Secrets

2. **测试通知**:
   - 手动触发工作流
   - 确认收到钉钉消息

3. **等待自动运行**:
   - 明天 08:00 自动执行
   - 08:05 收到通知

---

## ❓ 常见问题

### Q: 收不到消息？

**检查**:
1. 机器人是否在群中
2. 关键词设置是否正确
3. Token 是否正确
4. GitHub Secret 是否已添加

### Q: 消息格式错误？

**检查**:
1. 工作流日志中的 curl 命令
2. JSON 格式是否正确
3. Markdown 语法是否正确

### Q: 想发送到多个群？

**方案**:
1. 创建多个机器人
2. 添加多个 Secrets（如 `DINGTALK_TOKEN_1`, `DINGTALK_TOKEN_2`）
3. 在工作流中发送多次

---

**配置完成后，每天 08:05 左右会收到钉钉通知！** 🎉
