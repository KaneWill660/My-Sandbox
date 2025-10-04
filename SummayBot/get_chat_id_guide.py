#!/usr/bin/env python3
"""
Hướng dẫn lấy chat_id của group
"""

def get_chat_id_guide():
    """Hướng dẫn lấy chat_id của group"""
    
    print("HUONG DAN LAY CHAT_ID CUA GROUP")
    print("=" * 50)
    
    print("PHUONG PHAP 1: TU FILE JSON EXPORT")
    print("-" * 40)
    print("1. Export chat history tu Telegram Desktop")
    print("2. Mo file JSON")
    print("3. Tim field 'id' trong file:")
    print("""{
  "name": "Group Name",
  "type": "supergroup",
  "id": -1001234567890,  <-- Day la chat_id
  "messages": [...]
}""")
    print("4. Chat_id se co dang: -1001234567890")
    
    print()
    print("PHUONG PHAP 2: TU BOT LOG")
    print("-" * 40)
    print("1. Them bot vao group")
    print("2. Cap quyen Admin cho bot")
    print("3. Gui tin nhan trong group")
    print("4. Bot se log chat_id trong console")
    print("5. Chat_id se hien thi trong log")
    
    print()
    print("PHUONG PHAP 3: TU BOT COMMAND")
    print("-" * 40)
    print("1. Them bot vao group")
    print("2. Cap quyen Admin cho bot")
    print("3. Go lenh /start trong group")
    print("4. Bot se hien thi chat_id")
    print("5. Hoac go lenh /help de xem chat_id")
    
    print()
    print("PHUONG PHAP 4: TU TELEGRAM API")
    print("-" * 40)
    print("1. Su dung @userinfobot")
    print("2. Forward tin nhan tu group den @userinfobot")
    print("3. Bot se hien thi thong tin group")
    print("4. Chat_id se hien thi trong ket qua")
    
    print()
    print("PHUONG PHAP 5: TU TELEGRAM DESKTOP")
    print("-" * 40)
    print("1. Mo Telegram Desktop")
    print("2. Vao group can lay chat_id")
    print("3. Click vao ten group")
    print("4. Chon 'Export chat history'")
    print("5. Chat_id se hien thi trong file JSON")
    
    print()
    print("DINH DANG CHAT_ID:")
    print("-" * 40)
    print("+ Group: -1001234567890")
    print("+ Channel: -1001234567890")
    print("+ Private chat: 123456789")
    print("+ Bot chat: 123456789")
    
    print()
    print("LUU Y:")
    print("-" * 40)
    print("+ Chat_id cua group luon bat dau bang -100")
    print("+ Chat_id cua channel luon bat dau bang -100")
    print("+ Chat_id cua private chat la so duong")
    print("+ Chat_id cua bot chat la so duong")

def create_chat_id_finder():
    """Tạo script tìm chat_id"""
    
    script_content = '''#!/usr/bin/env python3
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
        f"Chat ID: {chat_id}\\n"
        f"Chat Type: {chat_type}\\n"
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
'''
    
    with open('find_chat_id.py', 'w', encoding='utf-8') as f:
        f.write(script_content)
    
    print("Đã tạo script find_chat_id.py")

def create_simple_chat_id_finder():
    """Tạo script đơn giản để tìm chat_id"""
    
    script_content = '''#!/usr/bin/env python3
"""
Script đơn giản để tìm chat_id
"""

import sqlite3

def find_chat_id_from_database():
    """Tìm chat_id từ database"""
    
    print("TIM CHAT_ID TU DATABASE")
    print("=" * 40)
    
    try:
        conn = sqlite3.connect("coin_tracker.db")
        cursor = conn.cursor()
        
        # Lấy tất cả chat_id
        cursor.execute("SELECT DISTINCT chat_id FROM coin_signals")
        chat_ids = cursor.fetchall()
        
        if chat_ids:
            print("Các chat_id đã có trong database:")
            for chat_id in chat_ids:
                print(f"  - {chat_id[0]}")
        else:
            print("Không có chat_id nào trong database")
            print("Hãy thêm bot vào group và gửi tin nhắn trước")
        
        conn.close()
        
    except Exception as e:
        print(f"Lỗi: {e}")

if __name__ == "__main__":
    find_chat_id_from_database()
'''
    
    with open('find_chat_id_simple.py', 'w', encoding='utf-8') as f:
        f.write(script_content)
    
    print("Đã tạo script find_chat_id_simple.py")

if __name__ == "__main__":
    get_chat_id_guide()
    print()
    create_chat_id_finder()
    print()
    create_simple_chat_id_finder()
