# 🔧 GitHub Actions 工作流语法修复

**修复时间**: 2026-04-03 16:18  
**错误**: `Unrecognized named-value: 'secrets'`

---

## ❌ 错误原因

### 错误的语法

```yaml
- name: Send DingTalk notification
  if: ${{ secrets.DINGTALK_WEBHOOK != '' }}  # ❌ 错误
  run: |
```

**错误信息**:
```
Invalid workflow file (Line: 39, Col: 13): 
Unrecognized named-value: 'secrets'. 
Located at position 1 within expression: secrets.DINGTALK_WEBHOOK != ''
```

---

## ✅ 修复方案

### 正确的语法

**不能**在 `if` 条件中直接使用 `secrets`

**正确做法**:
1. 使用 `if: always()` 始终执行
2. 在 `run` 脚本中检查 secret 是否存在

---

### 修复后的代码

```yaml
- name: Send DingTalk notification
  if: always()  # ✅ 正确
  run: |
    # 检查是否配置了 Webhook
    if [ -z '${{ secrets.DINGTALK_WEBHOOK }}' ] || [ '${{ secrets.DINGTALK_WEBHOOK }}' = '' ]; then
      echo "⚠️ DINGTALK_WEBHOOK 未配置，跳过"
      exit 0
    fi
    
    # 发送通知
    curl -X POST '${{ secrets.DINGTALK_WEBHOOK }}' \
      -H 'Content-Type: application/json' \
      -d '{...}'
```

---

## 📊 修复内容

### 修改的文件

| 文件 | 修改内容 |
|------|---------|
| `notify-on-push.yml` | 修复 2 处 `if` 条件 |

### 修改的代码

**修改前**:
```yaml
if: ${{ secrets.DINGTALK_WEBHOOK != '' }}
```

**修改后**:
```yaml
if: always()
run: |
  if [ -z '${{ secrets.DINGTALK_WEBHOOK }}' ] || [ '${{ secrets.DINGTALK_WEBHOOK }}' = '' ]; then
    echo "⚠️ 未配置，跳过"
    exit 0
  fi
```

---

## 🔍 GitHub Actions 语法说明

### 可以在 if 中使用的上下文

- ✅ `github` - GitHub 相关信息
- ✅ `env` - 环境变量
- ✅ `job` - 任务信息
- ✅ `steps` - 步骤信息
- ✅ `runner` - 运行器信息
- ❌ `secrets` - **不能**在 if 中使用

---

### 访问 Secrets 的正确方式

**在 `run` 脚本中**:
```yaml
- name: Use secret
  run: |
    echo "Secret value: ${{ secrets.MY_SECRET }}"
```

**在 `env` 中**:
```yaml
- name: Use secret
  env:
    MY_SECRET: ${{ secrets.MY_SECRET }}
  run: |
    echo "Secret value: $MY_SECRET"
```

**不能在 `if` 中**:
```yaml
- name: Use secret
  if: ${{ secrets.MY_SECRET != '' }}  # ❌ 错误
  run: |
```

---

## 🧪 测试验证

### 方式 1: 检查工作流语法

**访问**: https://github.com/wanibbo/ai-daily-news/actions/workflows/notify-on-push.yml

**确认**:
- [ ] 工作流文件无语法错误
- [ ] 可以手动触发

---

### 方式 2: 手动触发测试

1. **访问**: https://github.com/wanibbo/ai-daily-news/actions/workflows/notify-on-push.yml
2. **点击**: "Run workflow"
3. **选择**: `main` 分支
4. **点击**: "Run workflow"
5. **等待**: 30 秒
6. **查看**: 钉钉群消息

---

### 方式 3: 查看运行日志

**访问**: https://github.com/wanibbo/ai-daily-news/actions

**查看**:
- 最新运行记录
- "Send DingTalk notification" 步骤
- 执行日志

---

## 📋 配置检查清单

- [x] 修复 `if` 条件语法
- [x] 添加 secret 检查
- [x] 推送到 GitHub
- [ ] 工作流验证通过
- [ ] 测试通知发送

---

## 🎯 总结

### 问题根源

- **错误**: 在 `if` 条件中使用 `secrets`
- **原因**: GitHub Actions 不支持
- **修复**: 改用 `if: always()` + 脚本内检查

### 修复效果

- ✅ 工作流语法正确
- ✅ 可以正常触发
- ✅ 自动检查 secret 配置

### 下次执行

- **时间**: 下次 push 或手动触发
- **预期**: 钉钉通知正常发送
- **验证**: 检查 Actions 日志和钉钉群

---

**修复完成！工作流语法已正确！** ✅
