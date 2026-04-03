# 🔧 修复 GitHub Actions 推送权限问题

## ❌ 错误信息

```
remote: Permission to wanibbo/ai-daily-news.git denied to github-actions[bot].
fatal: unable to access 'https://github.com/wanibbo/ai-daily-news/': 
The requested URL returned error: 403
```

**原因**: GitHub Actions 没有写入仓库的权限

---

## ✅ 解决方案（2 步）

### 步骤 1：修改工作流权限配置

编辑 `.github/workflows/daily-update.yml`，在文件**开头**添加权限配置：

```yaml
name: Daily AI News Update

# 添加权限配置
permissions:
  contents: write  # 允许推送代码

on:
  schedule:
    - cron: '0 0 * * *'
  workflow_dispatch:

jobs:
  update:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
        with:
          fetch-depth: 0
          token: ${{ secrets.GITHUB_TOKEN }}  # 确保使用 GITHUB_TOKEN
      
      # ... 其他步骤不变 ...
```

---

### 步骤 2：修改仓库设置

访问：https://github.com/wanibbo/ai-daily-news/settings/actions

**找到**: **Workflow permissions**

**修改为**: ✅ **Read and write permissions**

**勾选**: ✅ "Allow GitHub Actions to create and approve pull requests"（可选）

**保存**

---

## 📝 完整的工作流文件

`.github/workflows/daily-update.yml`:

```yaml
name: Daily AI News Update

# 权限配置（必须）
permissions:
  contents: write

on:
  schedule:
    - cron: '0 0 * * *'  # 每天 UTC 0 点（北京时间 8 点）
  workflow_dispatch:  # 允许手动触发

jobs:
  update:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
        with:
          fetch-depth: 0
          token: ${{ secrets.GITHUB_TOKEN }}
      
      - name: Setup Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.10'
      
      - name: Install dependencies
        run: |
          pip install aiohttp beautifulsoup4 lxml
      
      - name: Generate daily news
        run: python skill_v12.py
      
      - name: Commit and push
        run: |
          git config user.name "AI Assistant"
          git config user.email "ai@example.com"
          git add -A
          git commit -m "Daily update $(date +%Y-%m-%d %H:%M)" || echo "No changes"
          git push
```

---

## 🔧 修复步骤

### 方法 1：本地修改后推送

```bash
cd /home/admin/openclaw/workspace/skills/ai-daily-news

# 1. 编辑工作流文件
vim .github/workflows/daily-update.yml

# 添加权限配置（在 name: 之后）
# permissions:
#   contents: write

# 2. 提交并推送
git add .github/workflows/daily-update.yml
git commit -m "fix: add workflow permissions"
git push
```

### 方法 2：GitHub 网页编辑

1. 访问：https://github.com/wanibbo/ai-daily-news/edit/main/.github/workflows/daily-update.yml
2. 在 `name: Daily AI News Update` 下方添加：
   ```yaml
   permissions:
     contents: write
   ```
3. 点击 "Commit changes"
4. 保存后，访问仓库设置修改权限

---

## ✅ 验证修复

### 1. 检查仓库设置

访问：https://github.com/wanibbo/ai-daily-news/settings/actions

确认：
- ✅ **Workflow permissions** = "Read and write permissions"

### 2. 重新运行工作流

访问：https://github.com/wanibbo/ai-daily-news/actions/workflows/daily-update.yml

- 点击 "Run workflow"
- 等待运行完成
- 确认成功（绿色勾）

---

## 🔍 如果仍然失败

### 检查点 1：GITHUB_TOKEN 是否可用

GitHub 自动提供 `GITHUB_TOKEN`，无需手动配置。

确保 checkout 步骤使用：
```yaml
- uses: actions/checkout@v3
  with:
    token: ${{ secrets.GITHUB_TOKEN }}
```

### 检查点 2：仓库是否为私有

如果是私有仓库，需要额外配置：

访问：https://github.com/wanibbo/ai-daily-news/settings

确认：
- 仓库可见性
- Actions 是否启用

### 检查点 3：分支保护规则

访问：https://github.com/wanibbo/ai-daily-news/settings/branches

检查是否有分支保护规则阻止推送。

---

## 📊 权限说明

| 权限 | 用途 | 必需 |
|------|------|------|
| `contents: write` | 推送代码到仓库 | ✅ 必需 |
| `actions: read` | 读取工作流状态 | ⬜ 可选 |
| `pull-requests: write` | 创建 PR | ⬜ 可选 |

---

## 🎯 快速修复命令

```bash
# 1. 本地修改工作流文件
cd /home/admin/openclaw/workspace/skills/ai-daily-news

# 2. 使用 sed 添加权限配置
sed -i '/^name: Daily AI News Update$/a\\n# 权限配置\npermissions:\n  contents: write' .github/workflows/daily-update.yml

# 3. 验证修改
cat .github/workflows/daily-update.yml | head -20

# 4. 提交推送
git add .github/workflows/daily-update.yml
git commit -m "fix: add workflow permissions"
git push
```

---

## 🔗 相关文档

- GitHub Actions 权限：https://docs.github.com/en/actions/security-guides/automatic-token-authentication
- 工作流语法：https://docs.github.com/en/actions/using-workflows/workflow-syntax-for-github-actions
- 权限示例：https://docs.github.com/en/actions/using-jobs/assigning-permissions-to-jobs

---

**下一步**: 
1. 修改工作流文件添加 `permissions` 配置
2. 修改仓库设置为 "Read and write permissions"
3. 重新运行工作流测试
