#!/usr/bin/env python3
"""
Script import chat history tự động với options
"""

import json
import sqlite3
import re
from datetime import datetime
import os
import sys

def create_table():
    """Tạo bảng nếu chưa có"""
    conn = sqlite3.connect('coin_tracker.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS coin_signals (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            contract_address TEXT NOT NULL,
            sender_id INTEGER,
            sender_username TEXT,
            message_id INTEGER,
            chat_id INTEGER,
            timestamp TEXT NOT NULL,
            price_at_signal REAL,
            UNIQUE(contract_address, sender_id, chat_id)
        )
    ''')
    conn.commit()
    conn.close()

def clear_old_data(chat_id):
    """Xóa dữ liệu cũ của group"""
    conn = sqlite3.connect('coin_tracker.db')
    cursor = conn.cursor()
    
    cursor.execute('DELETE FROM coin_signals WHERE chat_id = ?', (chat_id,))
    deleted_count = cursor.rowcount
    
    conn.commit()
    conn.close()
    
    print(f"Da xoa {deleted_count} tin nhan cu cua group {chat_id}")
    return deleted_count

def import_history(json_file_path, target_chat_id, clear_old=False):
    """Import chat history với options"""
    
    print("IMPORT CHAT HISTORY - AUTO MODE")
    print("=" * 50)
    print(f"File JSON: {json_file_path}")
    print(f"Chat ID: {target_chat_id}")
    print(f"Clear old data: {'Yes' if clear_old else 'No'}")
    print()
    
    if not os.path.exists(json_file_path):
        print(f"Khong tim thay file: {json_file_path}")
        return
    
    # Tạo bảng
    create_table()
    
    # Clear dữ liệu cũ nếu được yêu cầu
    deleted_count = 0
    if clear_old:
        deleted_count = clear_old_data(target_chat_id)
        print()
    
    try:
        with open(json_file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        messages = data.get('messages', [])
        group_name = data.get('name', 'Unknown Group')
        group_id_from_json = data.get('id', 'Unknown ID')
        
        print(f"Dang doc file: {json_file_path}")
        print(f"Group Name: {group_name}")
        print(f"Group ID trong file: {group_id_from_json}")
        print(f"Tim thay {len(messages)} tin nhan")
        print()
        
        # Tìm contract addresses
        contract_pattern = r'0x[a-fA-F0-9]{40}'
        contract_messages = []
        
        for msg in messages:
            text = msg.get('text')
            if text and isinstance(text, str):
                contracts = re.findall(contract_pattern, text)
                if contracts:
                    contract_messages.append({
                        'text': text,
                        'contracts': contracts,
                        'date': msg.get('date', ''),
                        'from': msg.get('from', 'Unknown')
                    })
        
        print(f"Tim thay {len(contract_messages)} tin nhan co contract address")
        
        # Đếm tổng số contract addresses duy nhất
        all_contracts = set()
        for msg in contract_messages:
            for contract in msg['contracts']:
                all_contracts.add(contract)
        
        print(f"Tong so contract addresses duy nhat: {len(all_contracts)}")
        print()
        
        # Lưu vào database
        saved_count = save_to_database(contract_messages, target_chat_id, clear_old)
        
        print(f"HOAN THANH!")
        print(f"Da luu {saved_count} contract addresses vao database")
        if clear_old:
            print(f"Da xoa {deleted_count} tin nhan cu")
        
    except Exception as e:
        print(f"Loi doc file: {e}")

def save_to_database(contract_messages, chat_id, clear_old):
    """Lưu tin nhắn vào database"""
    
    conn = sqlite3.connect("coin_tracker.db")
    cursor = conn.cursor()
    
    saved_count = 0
    duplicate_count = 0
    
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
            
            # Kiểm tra xem đã tồn tại chưa (chỉ nếu không clear old)
            if not clear_old:
                cursor.execute('''
                    SELECT id FROM coin_signals 
                    WHERE contract_address = ? AND chat_id = ?
                ''', (contract, chat_id))
                
                if cursor.fetchone():
                    duplicate_count += 1
                    continue
            
            # Save to database
            cursor.execute('''
                INSERT OR IGNORE INTO coin_signals 
                (contract_address, sender_id, sender_username, message_id, chat_id, timestamp, price_at_signal)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (contract, 0, msg['from'], 0, chat_id, date_obj, None))
            
            saved_count += 1
    
    conn.commit()
    conn.close()
    
    if not clear_old:
        print(f"Bo qua {duplicate_count} contract addresses da ton tai")
    
    return saved_count

def main():
    """Main function"""
    print("IMPORT CHAT HISTORY - AUTO MODE")
    print("=" * 50)
    
    # Cấu hình
    json_file = r".\data\result.json"
    chat_id = -1002385574544
    
    # Lấy option từ command line argument
    if len(sys.argv) > 1:
        if sys.argv[1] == "clear":
            clear_old = True
        elif sys.argv[1] == "keep":
            clear_old = False
        else:
            print("Usage: python import_auto.py [clear|keep]")
            print("  clear: Xoa het data cu")
            print("  keep:  Giu nguyen data cu")
            return
    else:
        # Mặc định là giữ nguyên
        clear_old = False
    
    print(f"File JSON: {json_file}")
    print(f"Chat ID: {chat_id}")
    print(f"Mode: {'Clear old data' if clear_old else 'Keep old data'}")
    print()
    
    # Import
    import_history(json_file, chat_id, clear_old)
    
    print()
    print("IMPORT HOAN THANH!")
    print("Bot gio da co the doc tin nhan lich su")

if __name__ == "__main__":
    main()
