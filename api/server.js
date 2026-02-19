// TON空投Bot - Node.js版本（完整功能）
// 实际调用Telegram API发送回复

const express = require('express');
const app = express();
const PORT = process.env.PORT || 3000;

// Node.js 18+ 内置了fetch，无需额外导入

// 中间件
app.use(express.json());
app.use(express.urlencoded({ extended: true }));

// 健康检查
app.get('/', (req, res) => {
  res.json({
    status: 'ok',
    service: 'TON Airdrop Bot',
    version: '1.0.0',
    environment: process.env.NODE_ENV || 'development',
    timestamp: new Date().toISOString()
  });
});

// API健康检查
app.get('/api/health', (req, res) => {
  res.json({
    status: 'healthy',
    bot_token_configured: !!process.env.TELEGRAM_BOT_TOKEN,
    timestamp: new Date().toISOString()
  });
});

// Telegram Webhook
app.post('/api/webhook', async (req, res) => {
  try {
    const { message } = req.body;
    
    if (!message) {
      return res.json({ status: 'ignored', reason: 'No message' });
    }
    
    const { text, from, chat } = message;
    const userId = from?.id;
    const username = from?.username || 'user';
    const chatId = chat?.id;
    
    if (!text) {
      return res.json({ status: 'ignored', reason: 'No text' });
    }
    
    // 立即响应Telegram，避免超时
    res.json({ status: 'received' });
    
    // 处理命令
    const responseText = processCommand(text, userId, username);
    
    // 调用Telegram API发送回复
    await sendTelegramMessage(chatId, responseText);
    
  } catch (error) {
    console.error('Webhook error:', error);
    // 已经发送了响应，只能记录错误
  }
});

// 发送Telegram消息函数
async function sendTelegramMessage(chatId, text) {
  const TELEGRAM_BOT_TOKEN = process.env.TELEGRAM_BOT_TOKEN;
  
  if (!TELEGRAM_BOT_TOKEN || !chatId) {
    console.error('Missing Telegram token or chat ID');
    return;
  }
  
  try {
    const response = await fetch(`https://api.telegram.org/bot${TELEGRAM_BOT_TOKEN}/sendMessage`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        chat_id: chatId,
        text: text,
        parse_mode: 'HTML'
      })
    });
    
    const result = await response.json();
    
    if (!result.ok) {
      console.error('Telegram API error:', result);
    } else {
      console.log('Message sent successfully to chat:', chatId);
    }
    
  } catch (error) {
    console.error('Failed to send Telegram message:', error);
  }
}

// 命令处理函数
function processCommand(command, userId, username) {
  const commands = {
    '/start': `欢迎 ${username} 来到TON空投仪表盘！🎉

我是你的TON生态空投助手。

📋 可用命令：
/start - 显示此信息
/help - 获取帮助
/airdrops - 查看空投项目
/myprogress - 查看进度

🚀 开始你的空投之旅！`,
    
    '/help': `📚 TON空投Bot帮助

🤖 功能：
• 提供TON空投信息
• 指导完成任务
• 追踪你的进度

📋 命令：
/start - 开始使用
/airdrops - 查看项目
/myprogress - 查看进度

💡 建议从/start开始！`,
    
    '/airdrops': `📊 当前空投项目：

1. Tonkeeper钱包
   难度: 简单
   任务: 下载、创建账户、交易

2. STON.fi DEX
   难度: 中等  
   任务: 连接钱包、Swap交易、流动性

3. Fragment NFT
   难度: 简单
   任务: 浏览NFT、购买域名

💡 更多功能开发中！`,
    
    '/myprogress': `📈 ${username} 的个人进度

🎯 总体进度: 25%
✅ 已完成: 1/3项目
⏳ 进行中: 2/3项目

📊 详情：
• Tonkeeper - ✅ 完成
• STON.fi - 🔄 50%
• Fragment - 🔄 25%

💪 继续努力！`
  };
  
  // 默认响应
  const defaultResponse = `未知命令: ${command}

📋 可用命令：
/start - 开始使用
/help - 获取帮助  
/airdrops - 查看项目
/myprogress - 查看进度

使用 /help 获取详细信息`;
  
  return commands[command] || defaultResponse;
}

// 404处理
app.use((req, res) => {
  res.status(404).json({
    error: 'Not found',
    path: req.path,
    method: req.method,
    available_endpoints: [
      'GET /',
      'GET /api/health',
      'POST /api/webhook'
    ]
  });
});

// 错误处理
app.use((err, req, res, next) => {
  console.error('Server error:', err);
  res.status(500).json({ error: 'Internal server error' });
});

// 启动服务器
if (require.main === module) {
  app.listen(PORT, () => {
    console.log(`TON Airdrop Bot running on port ${PORT}`);
    console.log(`Health check: http://localhost:${PORT}/`);
    console.log(`Webhook endpoint: http://localhost:${PORT}/api/webhook`);
  });
}

// 导出给Vercel使用
module.exports = app;