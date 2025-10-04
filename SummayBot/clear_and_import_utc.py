#!/usr/bin/env python3
"""
Script clear database và import lại với UTC time
"""

import sqlite3
import json
import re
from datetime import datetime, timezone, timedelta
import os

def clear_database():
    """Xóa toàn bộ database"""
    conn = sqlite3.connect('coin_tracker.db')
    cursor = conn.cursor()
    
    cursor.execute('DELETE FROM coin_signals')
    deleted_count = cursor.rowcount
    
    conn.commit()
    conn.close()
    
    print(f"Da xoa {deleted_count} tin nhan cu")
    return deleted_count

def import_with_utc(json_file_path, target_chat_id):
    """Import với UTC time"""
    
    print("IMPORT WITH UTC TIME")
    print("=" * 40)
    
    if not os.path.exists(json_file_path):
        print(f"Khong tim thay file: {json_file_path}")
        return
    
    try:
        with open(json_file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        messages = data.get('messages', [])
        print(f"Tim thay {len(messages)} tin nhan")
        
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
        
        # Lưu vào database với UTC time
        conn = sqlite3.connect("coin_tracker.db")
        cursor = conn.cursor()
        
        saved_count = 0
        
        for msg in contract_messages:
            for contract in msg['contracts']:
                # Convert contract address về lowercase để tránh duplicate do case sensitivity
                contract = contract.lower()
                
                # Parse date từ JSON (UTC+7) và convert sang UTC
                try:
                    date_str = msg['date']
                    if 'T' in date_str:
                        # Parse ISO format - JSON date là UTC+7
                        dt = datetime.fromisoformat(date_str)
                        # Nếu không có timezone info, giả sử là UTC+7
                        if dt.tzinfo is None:
                            # Thêm timezone UTC+7
                            vietnam_tz = timezone(timedelta(hours=7))
                            dt = dt.replace(tzinfo=vietnam_tz)
                        # Convert từ UTC+7 sang UTC (trừ 7 giờ)
                        dt = dt.astimezone(timezone.utc)
                    else:
                        dt = datetime.now(timezone.utc)
                except:
                    dt = datetime.now(timezone.utc)
                
                # Kiểm tra xem contract này đã tồn tại chưa
                cursor.execute('''
                    SELECT id, timestamp FROM coin_signals 
                    WHERE LOWER(contract_address) = ? AND chat_id = ?
                ''', (contract, target_chat_id))
                
                existing = cursor.fetchone()
                
                if existing:
                    # Đã tồn tại, kiểm tra xem lần này có sớm hơn không
                    existing_id, existing_timestamp = existing
                    
                    # So sánh timestamp
                    if isinstance(existing_timestamp, str):
                        try:
                            existing_timestamp = datetime.fromisoformat(existing_timestamp.replace('Z', '+00:00'))
                        except:
                            # Nếu không parse được, lưu mới
                            pass
                    
                    # Nếu timestamp mới sớm hơn, cập nhật
                    if dt < existing_timestamp:
                        cursor.execute('''
                            UPDATE coin_signals 
                            SET sender_id = ?, sender_username = ?, message_id = ?, 
                                timestamp = ?, price_at_signal = ?
                            WHERE id = ?
                        ''', (0, msg['from'], 0, dt, None, existing_id))
                        print(f"Updated contract {contract} with earlier timestamp")
                    else:
                        print(f"Contract {contract} already exists with earlier timestamp, skipping")
                else:
                    # Chưa tồn tại, lưu mới
                    cursor.execute('''
                        INSERT INTO coin_signals 
                        (contract_address, sender_id, sender_username, message_id, chat_id, timestamp, price_at_signal)
                        VALUES (?, ?, ?, ?, ?, ?, ?)
                    ''', (contract, 0, msg['from'], 0, target_chat_id, dt, None))
                    saved_count += 1
        
        conn.commit()
        conn.close()
        
        print(f"Da luu {saved_count} contract addresses vao database")
        
    except Exception as e:
        print(f"Loi doc file: {e}")

def main():
    """Main function"""
    print("CLEAR AND IMPORT WITH UTC TIME")
    print("=" * 50)
    
    # Clear database
    clear_database()
    
    # Import với UTC time
    json_file = r".\data\result.json"
    chat_id = -1002385574544
    
    import_with_utc(json_file, chat_id)
    
    print()
    print("HOAN THANH!")
    print("Database da duoc clear va import lai voi UTC time")

if __name__ == "__main__":
    main()
