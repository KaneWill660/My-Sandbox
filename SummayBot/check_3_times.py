#!/usr/bin/env python3
"""
Script kiểm tra 3 loại time
"""

import sqlite3
from datetime import datetime, timezone, timedelta

def check_3_times():
    """Kiểm tra 3 loại time"""
    
    print("KIEM TRA 3 LOAI TIME")
    print("=" * 50)
    
    # Kết nối database
    conn = sqlite3.connect("coin_tracker.db")
    cursor = conn.cursor()
    
    # Lấy tin nhắn gần nhất
    cursor.execute('''
        SELECT contract_address, sender_username, timestamp
        FROM coin_signals 
        WHERE chat_id = -1002385574544
        ORDER BY timestamp DESC
        LIMIT 1
    ''')
    
    signal = cursor.fetchone()
    
    if signal:
        contract = signal[0]
        sender = signal[1] or "Unknown"
        timestamp = signal[2]
        
        print(f"Tin nhan gan nhat:")
        print(f"  Contract: {contract}")
        print(f"  Sender: {sender}")
        print(f"  Timestamp trong DB: {timestamp}")
        print()
        
        # Parse timestamp
        try:
            dt = datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
            print(f"  Parsed: {dt}")
            print(f"  Timezone: {dt.tzinfo}")
            
            # Convert sang UTC+7
            vietnam_tz = timezone(timedelta(hours=7))
            local_time = dt.astimezone(vietnam_tz)
            print(f"  Vietnam time: {local_time}")
            
            # So sánh với thời gian hiện tại
            now_utc = datetime.now(timezone.utc)
            now_vietnam = now_utc.astimezone(vietnam_tz)
            
            print(f"  Thoi gian hien tai UTC: {now_utc}")
            print(f"  Thoi gian hien tai Vietnam: {now_vietnam}")
            
            # Tính khoảng cách
            time_diff = now_utc - dt
            print(f"  Khoang cach: {time_diff}")
            
        except Exception as e:
            print(f"  Parse error: {e}")
    
    print()
    print("PHAN TICH:")
    print("1. Time import tu file JSON: UTC")
    print("2. Time luu khi bot active: CAN KIEM TRA")
    print("3. Time hien thi: UTC+7")
    print()
    
    # Kiểm tra kèo từ bot active (gần đây nhất)
    cursor.execute('''
        SELECT contract_address, sender_username, timestamp
        FROM coin_signals 
        WHERE chat_id = -1002385574544
        ORDER BY timestamp DESC
        LIMIT 3
    ''')
    
    recent_signals = cursor.fetchall()
    
    print("3 tin nhan gan nhat:")
    for i, signal in enumerate(recent_signals, 1):
        contract = signal[0]
        sender = signal[1] or "Unknown"
        timestamp = signal[2]
        
        print(f"{i}. {sender}")
        print(f"   Contract: {contract[:30]}...")
        print(f"   Timestamp: {timestamp}")
        
        # Parse và convert
        try:
            dt = datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
            vietnam_tz = timezone(timedelta(hours=7))
            local_time = dt.astimezone(vietnam_tz)
            print(f"   Vietnam time: {local_time}")
        except:
            print(f"   Parse error")
        print()
    
    conn.close()

if __name__ == "__main__":
    check_3_times()
