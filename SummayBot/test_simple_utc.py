#!/usr/bin/env python3
"""
Script test đơn giản với UTC
"""

import sqlite3
from datetime import datetime, timezone, timedelta

def test_simple_utc():
    """Test đơn giản với UTC"""
    
    print("TEST SIMPLE UTC")
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
            dt = datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
            print(f"  Parsed UTC: {dt}")
            
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
    print()
    
    # Kiểm tra kèo trong 1 giờ qua
    one_hour_ago_utc = now_utc - timedelta(hours=1)
    one_hour_ago_vietnam = one_hour_ago_utc.astimezone(vietnam_tz)
    
    print(f"1 gio truoc:")
    print(f"  UTC: {one_hour_ago_utc}")
    print(f"  Vietnam: {one_hour_ago_vietnam}")
    print()
    
    # Lấy kèo trong 1 giờ qua
    cursor.execute('''
        SELECT COUNT(*) FROM coin_signals 
        WHERE timestamp >= ? AND chat_id = -1002385574544
    ''', (one_hour_ago_utc.isoformat(),))
    
    count = cursor.fetchone()[0]
    print(f"Keo trong 1 gio qua: {count}")
    
    conn.close()

if __name__ == "__main__":
    test_simple_utc()
