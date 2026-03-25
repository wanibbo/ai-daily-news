# 🔓 Netlify 去掉访问密码

## ❌ 为什么会有密码？

Netlify 默认是公开访问的，如果有密码，可能是：

1. **Password Protection** 功能被开启
2. **Netlify Identity** 被启用
3. **部署到 Draft 模式**
4. **使用了 Netlify 的付费功能**

---

## ✅ 去掉密码的方法

### 方法 1：关闭 Password Protection

**步骤**：

1. **访问**：https://app.netlify.com
2. **登录**你的 Netlify 账号
3. **选择你的网站**（ai-daily-news）
4. **进入 Settings**（网站设置）
5. **找到**："Password Protection" 或 "Access Control"
6. **关闭**密码保护
7. **保存**设置

**具体路径**：
```
Site Settings → Access Control → Password Protection → Disable
```

---

### 方法 2：检查 Netlify Identity

如果启用了 Identity 服务：

1. **访问**：https://app.netlify.com
2. **选择网站**
3. **进入 Settings**
4. **找到**："Identity"
5. **禁用** Identity 服务
6. **保存**

**路径**：
```
Site Settings → Identity → Disable Identity
```

---

### 方法 3：重新部署（最简单）

如果以上都不行，重新部署：

1. **访问**：https://app.netlify.com/drop
2. **删除旧部署**（如果有）
3. **重新拖拽文件夹**：
   ```
   /home/admin/openclaw/workspace/skills/ai-daily-news/
   ```
4. **等待上传完成**
5. **获得公开 URL**

---

## 📊 检查清单

在 Netlify 后台检查以下设置：

- [ ] **Password Protection**: ❌ 关闭
- [ ] **Netlify Identity**: ❌ 禁用
- [ ] **Site Access**: ✅ 公开
- [ ] **Deploy Context**: ✅ Production（不是 Draft）

---

## 🎯 详细步骤

### 第 1 步：登录 Netlify

**访问**：https://app.netlify.com

**登录**你的账号

---

### 第 2 步：选择网站

在 Dashboard 找到你的网站：
```
ai-daily-news-xxxx
```

**点击进入**

---

### 第 3 步：检查访问设置

**点击**："Site settings"

**找到**："Access control" 或 "Password protection"

**如果看到**：
- "Password protection is enabled"
- "This site is password protected"

**点击**："Disable" 或 "Remove password"

---

### 第 4 步：保存设置

**点击**："Save changes"

**等待**设置生效（约 1 分钟）

---

### 第 5 步：测试访问

**访问你的网站 URL**：
```
https://ai-daily-news-xxxx.netlify.app
```

**应该可以直接访问，不需要密码！**

---

## 🔧 如果还是不行

### 方案 A：重新部署

1. **访问**：https://app.netlify.com/drop
2. **删除旧网站**（如果有）
3. **重新拖拽上传**
4. **获得新 URL**

### 方案 B：使用 Cloudflare Pages

如果 Netlify 一直有问题：

1. **访问**：https://pages.cloudflare.com
2. **用邮箱注册**
3. **拖拽部署**
4. **获得 URL**：`https://ai-daily-news.pages.dev`

**Cloudflare Pages 默认公开，无需密码！**

---

## 📱 快速检查

**在 Netlify 后台**：

```
Site Overview
    ↓
Site settings
    ↓
Access control
    ↓
确保 "Password protection" 是 OFF
```

---

## 🎯 现在请执行

1. **访问**：https://app.netlify.com
2. **登录**你的账号
3. **选择网站**
4. **进入 Settings**
5. **关闭 Password Protection**
6. **保存**

**完成后告诉我，我们测试访问！**

---

**状态**: ⏳ 等待关闭密码保护  
**预计时间**: 2 分钟  
**结果**: 公开访问，无需密码
