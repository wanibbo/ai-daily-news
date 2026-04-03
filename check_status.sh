#!/bin/bash
# 检查 AI 日报服务器状态

echo "======================================"
echo "🤖 AI 日报 - 服务状态检查"
echo "======================================"
echo ""

# 检查进程
echo "📊 服务器进程:"
ps aux | grep "http.server" | grep -v grep || echo "❌ 服务器未运行"
echo ""

# 检查端口
echo "🔌 端口 8080:"
netstat -tlnp 2>/dev/null | grep 8080 || ss -tlnp | grep 8080 || echo "❌ 端口未监听"
echo ""

# 检查公网访问
echo "🌐 公网 IP:"
curl -s ifconfig.me
echo ""
echo ""

# 测试访问
echo "🧪 测试访问:"
response=$(curl -s -o /dev/null -w "%{http_code}" http://localhost:8080/ 2>&1)
if [ "$response" = "200" ]; then
    echo "✅ 访问正常 (HTTP $response)"
else
    echo "❌ 访问失败 (HTTP $response)"
fi
echo ""

# 显示访问地址
echo "======================================"
echo "📍 访问地址:"
echo "======================================"
echo "主站：http://$(curl -s ifconfig.me):8080"
echo "历史：http://$(curl -s ifconfig.me):8080/history/"
echo "数据：http://$(curl -s ifconfig.me):8080/news_data.json"
echo "======================================"
