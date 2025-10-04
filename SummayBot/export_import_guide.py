#!/usr/bin/env python3
"""
Hướng dẫn export chat history và import vào database
"""

def export_import_guide():
    """Hướng dẫn export chat history và import vào database"""
    
    print("HUONG DAN EXPORT CHAT HISTORY VA IMPORT VAO DATABASE")
    print("=" * 70)
    
    print("BUOC 1: EXPORT CHAT HISTORY")
    print("-" * 40)
    print("1. Cai dat Telegram Desktop:")
    print("   + Tai ve tu: https://desktop.telegram.org/")
    print("   + Dang nhap bang tai khoan Telegram cua ban")
    print()
    print("2. Export chat history:")
    print("   + Vao group can export")
    print("   + Click vao ten group (o dau chat)")
    print("   + Chon 'Export chat history'")
    print("   + Chon cac tuy chon:")
    print("     * Format: JSON")
    print("     * Date range: All time")
    print("     * Media: Khong can (chi can text)")
    print("   + Click 'Export'")
    print("   + Download file JSON")
    
    print()
    print("BUOC 2: CHUAN BI FILE JSON")
    print("-" * 40)
    print("File JSON se co cau truc nhu sau:")
    print("""{
  "name": "Group Name",
  "type": "supergroup",
  "id": -1001234567890,
  "messages": [
    {
      "id": 123,
      "date": "2025-10-03T10:30:00",
      "from": "username",
      "text": "Check this token: 0x1234567890123456789012345678901234567890"
    }
  ]
}""")
    
    print()
    print("BUOC 3: IMPORT VAO DATABASE")
    print("-" * 40)
    print("1. Dat file JSON vao cung thu muc voi bot")
    print("2. Chay script import:")
    print("   python import_chat_history.py")
    print("3. Bot se tu dong:")
    print("   + Doc file JSON")
    print("   + Tim contract addresses (0x...)")
    print("   + Luu vao database")
    print("   + Hien thi ket qua")
    
    print()
    print("BUOC 4: KIEM TRA KET QUA")
    print("-" * 40)
    print("1. Chay script kiem tra:")
    print("   python check_imported_data.py")
    print("2. Go lenh /summary trong group")
    print("3. Bot se hien thi keo tu tin nhan lich su")
    
    print()
    print("LUU Y QUAN TRONG:")
    print("-" * 40)
    print("+ Chi lam 1 lan khi bat dau su dung bot")
    print("+ Sau do bot se tu dong doc tin nhan moi")
    print("+ Khong can export lai")
    print("+ Bot se ket hop du lieu cu va moi")

def create_import_script():
    """Tạo script import chat history"""
    
    script_content = '''#!/usr/bin/env python3
"""
Script import chat history từ file JSON
"""

import json
import sqlite3
import re
from datetime import datetime
import os

def import_chat_history(json_file_path, chat_id):
    """Import chat history từ file JSON"""
    
    print(f"Dang doc file: {json_file_path}")
    
    if not os.path.exists(json_file_path):
        print(f"Khong tim thay file: {json_file_path}")
        return
    
    try:
        with open(json_file_path, 'r', encoding='utf-8') as f:
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
        
        # Luu vao database
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
    
    print(f"Da luu {saved_count} contract addresses vao database")

if __name__ == "__main__":
    # Thay doi cac tham so nay
    json_file = "chat_history.json"  # Ten file JSON
    chat_id = -1001234567890  # Chat ID cua group
    
    print("IMPORT CHAT HISTORY")
    print("=" * 50)
    print(f"File JSON: {json_file}")
    print(f"Chat ID: {chat_id}")
    print()
    
    import_chat_history(json_file, chat_id)
    
    print()
    print("HOAN THANH!")
    print("Bot gio da co the doc tin nhan lich su")
'''
    
    with open('import_chat_history.py', 'w', encoding='utf-8') as f:
        f.write(script_content)
    
    print("Da tao script import_chat_history.py")

def create_check_script():
    """Tạo script kiểm tra dữ liệu đã import"""
    
    script_content = '''#!/usr/bin/env python3
"""
Script kiểm tra dữ liệu đã import
"""

import sqlite3
from datetime import datetime, timedelta

def check_imported_data():
    """Kiểm tra dữ liệu đã import"""
    
    print("KIEM TRA DU LIEU DA IMPORT")
    print("=" * 50)
    
    conn = sqlite3.connect("coin_tracker.db")
    cursor = conn.cursor()
    
    # Lấy tất cả group
    cursor.execute("SELECT DISTINCT chat_id FROM coin_signals")
    chat_ids = cursor.fetchall()
    
    print(f"Bot hien tai co {len(chat_ids)} group:")
    for chat_id in chat_ids:
        print(f"  - Group ID: {chat_id[0]}")
    
    print()
    
    # Kiểm tra tin nhắn theo thời gian
    for chat_id in chat_ids:
        chat_id = chat_id[0]
        
        # Đếm tin nhắn theo ngày
        cursor.execute("""
            SELECT DATE(timestamp) as date, COUNT(*) as count
            FROM coin_signals 
            WHERE chat_id = ?
            GROUP BY DATE(timestamp)
            ORDER BY date DESC
            LIMIT 7
        """, (chat_id,))
        
        daily_counts = cursor.fetchall()
        
        print(f"Group {chat_id} - Tin nhan theo ngay (7 ngay gan nhat):")
        for date, count in daily_counts:
            print(f"  {date}: {count} tin nhan")
        
        # Lấy tin nhắn gần nhất
        cursor.execute("""
            SELECT contract_address, sender_username, timestamp
            FROM coin_signals 
            WHERE chat_id = ?
            ORDER BY timestamp DESC 
            LIMIT 5
        """, (chat_id,))
        
        recent = cursor.fetchall()
        
        print(f"\\n5 tin nhan gan nhat:")
        for contract, sender, timestamp in recent:
            print(f"  {timestamp}: {sender} - {contract[:20]}...")
        
        print()
    
    conn.close()
    
    print("HUONG DAN SU DUNG:")
    print("-" * 30)
    print("1. Go lenh /summary trong group")
    print("2. Bot se hien thi keo tu tin nhan lich su")
    print("3. Bot se tu dong doc tin nhan moi")

if __name__ == "__main__":
    check_imported_data()
'''
    
    with open('check_imported_data.py', 'w', encoding='utf-8') as f:
        f.write(script_content)
    
    print("Da tao script check_imported_data.py")

if __name__ == "__main__":
    export_import_guide()
    print()
    create_import_script()
    print()
    create_check_script()
