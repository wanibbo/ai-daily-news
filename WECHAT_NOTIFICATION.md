# 📱 微信通知配置指南

**更新时间**: 2026-04-01 11:26

---

## ✅ 支持的微信通知方式

| 方式 | 难度 | 成本 | 推荐度 |
|------|------|------|------|
| **企业微信机器人** | ⭐简单 | 免费 | ⭐⭐⭐⭐⭐ |
| **Server 酱** | ⭐简单 | 免费 | ⭐⭐⭐⭐ |
| **PushPlus** | ⭐简单 | 免费 | ⭐⭐⭐⭐ |

---

## 方案一：企业微信机器人（推荐 ⭐）

### 适用场景
- 企业微信用户
- 团队通知
- 支持 Markdown 格式

### 配置步骤

#### 1. 创建企业微信群机器人

1. **打开企业微信**
   - 手机或电脑端均可

2. **创建群聊**（或选择现有群）
   - 可以只拉自己一个人

3. **添加机器人**
   - 点击群右上角「...」
   - 选择「智能群助手」
   - 点击「添加机器人」
   - 选择「自定义」

4. **配置机器人**
   - **名称**: `AI Daily News`
   - **头像**: 可选
   - **Webhook 地址**: 复制保存
     ```
     https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
     ```

#### 2. 添加到 GitHub Secrets

访问：https://github.com/wanibbo/ai-daily-news/settings/secrets/actions

- **Name**: `WECHAT_WORK_WEBHOOK`
- **Value**: 复制的完整 Webhook URL
- 点击 "Add secret"

---

### 测试通知

```bash
# 测试消息
curl -X POST 'https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=YOUR_KEY' \
  -H 'Content-Type: application/json' \
  -d '{
    "msgtype": "markdown",
    "markdown": {
      "content": "## 测试消息\n\n> AI 日报通知测试\n\n**时间**：'"$(date +%Y-%m-%d %H:%M:%S)"'
    }
  }'
```

---

## 方案二：Server 酱（个人微信推荐 ⭐）

### 适用场景
- 个人微信接收
- 无需安装 APP
- 免费额度够用

### 配置步骤

#### 1. 注册 Server 酱

访问：https://sct.ftqq.com/

1. 使用 GitHub 账号登录
2. 获取 **SendKey**（在「消息推送」页面）

#### 2. 绑定微信

1. 关注「方糖」公众号
2. 在公众号中绑定账号

#### 3. 添加到 GitHub Secrets

访问：https://github.com/wanibbo/ai-daily-news/settings/secrets/actions

- **Name**: `SERVERCHAN_SENDKEY`
- **Value**: 获取的 SendKey（如：`SCTxxxxxxxxxxxxx`）
- 点击 "Add secret"

---

### 测试通知

```bash
# 测试消息
curl -X POST 'https://sctapi.ftqq.com/YOUR_SENDKEY.send' \
  -d 'title=AI 日报测试' \
  -d 'desp=这是一条测试消息%0A%0A**时间**：'"$(date +%Y-%m-%d %H:%M:%S)"
```

---

## 方案三：PushPlus（备选方案）

### 适用场景
- 个人微信接收
- 支持多种推送渠道
- 免费额度充足

### 配置步骤

#### 1. 注册 PushPlus

访问：http://www.pushplus.plus/

1. 微信扫码登录
2. 获取 **Token**

#### 2. 关注公众号

- 关注「PushPlus」公众号
- 会自动接收消息

#### 3. 添加到 GitHub Secrets

访问：https://github.com/wanibbo/ai-daily-news/settings/secrets/actions

- **Name**: `PUSHPLUS_TOKEN`
- **Value**: 获取的 Token
- 点击 "Add secret"

---

### 测试通知

```bash
# 测试消息
curl -X POST 'http://www.pushplus.plus/send' \
  -H 'Content-Type: application/json' \
  -d '{
    "token": "YOUR_TOKEN",
    "title": "AI 日报测试",
    "content": "这是一条测试消息",
    "template": "markdown"
  }'
```

---

## 📊 消息格式示例

### 企业微信消息

```markdown
## ✅ AI 日报生成成功

> 今日 AI 日报已自动生成并部署！

**📊 数据来源**：量子位、InfoQ、界面新闻、虎嗅网
**📁 报告**：history/report_2026-04-01.html
**🌐 部署**：Netlify 已完成
**🔗 查看**：https://ai-daily-daily.netlify.app/

_⏰ 时间：2026-04-01 07:08:30_
_🤖 自动发送_
```

### Server 酱消息

```markdown
# AI 日报已生成

**时间**：2026-04-01 07:08:30

**来源**：量子位、InfoQ、界面新闻、虎嗅网

**查看**：https://ai-daily-daily.netlify.app/
```

### PushPlus 消息

同 Server 酱格式，支持 Markdown。

---

## 🔧 工作流配置

**文件**: `.github/workflows/daily-update.yml`

**新增步骤**:

```yaml
- name: Send WeChat notification
  if: always()
  run: |
    # 企业微信通知
    if [ -n "${{ secrets.WECHAT_WORK_WEBHOOK }}" ]; then
      # 发送消息...
    fi
    
    # Server 酱通知（可选）
    if [ -n "${{ secrets.SERVERCHAN_SENDKEY }}" ]; then
      # 发送消息...
    fi
    
    # PushPlus 通知（可选）
    if [ -n "${{ secrets.PUSHPLUS_TOKEN }}" ]; then
      # 发送消息...
    fi
```

---

## 📋 配置检查清单

### 企业微信机器人

- [ ] 企业微信已安装
- [ ] 群聊已创建
- [ ] 机器人已添加
- [ ] Webhook URL 已复制
- [ ] GitHub Secret 已添加（`WECHAT_WORK_WEBHOOK`）
- [ ] 测试消息发送成功

### Server 酱

- [ ] 账号已注册
- [ ] SendKey 已获取
- [ ] 公众号已关注
- [ ] GitHub Secret 已添加（`SERVERCHAN_SENDKEY`）
- [ ] 测试消息发送成功

### PushPlus

- [ ] 账号已注册
- [ ] Token 已获取
- [ ] 公众号已关注
- [ ] GitHub Secret 已添加（`PUSHPLUS_TOKEN`）
- [ ] 测试消息发送成功

---

## 🎯 推荐配置

### 个人用户

**推荐**: Server 酱 或 PushPlus

**原因**:
- ✅ 配置简单
- ✅ 直接推送到个人微信
- ✅ 无需安装额外 APP

### 团队用户

**推荐**: 企业微信机器人

**原因**:
- ✅ 支持 Markdown 格式
- ✅ 可推送到群聊
- ✅ 可@特定人员

---

## 🔗 快速链接

| 功能 | 链接 |
|------|------|
| **企业微信** | https://work.weixin.qq.com/ |
| **Server 酱** | https://sct.ftqq.com/ |
| **PushPlus** | http://www.pushplus.plus/ |
| **GitHub Secrets** | https://github.com/wanibbo/ai-daily-news/settings/secrets/actions |

---

## 💡 提示

1. **可以同时配置多个通知方式**
   - 企业微信 + Server 酱
   - 钉钉 + 企业微信
   - 互不影响

2. **Secret 名称**
   - `WECHAT_WORK_WEBHOOK` - 企业微信
   - `SERVERCHAN_SENDKEY` - Server 酱
   - `PUSHPLUS_TOKEN` - PushPlus
   - `DINGTALK_WEBHOOK` - 钉钉

3. **发送时间**
   - 每天 07:08 左右
   - 与钉钉通知同时发送

---

**配置完成后，每天 07:08 自动收到微信通知！** 🎉
