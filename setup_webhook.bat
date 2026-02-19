@echo off
chcp 65001 > nul
echo ==========================================
echo 🤖 TON空投Bot - Webhook配置脚本
echo ==========================================
echo.

set BOT_TOKEN=7977389930:AAEcWTH5gt9OX7vlCgKlD0Y-bkFjDTf_jzM
set VERCEL_URL=https://ton-airdrop-bot-7553.vercel.app
set WEBHOOK_URL=%VERCEL_URL%/api/webhook

echo Bot Token: %BOT_TOKEN:~0,10%...
echo Vercel URL: %VERCEL_URL%
echo Webhook URL: %WEBHOOK_URL%
echo.

echo 步骤1: 设置Telegram Webhook...
curl -X POST "https://api.telegram.org/bot%BOT_TOKEN%/setWebhook" ^
  -H "Content-Type: application/json" ^
  -d "{\"url\": \"%WEBHOOK_URL%\"}"

echo.
echo.
echo 步骤2: 验证Webhook配置...
curl "https://api.telegram.org/bot%BOT_TOKEN%/getWebhookInfo"

echo.
echo.
echo 步骤3: 测试Vercel部署...
echo 健康检查:
curl "%VERCEL_URL%/"

echo.
echo API状态:
curl "%VERCEL_URL%/api/health"

echo.
echo.
echo ==========================================
echo 🎉 Webhook配置完成！
echo ==========================================
echo.
echo 📋 下一步:
echo 1. 打开Telegram
echo 2. 搜索 @TONAirdropDashboardBot
echo 3. 发送 /start 命令
echo 4. 测试其他命令:
echo    • /help - 帮助信息
echo    • /airdrops - 空投项目
echo    • /myprogress - 个人进度
echo.
echo 🔗 重要链接:
echo • Bot: https://t.me/TONAirdropDashboardBot
echo • Vercel: %VERCEL_URL%
echo • GitHub: https://github.com/goldland2021/ton-airdrop-bot
echo.
pause