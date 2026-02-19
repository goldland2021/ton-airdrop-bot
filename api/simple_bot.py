#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
TON空投Bot - 极简Vercel版本
无外部依赖，纯Python标准库
"""

import json
import os
from datetime import datetime

def handler(request, context):
    """Vercel Serverless Function主处理函数"""
    
    # 解析请求
    method = request.get('method', 'GET')
    path = request.get('path', '/')
    body = request.get('body', '')
    
    # 根路径 - 健康检查
    if method == 'GET' and path == '/':
        return {
            'statusCode': 200,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'
            },
            'body': json.dumps({
                'status': 'ok',
                'service': 'TON Airdrop Bot',
                'version': '1.0.0',
                'timestamp': datetime.now().isoformat(),
                'environment': 'vercel',
                'bot_token_configured': bool(os.getenv('TELEGRAM_BOT_TOKEN', ''))
            })
        }
    
    # Webhook端点
    elif method == 'POST' and path == '/api/webhook':
        try:
            if not body:
                return {
                    'statusCode': 400,
                    'body': json.dumps({'error': 'No body provided'})
                }
            
            data = json.loads(body)
            
            # 简单的命令处理
            message = data.get('message', {})
            if message:
                text = message.get('text', '')
                user_id = message.get('from', {}).get('id', 'unknown')
                username = message.get('from', {}).get('username', 'user')
                
                # 处理命令
                response = process_command(text, user_id, username)
                
                return {
                    'statusCode': 200,
                    'headers': {'Content-Type': 'application/json'},
                    'body': json.dumps({
                        'status': 'processed',
                        'user_id': user_id,
                        'username': username,
                        'command': text,
                        'response': response[:200]  # 限制长度
                    })
                }
            else:
                return {
                    'statusCode': 200,
                    'body': json.dumps({'status': 'ignored', 'reason': 'No message'})
                }
                
        except json.JSONDecodeError:
            return {
                'statusCode': 400,
                'body': json.dumps({'error': 'Invalid JSON'})
            }
        except Exception as e:
            return {
                'statusCode': 500,
                'body': json.dumps({'error': str(e)})
            }
    
    # 404处理
    else:
        return {
            'statusCode': 404,
            'headers': {'Content-Type': 'application/json'},
            'body': json.dumps({
                'error': 'Not found',
                'path': path,
                'method': method,
                'available_endpoints': [
                    'GET / - 健康检查',
                    'POST /api/webhook - Telegram Webhook'
                ]
            })
        }

def process_command(command, user_id, username):
    """处理用户命令（无外部依赖）"""
    
    commands = {
        '/start': f"""欢迎 {username} 来到TON空投仪表盘！🎉

我是你的TON生态空投助手。

📋 可用命令：
/start - 显示此信息
/help - 获取帮助
/airdrops - 查看空投项目
/myprogress - 查看进度

🚀 开始你的空投之旅！""",
        
        '/help': """📚 TON空投Bot帮助

🤖 功能：
• 提供TON空投信息
• 指导完成任务
• 追踪你的进度

📋 命令：
/start - 开始使用
/airdrops - 查看项目
/myprogress - 查看进度

💡 建议从/start开始！""",
        
        '/airdrops': """📊 当前空投项目：

1. Tonkeeper钱包
   难度: 简单
   任务: 下载、创建账户、交易

2. STON.fi DEX
   难度: 中等  
   任务: 连接钱包、Swap交易、流动性

3. Fragment NFT
   难度: 简单
   任务: 浏览NFT、购买域名

💡 更多功能开发中！""",
        
        '/myprogress': f"""📈 {username} 的个人进度

🎯 总体进度: 25%
✅ 已完成: 1/3项目
⏳ 进行中: 2/3项目

📊 详情：
• Tonkeeper - ✅ 完成
• STON.fi - 🔄 50%
• Fragment - 🔄 25%

💪 继续努力！"""
    }
    
    # 默认响应
    default_response = f"""未知命令: {command}

📋 可用命令：
/start - 开始使用
/help - 获取帮助  
/airdrops - 查看项目
/myprogress - 查看进度

使用 /help 获取详细信息"""
    
    return commands.get(command, default_response)

# 本地测试
if __name__ == '__main__':
    # 测试请求
    test_requests = [
        {'method': 'GET', 'path': '/', 'body': ''},
        {'method': 'POST', 'path': '/api/webhook', 'body': json.dumps({
            'message': {
                'text': '/start',
                'from': {'id': 123, 'username': 'test_user'}
            }
        })}
    ]
    
    for req in test_requests:
        print(f"\n测试请求: {req['method']} {req['path']}")
        response = handler(req, {})
        print(f"响应: {json.dumps(response, indent=2, ensure_ascii=False)}")