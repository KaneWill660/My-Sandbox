#!/usr/bin/env python3
"""
Script test timezone fix
"""

import sqlite3
from datetime import datetime, timezone, timedelta

def test_timezone_fix():
    """Test timezone fix"""
    
    print("TEST TIMEZONE FIX")
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
    
    # Kiểm tra thời gian
    now_local = datetime.now()
    one_hour_ago = now_local - timedelta(hours=1)
    
    print(f"Thoi gian hien tai (Local): {now_local}")
    print(f"1 gio truoc (Local): {one_hour_ago}")
    print()
    
    # Kiểm tra kèo trong 1 giờ qua
    cursor.execute('''
        SELECT COUNT(*) FROM coin_signals 
        WHERE timestamp >= ? AND chat_id = -1002385574544
    ''', (one_hour_ago.isoformat(),))
    
    count = cursor.fetchone()[0]
    print(f"Keo trong 1 gio qua: {count}")
    
    if count > 0:
        print("✅ Co keo trong 1 gio qua!")
        print("Bot se hoat dong dung voi /summary 1")
    else:
        print("❌ Khong co keo nao trong 1 gio qua")
        print("Can gui keo moi hoac restart bot")
    
    conn.close()

if __name__ == "__main__":
    test_timezone_fix()
