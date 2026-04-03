# AI 日报 - 外网访问配置指南

## 🌐 方案 1：Python HTTP 服务器（最简单）

### 启动服务器
```bash
cd /home/admin/openclaw/workspace/skills/ai-daily-news
python3 -m http.server 8080
```

### 外网访问
1. **获取公网 IP**：
   ```bash
   curl ifconfig.me
   ```

2. **配置防火墙**：
   ```bash
   sudo ufw allow 8080/tcp
   ```

3. **访问地址**：
   ```
   http://<公网IP>:8080
   ```

### 后台运行
```bash
nohup python3 -m http.server 8080 > server.log 2>&1 &
```

---

## 🌐 方案 2：Nginx 反向代理（推荐）

### 安装 Nginx
```bash
sudo apt update
sudo apt install nginx -y
```

### 配置 Nginx
```bash
sudo nano /etc/nginx/sites-available/ai-daily
```

```nginx
server {
    listen 80;
    server_name your-domain.com;  # 或公网 IP
    
    location / {
        root /home/admin/openclaw/workspace/skills/ai-daily-news;
        index index.html;
        try_files $uri $uri/ =404;
    }
    
    location /history {
        root /home/admin/openclaw/workspace/skills/ai-daily-news;
        try_files $uri $uri/ =404;
    }
}
```

### 启用配置
```bash
sudo ln -s /etc/nginx/sites-available/ai-daily /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

### 访问地址
```
http://your-domain.com
```

---

## 🌐 方案 3：Vercel/Netlify 部署（免费）

### 步骤
1. 将 `ai-daily-news` 目录推送到 GitHub
2. 在 Vercel/Netlify 导入仓库
3. 配置构建设置（无需构建）
4. 自动部署

---

## ⏰ 定时任务配置

### 添加 cron 任务
```bash
crontab -e
```

### 添加以下内容（每天早上 8 点执行）
```bash
0 8 * * * /home/admin/openclaw/workspace/skills/ai-daily-news/cron_run.sh >> /var/log/ai_daily.log 2>&1
```

### 验证 cron
```bash
# 查看 cron 日志
grep CRON /var/log/syslog

# 查看 AI 日报日志
tail -f /var/log/ai_daily.log
```

---

## 📁 目录结构

```
ai-daily-news/
├── skill_v12.py          # 主程序
├── cron_run.sh           # 定时任务脚本
├── index.html            # 当前日报
├── news_data.json        # 当前数据
├── history/              # 历史日报目录
│   ├── report_2026-03-24.html
│   └── report_2026-03-24.json
└── README_DEPLOYMENT.md  # 部署文档
```

---

## 🔧 快速部署脚本

```bash
#!/bin/bash
# deploy.sh - 一键部署脚本

set -e

echo "🚀 开始部署 AI 日报..."

# 1. 安装依赖
pip3 install -q aiohttp beautifulsoup4 lxml

# 2. 生成日报
cd /home/admin/openclaw/workspace/skills/ai-daily-news
python3 skill_v12.py

# 3. 启动 HTTP 服务器（如果未运行）
if ! pgrep -f "http.server 8080" > /dev/null; then
    nohup python3 -m http.server 8080 > server.log 2>&1 &
    echo "✅ HTTP 服务器已启动"
fi

# 4. 配置 cron（如果未配置）
if ! crontab -l | grep -q "cron_run.sh"; then
    (crontab -l 2>/dev/null; echo "0 8 * * * /home/admin/openclaw/workspace/skills/ai-daily-news/cron_run.sh") | crontab -
    echo "✅ 定时任务已配置"
fi

echo ""
echo "======================================"
echo "✅ 部署完成！"
echo "======================================"
echo "访问地址：http://$(curl -s ifconfig.me):8080"
echo "日志文件：/var/log/ai_daily.log"
```

---

## 📊 监控和维护

### 查看运行状态
```bash
# 检查 HTTP 服务器
ps aux | grep "http.server"

# 查看最新日报
ls -lt history/ | head -5

# 查看 cron 状态
systemctl status cron
```

### 清理旧日报（保留最近 30 天）
```bash
find history/ -name "report_*.json" -mtime +30 -delete
find history/ -name "report_*.html" -mtime +30 -delete
```

---

**状态**: ✅ 完成  
**版本**: v12  
**更新**: 2026-03-24 21:15
