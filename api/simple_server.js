// 极简Telegram Bot - 确保能工作
const express = require('express');
const app = express();

app.use(express.json());

// 健康检查
app.get('/', (req, res) => {
  res.json({ 
    status: 'ok', 
    service: 'TON Bot Simple',
    timestamp: new Date().toISOString()
  });
});

// Telegram Webhook - 极简版本
app.post('/api/webhook', async (req, res) => {
  console.log('收到Webhook请求:', JSON.stringify(req.body).substring(0, 200));
  
  try {
    const { message } = req.body;
    
    if (!message) {
      console.log('没有message字段');
      return res.json({ status: 'ignored' });
    }
    
    const { text, chat, from } = message;
    const chatId = chat?.id;
    const username = from?.username || 'user';
    
    console.log(`收到消息: chatId=${chatId}, text=${text}, user=${username}`);
    
    // 立即响应Telegram
    res.json({ status: 'received' });
    
    if (!text || !chatId) {
      console.log('缺少text或chatId');
      return;
    }
    
    // 处理命令
    let responseText = '未知命令';
    
    if (text === '/start') {
      responseText = `欢迎 ${username}！🎉\n\n我是TON空投Bot测试版本。\n发送 /help 查看可用命令。`;
    } else if (text === '/help') {
      responseText = '可用命令:\n/start - 开始\n/help - 帮助\ntest - 测试';
    } else if (text === 'test') {
      responseText = '测试成功！Bot正常工作。';
    } else {
      responseText = `收到: ${text}\n发送 /help 查看命令。`;
    }
    
    console.log(`准备发送回复: ${responseText.substring(0, 50)}...`);
    
    // 发送回复到Telegram
    const TELEGRAM_TOKEN = process.env.TELEGRAM_BOT_TOKEN;
    
    if (!TELEGRAM_TOKEN) {
      console.error('错误: TELEGRAM_BOT_TOKEN环境变量未设置');
      return;
    }
    
    const telegramResponse = await fetch(`https://api.telegram.org/bot${TELEGRAM_TOKEN}/sendMessage`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        chat_id: chatId,
        text: responseText,
        parse_mode: 'HTML'
      })
    });
    
    const result = await telegramResponse.json();
    console.log('Telegram API响应:', JSON.stringify(result).substring(0, 200));
    
    if (!result.ok) {
      console.error('Telegram API错误:', result.description);
    }
    
  } catch (error) {
    console.error('处理Webhook时出错:', error);
    // 已经发送了响应，只能记录错误
  }
});

// 导出给Vercel
module.exports = app;