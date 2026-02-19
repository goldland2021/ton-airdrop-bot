#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
TON空投Bot - Vercel Serverless Function
符合Vercel Python Runtime规范
"""

import os
import json
import logging
from http.server import BaseHTTPRequestHandler
import sys
import io

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 从环境变量获取配置
TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN', '')
WEBHOOK_SECRET = os.getenv('WEBHOOK_SECRET', '')

# 简单的Bot逻辑（避免复杂依赖）
class SimpleTONBot:
    """简化的Bot逻辑，避免外部依赖问题"""
    
    def __init__(self, token):
        self.token = token
        self.commands = {
            '/start': self.handle_start,
            '/help': self.handle_help,
            '/airdrops': self.handle_airdrops,
            '/myprogress': self.handle_progress,
            '/tonkeeper': self.handle_tonkeeper,
            '/stonfi': self.handle_stonfi,
            '/fragment': self.handle_fragment,
        }
        
        # 模拟的空投项目数据
        self.projects = [
            {"name": "Tonkeeper", "difficulty": "简单", "tasks": ["下载钱包", "创建账户", "完成一次交易"]},
            {"name": "STON.fi", "difficulty": "中等", "tasks": ["连接钱包", "进行swap交易", "提供流动性"]},
            {"name": "Fragment", "difficulty": "简单", "tasks": ["浏览NFT", "关注收藏", "购买一个域名"]},
            {"name": "Getgems", "difficulty": "中等", "tasks": ["创建NFT", "设置合集", "上架作品"]},
            {"name": "Ton Play", "difficulty": "困难", "tasks": ["玩游戏", "完成任务", "邀请好友"]},
        ]
    
    def handle_start(self, user_id, username):
        """处理/start命令"""
        return f"""欢迎 {username} 来到TON空投仪表盘！🎉

我是你的TON生态空投助手，帮你追踪和管理各种空投机会。

📋 可用命令：
/start - 显示此欢迎信息
/help - 获取帮助
/airdrops - 查看当前空投项目
/myprogress - 查看个人进度
/tonkeeper - Tonkeeper教程
/stonfi - STON.fi教程  
/fragment - Fragment教程

🚀 开始你的TON空投之旅吧！"""
    
    def handle_help(self, user_id, username):
        """处理/help命令"""
        return """📚 TON空投Bot帮助指南

🤖 我是谁？
我是TON空投仪表盘Bot，专门帮你追踪和管理TON生态系统的空投机会。

🎯 我能做什么？
• 提供最新的TON空投项目信息
• 指导你完成空投任务
• 追踪你的进度
• 发送提醒通知

📋 核心命令：
/start - 开始使用
/airdrops - 查看所有空投项目
/myprogress - 查看个人进度
/tonkeeper - Tonkeeper钱包教程
/stonfi - STON.fi DEX教程
/fragment - Fragment NFT教程

💡 使用建议：
1. 从/start开始
2. 查看/airdrops了解项目
3. 选择感兴趣的项目开始
4. 使用教程命令获取详细指导

有任何问题？随时联系！"""
    
    def handle_airdrops(self, user_id, username):
        """处理/airdrops命令"""
        projects_text = "📊 当前空投项目列表：\n\n"
        
        for i, project in enumerate(self.projects, 1):
            projects_text += f"{i}. {project['name']}\n"
            projects_text += f"   难度: {project['difficulty']}\n"
            projects_text += f"   任务: {', '.join(project['tasks'][:2])}...\n\n"
        
        projects_text += "💡 使用 /tonkeeper, /stonfi, /fragment 获取详细教程"
        return projects_text
    
    def handle_progress(self, user_id, username):
        """处理/myprogress命令"""
        return f"""📈 {username} 的个人进度

🎯 总体进度: 25%
✅ 已完成项目: 1/5
⏳ 进行中项目: 2/5
📅 注册时间: 2026-02-19

📊 项目详情：
1. Tonkeeper - ✅ 已完成
2. STON.fi - 🔄 进行中 (50%)
3. Fragment - 🔄 进行中 (25%)
4. Getgems - ⏸️ 未开始
5. Ton Play - ⏸️ 未开始

💪 继续努力！完成更多项目获得更多空投机会！"""
    
    def handle_tonkeeper(self, user_id, username):
        """处理/tonkeeper命令"""
        return """🔐 Tonkeeper钱包教程

Tonkeeper是TON生态最流行的钱包，以下是详细步骤：

📱 步骤1: 下载安装
• iOS: App Store搜索"Tonkeeper"
• Android: Google Play搜索"Tonkeeper"
• 或访问: https://tonkeeper.com

🔑 步骤2: 创建钱包
1. 打开Tonkeeper应用
2. 点击"创建新钱包"
3. 备份助记词（非常重要！）
4. 设置密码

💰 步骤3: 获取测试币
1. 访问: https://t.me/testgiver_ton_bot
2. 发送 /start
3. 获取免费测试TON币

🔄 步骤4: 完成基本任务
1. 发送一笔交易（任意金额）
2. 接收一笔交易
3. 探索DApp浏览器

🎯 空投任务：
• 完成至少3笔交易
• 连接至少2个DApp
• 持有至少1个TON

💡 提示：保持钱包活跃，定期使用！"""
    
    def handle_stonfi(self, user_id, username):
        """处理/stonfi命令"""
        return """💱 STON.fi DEX教程

STON.fi是TON生态最大的去中心化交易所：

🌐 步骤1: 访问网站
• 网址: https://ston.fi
• 连接Tonkeeper钱包

💼 步骤2: 首次使用
1. 点击"Connect Wallet"
2. 选择Tonkeeper
3. 授权连接

🔄 步骤3: 进行Swap交易
1. 选择要交换的代币（如TON→jUSDT）
2. 输入金额
3. 确认交易
4. 等待完成

🏊 步骤4: 提供流动性
1. 进入"Liquidity"页面
2. 选择交易对（如TON/jUSDT）
3. 输入等值的两种代币
4. 确认添加流动性

🎯 空投任务：
• 完成至少5次Swap交易
• 提供至少1个流动性池
• 交易总额超过$100

📈 提示：从小额开始，熟悉界面后再进行大额操作！"""
    
    def handle_fragment(self, user_id, username):
        """处理/fragment命令"""
        return """🎨 Fragment NFT教程

Fragment是TON生态的NFT和域名市场：

🌐 步骤1: 访问平台
• 网址: https://fragment.com
• 无需连接钱包（直接使用Telegram）

🔍 步骤2: 浏览收藏
1. 探索热门NFT合集
2. 查看TON域名（.ton）
3. 了解价格趋势

🛒 步骤3: 购买NFT
1. 选择喜欢的NFT
2. 点击"Buy Now"
3. 通过Telegram支付
4. 确认交易

🏷️ 步骤4: 获取域名
1. 搜索想要的.ton域名
2. 检查可用性
3. 购买并设置解析

🎯 空投任务：
• 购买至少1个NFT
• 浏览10个不同合集
• 关注官方Fragment频道

💎 提示：.ton域名有实际使用价值，可以考虑投资！"""
    
    def process_command(self, user_id, username, text):
        """处理用户命令"""
        command = text.split()[0] if text else ""
        
        if command in self.commands:
            return self.commands[command](user_id, username)
        else:
            return f"未知命令: {command}\n使用 /help 查看可用命令"

# 初始化Bot
bot = SimpleTONBot(TELEGRAM_BOT_TOKEN) if TELEGRAM_BOT_TOKEN else None

def handler(request, context):
    """Vercel Serverless Function主处理函数"""
    
    # 解析请求
    method = request.get('method', 'GET')
    path = request.get('path', '/')
    headers = request.get('headers', {})
    body = request.get('body', '')
    
    logger.info(f"收到请求: {method} {path}")
    
    # 健康检查端点
    if method == 'GET' and path == '/api/health':
        return {
            'statusCode': 200,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'
            },
            'body': json.dumps({
                'status': 'ok',
                'service': 'TON Airdrop Bot',
                'bot_available': bot is not None,
                'timestamp': '2026-02-19T19:00:00Z'
            })
        }
    
    # Telegram Webhook端点
    elif method == 'POST' and path == '/api/webhook':
        try:
            if not body:
                return {
                    'statusCode': 400,
                    'body': json.dumps({'error': 'No body provided'})
                }
            
            data = json.loads(body)
            logger.info(f"Webhook数据: {json.dumps(data)[:200]}")
            
            # 提取消息
            message = data.get('message', {})
            if not message:
                return {
                    'statusCode': 200,
                    'body': json.dumps({'status': 'ignored', 'reason': 'No message'})
                }
            
            # 处理消息
            user_id = message.get('from', {}).get('id')
            username = message.get('from', {}).get('username', 'user')
            text = message.get('text', '')
            
            if not text:
                return {
                    'statusCode': 200,
                    'body': json.dumps({'status': 'ignored', 'reason': 'No text'})
                }
            
            # 使用Bot处理命令
            if bot:
                response_text = bot.process_command(user_id, username, text)
                
                # 在实际部署中，这里应该调用Telegram API发送消息
                # 但由于是Serverless演示，我们只返回处理结果
                
                return {
                    'statusCode': 200,
                    'headers': {'Content-Type': 'application/json'},
                    'body': json.dumps({
                        'status': 'processed',
                        'user_id': user_id,
                        'username': username,
                        'command': text,
                        'response_preview': response_text[:100]
                    })
                }
            else:
                return {
                    'statusCode': 503,
                    'body': json.dumps({'error': 'Bot not initialized'})
                }
                
        except json.JSONDecodeError:
            return {
                'statusCode': 400,
                'body': json.dumps({'error': 'Invalid JSON'})
            }
        except Exception as e:
            logger.error(f"处理Webhook时出错: {e}")
            return {
                'statusCode': 500,
                'body': json.dumps({'error': str(e)})
            }
    
    # 默认响应
    else:
        return {
            'statusCode': 404,
            'headers': {'Content-Type': 'application/json'},
            'body': json.dumps({
                'error': 'Not found',
                'available_endpoints': ['GET /api/health', 'POST /api/webhook']
            })
        }

# 本地测试
if __name__ == '__main__':
    # 模拟请求
    test_request = {
        'method': 'GET',
        'path': '/api/health',
        'headers': {},
        'body': ''
    }
    
    response = handler(test_request, {})
    print(json.dumps(response, indent=2))