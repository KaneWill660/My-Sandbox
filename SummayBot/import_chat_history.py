#!/usr/bin/env python3
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
    json_file = r".\data\result.json"  # Ten file JSON
    chat_id = -1002385574544  # Chat ID cua group
    
    print("IMPORT CHAT HISTORY")
    print("=" * 50)
    print(f"File JSON: {json_file}")
    print(f"Chat ID: {chat_id}")
    print()
    
    import_chat_history(json_file, chat_id)
    
    print()
    print("HOAN THANH!")
    print("Bot gio da co the doc tin nhan lich su")