#!/usr/bin/env python3
"""
Script tìm chat_id của group
"""

import logging
from telegram.ext import Updater, MessageHandler, Filters

# Cấu hình logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

def find_chat_id(update, context):
    """Tìm chat_id của group"""
    
    chat_id = update.message.chat_id
    chat_type = update.message.chat.type
    chat_title = update.message.chat.title or "Private Chat"
    
    print(f"Chat ID: {chat_id}")
    print(f"Chat Type: {chat_type}")
    print(f"Chat Title: {chat_title}")
    
    # Gửi thông tin về chat_id
    update.message.reply_text(
        f"Chat ID: {chat_id}\n"
        f"Chat Type: {chat_type}\n"
        f"Chat Title: {chat_title}"
    )

def main():
    """Hàm chính"""
    
    # Thay YOUR_BOT_TOKEN bằng token thực tế
    TOKEN = "YOUR_BOT_TOKEN"
    
    updater = Updater(token=TOKEN, use_context=True)
    dispatcher = updater.dispatcher
    
    # Thêm handler để tìm chat_id
    dispatcher.add_handler(MessageHandler(Filters.text, find_chat_id))
    
    print("Bot đang chạy... Nhấn Ctrl+C để dừng")
    print("Gửi tin nhắn bất kỳ trong group để lấy chat_id")
    
    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()
