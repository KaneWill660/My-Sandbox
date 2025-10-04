#!/usr/bin/env python3
"""
Script debug timezone mismatch
"""

import sqlite3
from datetime import datetime, timezone, timedelta

def debug_timezone():
    """Debug timezone mismatch"""
    
    print("DEBUG TIMEZONE MISMATCH")
    print("=" * 50)
    
    # Kết nối database
    conn = sqlite3.connect("coin_tracker.db")
    cursor = conn.cursor()
    
    # Lấy 5 tin nhắn gần nhất
    cursor.execute('''
        SELECT contract_address, sender_username, timestamp, price_at_signal
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
        price = signal[3]
        
        print(f"{i}. {sender}")
        print(f"   Contract: {contract[:30]}...")
        print(f"   Timestamp: {timestamp}")
        print(f"   Price: {price}")
        print()
    
    # Kiểm tra thời gian
    now_utc = datetime.now(timezone.utc)
    now_local = datetime.now()
    one_hour_ago_utc = now_utc - timedelta(hours=1)
    one_hour_ago_local = now_local - timedelta(hours=1)
    
    print("THOI GIAN:")
    print(f"UTC now: {now_utc}")
    print(f"Local now: {now_local}")
    print(f"1h ago (UTC): {one_hour_ago_utc}")
    print(f"1h ago (Local): {one_hour_ago_local}")
    print()
    
    # Kiểm tra kèo trong 1 giờ qua (UTC)
    cursor.execute('''
        SELECT COUNT(*) FROM coin_signals 
        WHERE timestamp >= ? AND chat_id = -1002385574544
    ''', (one_hour_ago_utc.isoformat(),))
    
    utc_count = cursor.fetchone()[0]
    print(f"Keo trong 1h qua (UTC): {utc_count}")
    
    # Kiểm tra kèo trong 1 giờ qua (Local)
    cursor.execute('''
        SELECT COUNT(*) FROM coin_signals 
        WHERE timestamp >= ? AND chat_id = -1002385574544
    ''', (one_hour_ago_local.isoformat(),))
    
    local_count = cursor.fetchone()[0]
    print(f"Keo trong 1h qua (Local): {local_count}")
    
    # Kiểm tra kèo trong 2 giờ qua (UTC)
    two_hours_ago_utc = now_utc - timedelta(hours=2)
    cursor.execute('''
        SELECT COUNT(*) FROM coin_signals 
        WHERE timestamp >= ? AND chat_id = -1002385574544
    ''', (two_hours_ago_utc.isoformat(),))
    
    utc_2h_count = cursor.fetchone()[0]
    print(f"Keo trong 2h qua (UTC): {utc_2h_count}")
    
    # Kiểm tra kèo trong 2 giờ qua (Local)
    two_hours_ago_local = now_local - timedelta(hours=2)
    cursor.execute('''
        SELECT COUNT(*) FROM coin_signals 
        WHERE timestamp >= ? AND chat_id = -1002385574544
    ''', (two_hours_ago_local.isoformat(),))
    
    local_2h_count = cursor.fetchone()[0]
    print(f"Keo trong 2h qua (Local): {local_2h_count}")
    
    conn.close()
    
    print()
    print("KET LUAN:")
    if utc_count > 0:
        print("✅ Bot dang luu UTC time")
        print("✅ Script test can su dung UTC time")
    elif local_count > 0:
        print("✅ Bot dang luu Local time")
        print("✅ Script test dang su dung Local time")
    else:
        print("❌ Khong co keo nao trong 1-2h qua")
        print("❌ Can kiem tra lai")

if __name__ == "__main__":
    debug_timezone()
