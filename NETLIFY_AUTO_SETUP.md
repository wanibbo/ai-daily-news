# 🌐 Netlify 自动部署解决方案

**创建时间**: 2026-04-01 11:20

---

## ✅ 已完成的工作

1. **Netlify CLI 已安装**
   - 版本：24.9.0
   - 位置：`/opt/jvs-claw/base/bin/netlify`

2. **部署脚本已创建**
   - 文件：`deploy_netlify.py`
   - 功能：状态检查、登录、初始化、部署

3. **GitHub Actions 工作流已配置**
   - 文件：`.github/workflows/auto-deploy-all.yml`
   - 触发条件：push 到 main 分支

---

## ⏳ 需要配置的认证信息

### 方案 A：使用 GitHub Secrets（推荐 ⭐）

**适用场景**: GitHub Actions 自动部署

**步骤**:

1. **创建 Netlify Personal Access Token**
   ```
   访问：https://app.netlify.com/user/applications#personal-access-tokens
   点击：New personal access token
   Description: AI Daily News Deploy
   Scopes: sites:write, sites:read, deploys:write
   复制 Token: nfp_xxxxxxxxxxxx
   ```

2. **获取 Site ID**
   ```
   访问：https://app.netlify.com
   创建站点（导入 GitHub 仓库 wanibbo/ai-daily-news）
   Site settings → General → Site details
   复制 Site ID: xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
   ```

3. **添加到 GitHub Secrets**
   ```
   访问：https://github.com/wanibbo/ai-daily-news/settings/secrets/actions
   
   添加两个 secrets:
   - NETLIFY_AUTH_TOKEN = nfp_xxxxxxxxxxxx
   - NETLIFY_SITE_ID = xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
   ```

4. **测试部署**
   ```
   访问：https://github.com/wanibbo/ai-daily-news/actions/workflows/auto-deploy-all.yml
   点击：Run workflow
   等待：3-5 分钟
   验证：https://ai-daily-daily.netlify.app/
   ```

---

### 方案 B：本地部署测试

**适用场景**: 本地测试部署

**步骤**:

1. **设置环境变量**
   ```bash
   export NETLIFY_AUTH_TOKEN="nfp_xxxxxxxxxxxx"
   export NETLIFY_SITE_ID="xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx"
   ```

2. **运行部署脚本**
   ```bash
   cd /home/admin/openclaw/workspace/skills/ai-daily-news
   
   # 检查状态
   python3 deploy_netlify.py status
   
   # 登录
   python3 deploy_netlify.py login
   
   # 初始化站点
   python3 deploy_netlify.py init
   
   # 部署到生产环境
   python3 deploy_netlify.py deploy
   ```

---

### 方案 C：使用 netlify.toml（最简单）

**适用场景**: 快速测试

**步骤**:

1. **创建 netlify.toml**（已存在）
   ```toml
   [build]
     command = "echo 'No build needed'"
     publish = "."
   ```

2. **使用 Netlify Drop（无需 CLI）**
   ```
   访问：https://app.netlify.com/drop
   拖拽整个项目文件夹
   自动部署
   ```

3. **或使用 Netlify 网页界面**
   ```
   访问：https://app.netlify.com
   Add new site → Import an existing project
   选择 GitHub 仓库
   自动配置部署
   ```

---

## 🔧 故障排查

### 问题 1: GitHub Actions 部署失败

**错误**: `Invalid NETLIFY_AUTH_TOKEN`

**解决**:
1. 重新创建 Token
2. 确认 Scopes 正确
3. 更新 GitHub Secret

---

### 问题 2: 站点未找到

**错误**: `Site not found` 或 `Site ID does not exist`

**解决**:
1. 确认 Netlify 站点已创建
2. 重新复制 Site ID
3. 检查是否有拼写错误

---

### 问题 3: 部署成功但内容未更新

**原因**: 浏览器缓存

**解决**:
1. 强制刷新：Ctrl+F5
2. 清除浏览器缓存
3. 使用无痕模式访问

---

## 📊 部署流程对比

| 方式 | 优点 | 缺点 | 适用场景 |
|------|------|------|---------|
| **GitHub Actions** | 全自动 | 需配置 Secrets | 生产环境 |
| **本地 CLI** | 可调试 | 需手动执行 | 测试环境 |
| **Netlify Drop** | 最简单 | 无版本控制 | 快速验证 |
| **网页导入** | 简单 | 配置有限 | 初次设置 |

---

## 🎯 推荐方案

### 生产环境（每日自动部署）

**使用 GitHub Actions + Secrets**

```yaml
# .github/workflows/auto-deploy-all.yml
- name: Deploy to Netlify
  run: netlify deploy --prod --dir=.
  env:
    NETLIFY_AUTH_TOKEN: ${{ secrets.NETLIFY_AUTH_TOKEN }}
    NETLIFY_SITE_ID: ${{ secrets.NETLIFY_SITE_ID }}
```

**优势**:
- ✅ 全自动（每天 07:05 触发）
- ✅ 版本控制
- ✅ 部署历史
- ✅ 失败通知

---

### 测试环境（手动验证）

**使用本地 CLI**

```bash
cd /home/admin/openclaw/workspace/skills/ai-daily-news
export NETLIFY_AUTH_TOKEN="nfp_xxx"
export NETLIFY_SITE_ID="xxx-xxx"
python3 deploy_netlify.py deploy
```

**优势**:
- ✅ 即时反馈
- ✅ 可调试
- ✅ 无需等待 CI

---

## 📋 配置检查清单

### GitHub Actions 自动部署

- [ ] Netlify 账号已创建
- [ ] 站点已创建（ai-daily-daily）
- [ ] Personal Access Token 已创建
- [ ] Site ID 已获取
- [ ] GitHub Secrets 已添加：
  - [ ] `NETLIFY_AUTH_TOKEN`
  - [ ] `NETLIFY_SITE_ID`
- [ ] 工作流文件已推送
- [ ] 手动触发测试成功
- [ ] 访问 URL 显示最新日报

### 本地部署测试

- [ ] Netlify CLI 已安装
- [ ] 已登录 Netlify
- [ ] 环境变量已设置
- [ ] 站点已初始化
- [ ] 本地部署测试成功

---

## 🔗 快速链接

| 功能 | 链接 |
|------|------|
| **Netlify 登录** | https://app.netlify.com |
| **创建 Token** | https://app.netlify.com/user/applications#personal-access-tokens |
| **创建站点** | https://app.netlify.com/new |
| **GitHub Secrets** | https://github.com/wanibbo/ai-daily-news/settings/secrets/actions |
| **部署工作流** | https://github.com/wanibbo/ai-daily-news/actions/workflows/auto-deploy-all.yml |
| **访问 URL** | https://ai-daily-daily.netlify.app/ |
| **Netlify Drop** | https://app.netlify.com/drop |

---

## 💡 下一步

### 立即执行（5 分钟）

1. **创建 Netlify 站点**
   ```
   https://app.netlify.com/new
   导入 GitHub 仓库：wanibbo/ai-daily-news
   ```

2. **获取认证信息**
   ```
   - Personal Access Token
   - Site ID
   ```

3. **配置 GitHub Secrets**
   ```
   https://github.com/wanibbo/ai-daily-news/settings/secrets/actions
   添加：NETLIFY_AUTH_TOKEN + NETLIFY_SITE_ID
   ```

4. **测试部署**
   ```
   手动触发工作流
   验证访问 URL
   ```

---

## 🛠️ 需要协助？

如果需要帮助配置，请提供：

1. **Netlify 账号状态**
   - [ ] 已有账号
   - [ ] 需要创建

2. **站点状态**
   - [ ] 已创建站点
   - [ ] 未创建站点

3. **认证信息**
   - [ ] 已有 Token 和 Site ID
   - [ ] 需要指导获取

4. **部署方式**
   - [ ] GitHub Actions 自动部署
   - [ ] 本地手动部署
   - [ ] Netlify Drop

---

**配置完成后，每天 07:08 自动部署最新日报！** 🎉
