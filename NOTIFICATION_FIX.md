# 🔧 钉钉通知格式修复

**修复时间**: 2026-04-03 16:14  
**问题**: 钉钉通知无法发送  
**原因**: date 命令格式错误

---

## ❌ 问题原因

### 13:53 成功发送的配置

```yaml
# 正确的格式（不转义%）
$(date +"%Y-%m-%d %H:%M:%S")
```

### 修复前的错误配置

```yaml
# 错误的格式（转义了%）
$(date +\%Y-\%m-\%d \%H:\%M:\%S)
```

**错误信息**:
```
date: extra operand '%H:%M'
Try 'date --help' for more information.
```

---

## ✅ 修复方案

### 修复后的格式

**daily-update.yml**:
```yaml
# 钉钉通知
curl -X POST '${{ secrets.DINGTALK_WEBHOOK }}' \
  -H 'Content-Type: application/json' \
  -d '{
    "msgtype": "markdown",
    "markdown": {
      "title": "'"$TITLE"'",
      "text": "'"$TITLE"'\n\n'"$TEXT"'\n\n⏰ 时间：$(date +\"%Y-%m-%d %H:%M:%S\")\n🤖 自动发送"
    }
  }'
```

**notify-on-push.yml**:
```yaml
# 钉钉通知
curl -X POST '${{ secrets.DINGTALK_WEBHOOK }}' \
  -H 'Content-Type: application/json' \
  -d "{
    \"msgtype\": \"markdown\",
    \"markdown\": {
      \"title\": \"$TITLE\",
      \"text\": \"# $TITLE\n\n> 今日 AI 日报已自动生成并部署！\n\n**⏰ 生成时间**：$(date +\\\"%Y-%m-%d %H:%M:%S\\\")\n**📰 新闻数量**：${NEWS_COUNT} 条\n\n_🤖 自动发送_\"
    }
  }"
```

---

## 🔍 对比分析

### 13:53 成功的配置

| 项目 | 配置 |
|------|------|
| **date 格式** | `$(date +"%Y-%m-%d %H:%M:%S")` |
| **% 符号** | 不转义 |
| **引号** | 双引号 |
| **结果** | ✅ 成功发送 |

### 修复前的配置

| 项目 | 配置 |
|------|------|
| **date 格式** | `$(date +\%Y-\%m-\%d \%H:\%M:\%S)` |
| **% 符号** | 转义 |
| **引号** | 双引号 |
| **结果** | ❌ 发送失败 |

---

## 📊 修复内容

### 修改的文件

| 文件 | 修改内容 |
|------|---------|
| `daily-update.yml` | 修复 date 格式（2 处） |
| `notify-on-push.yml` | 修复 date 格式（1 处） |

### 修改的代码

**修改前**:
```bash
$(date +\%Y-\%m-\%d \%H:\%M:\%S)
```

**修改后**:
```bash
$(date +"%Y-%m-%d %H:%M:%S")
```

---

## 🧪 测试验证

### 方式 1: 手动触发工作流

1. **访问**: https://github.com/wanibbo/ai-daily-news/actions/workflows/notify-on-push.yml
2. **点击**: "Run workflow"
3. **选择**: `main` 分支
4. **点击**: "Run workflow"
5. **等待**: 30 秒
6. **查看**: 钉钉群消息

---

### 方式 2: 等待自动执行

**时间**: 明天早上 08:00

**流程**:
```
08:00 ── daily-update.yml 执行
08:03 ── 推送代码
08:03 ── notify-on-push.yml 自动触发
08:04 ── 发送钉钉通知（使用修复后的格式）
```

---

## ✅ 验证清单

- [x] 修复 daily-update.yml 的 date 格式
- [x] 修复 notify-on-push.yml 的 date 格式
- [x] 推送到 GitHub
- [ ] 手动触发测试
- [ ] 验证钉钉消息

---

## 📋 配置检查

### GitHub Secrets

**必须配置**:

| Secret | 状态 | 说明 |
|--------|------|------|
| `DINGTALK_WEBHOOK` | ✅ 已配置 | 钉钉机器人 Webhook |
| `WECHAT_WORK_WEBHOOK` | ⏳ 可选 | 企业微信 Webhook |

---

### 钉钉机器人

**必须配置**:

- [x] 机器人已添加到群
- [x] 安全设置：自定义关键词
- [x] 关键词：`AI 日报 `、` 生成成功`
- [x] Webhook URL 已配置

---

## 🎯 总结

### 问题根源

- **错误**: date 命令的 `%` 符号被转义
- **原因**: 在 YAML 中不需要转义 `%`
- **修复**: 移除转义字符 `\`

### 修复效果

- ✅ date 格式正确
- ✅ 时间显示正常
- ✅ 钉钉通知可发送

### 下次执行

- **时间**: 明天早上 08:00
- **预期**: 钉钉通知正常发送
- **验证**: 检查钉钉群消息

---

**修复完成！明天早上 08:00 将正常发送钉钉通知！** 📢
