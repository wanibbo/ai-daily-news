# ⚠️ GitHub Pages 启用指南

**错误原因**: GitHub Pages 尚未在仓库设置中启用

---

## ✅ 必须手动启用 GitHub Pages

### 步骤 1: 访问设置页面

**请点击这里**: https://github.com/wanibbo/ai-daily-news/settings/pages

---

### 步骤 2: 配置 Pages

在打开的页面中：

1. **找到 "Build and deployment" 部分**

2. **Source**: 
   - 选择 **"Deploy from a branch"**

3. **Branch**:
   - 选择 **"main"**
   - Folder 保持 **"/ (root)"**

4. **点击 "Save" 按钮**

---

### 步骤 3: 等待自动部署

保存后，GitHub 会：
1. 自动创建 gh-pages 分支
2. 触发自动部署
3. 1-2 分钟后网站可访问

**查看部署状态**:
```
https://github.com/wanibbo/ai-daily-news/actions/workflows/deploy-pages.yml
```

---

### 步骤 4: 获取访问 URL

部署完成后，您的网站 URL 是：
```
https://wanibbo.github.io/ai-daily-news/
```

**查看方式**:
- 访问：https://github.com/wanibbo/ai-daily-news/settings/pages
- 页面顶部会显示 "Your site is live at..."
- 点击链接访问

---

## 🔍 截图指引

### 设置页面应该看到：

```
Build and deployment

Source:  [Deploy from a branch ▼]

Branch:  [main ▼] [/ (root) ▼]

         [Save]
```

---

## ❓ 常见问题

### Q: 找不到 Pages 设置？

**A**: 确保您有仓库管理员权限

---

### Q: 保存后没反应？

**A**: 
1. 刷新页面
2. 检查 Actions 标签是否有运行中的工作流
3. 等待 1-2 分钟

---

### Q: 部署失败？

**A**: 
1. 检查 Actions 日志
2. 确认 index.html 在根目录
3. 重新触发部署

---

## 📋 完成检查清单

- [ ] 访问了 https://github.com/wanibbo/ai-daily-news/settings/pages
- [ ] 选择了 "Deploy from a branch"
- [ ] Branch 选择了 "main"
- [ ] 点击了 "Save"
- [ ] 看到 "Your site is being built..." 提示
- [ ] 等待部署完成
- [ ] 访问 URL 验证网站

---

## 🎯 立即执行

**请现在访问**: https://github.com/wanibbo/ai-daily-news/settings/pages

**然后**:
1. 选择 "Deploy from a branch"
2. Branch 选择 "main"
3. 点击 Save
4. 告诉我 "已启用"

**我会帮您验证部署！** 🚀
