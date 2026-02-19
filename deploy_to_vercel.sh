#!/bin/bash
# TON空投Bot - Vercel一键部署脚本

echo "🚀 TON空投仪表盘Bot - Vercel部署脚本"
echo "=========================================="

# 检查必要工具
echo "🔧 检查必要工具..."
if ! command -v git &> /dev/null; then
    echo "❌ Git未安装，请先安装Git"
    exit 1
fi

if ! command -v curl &> /dev/null; then
    echo "❌ curl未安装，请先安装curl"
    exit 1
fi

# 设置变量
PROJECT_NAME="ton-airdrop-bot"
GITHUB_USERNAME=""  # 请填写你的GitHub用户名
TELEGRAM_BOT_TOKEN="7977389930:AAEcWTH5gt9OX7vlCgKlD0Y-bkFjDTf_jzM"

echo "📁 项目名称: $PROJECT_NAME"
echo "🔑 Telegram Bot Token: ${TELEGRAM_BOT_TOKEN:0:10}..."

# 步骤1: 创建GitHub仓库
echo ""
echo "📦 步骤1: 创建GitHub仓库"
echo "请访问: https://github.com/new"
echo "创建名为 '$PROJECT_NAME' 的仓库"
read -p "按Enter键继续..."

# 步骤2: 初始化Git仓库
echo ""
echo "📁 步骤2: 初始化Git仓库"
if [ -d ".git" ]; then
    echo "✅ Git仓库已存在"
else
    git init
    git add .
    git commit -m "初始提交: TON空投Bot Vercel版本"
    echo "✅ Git仓库初始化完成"
fi

# 步骤3: 连接到GitHub
echo ""
echo "🔗 步骤3: 连接到GitHub"
if [ -z "$GITHUB_USERNAME" ]; then
    read -p "请输入你的GitHub用户名: " GITHUB_USERNAME
fi

GITHUB_URL="https://github.com/$GITHUB_USERNAME/$PROJECT_NAME.git"
git remote add origin $GITHUB_URL 2>/dev/null || git remote set-url origin $GITHUB_URL
git branch -M main

echo "GitHub仓库URL: $GITHUB_URL"
read -p "按Enter键上传代码..."

# 步骤4: 上传代码
echo ""
echo "⬆️  步骤4: 上传代码到GitHub"
git push -u origin main
if [ $? -eq 0 ]; then
    echo "✅ 代码上传成功"
else
    echo "❌ 代码上传失败，请检查GitHub仓库设置"
    exit 1
fi

# 步骤5: 部署到Vercel
echo ""
echo "☁️  步骤5: 部署到Vercel"
echo "请访问: https://vercel.com/new"
echo "使用GitHub账号登录"
echo "导入仓库: $GITHUB_USERNAME/$PROJECT_NAME"
echo ""
echo "在Vercel部署时，请设置环境变量:"
echo "• TELEGRAM_BOT_TOKEN: $TELEGRAM_BOT_TOKEN"
echo "• WEBHOOK_SECRET: (可选，设置一个随机字符串)"
echo ""
echo "部署完成后，你会获得一个URL，例如:"
echo "https://ton-airdrop-bot.vercel.app"

# 步骤6: 配置Telegram Webhook
echo ""
echo "🤖 步骤6: 配置Telegram Webhook"
read -p "请输入你的Vercel部署URL (例如 https://ton-bot.vercel.app): " VERCEL_URL

if [ -n "$VERCEL_URL" ]; then
    WEBHOOK_URL="$VERCEL_URL/api"
    echo ""
    echo "设置Webhook命令:"
    echo "curl -X POST \\"
    echo "  https://api.telegram.org/bot$TELEGRAM_BOT_TOKEN/setWebhook \\"
    echo "  -H \"Content-Type: application/json\" \\"
    echo "  -d '{\"url\": \"$WEBHOOK_URL\"}'"
    echo ""
    echo "验证Webhook命令:"
    echo "curl https://api.telegram.org/bot$TELEGRAM_BOT_TOKEN/getWebhookInfo"
    
    read -p "是否立即设置Webhook? (y/n): " SET_WEBHOOK
    if [ "$SET_WEBHOOK" = "y" ] || [ "$SET_WEBHOOK" = "Y" ]; then
        echo "设置Webhook..."
        curl -X POST \
          "https://api.telegram.org/bot$TELEGRAM_BOT_TOKEN/setWebhook" \
          -H "Content-Type: application/json" \
          -d "{\"url\": \"$WEBHOOK_URL\"}"
        echo ""
        echo "✅ Webhook设置完成"
    fi
fi

# 步骤7: 测试部署
echo ""
echo "🧪 步骤7: 测试部署"
echo "测试步骤:"
echo "1. 在Telegram中搜索 @TONAirdropDashboardBot"
echo "2. 发送 /start 命令"
echo "3. 测试其他命令: /airdrops, /tonkeeper, /help"
echo "4. 在Vercel控制台查看日志"
echo ""
echo "如果遇到问题，检查:"
echo "• Vercel环境变量是否正确"
echo "• Webhook是否设置成功"
echo "• 查看Vercel函数日志"

# 完成
echo ""
echo "🎉 部署完成！"
echo "=========================================="
echo "📊 项目信息:"
echo "• GitHub仓库: $GITHUB_URL"
echo "• Vercel项目: $VERCEL_URL (如果已设置)"
echo "• Bot用户名: @TONAirdropDashboardBot"
echo "• 测试命令: /start, /airdrops, /help"
echo ""
echo "🔧 维护命令:"
echo "• 更新代码: git push origin main"
echo "• 查看日志: Vercel控制台 → Functions"
echo "• 监控状态: Vercel控制台 → Analytics"
echo ""
echo "🚀 祝你部署顺利！"