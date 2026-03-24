# 🔧 AI 日报 - 访问问题解决方案

## ❌ 问题分析

### 当前状态
- ✅ 服务器：运行正常（PID: 9263）
- ✅ 端口：8080 已监听
- ✅ 本地访问：正常（HTTP 200）
- ❌ 外网访问：**无法直接访问**

### 问题原因

服务器位于内网环境：
- **内网 IP**: `10.0.24.14`
- **公网 IP**: `8.139.156.39`（这是网关 IP，不是本机）

**需要端口映射或内网穿透才能外网访问**。

---

## ✅ 解决方案

### 方案 1：内网穿透（推荐，最简单）

#### 使用 ngrok

```bash
# 1. 下载 ngrok
wget https://bin.equinox.io/c/bNyj1mQVY4c/ngrok-v3-stable-linux-amd64.tgz
tar -xzf ngrok-v3-stable-linux-amd64.tgz

# 2. 启动 ngrok（映射 8080 端口）
./ngrok http 8080
```

**获得外网 URL**：
```
https://xxxx-xxxx-xxxx.ngrok.io
```

#### 使用 Cloudflare Tunnel

```bash
# 1. 安装 cloudflared
wget https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-amd64
chmod +x cloudflared-linux-amd64

# 2. 启动隧道
./cloudflared-linux-amd64 tunnel --url http://localhost:8080
```

---

### 方案 2：云服务器端口映射

如果你有云服务器（阿里云/腾讯云等）：

#### 阿里云 ECS

1. **登录阿里云控制台**
2. **安全组配置**：
   - 添加入站规则
   - 端口：8080
   - 授权对象：0.0.0.0/0
3. **端口转发**（如果需要）：
   ```bash
   sudo iptables -t nat -A PREROUTING -p tcp --dport 8080 -j DNAT --to-destination 10.0.24.14:8080
   ```

#### 腾讯云 CVM

1. **登录腾讯云控制台**
2. **安全组配置**：
   - 放行 8080 端口
3. **NAT 网关配置**（如果需要）

---

### 方案 3：使用 frp 内网穿透

#### 服务端（有公网 IP 的服务器）

```bash
# 1. 下载 frp
wget https://github.com/fatedier/frp/releases/download/v0.50.0/frp_0.50.0_linux_amd64.tar.gz
tar -xzf frp_0.50.0_linux_amd64.tar.gz

# 2. 配置 frps.ini
cat > frps.ini << EOF
[common]
bind_port = 7000
EOF

# 3. 启动服务端
./frps -c frps.ini
```

#### 客户端（本机）

```bash
# 1. 配置 frpc.ini
cat > frpc.ini << EOF
[common]
server_addr = <公网服务器 IP>
server_port = 7000

[ai-daily]
type = tcp
local_ip = 127.0.0.1
local_port = 8080
remote_port = 8080
EOF

# 2. 启动客户端
./frpc -c frpc.ini
```

**访问地址**：
```
http://<公网服务器IP>:8080
```

---

### 方案 4：Vercel/Netlify 部署（最稳定）

#### 步骤

1. **准备文件**
   ```bash
   cd /home/admin/openclaw/workspace/skills/ai-daily-news
   # 确保有 index.html
   ```

2. **推送到 GitHub**
   ```bash
   git init
   git add .
   git commit -m "AI 日报"
   git remote add origin <your-github-repo>
   git push -u origin main
   ```

3. **部署到 Vercel**
   - 访问 https://vercel.com
   - 导入 GitHub 仓库
   - 自动部署

**获得外网 URL**：
```
https://ai-daily.vercel.app
```

---

### 方案 5：使用 serveo.net（免安装）

```bash
# 直接运行
ssh -R 80:localhost:8080 serveo.net
```

**获得外网 URL**：
```
https://xxxx.serveo.net
```

---

## 🎯 推荐方案

### 最快上手（5 分钟）
**使用 ngrok**：
```bash
wget https://bin.equinox.io/c/bNyj1mQVY4c/ngrok-v3-stable-linux-amd64.tgz
tar -xzf ngrok-v3-stable-linux-amd64.tgz
./ngrok http 8080
```

### 最稳定（长期运行）
**使用 Vercel 部署**：
- 免费
- 自动 HTTPS
- 全球 CDN
- 自动部署

### 最可控（有自己的服务器）
**使用 frp 内网穿透**：
- 完全控制
- 数据私有
- 长期稳定

---

## 📊 当前服务状态

```
✅ HTTP 服务器：运行中（PID: 9263）
✅ 端口监听：0.0.0.0:8080
✅ 本地访问：http://localhost:8080
✅ 内网访问：http://10.0.24.14:8080
❌ 外网访问：需要端口映射/内网穿透
```

---

## 🔧 立即执行（推荐 ngrok）

```bash
cd /home/admin/openclaw/workspace/skills/ai-daily-news

# 1. 下载并解压
wget -q https://bin.equinox.io/c/bNyj1mQVY4c/ngrok-v3-stable-linux-amd64.tgz
tar -xzf ngrok-v3-stable-linux-amd64.tgz

# 2. 启动（后台运行）
nohup ./ngrok http 8080 > ngrok.log 2>&1 &

# 3. 查看外网 URL
sleep 3
grep -oP 'https://[^\s]+' ngrok.log | head -1
```

**获得的外网 URL 格式**：
```
https://xxxx-xxxx-xxxx.ngrok.io
```

---

## 📞 获取帮助

如果遇到问题：
1. 检查服务器日志：`tail -f server.log`
2. 检查 ngrok 日志：`tail -f ngrok.log`
3. 测试本地访问：`curl http://localhost:8080`

---

**状态**: ⚠️ 需要内网穿透  
**本地访问**: http://localhost:8080  
**内网访问**: http://10.0.24.14:8080  
**外网访问**: 需要配置端口映射
