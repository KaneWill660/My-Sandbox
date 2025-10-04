#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sqlite3
from datetime import datetime, timezone, timedelta

def verify_final_fix():
    """Verify final timezone fix"""
    
    print("=== VERIFY FINAL TIMEZONE FIX ===")
    
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
        
        # Test logic mới
        if isinstance(timestamp, str):
            try:
                # Thử parse với timezone info trước
                if '+00:00' in timestamp or 'Z' in timestamp:
                    # Có timezone info, parse bình thường
                    print(f"   Type: Has timezone info")
                    dt = datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
                else:
                    # Không có timezone info, giả sử là UTC+7 (data cũ từ import)
                    print(f"   Type: No timezone info (old data)")
                    dt = datetime.fromisoformat(timestamp)
                    # Thêm timezone UTC+7
                    vietnam_tz = timezone(timedelta(hours=7))
                    dt = dt.replace(tzinfo=vietnam_tz)
                    # Convert sang UTC
                    dt = dt.astimezone(timezone.utc)
                
                # Convert UTC sang UTC+7 để hiển thị
                vietnam_tz = timezone(timedelta(hours=7))
                display_time = dt.astimezone(vietnam_tz)
                
                print(f"   UTC time: {dt.strftime('%Y-%m-%d %H:%M:%S')}")
                print(f"   UTC+7 time: {display_time.strftime('%Y-%m-%d %H:%M:%S')}")
                print(f"   Display time: {display_time.strftime('%H:%M')}")
                
            except Exception as e:
                print(f"   Error: {e}")
        else:
            print(f"   Type: {type(timestamp)}")
        
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
    print(f"Timezone conversion: UTC+7 -> UTC (for storage)")
    print(f"Display conversion: UTC -> UTC+7 (for display)")
    print(f"Mixed data handling: Both old and new timestamp formats")
    print(f"Database storage: UTC")
    print(f"Summary logic: UTC comparison")
    print(f"Records in 1h: {count_1h}")
    print(f"Records in 24h: {count_24h}")

if __name__ == "__main__":
    verify_final_fix()
