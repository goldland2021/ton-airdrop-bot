#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
TON空投仪表盘 - Vercel Serverless Function主入口
处理Telegram Webhook请求
"""

import os
import json
import logging
from datetime import datetime

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# 导入Bot核心逻辑
try:
    import sys
    sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    from bot_framework import TONAirdropBot
    BOT_AVAILABLE = True
except ImportError as e:
    logger.error(f"导入Bot模块失败: {e}")
    BOT_AVAILABLE = False

# 环境变量
TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN', '')
WEBHOOK_SECRET = os.getenv('WEBHOOK_SECRET', '')
VERCEL_ENV = os.getenv('VERCEL_ENV', 'development')

# 初始化Bot
bot = None
if BOT_AVAILABLE and TELEGRAM_BOT_TOKEN:
    try:
        bot = TONAirdropBot(TELEGRAM_BOT_TOKEN)
        logger.info(f"Bot初始化成功，环境: {VERCEL_ENV}")
    except Exception as e:
        logger.error(f"Bot初始化失败: {e}")
        bot = None

def handle_health_check():
    """处理健康检查请求"""
    return {
        'statusCode': 200,
        'headers': {
            'Content-Type': 'application/json',
            'Cache-Control': 'no-cache'
        },
        'body': json.dumps({
            'status': 'healthy',
            'service': 'TON Airdrop Dashboard Bot',
            'version': '1.0.0',
            'environment': VERCEL_ENV,
            'timestamp': datetime.now().isoformat(),
            'bot_available': BOT_AVAILABLE,
            'bot_initialized': bot is not None
        }, ensure_ascii=False)
    }

def handle_telegram_webhook(event):
    """处理Telegram Webhook请求"""
    try:
        # 解析请求体
        body = event.get('body', '{}')
        data = json.loads(body)
        
        logger.info(f"收到Webhook数据: {json.dumps(data, ensure_ascii=False)[:200]}...")
        
        # 验证Webhook秘密（如果设置了）
        if WEBHOOK_SECRET:
            secret = event.get('headers', {}).get('x-webhook-secret')
            if secret != WEBHOOK_SECRET:
                logger.warning("Webhook秘密验证失败")
                return {
                    'statusCode': 401,
                    'body': json.dumps({'error': 'Unauthorized'})
                }
        
        # 处理消息更新
        if 'message' in data:
            message = data['message']
            return process_message(message)
        elif 'callback_query' in data:
            # 处理回调查询（未来支持按钮）
            callback = data['callback_query']
            logger.info(f"收到回调查询: {callback.get('data')}")
            return {
                'statusCode': 200,
                'body': json.dumps({'status': 'callback_received'})
            }
        else:
            logger.info("收到非消息更新，忽略")
            return {
                'statusCode': 200,
                'body': json.dumps({'status': 'ignored'})
            }
            
    except json.JSONDecodeError as e:
        logger.error(f"JSON解析错误: {e}")
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

def process_message(message):
    """处理消息"""
    if not bot:
        return {
            'statusCode': 503,
            'body': json.dumps({'error': 'Bot not available'})
        }
    
    # 提取消息信息
    user_info = message.get('from', {})
    user_id = user_info.get('id')
    username = user_info.get('username', '')
    first_name = user_info.get('first_name', '')
    text = message.get('text', '')
    
    if not user_id or not text:
        logger.warning("无效消息: 缺少用户ID或文本")
        return {
            'statusCode': 200,
            'body': json.dumps({'status': 'invalid_message'})
        }
    
    # 使用用户名或名字
    display_name = username if username else first_name
    if not display_name:
        display_name = f"用户{user_id}"
    
    logger.info(f"处理消息: 用户={display_name}, 命令={text}")
    
    # 处理命令
    try:
        response_text = bot.process_command(user_id, display_name, text)
        logger.info(f"命令处理完成: {text}")
        
        # 在实际部署中，这里应该调用Telegram API发送回复
        # 但由于Serverless限制，我们记录日志并返回成功
        
        # 记录用户交互（可扩展为数据库存储）
        log_user_interaction(user_id, display_name, text, response_text[:100])
        
        return {
            'statusCode': 200,
            'headers': {'Content-Type': 'application/json'},
            'body': json.dumps({
                'status': 'processed',
                'user_id': user_id,
                'username': display_name,
                'command': text,
                'response_preview': response_text[:100]
            }, ensure_ascii=False)
        }
        
    except Exception as e:
        logger.error(f"处理命令时出错: {e}, 命令: {text}")
        return {
            'statusCode': 500,
            'body': json.dumps({'error': 'Command processing failed'})
        }

def log_user_interaction(user_id, username, command, response_preview):
    """记录用户交互（可扩展为数据库存储）"""
    log_entry = {
        'timestamp': datetime.now().isoformat(),
        'user_id': user_id,
        'username': username,
        'command': command,
        'response_preview': response_preview,
        'environment': VERCEL_ENV
    }
    logger.info(f"用户交互记录: {json.dumps(log_entry, ensure_ascii=False)}")
    
    # 这里可以添加数据库存储逻辑
    # 例如：存储到Vercel Postgres、Supabase等

def handler(event, context):
    """Vercel Serverless Function主处理函数"""
    
    # 记录请求信息
    logger.info(f"收到请求: {event.get('path')}, 方法: {event.get('httpMethod')}")
    
    # 根据路径和方法路由
    path = event.get('path', '')
    method = event.get('httpMethod', 'GET')
    
    # 健康检查
    if path == '/api' and method == 'GET':
        return handle_health_check()
    
    # Telegram Webhook
    elif path == '/api' and method == 'POST':
        return handle_telegram_webhook(event)
    
    # 其他路径
    else:
        logger.warning(f"未知路径: {path}, 方法: {method}")
        return {
            'statusCode': 404,
            'body': json.dumps({'error': 'Not found'})
        }

# 本地测试代码
if __name__ == '__main__':
    # 模拟Vercel事件
    test_event = {
        'path': '/api',
        'httpMethod': 'GET',
        'headers': {},
        'body': '{}'
    }
    
    # 设置环境变量用于测试
    os.environ['TELEGRAM_BOT_TOKEN'] = 'test_token'
    os.environ['VERCEL_ENV'] = 'development'
    
    print("测试健康检查...")
    result = handler(test_event, None)
    print(f"结果: {result}")
    
    # 测试Webhook
    test_webhook_event = {
        'path': '/api',
        'httpMethod': 'POST',
        'headers': {},
        'body': json.dumps({
            'message': {
                'from': {
                    'id': 123456789,
                    'username': 'test_user',
                    'first_name': 'Test'
                },
                'text': '/start'
            }
        })
    }
    
    print("\n测试Webhook处理...")
    result = handler(test_webhook_event, None)
    print(f"结果: {result}")