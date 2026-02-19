#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
TON空投Bot - Vercel主入口点
简化版本，避免依赖问题
"""

import json
import os

def handler(request, context):
    """Vercel Serverless Function主处理函数"""
    
    # 解析请求
    method = request.get('method', 'GET')
    path = request.get('path', '/')
    
    # 健康检查
    if method == 'GET' and path == '/':
        return {
            'statusCode': 200,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'
            },
            'body': json.dumps({
                'status': 'ok',
                'service': 'TON Airdrop Dashboard Bot',
                'version': '1.0.0',
                'endpoints': [
                    'GET / - 健康检查',
                    'GET /api/health - 服务状态',
                    'POST /api/webhook - Telegram Webhook'
                ],
                'environment': 'vercel'
            })
        }
    
    # API健康检查
    elif method == 'GET' and path == '/api/health':
        return {
            'statusCode': 200,
            'headers': {'Content-Type': 'application/json'},
            'body': json.dumps({
                'status': 'healthy',
                'bot_token_configured': bool(os.getenv('TELEGRAM_BOT_TOKEN', '')),
                'timestamp': '2026-02-19T19:00:00Z'
            })
        }
    
    # Webhook端点（简化版本）
    elif method == 'POST' and path == '/api/webhook':
        try:
            body = request.get('body', '')
            if not body:
                return {
                    'statusCode': 400,
                    'body': json.dumps({'error': 'No body provided'})
                }
            
            # 在实际部署中，这里会处理Telegram消息
            # 现在只返回确认响应
            
            return {
                'statusCode': 200,
                'headers': {'Content-Type': 'application/json'},
                'body': json.dumps({
                    'status': 'received',
                    'message': 'Webhook received successfully',
                    'note': 'In production, this would process Telegram messages'
                })
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
                    'GET /',
                    'GET /api/health',
                    'POST /api/webhook'
                ]
            })
        }

# 本地测试
if __name__ == '__main__':
    # 测试请求
    test_request = {
        'method': 'GET',
        'path': '/',
        'headers': {},
        'body': ''
    }
    
    response = handler(test_request, {})
    print(json.dumps(response, indent=2))