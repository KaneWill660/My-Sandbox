#!/usr/bin/env python3
"""
Script test 15 phút
"""

import sqlite3
from datetime import datetime, timezone, timedelta

def test_15min():
    """Test 15 phút"""
    
    print("TEST 15 PHUT")
    print("=" * 30)
    
    # Kết nối database
    conn = sqlite3.connect("coin_tracker.db")
    cursor = conn.cursor()
    
    # Tính thời gian 15 phút trước
    vietnam_tz = timezone(timedelta(hours=7))
    now_vietnam = datetime.now(vietnam_tz)
    fifteen_min_ago = now_vietnam - timedelta(minutes=15)
    
    print(f"Thoi gian hien tai: {now_vietnam}")
    print(f"15 phut truoc: {fifteen_min_ago}")
    print()
    
    # Lấy kèo trong 15 phút qua
    cursor.execute('''
        SELECT contract_address, sender_username, timestamp
        FROM coin_signals 
        WHERE timestamp >= ? AND chat_id = -1002385574544
        ORDER BY timestamp DESC
    ''', (fifteen_min_ago.isoformat(),))
    
    signals = cursor.fetchall()
    
    print(f"Keo trong 15 phut qua: {len(signals)}")
    
    for signal in signals:
        contract = signal[0]
        sender = signal[1] or "Unknown"
        timestamp = signal[2]
        
        print(f"- {sender}: {timestamp}")
    
    conn.close()

if __name__ == "__main__":
    test_15min()
