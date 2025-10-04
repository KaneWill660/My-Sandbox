#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sqlite3
from datetime import datetime, timezone, timedelta

def verify_timezone_fix():
    """Verify timezone conversion đã đúng chưa"""
    
    print("=== VERIFY TIMEZONE FIX ===")
    
    # Kết nối database
    conn = sqlite3.connect("coin_tracker.db")
    cursor = conn.cursor()
    
    # Lấy một vài records để kiểm tra
    cursor.execute("""
        SELECT contract_address, sender_username, timestamp 
        FROM coin_signals 
        ORDER BY timestamp DESC 
        LIMIT 5
    """)
    
    records = cursor.fetchall()
    
    print("Top 5 records gan nhat:")
    print("=" * 80)
    
    for i, (contract, username, timestamp) in enumerate(records, 1):
        print(f"{i}. Contract: {contract[:20]}...")
        print(f"   User: {username.encode('ascii', 'ignore').decode('ascii')}")
        print(f"   Raw timestamp: {timestamp}")
        
        # Parse timestamp từ database (UTC)
        if isinstance(timestamp, str):
            try:
                db_time = datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
            except:
                db_time = None
        else:
            db_time = timestamp
        
        if db_time:
            # Convert UTC sang UTC+7 để hiển thị
            vietnam_tz = timezone(timedelta(hours=7))
            display_time = db_time.astimezone(vietnam_tz)
            
            print(f"   UTC time: {db_time.strftime('%Y-%m-%d %H:%M:%S')}")
            print(f"   UTC+7 time: {display_time.strftime('%Y-%m-%d %H:%M:%S')}")
            print(f"   Time difference: {db_time.hour - display_time.hour} hours")
        
        print("-" * 40)
    
    # Kiểm tra thời gian hiện tại
    now_utc = datetime.now(timezone.utc)
    now_utc7 = now_utc.astimezone(timezone(timedelta(hours=7)))
    
    print(f"\nCurrent time:")
    print(f"UTC:   {now_utc.strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"UTC+7: {now_utc7.strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Test với 1 giờ trước
    one_hour_ago_utc = now_utc - timedelta(hours=1)
    one_hour_ago_utc7 = one_hour_ago_utc.astimezone(timezone(timedelta(hours=7)))
    
    print(f"\n1 hour ago:")
    print(f"UTC:   {one_hour_ago_utc.strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"UTC+7: {one_hour_ago_utc7.strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Kiểm tra records trong 1 giờ qua
    cursor.execute("""
        SELECT COUNT(*) FROM coin_signals 
        WHERE timestamp >= ?
    """, (one_hour_ago_utc,))
    
    count_1h = cursor.fetchone()[0]
    print(f"\nRecords trong 1 gio qua (UTC): {count_1h}")
    
    # Kiểm tra records trong 24 giờ qua
    twenty_four_hours_ago_utc = now_utc - timedelta(hours=24)
    cursor.execute("""
        SELECT COUNT(*) FROM coin_signals 
        WHERE timestamp >= ?
    """, (twenty_four_hours_ago_utc,))
    
    count_24h = cursor.fetchone()[0]
    print(f"Records trong 24 gio qua (UTC): {count_24h}")
    
    conn.close()
    
    print(f"\n=== SUMMARY ===")
    print(f"Timezone conversion: UTC+7 -> UTC")
    print(f"Display conversion: UTC -> UTC+7")
    print(f"Database storage: UTC")
    print(f"Summary logic: UTC comparison")
    print(f"Records in 1h: {count_1h}")
    print(f"Records in 24h: {count_24h}")

if __name__ == "__main__":
    verify_timezone_fix()
