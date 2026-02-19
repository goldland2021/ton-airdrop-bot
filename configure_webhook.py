#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
配置Telegram Webhook
"""

import requests
import json

# 配置
TELEGRAM_BOT_TOKEN = "7977389930:AAEcWTH5gt9OX7vlCgKlD0Y-bkFjDTf_jzM"
VERCEL_URL = "https://ton-airdrop-bot-7553.vercel.app"
WEBHOOK_URL = f"{VERCEL_URL}/api/webhook"

def set_webhook():
    """设置Telegram Webhook"""
    print(f"设置Telegram Webhook...")
    print(f"Bot Token: {TELEGRAM_BOT_TOKEN[:10]}...")
    print(f"Webhook URL: {WEBHOOK_URL}")
    
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/setWebhook"
    data = {"url": WEBHOOK_URL}
    
    try:
        response = requests.post(url, json=data, timeout=10)
        result = response.json()
        
        print(f"状态码: {response.status_code}")
        print(f"响应: {json.dumps(result, indent=2, ensure_ascii=False)}")
        
        if result.get('ok'):
            print("✅ Webhook设置成功！")
            return True
        else:
            print(f"❌ Webhook设置失败: {result.get('description')}")
            return False
            
    except Exception as e:
        print(f"❌ 请求失败: {e}")
        return False

def get_webhook_info():
    """获取Webhook信息"""
    print(f"\n获取Webhook信息...")
    
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/getWebhookInfo"
    
    try:
        response = requests.get(url, timeout=10)
        result = response.json()
        
        print(f"状态码: {response.status_code}")
        print(f"Webhook信息: {json.dumps(result, indent=2, ensure_ascii=False)}")
        
        if result.get('ok'):
            webhook_info = result.get('result', {})
            print(f"\n📊 Webhook详情:")
            print(f"• URL: {webhook_info.get('url', '未设置')}")
            print(f"• 有证书: {webhook_info.get('has_custom_certificate', False)}")
            print(f"• 挂起更新: {webhook_info.get('pending_update_count', 0)}")
            print(f"• 最后错误: {webhook_info.get('last_error_message', '无')}")
            print(f"• 最后同步: {webhook_info.get('last_synchronization_error_date', '从未')}")
            
        return result
        
    except Exception as e:
        print(f"❌ 获取信息失败: {e}")
        return None

def test_vercel_deployment():
    """测试Vercel部署"""
    print(f"\n测试Vercel部署...")
    
    endpoints = [
        ("/", "健康检查"),
        ("/api/health", "API状态"),
        ("/api/webhook", "Webhook端点")
    ]
    
    for endpoint, description in endpoints:
        url = f"{VERCEL_URL}{endpoint}"
        print(f"\n测试 {description}: {url}")
        
        try:
            if endpoint == "/api/webhook":
                # POST请求测试
                response = requests.post(url, json={"test": True}, timeout=5)
            else:
                # GET请求测试
                response = requests.get(url, timeout=5)
            
            print(f"状态码: {response.status_code}")
            print(f"响应: {response.text[:200]}...")
            
        except Exception as e:
            print(f"❌ 测试失败: {e}")

def main():
    """主函数"""
    print("=" * 60)
    print("🤖 Telegram Bot Webhook配置")
    print("=" * 60)
    
    # 测试Vercel部署
    test_vercel_deployment()
    
    # 设置Webhook
    if set_webhook():
        # 获取Webhook信息
        get_webhook_info()
        
        print("\n" + "=" * 60)
        print("🎉 配置完成！")
        print("=" * 60)
        print("\n📋 下一步:")
        print("1. 在Telegram搜索 @TONAirdropDashboardBot")
        print("2. 发送 /start 命令")
        print("3. 测试其他命令: /help, /airdrops, /myprogress")
        print("4. 查看Vercel日志确认请求")
        
        print(f"\n🔗 重要链接:")
        print(f"• Vercel部署: {VERCEL_URL}")
        print(f"• GitHub仓库: https://github.com/goldland2021/ton-airdrop-bot")
        print(f"• Vercel控制台: https://vercel.com/dashboard")
        
    else:
        print("\n❌ 配置失败，请手动设置Webhook")

if __name__ == "__main__":
    main()