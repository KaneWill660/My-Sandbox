#!/usr/bin/env python3
"""
Script demo import chat history
"""

import json
import sqlite3
import re
from datetime import datetime

def create_demo_json():
    """Tạo file JSON demo"""
    
    demo_data = {
        "name": "Demo Group",
        "type": "supergroup",
        "id": -1001234567890,
        "messages": [
            {
                "id": 1,
                "date": "2025-10-03T10:30:00",
                "from": "user1",
                "text": "Check this token: 0x1234567890123456789012345678901234567890"
            },
            {
                "id": 2,
                "date": "2025-10-03T11:15:00",
                "from": "user2",
                "text": "Another token: 0xabcdef1234567890abcdef1234567890abcdef12"
            },
            {
                "id": 3,
                "date": "2025-10-03T12:00:00",
                "from": "user3",
                "text": "This is not a token message"
            },
            {
                "id": 4,
                "date": "2025-10-03T13:30:00",
                "from": "user1",
                "text": "New token: 0x9876543210987654321098765432109876543210"
            }
        ]
    }
    
    with open('demo_chat_history.json', 'w', encoding='utf-8') as f:
        json.dump(demo_data, f, indent=2, ensure_ascii=False)
    
    print("Da tao file demo_chat_history.json")

def demo_import():
    """Demo import chat history"""
    
    print("DEMO IMPORT CHAT HISTORY")
    print("=" * 50)
    
    # Tạo file JSON demo
    create_demo_json()
    
    # Import dữ liệu
    json_file = "demo_chat_history.json"
    chat_id = -1001234567890
    
    print(f"Dang doc file: {json_file}")
    
    try:
        with open(json_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        messages = data.get('messages', [])
        print(f"Tim thay {len(messages)} tin nhan")
        
        # Tim contract addresses
        contract_pattern = r'0x[a-fA-F0-9]{40}'
        contract_messages = []
        
        for msg in messages:
            text = msg.get('text', '')
            if isinstance(text, str):
                contracts = re.findall(contract_pattern, text)
                if contracts:
                    contract_messages.append({
                        'text': text,
                        'contracts': contracts,
                        'date': msg.get('date', ''),
                        'from': msg.get('from', 'Unknown')
                    })
        
        print(f"Tim thay {len(contract_messages)} tin nhan co contract address")
        
        # Hiển thị kết quả
        for i, msg in enumerate(contract_messages, 1):
            print(f"\\n{i}. Tin nhan tu {msg['from']}:")
            print(f"   Thoi gian: {msg['date']}")
            print(f"   Noi dung: {msg['text']}")
            print(f"   Contract: {msg['contracts']}")
        
        # Lưu vào database
        save_to_database(contract_messages, chat_id)
        
    except Exception as e:
        print(f"Loi doc file: {e}")

def save_to_database(contract_messages, chat_id):
    """Lưu tin nhắn vào database"""
    
    conn = sqlite3.connect("coin_tracker.db")
    cursor = conn.cursor()
    
    saved_count = 0
    
    for msg in contract_messages:
        for contract in msg['contracts']:
            # Parse date
            try:
                date_str = msg['date']
                if 'T' in date_str:
                    date_obj = datetime.fromisoformat(date_str.replace('Z', '+00:00'))
                else:
                    date_obj = datetime.now()
            except:
                date_obj = datetime.now()
            
            # Save to database
            cursor.execute('''
                INSERT OR IGNORE INTO coin_signals 
                (contract_address, sender_id, sender_username, message_id, chat_id, timestamp, price_at_signal)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (contract, 0, msg['from'], 0, chat_id, date_obj, None))
            
            saved_count += 1
    
    conn.commit()
    conn.close()
    
    print(f"\\nDa luu {saved_count} contract addresses vao database")

if __name__ == "__main__":
    demo_import()
    
    print("\\nHOAN THANH DEMO!")
    print("Bot gio da co the doc tin nhan lich su")
    print("\\nDe su dung voi du lieu thuc:")
    print("1. Export chat history tu Telegram Desktop")
    print("2. Chinh sua script import_chat_history.py")
    print("3. Chay script import")
