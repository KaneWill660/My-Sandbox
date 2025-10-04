#!/usr/bin/env python3
"""
Script test summary 1 giờ để kiểm tra logic thời gian
"""

import sqlite3
from datetime import datetime, timezone, timedelta

def test_1h_summary():
    """Test logic lấy kèo 1 giờ"""
    
    print("TEST 1H SUMMARY LOGIC")
    print("=" * 50)
    
    # Kết nối database
    conn = sqlite3.connect("coin_tracker.db")
    cursor = conn.cursor()
    
    # Tính thời gian 1 giờ trước (sử dụng local time)
    now_local = datetime.now()
    one_hour_ago = now_local - timedelta(hours=1)
    
    print(f"Thoi gian hien tai (Local): {now_local}")
    print(f"1 gio truoc (Local): {one_hour_ago}")
    print()
    
    # Lấy tất cả kèo trong 1 giờ qua
    cursor.execute('''
        SELECT contract_address, sender_username, timestamp, price_at_signal
        FROM coin_signals 
        WHERE timestamp >= ? AND chat_id = -1002385574544
        ORDER BY timestamp DESC
    ''', (one_hour_ago.isoformat(),))
    
    all_signals = cursor.fetchall()
    print(f"Tat ca keo trong 1 gio qua: {len(all_signals)}")
    
    # Hiển thị 10 kèo gần nhất
    print("\n10 keo gan nhat:")
    for i, signal in enumerate(all_signals[:10], 1):
        contract = signal[0]
        sender = signal[1] or "Unknown"
        timestamp = signal[2]
        price = signal[3]
        
        print(f"{i}. {sender} - {contract[:20]}...")
        print(f"   Thoi gian: {timestamp}")
        print(f"   Gia: {price}")
        print()
    
    # Lấy kèo unique (chỉ người gửi đầu tiên)
    cursor.execute('''
        SELECT cs1.contract_address, cs1.sender_id, cs1.sender_username, 
               cs1.timestamp, cs1.price_at_signal
        FROM coin_signals cs1
        INNER JOIN (
            SELECT contract_address, MIN(timestamp) as first_time
            FROM coin_signals 
            WHERE timestamp >= ? AND chat_id = -1002385574544
            GROUP BY contract_address
        ) cs2 ON cs1.contract_address = cs2.contract_address 
               AND cs1.timestamp = cs2.first_time
        ORDER BY cs1.timestamp ASC
    ''', (one_hour_ago.isoformat(),))
    
    unique_signals = cursor.fetchall()
    print(f"Keo unique trong 1 gio qua: {len(unique_signals)}")
    
    # Hiển thị kèo unique
    print("\nKeo unique (nguoi gui dau tien):")
    for i, signal in enumerate(unique_signals, 1):
        contract = signal[0]
        sender = signal[2] or f"User_{signal[1]}"
        timestamp = signal[3]
        price = signal[4]
        
        print(f"{i}. {sender} - {contract[:20]}...")
        print(f"   Thoi gian: {timestamp}")
        print(f"   Gia: {price}")
        print()
    
    # Kiểm tra kèo ngoài 1 giờ
    cursor.execute('''
        SELECT contract_address, sender_username, timestamp
        FROM coin_signals 
        WHERE timestamp < ? AND chat_id = -1002385574544
        ORDER BY timestamp DESC
        LIMIT 5
    ''', (one_hour_ago.isoformat(),))
    
    old_signals = cursor.fetchall()
    print(f"5 keo gan nhat NGOAI 1 gio qua:")
    for i, signal in enumerate(old_signals, 1):
        contract = signal[0]
        sender = signal[1] or "Unknown"
        timestamp = signal[2]
        
        print(f"{i}. {sender} - {contract[:20]}...")
        print(f"   Thoi gian: {timestamp}")
        print()
    
    conn.close()
    
    print("=" * 50)
    print("KET LUAN:")
    print(f"- Tat ca keo trong 1h: {len(all_signals)}")
    print(f"- Keo unique trong 1h: {len(unique_signals)}")
    print(f"- Keo ngoai 1h: {len(old_signals)}")
    
    if len(unique_signals) > 0:
        print("✅ Co keo trong 1 gio qua")
    else:
        print("❌ Khong co keo nao trong 1 gio qua")

if __name__ == "__main__":
    test_1h_summary()
