#!/usr/bin/env python3
"""
Script import chat history đúng với chat_id chính xác
"""

import json
import sqlite3
import re
from datetime import datetime
import os

def import_chat_history_correct(json_file_path, chat_id):
    """Import chat history với chat_id chính xác"""
    
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
        
        # Dem tong so contract addresses duy nhat
        all_contracts = set()
        for msg in contract_messages:
            for contract in msg['contracts']:
                all_contracts.add(contract)
        
        print(f"Tong so contract addresses duy nhat: {len(all_contracts)}")
        
        # Luu vao database
        save_to_database(contract_messages, chat_id)
        
    except Exception as e:
        print(f"Loi doc file: {e}")

def save_to_database(contract_messages, chat_id):
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
            
            # Kiem tra xem da ton tai chua
            cursor.execute('''
                SELECT id FROM coin_signals 
                WHERE contract_address = ? AND chat_id = ?
            ''', (contract, chat_id))
            
            if cursor.fetchone():
                duplicate_count += 1
                continue
            
            # Save to database
            cursor.execute('''
                INSERT INTO coin_signals 
                (contract_address, sender_id, sender_username, message_id, chat_id, timestamp, price_at_signal)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (contract, 0, msg['from'], 0, chat_id, date_obj, None))
            
            saved_count += 1
    
    conn.commit()
    conn.close()
    
    print(f"Da luu {saved_count} contract addresses moi vao database")
    print(f"Bo qua {duplicate_count} contract addresses da ton tai")

if __name__ == "__main__":
    # Chat ID đúng (thêm prefix -100)
    json_file = r".\data\result.json"
    chat_id = -1002385574544  # Chat ID đúng với prefix -100
    
    print("IMPORT CHAT HISTORY - CHAT_ID DUNG")
    print("=" * 50)
    print(f"File JSON: {json_file}")
    print(f"Chat ID: {chat_id}")
    print()
    
    import_chat_history_correct(json_file, chat_id)
    
    print()
    print("HOAN THANH!")
    print("Bot gio da co the doc tin nhan lich su")
