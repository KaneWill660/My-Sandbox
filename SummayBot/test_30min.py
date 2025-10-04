#!/usr/bin/env python3
"""
Script test 30 phút
"""

import sqlite3
from datetime import datetime, timezone, timedelta

def test_30min():
    """Test 30 phút"""
    
    print("TEST 30 PHUT")
    print("=" * 30)
    
    # Kết nối database
    conn = sqlite3.connect("coin_tracker.db")
    cursor = conn.cursor()
    
    # Tính thời gian 30 phút trước
    vietnam_tz = timezone(timedelta(hours=7))
    now_vietnam = datetime.now(vietnam_tz)
    thirty_min_ago = now_vietnam - timedelta(minutes=30)
    
    print(f"Thoi gian hien tai: {now_vietnam}")
    print(f"30 phut truoc: {thirty_min_ago}")
    print()
    
    # Lấy kèo trong 30 phút qua
    cursor.execute('''
        SELECT contract_address, sender_username, timestamp
        FROM coin_signals 
        WHERE timestamp >= ? AND chat_id = -1002385574544
        ORDER BY timestamp DESC
    ''', (thirty_min_ago.isoformat(),))
    
    signals = cursor.fetchall()
    
    print(f"Keo trong 30 phut qua: {len(signals)}")
    
    for signal in signals:
        contract = signal[0]
        sender = signal[1] or "Unknown"
        timestamp = signal[2]
        
        print(f"- {sender}: {timestamp}")
    
    conn.close()

if __name__ == "__main__":
    test_30min()
