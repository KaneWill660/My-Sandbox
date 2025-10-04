#!/usr/bin/env python3
"""
Script kiểm tra kèo mới vừa được lưu
"""

import sqlite3
from datetime import datetime, timezone, timedelta

def check_recent_signals():
    """Kiểm tra kèo mới vừa được lưu"""
    
    print("KIEM TRA KEO MOI VUA DUOC LUU")
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
        print(f"   Price: {price}")
        print()
    
    # Kiểm tra thời gian hiện tại
    now_utc = datetime.now(timezone.utc)
    now_local = datetime.now()
    
    print("THOI GIAN HIEN TAI:")
    print(f"UTC: {now_utc}")
    print(f"Local: {now_local}")
    print()
    
    # Kiểm tra kèo trong 1 giờ qua (UTC)
    one_hour_ago_utc = now_utc - timedelta(hours=1)
    print(f"1 gio truoc (UTC): {one_hour_ago_utc}")
    
    cursor.execute('''
        SELECT contract_address, sender_username, timestamp
        FROM coin_signals 
        WHERE timestamp >= ? AND chat_id = -1002385574544
        ORDER BY timestamp DESC
    ''', (one_hour_ago_utc.isoformat(),))
    
    utc_signals = cursor.fetchall()
    print(f"Keo trong 1 gio qua (UTC): {len(utc_signals)}")
    
    # Kiểm tra kèo trong 1 giờ qua (Local)
    one_hour_ago_local = now_local - timedelta(hours=1)
    print(f"1 gio truoc (Local): {one_hour_ago_local}")
    
    cursor.execute('''
        SELECT contract_address, sender_username, timestamp
        FROM coin_signals 
        WHERE timestamp >= ? AND chat_id = -1002385574544
        ORDER BY timestamp DESC
    ''', (one_hour_ago_local.isoformat(),))
    
    local_signals = cursor.fetchall()
    print(f"Keo trong 1 gio qua (Local): {len(local_signals)}")
    
    print("\nKeo trong 1 gio qua (Local):")
    for signal in local_signals:
        contract = signal[0]
        sender = signal[1] or "Unknown"
        timestamp = signal[2]
        
        print(f"- {sender}: {timestamp}")
    
    conn.close()

if __name__ == "__main__":
    check_recent_signals()
