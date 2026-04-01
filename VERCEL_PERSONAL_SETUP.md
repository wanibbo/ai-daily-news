# 🚀 Vercel 个人账户配置指南

**更新时间**: 2026-04-01 11:59

---

## ✅ 配置步骤（个人账户版）

### 步骤 1: 创建 Vercel 项目 ✅

**状态**: 已完成

---

### 步骤 2: 获取 Project ID ⏳

**访问**:
```
https://vercel.com/dashboard
```

**操作**:
1. 点击您的项目（ai-daily-news）
2. 点击右上角齿轮图标 ⚙️（Settings）
3. 在 **General** 页面找到 **Project ID**
4. 复制：`prj_xxxxxxxxxxxxxx`

---

### 步骤 3: 创建 Access Token ⏳

**访问**:
```
https://vercel.com/account/settings
```

**操作**:
1. 向下滚动到 **"Tokens"** 部分
2. 点击 **"Create Token"**
3. 填写：
   - **Name**: `AI Daily News Deploy`
   - **Scope**: 选择您的个人账号
4. 点击 **"Create"**
5. **立即复制 Token**：`xxxxxxxxxxxxxxxx`

**备用链接**:
```
如果上面链接不行，试试：
https://vercel.com/settings/tokens
```

---

### 步骤 4: 添加 GitHub Secrets ⏳

**访问**:
```
https://github.com/wanibbo/ai-daily-news/settings/secrets/actions
```

**添加 2 个 Secrets**（个人账户不需要 Org ID）:

| Name | Value | 示例 |
|------|-------|------|
| `VERCEL_TOKEN` | 步骤 3 创建的 Token | `xxxxxxxx` |
| `VERCEL_PROJECT_ID` | 步骤 2 获取的 Project ID | `prj_xxx` |

**操作步骤**:
1. 点击 "New repository secret"
2. 填写 Name 和 Value
3. 点击 "Add secret"
4. 重复添加另一个

---

### 步骤 5: 测试部署 ✅

**访问**:
```
https://github.com/wanibbo/ai-daily-news/actions/workflows/deploy-vercel.yml
```

**操作**:
1. 点击 "Run workflow" 按钮
2. 选择分支 `main`
3. 点击 "Run workflow"
4. 等待 2-3 分钟
5. 查看部署结果

---

## 🔍 常见问题

### Q1: 找不到 Tokens 选项？

**解决方案**:
```
1. 确保已登录 Vercel
2. 访问：https://vercel.com/account/settings
3. 向下滚动到页面底部
4. 找到 "Tokens" 部分
```

### Q2: Project ID 在哪里？

**解决方案**:
```
1. 访问：https://vercel.com/dashboard
2. 点击您的项目
3. 点击 Settings（齿轮图标）
4. General 页面第一个就是 Project ID
```

### Q3: 需要配置 Org ID 吗？

**答案**: **不需要！**

个人账户只需 2 个配置：
- ✅ VERCEL_TOKEN
- ✅ VERCEL_PROJECT_ID

---

## 📊 完整配置清单

- [ ] Vercel 项目已创建 ✅
- [ ] Project ID 已获取
- [ ] Access Token 已创建
- [ ] GitHub Secrets 已添加：
  - [ ] `VERCEL_TOKEN`
  - [ ] `VERCEL_PROJECT_ID`
- [ ] 手动触发测试部署
- [ ] 访问 Vercel URL 验证

---

## 🔗 快速链接

| 功能 | 链接 |
|------|------|
| **Vercel 控制台** | https://vercel.com/dashboard |
| **账号设置** | https://vercel.com/account/settings |
| **项目设置** | https://vercel.com/dashboard → 选择项目 → Settings |
| **GitHub Secrets** | https://github.com/wanibbo/ai-daily-news/settings/secrets/actions |
| **部署工作流** | https://github.com/wanibbo/ai-daily-news/actions/workflows/deploy-vercel.yml |

---

## 💡 下一步

**立即执行**:

1. **获取 Project ID**（1 分钟）
   ```
   https://vercel.com/dashboard
   选择项目 → Settings → General
   复制 Project ID
   ```

2. **创建 Token**（1 分钟）
   ```
   https://vercel.com/account/settings
   创建 Token → 复制
   ```

3. **配置 Secrets**（1 分钟）
   ```
   https://github.com/wanibbo/ai-daily-news/settings/secrets/actions
   添加 VERCEL_TOKEN + VERCEL_PROJECT_ID
   ```

4. **测试部署**（3 分钟）
   ```
   https://github.com/wanibbo/ai-daily-news/actions/workflows/deploy-vercel.yml
   Run workflow
   ```

---

**完成后告诉我，我帮您验证部署！** 🎉
