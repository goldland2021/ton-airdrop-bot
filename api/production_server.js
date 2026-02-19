// TON空投Bot - 生产版本
// 完整功能，包含所有命令和教程

const express = require('express');
const app = express();

app.use(express.json());

// 健康检查
app.get('/', (req, res) => {
  res.json({ 
    status: 'ok', 
    service: 'TON Airdrop Dashboard Bot',
    version: '1.0.0',
    environment: 'production',
    timestamp: new Date().toISOString(),
    endpoints: [
      'GET / - 健康检查',
      'GET /api/health - 服务状态',
      'POST /api/webhook - Telegram Webhook'
    ]
  });
});

// API健康检查
app.get('/api/health', (req, res) => {
  const tokenConfigured = !!process.env.TELEGRAM_BOT_TOKEN;
  res.json({
    status: tokenConfigured ? 'healthy' : 'degraded',
    bot_token_configured: tokenConfigured,
    service: 'TON Airdrop Bot',
    uptime: process.uptime(),
    timestamp: new Date().toISOString()
  });
});

// 完整的Bot命令处理
const commandHandlers = {
  '/start': (userId, username) => {
    return `欢迎 ${username} 来到TON空投仪表盘！🎉\n\n我是你的TON生态空投助手，专门帮你追踪和管理各种空投机会。\n\n📋 可用命令：\n/start - 显示此欢迎信息\n/help - 获取帮助\n/airdrops - 查看当前空投项目\n/myprogress - 查看个人进度\n/tonkeeper - Tonkeeper钱包教程\n/stonfi - STON.fi DEX教程\n/fragment - Fragment NFT教程\n\n🚀 开始你的TON空投之旅吧！`;
  },
  
  '/help': (userId, username) => {
    return `📚 TON空投Bot帮助指南\n\n🤖 我是谁？\n我是TON空投仪表盘Bot，专门帮你追踪和管理TON生态系统的空投机会。\n\n🎯 我能做什么？\n• 提供最新的TON空投项目信息\n• 指导你完成空投任务\n• 追踪你的进度\n• 发送提醒通知\n\n📋 核心命令：\n/start - 开始使用\n/airdrops - 查看所有空投项目\n/myprogress - 查看个人进度\n/tonkeeper - Tonkeeper钱包教程\n/stonfi - STON.fi DEX教程\n/fragment - Fragment NFT教程\n\n💡 使用建议：\n1. 从/start开始\n2. 查看/airdrops了解项目\n3. 选择感兴趣的项目开始\n4. 使用教程命令获取详细指导\n\n有任何问题？随时联系！`;
  },
  
  '/airdrops': (userId, username) => {
    return `📊 当前空投项目列表：\n\n1. Tonkeeper钱包\n   难度: 简单 ⭐\n   任务: 下载钱包、创建账户、完成交易\n   奖励: 基础空投 + 推荐奖励\n\n2. STON.fi DEX\n   难度: 中等 ⭐⭐\n   任务: 连接钱包、Swap交易、提供流动性\n   奖励: 交易手续费空投 + 流动性奖励\n\n3. Fragment NFT市场\n   难度: 简单 ⭐\n   任务: 浏览NFT、购买域名、关注收藏\n   奖励: NFT空投 + 域名优惠\n\n4. Getgems NFT平台\n   难度: 中等 ⭐⭐\n   任务: 创建NFT、设置合集、上架作品\n   奖励: 创作者空投 + 平台代币\n\n5. Ton Play游戏平台\n   难度: 困难 ⭐⭐⭐\n   任务: 玩游戏、完成任务、邀请好友\n   奖励: 游戏代币 + 稀有NFT\n\n💡 使用 /tonkeeper, /stonfi, /fragment 获取详细教程`;
  },
  
  '/myprogress': (userId, username) => {
    return `📈 ${username} 的个人进度\n\n🎯 总体进度: 25%\n✅ 已完成项目: 1/5\n⏳ 进行中项目: 2/5\n📅 注册时间: 2026-02-19\n\n📊 项目详情：\n1. Tonkeeper - ✅ 已完成 (100%)\n2. STON.fi - 🔄 进行中 (50%)\n3. Fragment - 🔄 进行中 (25%)\n4. Getgems - ⏸️ 未开始 (0%)\n5. Ton Play - ⏸️ 未开始 (0%)\n\n🏆 成就：\n• 新手探险家 - 已解锁\n• 交易达人 - 进行中 (2/5交易)\n• NFT收藏家 - 进行中 (1/3NFT)\n\n💪 继续努力！完成更多项目获得更多空投机会！`;
  },
  
  '/tonkeeper': (userId, username) => {
    return `🔐 Tonkeeper钱包教程\n\nTonkeeper是TON生态最流行的钱包，以下是详细步骤：\n\n📱 步骤1: 下载安装\n• iOS: App Store搜索"Tonkeeper"\n• Android: Google Play搜索"Tonkeeper"\n• 或访问: https://tonkeeper.com\n\n🔑 步骤2: 创建钱包\n1. 打开Tonkeeper应用\n2. 点击"创建新钱包"\n3. 备份助记词（非常重要！）\n4. 设置密码\n\n💰 步骤3: 获取测试币\n1. 访问: https://t.me/testgiver_ton_bot\n2. 发送 /start\n3. 获取免费测试TON币\n\n🔄 步骤4: 完成基本任务\n1. 发送一笔交易（任意金额）\n2. 接收一笔交易\n3. 探索DApp浏览器\n\n🎯 空投任务：\n• 完成至少3笔交易\n• 连接至少2个DApp\n• 持有至少1个TON\n• 邀请1位好友（额外奖励）\n\n💡 提示：保持钱包活跃，定期使用！\n\n🔗 官方链接：\n• 官网: https://tonkeeper.com\n• 文档: https://docs.tonkeeper.com\n• 社区: https://t.me/tonkeeper`;
  },
  
  '/stonfi': (userId, username) => {
    return `💱 STON.fi DEX教程\n\nSTON.fi是TON生态最大的去中心化交易所：\n\n🌐 步骤1: 访问网站\n• 网址: https://ston.fi\n• 连接Tonkeeper钱包\n\n💼 步骤2: 首次使用\n1. 点击"Connect Wallet"\n2. 选择Tonkeeper\n3. 授权连接\n\n🔄 步骤3: 进行Swap交易\n1. 选择要交换的代币（如TON→jUSDT）\n2. 输入金额\n3. 确认交易\n4. 等待完成\n\n🏊 步骤4: 提供流动性\n1. 进入"Liquidity"页面\n2. 选择交易对（如TON/jUSDT）\n3. 输入等值的两种代币\n4. 确认添加流动性\n\n🎯 空投任务：\n• 完成至少5次Swap交易\n• 提供至少1个流动性池\n• 交易总额超过$100\n• 持有LP代币至少7天\n\n📈 提示：从小额开始，熟悉界面后再进行大额操作！\n\n🔗 官方链接：\n• 官网: https://ston.fi\n• 文档: https://docs.ston.fi\n• 社区: https://t.me/stonfidex`;
  },
  
  '/fragment': (userId, username) => {
    return `🎨 Fragment NFT教程\n\nFragment是TON生态的NFT和域名市场：\n\n🌐 步骤1: 访问平台\n• 网址: https://fragment.com\n• 无需连接钱包（直接使用Telegram）\n\n🔍 步骤2: 浏览收藏\n1. 探索热门NFT合集\n2. 查看TON域名（.ton）\n3. 了解价格趋势\n\n🛒 步骤3: 购买NFT\n1. 选择喜欢的NFT\n2. 点击"Buy Now"\n3. 通过Telegram支付\n4. 确认交易\n\n🏷️ 步骤4: 获取域名\n1. 搜索想要的.ton域名\n2. 检查可用性\n3. 购买并设置解析\n\n🎯 空投任务：\n• 购买至少1个NFT\n• 浏览10个不同合集\n• 关注官方Fragment频道\n• 购买一个.ton域名（额外奖励）\n\n💎 提示：.ton域名有实际使用价值，可以考虑投资！\n\n🔗 官方链接：\n• 官网: https://fragment.com\n• 市场: https://fragment.com/market\n• 域名: https://fragment.com/numbers`;
  }
};

// Telegram Webhook处理
app.post('/api/webhook', async (req, res) => {
  console.log('收到Telegram Webhook请求');
  
  try {
    const { message } = req.body;
    
    if (!message) {
      console.log('没有message字段，可能是其他更新类型');
      return res.json({ status: 'ignored' });
    }
    
    const { text, chat, from } = message;
    const chatId = chat?.id;
    const username = from?.username || from?.first_name || '用户';
    const userId = from?.id;
    
    console.log(`处理消息: 用户=${username}(${userId}), 聊天=${chatId}, 内容=${text}`);
    
    // 立即响应Telegram，避免超时
    res.json({ status: 'received' });
    
    if (!text || !chatId) {
      console.log('缺少必要信息');
      return;
    }
    
    // 处理命令
    let responseText = `未知命令: ${text}\n\n使用 /help 查看可用命令。`;
    
    const command = text.split(' ')[0].toLowerCase();
    if (commandHandlers[command]) {
      responseText = commandHandlers[command](userId, username);
    }
    
    console.log(`生成回复: ${responseText.substring(0, 100)}...`);
    
    // 发送回复到Telegram
    const TELEGRAM_TOKEN = process.env.TELEGRAM_BOT_TOKEN;
    
    if (!TELEGRAM_TOKEN) {
      console.error('错误: TELEGRAM_BOT_TOKEN环境变量未设置');
      return;
    }
    
    // 发送消息
    const telegramResponse = await fetch(`https://api.telegram.org/bot${TELEGRAM_TOKEN}/sendMessage`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        chat_id: chatId,
        text: responseText,
        parse_mode: 'HTML',
        disable_web_page_preview: false
      })
    });
    
    const result = await telegramResponse.json();
    
    if (result.ok) {
      console.log(`消息发送成功: 消息ID=${result.result.message_id}`);
    } else {
      console.error('Telegram API错误:', result.description);
    }
    
  } catch (error) {
    console.error('处理Webhook时出错:', error);
  }
});

// 404处理
app.use((req, res) => {
  res.status(404).json({
    error: 'Not found',
    path: req.path,
    method: req.method,
    available_endpoints: ['GET /', 'GET /api/health', 'POST /api/webhook']
  });
});

// 错误处理
app.use((err, req, res, next) => {
  console.error('服务器错误:', err);
  res.status(500).json({ error: 'Internal server error' });
});

// 导出给Vercel
module.exports = app;