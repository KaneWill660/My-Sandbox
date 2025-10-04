#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sqlite3
from datetime import datetime, timezone, timedelta

def test_duplicate_contract_logic():
    """Test logic chỉ lưu lần sớm nhất cho mỗi contract"""
    
    # Kết nối database
    conn = sqlite3.connect("coin_tracker.db")
    cursor = conn.cursor()
    
    # Tạo bảng test nếu chưa có
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS test_coin_signals (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            contract_address TEXT NOT NULL,
            sender_id INTEGER,
            sender_username TEXT,
            message_id INTEGER,
            chat_id INTEGER,
            timestamp TEXT,
            price_at_signal REAL
        )
    ''')
    
    # Xóa dữ liệu test cũ
    cursor.execute('DELETE FROM test_coin_signals')
    
    # Test data - cùng 1 contract nhưng khác thời gian
    test_contract = "0x1234567890abcdef1234567890abcdef12345678"
    chat_id = -1001234567890
    
    # Lần 1: 10:00 UTC
    timestamp1 = datetime.now(timezone.utc) - timedelta(hours=2)
    cursor.execute('''
        INSERT INTO test_coin_signals 
        (contract_address, sender_id, sender_username, message_id, chat_id, timestamp, price_at_signal)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', (test_contract, 111, "user1", 1, chat_id, timestamp1, 0.001))
    
    # Lần 2: 11:00 UTC (muộn hơn)
    timestamp2 = datetime.now(timezone.utc) - timedelta(hours=1)
    cursor.execute('''
        INSERT INTO test_coin_signals 
        (contract_address, sender_id, sender_username, message_id, chat_id, timestamp, price_at_signal)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', (test_contract, 222, "user2", 2, chat_id, timestamp2, 0.002))
    
    # Lần 3: 09:00 UTC (sớm nhất)
    timestamp3 = datetime.now(timezone.utc) - timedelta(hours=3)
    cursor.execute('''
        INSERT INTO test_coin_signals 
        (contract_address, sender_id, sender_username, message_id, chat_id, timestamp, price_at_signal)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', (test_contract, 333, "user3", 3, chat_id, timestamp3, 0.0005))
    
    conn.commit()
    
    # Kiểm tra kết quả
    cursor.execute('''
        SELECT sender_username, timestamp, price_at_signal 
        FROM test_coin_signals 
        WHERE contract_address = ? AND chat_id = ?
        ORDER BY timestamp
    ''', (test_contract, chat_id))
    
    results = cursor.fetchall()
    
    print("=== Test Duplicate Contract Logic ===")
    print(f"Contract: {test_contract}")
    print(f"Chat ID: {chat_id}")
    print("\nAll records:")
    for i, (username, ts, price) in enumerate(results, 1):
        print(f"{i}. User: {username}, Time: {ts}, Price: {price}")
    
    # Kiểm tra logic mới
    print("\n=== Testing New Logic ===")
    
    # Simulate bot logic
    def save_coin_signal_test(contract_address, sender_id, sender_username, 
                             message_id, chat_id, timestamp, price):
        """Test version of save_coin_signal"""
        
        # Kiểm tra xem contract này đã tồn tại trong group này chưa
        cursor.execute('''
            SELECT id, timestamp FROM test_coin_signals 
            WHERE contract_address = ? AND chat_id = ?
        ''', (contract_address, chat_id))
        
        existing = cursor.fetchone()
        
        if existing:
            # Đã tồn tại, kiểm tra xem lần này có sớm hơn không
            existing_id, existing_timestamp = existing
            
            # So sánh timestamp
            if isinstance(timestamp, str):
                try:
                    new_timestamp = datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
                except:
                    return
            else:
                new_timestamp = timestamp
            
            if isinstance(existing_timestamp, str):
                try:
                    existing_timestamp = datetime.fromisoformat(existing_timestamp.replace('Z', '+00:00'))
                except:
                    pass
            
            # Nếu timestamp mới sớm hơn, cập nhật
            if new_timestamp < existing_timestamp:
                cursor.execute('''
                    UPDATE test_coin_signals 
                    SET sender_id = ?, sender_username = ?, message_id = ?, 
                        timestamp = ?, price_at_signal = ?
                    WHERE id = ?
                ''', (sender_id, sender_username, message_id, timestamp, price, existing_id))
                print(f"Updated signal for contract {contract_address} with earlier timestamp")
            else:
                print(f"Contract {contract_address} already exists with earlier timestamp, skipping")
            
            return
        
        # Chưa tồn tại, lưu mới
        cursor.execute('''
            INSERT INTO test_coin_signals 
            (contract_address, sender_id, sender_username, message_id, chat_id, timestamp, price_at_signal)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (contract_address, sender_id, sender_username, message_id, chat_id, timestamp, price))
        print(f"Saved new signal for contract {contract_address} from user {sender_username}")
    
    # Test với contract mới
    new_contract = "0xabcdef1234567890abcdef1234567890abcdef12"
    new_timestamp = datetime.now(timezone.utc) - timedelta(minutes=30)
    
    print(f"\nTesting new contract: {new_contract}")
    save_coin_signal_test(new_contract, 444, "user4", 4, chat_id, new_timestamp, 0.003)
    
    # Test với contract đã tồn tại (sớm hơn)
    earlier_timestamp = datetime.now(timezone.utc) - timedelta(hours=4)
    print(f"\nTesting existing contract with earlier time: {test_contract}")
    save_coin_signal_test(test_contract, 555, "user5", 5, chat_id, earlier_timestamp, 0.0001)
    
    # Test với contract đã tồn tại (muộn hơn)
    later_timestamp = datetime.now(timezone.utc) - timedelta(minutes=10)
    print(f"\nTesting existing contract with later time: {test_contract}")
    save_coin_signal_test(test_contract, 666, "user6", 6, chat_id, later_timestamp, 0.005)
    
    conn.commit()
    
    # Kiểm tra kết quả cuối cùng
    print("\n=== Final Results ===")
    cursor.execute('''
        SELECT contract_address, sender_username, timestamp, price_at_signal 
        FROM test_coin_signals 
        WHERE chat_id = ?
        ORDER BY contract_address, timestamp
    ''', (chat_id,))
    
    final_results = cursor.fetchall()
    for contract, username, ts, price in final_results:
        print(f"Contract: {contract[:20]}..., User: {username}, Time: {ts}, Price: {price}")
    
    # Cleanup
    cursor.execute('DROP TABLE test_coin_signals')
    conn.commit()
    conn.close()
    
    print("\nTest completed!")

if __name__ == "__main__":
    test_duplicate_contract_logic()
