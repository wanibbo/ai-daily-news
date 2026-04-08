# 🔧 修复钉钉消息重复发送问题

**问题时间**: 2026-04-08  
**问题**: 钉钉消息发送了 3 遍

---

## ❌ 问题原因

### 重复发送的配置

**4 个工作流都配置了钉钉通知**:

| 工作流 | 触发条件 | 发送通知 | 今天执行 |
|--------|---------|---------|---------|
| **daily-update.yml** | 08:00 Cron | ✅ 是 | ✅ 可能 |
| **notify-on-push.yml** | push 到 main | ✅ 是 | ✅ 是 |
| **health-check.yml** | 09:00 Cron | ✅ 是 | ✅ 可能 |
| **failure-alert.yml** | 10:00 Cron | ✅ 是（仅失败） | ❌ 否 |

---

### 为什么发送 3 遍？

**执行流程**:

```
08:00 ── daily-update.yml 执行 ──┬── 发送钉钉通知（第 1 遍）
                                │
08:03 ── 推送代码 ───────────────┼── 触发 notify-on-push.yml ── 发送钉钉通知（第 2 遍）
                                │
09:00 ── health-check.yml 执行 ──┴── 发送钉钉通知（第 3 遍）
```

**结果**: 同一次日报生成，触发了 3 次钉钉通知

---

## ✅ 解决方案

### 方案 1: 只保留 notify-on-push.yml 发送通知（推荐 ⭐⭐⭐⭐⭐）

**优势**:
- ✅ 所有推送都会触发
- ✅ 不会重复
- ✅ 逻辑清晰
- ✅ 代码简洁

**修改**:
1. 移除 `daily-update.yml` 中的通知步骤
2. 移除 `health-check.yml` 中的通知步骤
3. 保留 `notify-on-push.yml` 中的通知步骤
4. `failure-alert.yml` 仅在失败时发送

---

### 方案 2: 添加防重复机制（备选）

**实现**:
```yaml
# 使用锁机制防止重复发送
- name: Check if notification already sent
  run: |
    if [ -f "/tmp/notification_sent_$(date +%Y-%m-%d)" ]; then
      echo "通知已发送，跳过"
      exit 0
    fi
    touch /tmp/notification_sent_$(date +%Y-%m-%d)
```

**劣势**:
- ⚠️ 增加复杂度
- ⚠️ 需要额外存储
- ⚠️ 可能失效

---

## 🎯 推荐执行方案 1

### 修改清单

**1. daily-update.yml**
- 移除 Step 4 - Send notifications
- 改为简单的完成步骤

**2. health-check.yml**
- 移除成功时的通知
- 仅保留失败时的日志记录

**3. notify-on-push.yml**
- 保留完整的通知逻辑
- 作为唯一通知入口

**4. failure-alert.yml**
- 保留失败告警通知
- 仅在确实失败时发送

---

## 📋 执行步骤

### 步骤 1: 修改 daily-update.yml

**移除**: Step 4 - Send notifications

**添加**:
```yaml
- name: Step 4 - Complete
  run: |
    echo "✅ 步骤 4/4: 日报生成完成"
    echo "📢 通知由 notify-on-push.yml 工作流发送"
```

---

### 步骤 2: 修改 health-check.yml

**移除**: 成功时的钉钉通知

**保留**: 失败时的日志记录

---

### 步骤 3: 验证 notify-on-push.yml

**确认**: 通知逻辑完整

**包括**:
- 钉钉通知
- Server 酱通知
- 企业微信通知

---

### 步骤 4: 测试验证

**操作**:
```bash
# 手动触发测试
访问：https://github.com/wanibbo/ai-daily-news/actions/workflows/notify-on-push.yml
点击 "Run workflow"
检查：只收到 1 条钉钉消息
```

---

## ⚠️ 临时解决方案

### 如果不想修改工作流

**临时方案**: 禁用某些工作流的通知

**方法 1**: 注释掉钉钉通知代码

**方法 2**: 设置 Secret 为空

**方法 3**: 禁用工作流
```
访问：https://github.com/wanibbo/ai-daily-news/actions
选择工作流 → 点击右上角"..." → Disable workflow
```

---

## 📊 修改前后对比

### 修改前

| 事件 | 发送次数 |
|------|---------|
| 日报生成 + 推送 | 3 次 |
| 健康检查通过 | 1 次 |
| 健康检查失败 | 1 次 |
| 失败告警 | 1 次 |

---

### 修改后

| 事件 | 发送次数 |
|------|---------|
| 日报生成 + 推送 | 1 次 ✅ |
| 健康检查通过 | 0 次 ✅ |
| 健康检查失败 | 0 次 ✅ |
| 失败告警 | 1 次 ✅ |

---

## 🔗 快速链接

| 功能 | 链接 |
|------|------|
| **工作流配置** | https://github.com/wanibbo/ai-daily-news/tree/main/.github/workflows |
| **Actions 监控** | https://github.com/wanibbo/ai-daily-news/actions |

---

## 🎯 总结

### 问题根源

- 4 个工作流都配置了钉钉通知
- 同一事件触发多个工作流
- 导致重复发送

### 解决方案

- 只保留 notify-on-push.yml 发送通知
- 其他工作流移除通知逻辑
- 失败告警工作流仅在失败时发送

### 预期效果

- 每次日报生成只发送 1 条通知
- 失败时发送告警通知
- 逻辑清晰，易于维护

---

**需要我立即执行修改吗？** 🔧
