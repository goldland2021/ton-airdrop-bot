#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
TON空投仪表盘 - Vercel Serverless Function版本
通过Webhook接收Telegram消息
"""

import os
import json
import logging
from http.server import BaseHTTPRequestHandler
from datetime import datetime

# 尝试导入核心模块
try:
    from bot_framework import TONAirdropBot
    BOT_AVAILABLE = True
except ImportError:
    BOT_AVAILABLE = False

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 从环境变量获取配置
TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN', '')
WEBHOOK_SECRET = os.getenv('WEBHOOK_SECRET', 'vercel_ton_bot')

# 初始化Bot（如果可用）
bot = None
if BOT_AVAILABLE and TELEGRAM_BOT_TOKEN:
    try:
        bot = TONAirdropBot(TELEGRAM_BOT_TOKEN)
        logger.info("Bot初始化成功")
    except Exception as e:
        logger.error(f"Bot初始化失败: {e}")
        bot = None

class RequestHandler(BaseHTTPRequestHandler):
    """HTTP请求处理器"""
    
    def do_GET(self):
        """处理GET请求 - 健康检查"""
        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.end_headers()
        
        response = {
            "status": "ok",
            "service": "TON Airdrop Dashboard Bot",
            "version": "1.0.0",
            "bot_available": BOT_AVAILABLE,
            "bot_initialized": bot is not None,
            "timestamp": datetime.now().isoformat()
        }
        
        self.wfile.write(json.dumps(response).encode())
    
    def do_POST(self):
        """处理POST请求 - Telegram Webhook"""
        content_length = int(self.headers.get('Content-Length', 0))
        post_data = self.rfile.read(content_length)
        
        try:
            data = json.loads(post_data.decode('utf-8'))
            logger.info(f"收到Webhook数据: {json.dumps(data)[:200]}...")
            
            # 验证Webhook秘密（可选）
            if self.headers.get('X-Webhook-Secret') != WEBHOOK_SECRET:
                logger.warning("Webhook秘密验证失败")
            
            # 处理消息
            response = self.process_message(data)
            
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(response).encode())
            
        except Exception as e:
            logger.error(f"处理请求时出错: {e}")
            self.send_response(500)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            error_response = {"error": str(e), "status": "error"}
            self.wfile.write(json.dumps(error_response).encode())
    
    def process_message(self, data):
        """处理Telegram消息"""
        if not bot:
            return {"status": "error", "message": "Bot未初始化"}
        
        # 提取消息信息
        message = data.get('message', {})
        if not message:
            return {"status": "ignored", "message": "非消息更新"}
        
        user_id = message.get('from', {}).get('id')
        username = message.get('from', {}).get('username', '')
        text = message.get('text', '')
        
        if not user_id or not text:
            return {"status": "ignored", "message": "无效消息"}
        
        logger.info(f"处理消息: 用户={username}, 命令={text}")
        
        # 处理命令
        response_text = bot.process_command(user_id, username, text)
        
        # 在实际部署中，这里应该调用Telegram API发送回复
        # 但由于是Serverless，我们需要返回给调用者
        
        return {
            "status": "processed",
            "user_id": user_id,
            "username": username,
            "command": text,
            "response": response_text[:500]  # 限制长度
        }
    
    def log_message(self, format, *args):
        """自定义日志格式"""
        logger.info(format % args)

def handler(request, context):
    """Vercel Serverless Function入口点"""
    # 这是一个简化的处理函数
    # 实际部署时需要根据Vercel的格式调整
    
    if request.method == 'GET':
        return {
            'statusCode': 200,
            'headers': {'Content-Type': 'application/json'},
            'body': json.dumps({
                "status": "ok",
                "service": "TON Airdrop Bot",
                "endpoint": "/api/bot"
            })
        }
    
    elif request.method == 'POST':
        try:
            body = request.body
            data = json.loads(body) if body else {}
            
            # 这里应该调用Bot处理逻辑
            # 由于是Serverless，我们返回处理结果
            
            return {
                'statusCode': 200,
                'headers': {'Content-Type': 'application/json'},
                'body': json.dumps({
                    "status": "received",
                    "message": "Webhook received, processing..."
                })
            }
            
        except Exception as e:
            return {
                'statusCode': 500,
                'body': json.dumps({"error": str(e)})
            }
    
    else:
        return {
            'statusCode': 405,
            'body': json.dumps({"error": "Method not allowed"})
        }

# 用于本地测试
if __name__ == "__main__":
    from http.server import HTTPServer
    server = HTTPServer(('localhost', 3000), RequestHandler)
    print("启动测试服务器在 http://localhost:3000")
    print("按 Ctrl+C 停止")
    server.serve_forever()