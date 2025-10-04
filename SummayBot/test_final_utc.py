#!/usr/bin/env python3
"""
Script test cuối cùng với UTC
"""

import sqlite3
from datetime import datetime, timezone, timedelta

def safe_print(text):
    """In text an toàn với Unicode"""
    try:
        print(text)
    except UnicodeEncodeError:
        safe_text = text.encode('ascii', 'replace').decode('ascii')
        print(safe_text)

def test_final_utc():
    """Test cuối cùng với UTC"""
    
    safe_print("TEST FINAL UTC")
    safe_print("=" * 30)
    
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
        
        safe_print("Tin nhan gan nhat:")
        safe_print(f"  Contract: {contract[:30]}...")
        safe_print(f"  Sender: {sender}")
        safe_print(f"  Timestamp: {timestamp}")
        safe_print("")
        
        # Parse timestamp
        try:
            dt = datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
            safe_print(f"  Parsed UTC: {dt}")
            
            # Convert sang UTC+7
            vietnam_tz = timezone(timedelta(hours=7))
            local_time = dt.astimezone(vietnam_tz)
            safe_print(f"  Vietnam time: {local_time}")
        except Exception as e:
            safe_print(f"  Parse error: {e}")
    
    # Kiểm tra thời gian hiện tại
    now_utc = datetime.now(timezone.utc)
    vietnam_tz = timezone(timedelta(hours=7))
    now_vietnam = now_utc.astimezone(vietnam_tz)
    
    safe_print("Thoi gian hien tai:")
    safe_print(f"  UTC: {now_utc}")
    safe_print(f"  Vietnam: {now_vietnam}")
    safe_print("")
    
    # Kiểm tra kèo trong 1 giờ qua
    one_hour_ago_utc = now_utc - timedelta(hours=1)
    one_hour_ago_vietnam = one_hour_ago_utc.astimezone(vietnam_tz)
    
    safe_print("1 gio truoc:")
    safe_print(f"  UTC: {one_hour_ago_utc}")
    safe_print(f"  Vietnam: {one_hour_ago_vietnam}")
    safe_print("")
    
    # Lấy kèo trong 1 giờ qua
    cursor.execute('''
        SELECT COUNT(*) FROM coin_signals 
        WHERE timestamp >= ? AND chat_id = -1002385574544
    ''', (one_hour_ago_utc.isoformat(),))
    
    count = cursor.fetchone()[0]
    safe_print(f"Keo trong 1 gio qua: {count}")
    
    # Lấy kèo trong 2 giờ qua
    two_hours_ago_utc = now_utc - timedelta(hours=2)
    cursor.execute('''
        SELECT COUNT(*) FROM coin_signals 
        WHERE timestamp >= ? AND chat_id = -1002385574544
    ''', (two_hours_ago_utc.isoformat(),))
    
    count_2h = cursor.fetchone()[0]
    safe_print(f"Keo trong 2 gio qua: {count_2h}")
    
    conn.close()

if __name__ == "__main__":
    test_final_utc()
