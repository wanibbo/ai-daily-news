# 🚀 Vercel 快速配置指南

**更新时间**: 2026-04-01 11:45

---

## ✅ 配置步骤（按顺序执行）

### 步骤 1: 创建 Vercel 项目 ⏳

**请访问**: https://vercel.com/new

1. **登录**: 使用 GitHub 账号
2. **点击**: "Import Git Repository"
3. **搜索**: `ai-daily-news`
4. **点击**: "Import"
5. **配置**:
   - Framework Preset: `Other`
   - Build Command: 留空
   - Output Directory: 留空
6. **点击**: "Deploy"

**完成后继续步骤 2**

---

### 步骤 2: 获取 Vercel 信息 ⏳

**Project ID**:
```
Settings → General → Project ID
复制：prj_xxxxxxxxxxxxxx
```

**Org ID**:
```
Settings → General → Team ID
复制：team_xxxxxxxxxxxxxx
```

**Access Token**:
```
Settings → Tokens → Create Token
Name: AI Daily News Deploy
复制：xxxxxxxxxxxxxxxx
```

---

### 步骤 3: 配置 GitHub Secrets ⏳

**访问**: https://github.com/wanibbo/ai-daily-news/settings/secrets/actions

**添加 3 个 Secrets**:

| Name | Value | 示例 |
|------|-------|------|
| `VERCEL_TOKEN` | Access Token | `xxxxxxxx` |
| `VERCEL_ORG_ID` | Team ID | `team_xxx` |
| `VERCEL_PROJECT_ID` | Project ID | `prj_xxx` |

---

### 步骤 4: 测试部署 ✅

**访问**: https://github.com/wanibbo/ai-daily-news/actions/workflows/deploy-vercel.yml

**点击**: "Run workflow"

**等待**: 2-3 分钟

**验证**: 访问 Vercel 提供的 URL

---

## 📊 自动部署流程

```
推送代码到 GitHub
    ↓
GitHub Actions 触发
    ↓
安装 Vercel CLI
    ↓
vercel pull（拉取配置）
    ↓
vercel build（构建）
    ↓
vercel deploy（部署）
    ↓
✅ 部署完成
```

---

## 🔗 快速链接

| 功能 | 链接 |
|------|------|
| **创建项目** | https://vercel.com/new |
| **Vercel 控制台** | https://vercel.com/dashboard |
| **获取 Token** | https://vercel.com/settings/tokens |
| **GitHub Secrets** | https://github.com/wanibbo/ai-daily-news/settings/secrets/actions |
| **部署工作流** | https://github.com/wanibbo/ai-daily-news/actions/workflows/deploy-vercel.yml |

---

## 💡 提示

1. **Vercel 会自动部署**
   - 配置完成后，每次 push 都会自动部署
   - 无需手动触发

2. **访问 URL**
   - 默认：`https://ai-daily-news.vercel.app`
   - 可在 Vercel 控制台自定义域名

3. **免费额度**
   - 带宽：100GB/月
   - 构建：6000 分钟/月
   - 足够日常使用

---

**请按顺序完成上述步骤，完成后告诉我！** 🎉
