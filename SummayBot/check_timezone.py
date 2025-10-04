#!/usr/bin/env python3
"""
Script kiểm tra timezone trong database
"""

import sqlite3
from datetime import datetime, timezone, timedelta

def check_timezone():
    """Kiểm tra timezone trong database"""
    
    print("KIEM TRA TIMEZONE TRONG DATABASE")
    print("=" * 50)
    
    # Kết nối database
    conn = sqlite3.connect("coin_tracker.db")
    cursor = conn.cursor()
    
    # Lấy 10 tin nhắn gần nhất
    cursor.execute('''
        SELECT contract_address, sender_username, timestamp, price_at_signal
        FROM coin_signals 
        WHERE chat_id = -1002385574544
        ORDER BY timestamp DESC
        LIMIT 10
    ''')
    
    signals = cursor.fetchall()
    
    print("10 tin nhan gan nhat:")
    for i, signal in enumerate(signals, 1):
        contract = signal[0]
        sender = signal[1] or "Unknown"
        timestamp = signal[2]
        price = signal[3]
        
        print(f"{i}. {sender}")
        print(f"   Contract: {contract[:30]}...")
        print(f"   Timestamp: {timestamp}")
        
        # Parse timestamp
        try:
            if 'T' in timestamp:
                # ISO format
                dt = datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
                print(f"   Parsed: {dt}")
                print(f"   UTC: {dt.astimezone(timezone.utc)}")
            else:
                print(f"   Raw: {timestamp}")
        except Exception as e:
            print(f"   Parse error: {e}")
        
        print()
    
    # Kiểm tra thời gian hiện tại
    now_utc = datetime.now(timezone.utc)
    now_local = datetime.now()
    
    print("THOI GIAN HIEN TAI:")
    print(f"UTC: {now_utc}")
    print(f"Local: {now_local}")
    print()
    
    # Kiểm tra kèo trong 2 giờ qua
    two_hours_ago = now_utc - timedelta(hours=2)
    print(f"2 gio truoc (UTC): {two_hours_ago}")
    
    cursor.execute('''
        SELECT contract_address, sender_username, timestamp
        FROM coin_signals 
        WHERE timestamp >= ? AND chat_id = -1002385574544
        ORDER BY timestamp DESC
    ''', (two_hours_ago.isoformat(),))
    
    recent_signals = cursor.fetchall()
    print(f"Keo trong 2 gio qua: {len(recent_signals)}")
    
    for signal in recent_signals:
        contract = signal[0]
        sender = signal[1] or "Unknown"
        timestamp = signal[2]
        
        print(f"- {sender}: {timestamp}")
    
    conn.close()

if __name__ == "__main__":
    check_timezone()
