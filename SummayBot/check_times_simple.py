#!/usr/bin/env python3
"""
Script kiểm tra time đơn giản
"""

import sqlite3
from datetime import datetime, timezone, timedelta

def check_times_simple():
    """Kiểm tra time đơn giản"""
    
    print("KIEM TRA TIME")
    print("=" * 30)
    
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
        print(f"  Timestamp: {timestamp}")
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
            
        except Exception as e:
            print(f"  Parse error: {e}")
    
    # Kiểm tra thời gian hiện tại
    now_utc = datetime.now(timezone.utc)
    vietnam_tz = timezone(timedelta(hours=7))
    now_vietnam = now_utc.astimezone(vietnam_tz)
    
    print(f"Thoi gian hien tai:")
    print(f"  UTC: {now_utc}")
    print(f"  Vietnam: {now_vietnam}")
    
    conn.close()

if __name__ == "__main__":
    check_times_simple()
