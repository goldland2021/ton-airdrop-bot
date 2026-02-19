#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
TON空投仪表盘 - Telegram Bot主运行脚本
"""

import os
import sys
import logging
from typing import Optional

# 添加当前目录到路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    import telebot
    from telebot import types
    TELEBOT_AVAILABLE = True
except ImportError:
    TELEBOT_AVAILABLE = False
    print("警告: 未安装python-telegram-bot库")
    print("请运行: pip install pyTelegramBotAPI")

from bot_framework import TONAirdropBot

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('ton_bot.log', encoding='utf-8'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class TONAirdropTelegramBot:
    """TON空投仪表盘Telegram Bot实现"""
    
    def __init__(self, token: str):
        """
        初始化Telegram Bot
        
        Args:
            token: Telegram Bot Token (从 @BotFather 获取)
        """
        if not TELEBOT_AVAILABLE:
            raise ImportError("需要安装python-telegram-bot库")
        
        self.bot = telebot.TeleBot(token)
        self.core_bot = TONAirdropBot(token)
        self.setup_handlers()
        
        logger.info(f"TON空投Bot初始化完成")
        logger.info(f"Bot名称: {self.core_bot.bot_name}")
        logger.info(f"版本: {self.core_bot.version}")
    
    def setup_handlers(self):
        """设置命令处理器"""
        
        @self.bot.message_handler(commands=['start'])
        def handle_start(message):
            """处理 /start 命令"""
            user_id = message.from_user.id
            username = message.from_user.username or message.from_user.first_name
            
            logger.info(f"用户 {username} (ID: {user_id}) 使用 /start")
            
            response = self.core_bot.start_command(user_id, username)
            self.bot.reply_to(message, response, parse_mode='Markdown')
        
        @self.bot.message_handler(commands=['airdrops'])
        def handle_airdrops(message):
            """处理 /airdrops 命令"""
            user_id = message.from_user.id
            username = message.from_user.username or message.from_user.first_name
            
            logger.info(f"用户 {username} 查看空投列表")
            
            response = self.core_bot.airdrops_command(user_id)
            self.bot.reply_to(message, response, parse_mode='Markdown')
        
        @self.bot.message_handler(commands=['myprogress'])
        def handle_myprogress(message):
            """处理 /myprogress 命令"""
            user_id = message.from_user.id
            username = message.from_user.username or message.from_user.first_name
            
            logger.info(f"用户 {username} 查看进度")
            
            response = self.core_bot.myprogress_command(user_id)
            self.bot.reply_to(message, response, parse_mode='Markdown')
        
        @self.bot.message_handler(commands=['subscribe'])
        def handle_subscribe(message):
            """处理 /subscribe 命令"""
            user_id = message.from_user.id
            username = message.from_user.username or message.from_user.first_name
            
            logger.info(f"用户 {username} 订阅提醒")
            
            response = self.core_bot.subscribe_command(user_id)
            self.bot.reply_to(message, response, parse_mode='Markdown')
        
        @self.bot.message_handler(commands=['help'])
        def handle_help(message):
            """处理 /help 命令"""
            user_id = message.from_user.id
            username = message.from_user.username or message.from_user.first_name
            
            logger.info(f"用户 {username} 请求帮助")
            
            response = self.core_bot.help_command()
            self.bot.reply_to(message, response, parse_mode='Markdown')
        
        @self.bot.message_handler(commands=['tonkeeper'])
        def handle_tonkeeper(message):
            """处理 /tonkeeper 命令"""
            user_id = message.from_user.id
            username = message.from_user.username or message.from_user.first_name
            
            logger.info(f"用户 {username} 查看Tonkeeper教程")
            
            response = self.core_bot.tonkeeper_command()
            self.bot.reply_to(message, response, parse_mode='Markdown')
        
        @self.bot.message_handler(commands=['stonfi'])
        def handle_stonfi(message):
            """处理 /stonfi 命令"""
            user_id = message.from_user.id
            username = message.from_user.username or message.from_user.first_name
            
            logger.info(f"用户 {username} 查看STON.fi教程")
            
            response = self.core_bot.stonfi_command()
            self.bot.reply_to(message, response, parse_mode='Markdown')
        
        @self.bot.message_handler(commands=['fragment'])
        def handle_fragment(message):
            """处理 /fragment 命令"""
            user_id = message.from_user.id
            username = message.from_user.username or message.from_user.first_name
            
            logger.info(f"用户 {username} 查看Fragment教程")
            
            response = self.core_bot.fragment_command()
            self.bot.reply_to(message, response, parse_mode='Markdown')
        
        @self.bot.message_handler(func=lambda message: True)
        def handle_all_messages(message):
            """处理所有其他消息"""
            user_id = message.from_user.id
            username = message.from_user.username or message.from_user.first_name
            text = message.text
            
            logger.info(f"用户 {username} 发送消息: {text[:50]}...")
            
            # 如果是命令格式但未识别
            if text.startswith('/'):
                response = "未知命令，请使用 /help 查看可用命令。"
            else:
                response = (
                    "你好！我是TON空投助手。\n\n"
                    "请使用以下命令与我交互：\n"
                    "/start - 开始使用\n"
                    "/airdrops - 查看空投项目\n"
                    "/myprogress - 查看进度\n"
                    "/help - 获取帮助\n"
                )
            
            self.bot.reply_to(message, response, parse_mode='Markdown')
    
    def run(self):
        """运行Bot"""
        logger.info("启动TON空投Telegram Bot...")
        logger.info("按 Ctrl+C 停止")
        
        try:
            # 设置命令菜单（可选）
            self.bot.set_my_commands([
                types.BotCommand("/start", "开始使用"),
                types.BotCommand("/airdrops", "查看空投项目"),
                types.BotCommand("/myprogress", "我的进度"),
                types.BotCommand("/subscribe", "订阅提醒"),
                types.BotCommand("/help", "获取帮助"),
                types.BotCommand("/tonkeeper", "Tonkeeper教程"),
                types.BotCommand("/stonfi", "STON.fi教程"),
                types.BotCommand("/fragment", "Fragment教程")
            ])
            
            logger.info("Bot命令菜单已设置")
            
            # 启动Bot
            self.bot.infinity_polling(timeout=60, long_polling_timeout=60)
            
        except KeyboardInterrupt:
            logger.info("用户请求停止Bot")
        except Exception as e:
            logger.error(f"Bot运行错误: {e}")
            raise

def get_bot_token() -> Optional[str]:
    """获取Bot Token"""
    # 方法1: 从环境变量获取
    token = os.getenv('TON_BOT_TOKEN')
    
    if token:
        logger.info("从环境变量获取Token")
        return token
    
    # 方法2: 从配置文件获取
    config_file = os.path.join(os.path.dirname(__file__), 'config.py')
    if os.path.exists(config_file):
        try:
            import config
            if hasattr(config, 'TELEGRAM_BOT_TOKEN'):
                logger.info("从配置文件获取Token")
                return config.TELEGRAM_BOT_TOKEN
        except:
            pass
    
    # 方法3: 从用户输入获取
    print("\n" + "=" * 60)
    print("TON空投仪表盘 - Telegram Bot设置")
    print("=" * 60)
    print("\n需要Telegram Bot Token才能运行。")
    print("\n获取步骤：")
    print("1. 在Telegram中搜索 @BotFather")
    print("2. 发送 /newbot 创建新Bot")
    print("3. 设置Bot名称和用户名")
    print("4. 复制得到的Token（格式如: 1234567890:ABCdefGHIjklMNOpqrsTUVwxyz）")
    print("\n" + "=" * 60)
    
    token = input("\n请输入你的Telegram Bot Token: ").strip()
    
    if token:
        # 保存到配置文件
        with open(config_file, 'w', encoding='utf-8') as f:
            f.write(f'TELEGRAM_BOT_TOKEN = "{token}"\n')
        logger.info(f"Token已保存到 {config_file}")
        return token
    
    return None

def main():
    """主函数"""
    print("=" * 60)
    print("TON空投仪表盘 - Telegram Bot启动")
    print("=" * 60)
    
    # 检查依赖
    if not TELEBOT_AVAILABLE:
        print("\n❌ 缺少依赖库")
        print("请运行: pip install pyTelegramBotAPI")
        return
    
    # 获取Bot Token
    token = get_bot_token()
    
    if not token:
        print("\n❌ 未提供Bot Token，无法启动")
        return
    
    try:
        # 创建并运行Bot
        telegram_bot = TONAirdropTelegramBot(token)
        telegram_bot.run()
        
    except Exception as e:
        logger.error(f"启动失败: {e}")
        print(f"\n❌ 启动失败: {e}")
        
        if "Forbidden" in str(e):
            print("可能原因: Token无效或Bot被禁用")
        elif "Unauthorized" in str(e):
            print("可能原因: Token格式错误")
        else:
            print("请检查网络连接和Token有效性")

if __name__ == "__main__":
    main()