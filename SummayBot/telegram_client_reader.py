#!/usr/bin/env python3
"""
Script đọc tin nhắn lịch sử bằng Telegram Client API
"""

def explain_telegram_client():
    """Giải thích về Telegram Client API"""
    
    print("TELEGRAM CLIENT API - DOC TIN NHAN LICH SU")
    print("=" * 60)
    
    print("GIOI THIEU:")
    print("-" * 30)
    print("+ Telegram Client API cho phep doc tin nhắn lich su")
    print("+ Can dang nhap bang tai khoan Telegram")
    print("+ Co the doc tin nhắn tu bat ky group nao")
    print("+ Phuc tap hon Bot API nhung manh me hon")
    
    print()
    print("CACH HOAT DONG:")
    print("-" * 30)
    print("1. Dang nhap bang tai khoan Telegram")
    print("2. Ket noi den group")
    print("3. Doc tin nhắn lich su")
    print("4. Tim contract addresses")
    print("5. Luu vao database")
    
    print()
    print("THU VIEN CAN CAI DAT:")
    print("-" * 30)
    print("pip install telethon")
    print("pip install python-dotenv")
    
    print()
    print("CAU TRUC CODE:")
    print("-" * 30)
    print("""from telethon import TelegramClient
from telethon.tl.functions.messages import GetHistoryRequest

# Dang nhap
client = TelegramClient('session', api_id, api_hash)
client.start()

# Doc tin nhắn
messages = client.get_messages(group_entity, limit=1000)

# Tim contract addresses
for msg in messages:
    if '0x' in msg.text:
        # Luu vao database
        pass""")
    
    print()
    print("UU DIEM:")
    print("-" * 30)
    print("+ Doc duoc tin nhắn lich su")
    print("+ Khong can export thu cong")
    print("+ Tu dong hoa hoan toan")
    print("+ Co the doc tu nhieu group")
    
    print()
    print("NHUOC DIEM:")
    print("-" * 30)
    print("+ Can dang nhap bang tai khoan")
    print("+ Phuc tap hon Bot API")
    print("+ Co the bi gioi han rate limit")
    print("+ Can quan ly session")

def create_telegram_client_script():
    """Tạo script Telegram Client"""
    
    script_content = '''#!/usr/bin/env python3
"""
Script đọc tin nhắn lịch sử bằng Telegram Client API
"""

import asyncio
import sqlite3
import re
from datetime import datetime
from telethon import TelegramClient
from telethon.tl.functions.messages import GetHistoryRequest

# Cấu hình
API_ID = 'your_api_id'
API_HASH = 'your_api_hash'
PHONE = 'your_phone_number'

async def read_chat_history():
    """Đọc tin nhắn lịch sử"""
    
    client = TelegramClient('session', API_ID, API_HASH)
    
    try:
        await client.start(phone=PHONE)
        print("Đã đăng nhập thành công!")
        
        # Thay bằng username hoặc ID của group
        group_username = 'your_group_username'
        group_entity = await client.get_entity(group_username)
        
        # Đọc tin nhắn (giới hạn 1000 tin nhắn gần nhất)
        messages = await client.get_messages(group_entity, limit=1000)
        
        print(f"Đã đọc {len(messages)} tin nhắn")
        
        # Tìm contract addresses
        contract_pattern = r'0x[a-fA-F0-9]{40}'
        contract_messages = []
        
        for msg in messages:
            if msg.text:
                contracts = re.findall(contract_pattern, msg.text)
                if contracts:
                    contract_messages.append({
                        'text': msg.text,
                        'contracts': contracts,
                        'date': msg.date,
                        'sender': msg.sender.username if msg.sender else 'Unknown'
                    })
        
        print(f"Tìm thấy {len(contract_messages)} tin nhắn có contract address")
        
        # Lưu vào database
        save_to_database(contract_messages, group_entity.id)
        
    except Exception as e:
        print(f"Lỗi: {e}")
    finally:
        await client.disconnect()

def save_to_database(contract_messages, chat_id):
    """Lưu tin nhắn vào database"""
    
    conn = sqlite3.connect("coin_tracker.db")
    cursor = conn.cursor()
    
    saved_count = 0
    
    for msg in contract_messages:
        for contract in msg['contracts']:
            cursor.execute('''
                INSERT OR IGNORE INTO coin_signals 
                (contract_address, sender_id, sender_username, message_id, chat_id, timestamp, price_at_signal)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (contract, 0, msg['sender'], 0, chat_id, msg['date'], None))
            
            saved_count += 1
    
    conn.commit()
    conn.close()
    
    print(f"Đã lưu {saved_count} contract addresses vào database")

if __name__ == "__main__":
    asyncio.run(read_chat_history())
'''
    
    with open('telegram_client_reader.py', 'w', encoding='utf-8') as f:
        f.write(script_content)
    
    print("Đã tạo script telegram_client_reader.py")

if __name__ == "__main__":
    explain_telegram_client()
    print()
    create_telegram_client_script()
