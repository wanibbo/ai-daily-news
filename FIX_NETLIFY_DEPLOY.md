# 🔧 Netlify 部署失败排查指南

**创建时间**: 2026-04-01 11:31

---

## 🔍 常见失败原因

### 原因 1: Secrets 未配置或配置错误

**检查步骤**:

1. **访问 Secrets 页面**
   ```
   https://github.com/wanibbo/ai-daily-news/settings/secrets/actions
   ```

2. **确认以下 Secrets 已添加**:
   - [ ] `NETLIFY_AUTH_TOKEN`
   - [ ] `NETLIFY_SITE_ID`

3. **检查值是否正确**:
   - Token 格式：`nfp_xxxxxxxxxxxx`
   - Site ID 格式：`xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx`

**解决方案**:
```
1. 重新获取 Token 和 Site ID
2. 删除旧的 Secrets
3. 重新添加（注意不要有多余空格）
```

---

### 原因 2: Netlify 站点未创建

**检查步骤**:

1. **访问 Netlify**
   ```
   https://app.netlify.com
   ```

2. **确认站点是否存在**
   - 查找 `ai-daily-daily` 或类似名称的站点

**解决方案**:
```
1. 创建新站点
2. 选择 "Import an existing project"
3. 连接 GitHub
4. 选择 wanibbo/ai-daily-news 仓库
5. 点击 "Deploy site"
6. 获取 Site ID
```

---

### 原因 3: Token 权限不足

**检查步骤**:

1. **访问 Token 管理**
   ```
   https://app.netlify.com/user/applications#personal-access-tokens
   ```

2. **确认 Token 权限**
   - [ ] `sites:write`
   - [ ] `sites:read`
   - [ ] `deploys:write`

**解决方案**:
```
1. 删除旧 Token
2. 创建新 Token
3. 确保勾选所有 3 个权限
4. 更新 GitHub Secret
```

---

### 原因 4: 工作流配置错误

**检查步骤**:

1. **查看工作流文件**
   ```
   .github/workflows/auto-deploy-all.yml
   ```

2. **确认配置正确**:
   ```yaml
   - name: Deploy to Netlify
     run: |
       netlify deploy --prod --dir=.
     env:
       NETLIFY_AUTH_TOKEN: ${{ secrets.NETLIFY_AUTH_TOKEN }}
       NETLIFY_SITE_ID: ${{ secrets.NETLIFY_SITE_ID }}
   ```

**解决方案**:
```
工作流配置已正确，无需修改
```

---

## 📊 查看部署日志

### 方式 1: GitHub Actions 日志

1. **访问 Actions**
   ```
   https://github.com/wanibbo/ai-daily-news/actions/workflows/auto-deploy-all.yml
   ```

2. **点击失败的运行记录**

3. **查看详细日志**
   - 展开 "Deploy to Netlify" 步骤
   - 查找错误信息

**常见错误**:

| 错误信息 | 原因 | 解决方案 |
|---------|------|---------|
| `Invalid NETLIFY_AUTH_TOKEN` | Token 错误 | 重新创建 Token |
| `Site not found` | Site ID 错误 | 检查 Site ID |
| `Authentication required` | 未配置 Secrets | 添加 Secrets |
| `Command failed with exit code 1` | 部署失败 | 查看详细日志 |

---

### 方式 2: Netlify 控制台

1. **访问 Netlify**
   ```
   https://app.netlify.com/sites/ai-daily-daily/deploys
   ```

2. **查看部署历史**
   - 查看最近的失败记录
   - 点击查看详情

---

## 🛠️ 快速修复方案

### 方案 A: 重新配置 Secrets（推荐）

```bash
# 1. 获取新的 Token
访问：https://app.netlify.com/user/applications#personal-access-tokens
创建：New personal access token
权限：sites:write, sites:read, deploys:write
复制：nfp_xxxxxxxxxxxx

# 2. 获取 Site ID
访问：https://app.netlify.com
选择站点 → Site settings → General
复制：xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx

# 3. 更新 GitHub Secrets
访问：https://github.com/wanibbo/ai-daily-news/settings/secrets/actions
删除旧的 NETLIFY_AUTH_TOKEN 和 NETLIFY_SITE_ID
添加新的 Secrets
```

---

### 方案 B: 使用 Netlify 网页部署（临时方案）

```
1. 访问：https://app.netlify.com/drop
2. 拖拽项目文件夹
3. 自动部署
```

---

### 方案 C: 本地测试部署

```bash
cd /home/admin/openclaw/workspace/skills/ai-daily-news

# 设置环境变量
export NETLIFY_AUTH_TOKEN="nfp_xxx"
export NETLIFY_SITE_ID="xxx-xxx"

# 测试部署
python3 deploy_netlify.py deploy
```

---

## 📋 配置验证清单

### 必须配置

- [ ] Netlify 账号已创建
- [ ] 站点已创建（ai-daily-daily）
- [ ] Personal Access Token 已创建
- [ ] Token 权限正确（3 个）
- [ ] Site ID 已获取
- [ ] GitHub Secrets 已添加：
  - [ ] `NETLIFY_AUTH_TOKEN`（值：nfp_xxx）
  - [ ] `NETLIFY_SITE_ID`（值：xxx-xxx-xxx）

### 可选验证

- [ ] 本地部署测试成功
- [ ] Netlify Drop 测试成功
- [ ] GitHub Actions 手动触发成功

---

## 🔗 需要协助？

如需帮助，请提供以下信息：

1. **GitHub Actions 错误日志**
   ```
   访问：https://github.com/wanibbo/ai-daily-news/actions
   复制失败运行的错误信息
   ```

2. **Netlify 站点状态**
   - [ ] 已有站点
   - [ ] 未创建站点
   - 站点名称：_______

3. **Secrets 配置状态**
   - [ ] 已配置
   - [ ] 未配置
   - [ ] 配置但不确定是否正确

---

## 💡 下一步

**如果确认 Secrets 已正确配置**:

1. **手动触发工作流**
   ```
   https://github.com/wanibbo/ai-daily-news/actions/workflows/auto-deploy-all.yml
   点击：Run workflow
   ```

2. **查看运行日志**
   - 如果仍然失败，复制错误信息
   - 我可以帮您进一步分析

3. **临时方案**
   - 使用 Netlify Drop 手动部署
   - 确保网站可访问

---

**请告诉我具体的错误信息，我可以帮您精准定位问题！** 🔍
