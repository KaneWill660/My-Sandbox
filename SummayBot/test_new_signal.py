#!/usr/bin/env python3
"""
Script test kèo mới với UTC time
"""

import sqlite3
from datetime import datetime, timezone, timedelta

def test_new_signal():
    """Test kèo mới"""
    
    print("TEST NEW SIGNAL WITH UTC TIME")
    print("=" * 40)
    
    # Kết nối database
    conn = sqlite3.connect("coin_tracker.db")
    cursor = conn.cursor()
    
    # Lấy 5 tin nhắn gần nhất
    cursor.execute('''
        SELECT contract_address, sender_username, timestamp
        FROM coin_signals 
        WHERE chat_id = -1002385574544
        ORDER BY timestamp DESC
        LIMIT 5
    ''')
    
    signals = cursor.fetchall()
    
    print("5 tin nhan gan nhat:")
    for i, signal in enumerate(signals, 1):
        contract = signal[0]
        sender = signal[1] or "Unknown"
        timestamp = signal[2]
        
        print(f"{i}. {sender}")
        print(f"   Contract: {contract[:30]}...")
        print(f"   Timestamp: {timestamp}")
        print()
    
    # Kiểm tra thời gian hiện tại
    now_utc = datetime.now(timezone.utc)
    vietnam_tz = timezone(timedelta(hours=7))
    now_vietnam = now_utc.astimezone(vietnam_tz)
    
    print(f"Thoi gian hien tai:")
    print(f"  UTC: {now_utc}")
    print(f"  Vietnam (UTC+7): {now_vietnam}")
    print()
    
    # Kiểm tra kèo trong 1 giờ qua
    one_hour_ago_utc = now_utc - timedelta(hours=1)
    one_hour_ago_vietnam = one_hour_ago_utc.astimezone(vietnam_tz)
    
    print(f"1 gio truoc:")
    print(f"  UTC: {one_hour_ago_utc}")
    print(f"  Vietnam (UTC+7): {one_hour_ago_vietnam}")
    print()
    
    # Lấy kèo trong 1 giờ qua
    cursor.execute('''
        SELECT contract_address, sender_username, timestamp
        FROM coin_signals 
        WHERE timestamp >= ? AND chat_id = -1002385574544
        ORDER BY timestamp DESC
    ''', (one_hour_ago_utc.isoformat(),))
    
    recent_signals = cursor.fetchall()
    
    print(f"Keo trong 1 gio qua: {len(recent_signals)}")
    
    for signal in recent_signals:
        contract = signal[0]
        sender = signal[1] or "Unknown"
        timestamp = signal[2]
        
        # Convert UTC sang UTC+7 để hiển thị
        try:
            dt = datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
            local_time = dt.astimezone(vietnam_tz)
            time_str = local_time.strftime("%H:%M")
        except:
            time_str = "Unknown"
        
        print(f"- {sender}: {time_str} ({timestamp})")
    
    conn.close()

if __name__ == "__main__":
    test_new_signal()
