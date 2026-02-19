# ☁️ TON空投Bot - Vercel部署指南

## 🎯 为什么选择Vercel？

### 核心优势：
```
✅ 完全免费（Hobby计划）
✅ 自动SSL证书（HTTPS）
✅ 全球CDN加速
✅ Git推送自动部署
✅ 无需服务器运维
✅ Serverless自动扩缩容
✅ 内置监控和日志
✅ 非常适合Bot类应用
```

### 免费额度：
```
• Serverless Functions: 100GB小时/月
• 带宽: 100GB/月
• 构建时间: 100小时/月
• 完全足够初期使用
• 可升级到Pro（$20/月）获得更多资源
```

## 🚀 部署架构

### Webhook模式：
```
用户 → Telegram → Vercel Function → 返回响应
```

### 优点：
```
• 无需长期运行进程
• 按请求计费（免费额度内免费）
• 自动扩缩容
• 全球低延迟（通过CDN）
```

### 注意事项：
```
• 冷启动可能有1-2秒延迟
• 需要配置Telegram Webhook
• 函数执行时间限制（10秒默认）
• 适合大多数Bot场景
```

## 📋 部署前准备

### 1. 注册Vercel账号
```
访问: https://vercel.com
注册: 使用GitHub账号（推荐）
验证: 邮箱验证
```

### 2. 准备GitHub仓库
```
1. 在GitHub创建新仓库
2. 名称: ton-airdrop-bot
3. 描述: TON空投仪表盘Telegram Bot
4. 公开仓库（免费部署）
5. 初始化README（可选）
```

### 3. 代码调整
```
已创建的文件：
• vercel.json - Vercel配置
• api/bot.py - Serverless Function
• requirements.txt - Python依赖
• 其他原有文件保持不变
```

## 🔧 部署步骤

### 步骤1：上传代码到GitHub
```bash
# 初始化Git仓库
git init
git add .
git commit -m "初始提交: TON空投Bot Vercel版本"

# 连接到GitHub仓库
git remote add origin https://github.com/你的用户名/ton-airdrop-bot.git
git branch -M main
git push -u origin main
```

### 步骤2：在Vercel导入项目
```
1. 登录Vercel控制台
2. 点击"New Project"
3. 选择"Import Git Repository"
4. 选择你的ton-airdrop-bot仓库
5. 点击"Import"
```

### 步骤3：配置环境变量
```
在Vercel项目设置中配置：
• TELEGRAM_BOT_TOKEN: 你的Bot Token
• WEBHOOK_SECRET: 自定义密钥（可选）
• PYTHON_VERSION: 3.9（默认）
```

### 步骤4：部署
```
1. Vercel会自动检测配置
2. 点击"Deploy"
3. 等待构建完成（1-2分钟）
4. 获得部署URL（如：https://ton-bot.vercel.app）
```

### 步骤5：配置Telegram Webhook
```bash
# 设置Webhook（替换为你的Vercel URL）
curl -X POST https://api.telegram.org/bot<TELEGRAM_BOT_TOKEN>/setWebhook \
  -H "Content-Type: application/json" \
  -d '{"url": "https://ton-bot.vercel.app/api/bot"}'

# 验证Webhook设置
curl https://api.telegram.org/bot<TELEGRAM_BOT_TOKEN>/getWebhookInfo
```

## 📁 项目文件结构

### 部署所需文件：
```
ton-airdrop-bot/
├── api/
│   └── bot.py              # Serverless Function入口
├── bot_framework.py        # Bot核心逻辑
├── run_bot.py             # 本地运行脚本（保留）
├── config.py              # 配置文件（Token从环境变量读取）
├── requirements.txt       # Python依赖
├── vercel.json           # Vercel配置
├── .gitignore            # Git忽略文件
└── README.md             # 项目说明
```

### 关键文件说明：

#### `vercel.json`
```json
{
  "functions": {
    "api/bot.py": {
      "maxDuration": 10  // 函数最大执行时间（秒）
    }
  },
  "rewrites": [
    {
      "source": "/api/(.*)",
      "destination": "/api/bot.py"
    }
  ]
}
```

#### `api/bot.py`
```python
# Serverless Function处理Telegram Webhook
# 接收POST请求，处理消息，返回响应
# 通过环境变量获取配置
```

## ⚙️ 环境变量配置

### 必需变量：
```
TELEGRAM_BOT_TOKEN=7977389930:AAEcWTH5gt9OX7vlCgKlD0Y-bkFjDTf_jzM
```

### 可选变量：
```
WEBHOOK_SECRET=your_secret_key  # Webhook验证
PYTHON_VERSION=3.9              # Python版本
LOG_LEVEL=INFO                  # 日志级别
```

### 在Vercel中设置：
```
1. 项目控制台 → Settings → Environment Variables
2. 添加变量（区分生产/预览环境）
3. 点击"Save"
4. 重新部署生效
```

## 🔄 本地开发和工作流

### 本地测试：
```bash
# 安装Vercel CLI
npm i -g vercel

# 本地开发
vercel dev

# 访问 http://localhost:3000/api/bot
```

### 开发工作流：
```
1. 本地修改代码
2. 测试功能：python run_bot.py（本地模式）
3. 提交到GitHub
4. Vercel自动部署
5. 测试生产环境
```

### 分支策略：
```
main分支 → 生产环境（自动部署）
develop分支 → 预览环境（测试）
feature/*分支 → 功能开发
```

## 📊 监控和日志

### Vercel内置监控：
```
• 访问统计
• 函数执行时间
• 错误率
• 带宽使用
• 在控制台查看
```

### 查看日志：
```
1. Vercel控制台 → Analytics
2. 查看函数调用日志
3. 错误追踪
4. 性能监控
```

### 自定义日志：
```python
import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
logger.info("处理消息...")
```

## 🛡️ 安全配置

### Webhook验证：
```python
# 验证请求来源
if request.headers.get('X-Telegram-Bot-Api-Secret-Token') != SECRET:
    return {"error": "Unauthorized"}
```

### 环境变量保护：
```
• 不要将Token提交到代码
• 使用Vercel环境变量
• 定期轮换密钥
• 限制访问权限
```

### 速率限制：
```python
# 可添加速率限制
from flask_limiter import Limiter
limiter = Limiter(key_func=get_remote_address)
```

## 🚀 高级配置

### 自定义域名：
```
1. 在Vercel添加自定义域名
2. 配置DNS记录
3. 自动获取SSL证书
4. 提升专业形象
```

### 数据库集成：
```
• Vercel Postgres（免费套餐）
• 存储用户数据
• 持久化进度
• 在Vercel市场添加
```

### 定时任务（Cron Jobs）：
```
• Vercel Cron Jobs（Pro功能）
• 定时发送提醒
• 数据更新任务
• 监控检查
```

## 🆘 故障排除

### 常见问题：

#### 1. 部署失败
```
检查：requirements.txt是否正确
检查：Python版本兼容性
检查：环境变量是否设置
查看：Vercel构建日志
```

#### 2. Webhook不工作
```
验证：Webhook URL是否正确
验证：Token是否有权限
测试：手动发送请求测试
查看：Vercel函数日志
```

#### 3. 冷启动延迟
```
方案：使用Pro计划减少冷启动
方案：预热函数（定时调用）
方案：优化代码启动时间
```

#### 4. 函数超时
```
调整：vercel.json中的maxDuration
优化：减少初始化时间
拆分：复杂任务拆分为多个函数
```

### 调试命令：
```bash
# 查看部署状态
vercel logs

# 本地测试Webhook
curl -X POST http://localhost:3000/api/bot \
  -H "Content-Type: application/json" \
  -d '{"message": {"text": "/start"}}'

# 检查环境变量
vercel env ls
```

## 📈 性能优化

### 代码优化：
```python
# 延迟加载模块
def get_bot():
    if not hasattr(get_bot, '_instance'):
        from bot_framework import TONAirdropBot
        get_bot._instance = TONAirdropBot(os.getenv('TELEGRAM_BOT_TOKEN'))
    return get_bot._instance

# 减少冷启动时间
bot = None
def handler(event, context):
    global bot
    if bot is None:
        from bot_framework import TONAirdropBot
        bot = TONAirdropBot(os.getenv('TELEGRAM_BOT_TOKEN'))
    # 处理逻辑
```

### 依赖优化：
```
• 减少不必要的依赖
• 使用轻量级库
• 压缩代码大小
• 分层部署
```

## 🔄 从本地迁移到Vercel

### 迁移步骤：
```
1. 调整代码支持Webhook模式
2. 创建Vercel配置文件
3. 上传到GitHub
4. 在Vercel部署
5. 配置Telegram Webhook
6. 测试功能
7. 关闭本地Bot
```

### 数据迁移：
```
用户数据：目前是内存存储，需要添加数据库
配置文件：从文件读取改为环境变量
日志系统：使用Vercel日志服务
```

## 💰 成本分析

### 免费套餐（Hobby）：
```
• Serverless Functions: 100GB小时/月
• 带宽: 100GB/月
• 构建: 100小时/月
• 监控: 基本监控
• 足够支持：1000+日活跃用户
```

### Pro套餐（$20/月）：
```
• 无冷启动（优先执行）
• 更多构建时间
• 团队协作功能
• 高级监控
• 自定义域名SSL
```

### 与传统服务器对比：
```
腾讯云服务器: ¥35/月 ($5)
Vercel Pro: $20/月
优势: 无需运维，自动扩缩容，全球CDN
```

## 🎯 部署检查清单

### 部署前：
```
✅ 代码支持Webhook模式
✅ 创建vercel.json配置
✅ 准备requirements.txt
✅ 设置.gitignore
✅ 创建GitHub仓库
```

### 部署中：
```
✅ 在Vercel导入项目
✅ 配置环境变量
✅ 完成首次部署
✅ 获取部署URL
✅ 配置Telegram Webhook
```

### 部署后：
```
✅ 测试所有命令
✅ 验证响应时间
✅ 检查日志记录
✅ 监控资源使用
✅ 准备回滚方案
```

## 📞 支持资源

### 官方文档：
```
• Vercel文档: https://vercel.com/docs
• Python on Vercel: https://vercel.com/docs/concepts/functions/serverless-functions/runtimes/python
• Telegram Bot API: https://core.telegram.org/bots/api
```

### 社区支持：
```
• Vercel社区论坛
• GitHub Discussions
• Telegram Bot开发群组
• Stack Overflow
```

### 示例项目：
```
• Vercel官方示例: https://github.com/vercel/examples
• Telegram Bot模板: https://github.com/vercel/vercel/tree/main/examples/python-telegram-bot
```

---

## 🚀 立即开始部署！

### 预计时间：
```
代码准备: 30分钟（已完成）
GitHub上传: 10分钟
Vercel部署: 10分钟
Webhook配置: 5分钟
测试验证: 15分钟
总计: 约1小时
```

### 成功标志：
```
✅ Vercel部署成功（获得URL）
✅ Telegram Webhook设置成功
✅ Bot响应所有命令
✅ 日志记录正常
✅ 24/7可用性
```

### 你的行动：
```
1. 创建GitHub仓库
2. 上传代码
3. 在Vercel部署
4. 配置Webhook
5. 测试功能
```

---

**推荐程度**: ⭐⭐⭐⭐⭐（五星推荐）  
**成本**: 完全免费（初期）  
**复杂度**: 中等（需要配置Webhook）  
**稳定性**: 高（Vercel企业级基础设施）  
**维护需求**: 极低（自动部署和监控）  

**立即开始Vercel部署吧！** 😎🚀