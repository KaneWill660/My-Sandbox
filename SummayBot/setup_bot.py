#!/usr/bin/env python3
"""
Script setup để tạo Telegram bot và cấu hình ban đầu
"""

import os
import sys
import sqlite3
from datetime import datetime

def create_bot_with_botfather():
    """Hướng dẫn tạo bot với BotFather"""
    print("🤖 HƯỚNG DẪN TẠO TELEGRAM BOT")
    print("=" * 50)
    print("1. Mở Telegram và tìm @BotFather")
    print("2. Gửi lệnh: /newbot")
    print("3. Đặt tên cho bot (ví dụ: Coin Tracker Bot)")
    print("4. Đặt username (ví dụ: coin_tracker_bot)")
    print("5. Lưu lại BOT TOKEN được cung cấp")
    print("6. Thay YOUR_BOT_TOKEN trong config.py bằng token thật")
    print()

def setup_database():
    """Khởi tạo database"""
    print("🗄️ KHỞI TẠO DATABASE...")
    
    db_path = "coin_tracker.db"
    
    # Xóa database cũ nếu có
    if os.path.exists(db_path):
        os.remove(db_path)
        print(f"✅ Đã xóa database cũ: {db_path}")
    
    # Tạo database mới
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    cursor.execute('''
        CREATE TABLE coin_signals (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            contract_address TEXT NOT NULL,
            sender_id INTEGER NOT NULL,
            sender_username TEXT,
            message_id INTEGER NOT NULL,
            chat_id INTEGER NOT NULL,
            timestamp DATETIME NOT NULL,
            price_at_signal REAL,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    cursor.execute('''
        CREATE INDEX idx_contract_address ON coin_signals(contract_address);
    ''')
    
    cursor.execute('''
        CREATE INDEX idx_timestamp ON coin_signals(timestamp);
    ''')
    
    # Thêm dữ liệu mẫu để test
    sample_data = [
        ('0x1234567890123456789012345678901234567890', 12345, 'test_user', 1, -1001234567890, datetime.now(), 0.00012345),
        ('0xabcdefabcdefabcdefabcdefabcdefabcdefabcd', 67890, 'sample_user', 2, -1001234567890, datetime.now(), 0.00056789),
    ]
    
    cursor.executemany('''
        INSERT INTO coin_signals 
        (contract_address, sender_id, sender_username, message_id, chat_id, timestamp, price_at_signal)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', sample_data)
    
    conn.commit()
    conn.close()
    
    print(f"✅ Đã tạo database: {db_path}")
    print("✅ Đã thêm dữ liệu mẫu để test")

def check_dependencies():
    """Kiểm tra dependencies"""
    print("📦 KIỂM TRA DEPENDENCIES...")
    
    required_packages = [
        'telegram',
        'aiohttp',
        'sqlite3'
    ]
    
    missing_packages = []
    
    for package in required_packages:
        try:
            if package == 'telegram':
                import telegram
            elif package == 'aiohttp':
                import aiohttp
            elif package == 'sqlite3':
                import sqlite3
            print(f"✅ {package}")
        except ImportError:
            print(f"❌ {package} - CHƯA CÀI ĐẶT")
            missing_packages.append(package)
    
    if missing_packages:
        print(f"\n⚠️ Cần cài đặt: pip install {' '.join(missing_packages)}")
        return False
    
    print("✅ Tất cả dependencies đã sẵn sàng!")
    return True

def test_config():
    """Kiểm tra cấu hình"""
    print("⚙️ KIỂM TRA CẤU HÌNH...")
    
    try:
        from config import BOT_TOKEN
        
        if BOT_TOKEN == "YOUR_BOT_TOKEN":
            print("❌ Chưa cấu hình BOT_TOKEN trong config.py")
            print("   Vui lòng thay YOUR_BOT_TOKEN bằng token thật từ BotFather")
            return False
        else:
            print("✅ BOT_TOKEN đã được cấu hình")
            return True
            
    except ImportError:
        print("❌ Không tìm thấy file config.py")
        return False

def main():
    """Hàm main"""
    print("🚀 SETUP TELEGRAM COIN TRACKER BOT")
    print("=" * 50)
    
    # Kiểm tra dependencies
    if not check_dependencies():
        print("\n❌ Vui lòng cài đặt dependencies trước khi tiếp tục")
        return
    
    # Hướng dẫn tạo bot
    create_bot_with_botfather()
    
    # Khởi tạo database
    setup_database()
    
    # Kiểm tra cấu hình
    config_ok = test_config()
    
    print("\n" + "=" * 50)
    if config_ok:
        print("🎉 SETUP HOÀN TẤT!")
        print("✅ Bot đã sẵn sàng chạy")
        print("✅ Database đã được khởi tạo")
        print("✅ Cấu hình đã đúng")
        print("\n🚀 Chạy bot: python telegram_coin_tracker_bot.py")
    else:
        print("⚠️ SETUP CHƯA HOÀN TẤT")
        print("❌ Vui lòng cấu hình BOT_TOKEN trong config.py")
        print("❌ Sau đó chạy lại: python setup_bot.py")
    
    print("\n📖 Xem README.md để biết thêm chi tiết")

if __name__ == "__main__":
    main()
