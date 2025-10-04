#!/usr/bin/env python3
"""
Script debug đơn giản
"""

import sqlite3
from datetime import datetime, timezone, timedelta

def debug_simple():
    """Debug đơn giản"""
    
    print("DEBUG SIMPLE")
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
        print(f"  Contract: {contract[:30]}...")
        print(f"  Sender: {sender}")
        print(f"  Timestamp: {timestamp}")
        print()
        
        # Parse timestamp
        try:
            if '+' in timestamp:
                # Có timezone info
                dt = datetime.fromisoformat(timestamp)
                print(f"  Parsed: {dt}")
                print(f"  Timezone: {dt.tzinfo}")
            else:
                print(f"  Raw: {timestamp}")
        except Exception as e:
            print(f"  Parse error: {e}")
    
    # Kiểm tra thời gian hiện tại
    now_utc = datetime.now(timezone.utc)
    now_local = datetime.now()
    vietnam_tz = timezone(timedelta(hours=7))
    now_vietnam = datetime.now(vietnam_tz)
    
    print(f"Thoi gian hien tai:")
    print(f"  UTC: {now_utc}")
    print(f"  Local: {now_local}")
    print(f"  Vietnam (+07:00): {now_vietnam}")
    print()
    
    # Kiểm tra kèo trong 1 giờ qua với các timezone khác nhau
    one_hour_ago_utc = now_utc - timedelta(hours=1)
    one_hour_ago_local = now_local - timedelta(hours=1)
    one_hour_ago_vietnam = now_vietnam - timedelta(hours=1)
    
    print(f"1 gio truoc:")
    print(f"  UTC: {one_hour_ago_utc}")
    print(f"  Local: {one_hour_ago_local}")
    print(f"  Vietnam: {one_hour_ago_vietnam}")
    print()
    
    # Test với từng timezone
    for tz_name, start_time in [
        ("UTC", one_hour_ago_utc),
        ("Local", one_hour_ago_local),
        ("Vietnam", one_hour_ago_vietnam)
    ]:
        cursor.execute('''
            SELECT COUNT(*) FROM coin_signals 
            WHERE timestamp >= ? AND chat_id = -1002385574544
        ''', (start_time.isoformat(),))
        
        count = cursor.fetchone()[0]
        print(f"Keo trong 1h qua ({tz_name}): {count}")
    
    conn.close()

if __name__ == "__main__":
    debug_simple()
