#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sqlite3
from datetime import datetime, timezone, timedelta

def debug_time_comparison():
    """Debug time comparison logic"""
    
    print("=== DEBUG TIME COMPARISON ===")
    
    # Kết nối database
    conn = sqlite3.connect("coin_tracker.db")
    cursor = conn.cursor()
    
    # Lấy thời gian hiện tại
    now_utc = datetime.now(timezone.utc)
    one_hour_ago_utc = now_utc - timedelta(hours=1)
    
    print(f"Current UTC time: {now_utc}")
    print(f"1 hour ago UTC: {one_hour_ago_utc}")
    
    # Lấy một vài timestamps từ database
    cursor.execute("""
        SELECT timestamp, contract_address 
        FROM coin_signals 
        ORDER BY timestamp DESC 
        LIMIT 5
    """)
    
    records = cursor.fetchall()
    
    print(f"\nTop 5 timestamps from database:")
    for timestamp, contract in records:
        print(f"  {timestamp} | {contract[:20]}...")
        
        # Test comparison
        if isinstance(timestamp, str):
            try:
                # Parse timestamp
                if '+00:00' in timestamp or 'Z' in timestamp:
                    dt = datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
                else:
                    # Không có timezone info, giả sử là UTC+7
                    dt = datetime.fromisoformat(timestamp)
                    vietnam_tz = timezone(timedelta(hours=7))
                    dt = dt.replace(tzinfo=vietnam_tz)
                    dt = dt.astimezone(timezone.utc)
                
                # So sánh
                is_after = dt >= one_hour_ago_utc
                print(f"    Parsed: {dt}")
                print(f"    >= 1h ago: {is_after}")
                
            except Exception as e:
                print(f"    Error parsing: {e}")
    
    # Test SQL query với different approaches
    print(f"\n=== TESTING SQL QUERIES ===")
    
    # Approach 1: Direct comparison
    print(f"1. Direct comparison:")
    cursor.execute("""
        SELECT COUNT(*) FROM coin_signals 
        WHERE timestamp >= ?
    """, (one_hour_ago_utc,))
    count1 = cursor.fetchone()[0]
    print(f"   Count: {count1}")
    
    # Approach 2: String comparison
    print(f"2. String comparison:")
    start_date_str = one_hour_ago_utc.strftime('%Y-%m-%d %H:%M:%S')
    cursor.execute("""
        SELECT COUNT(*) FROM coin_signals 
        WHERE timestamp >= ?
    """, (start_date_str,))
    count2 = cursor.fetchone()[0]
    print(f"   Start date string: {start_date_str}")
    print(f"   Count: {count2}")
    
    # Approach 3: Manual parsing
    print(f"3. Manual parsing approach:")
    cursor.execute("""
        SELECT timestamp FROM coin_signals 
        ORDER BY timestamp DESC 
        LIMIT 10
    """)
    timestamps = cursor.fetchall()
    
    count3 = 0
    for (timestamp,) in timestamps:
        try:
            if '+00:00' in str(timestamp) or 'Z' in str(timestamp):
                dt = datetime.fromisoformat(str(timestamp).replace('Z', '+00:00'))
            else:
                dt = datetime.fromisoformat(str(timestamp))
                vietnam_tz = timezone(timedelta(hours=7))
                dt = dt.replace(tzinfo=vietnam_tz)
                dt = dt.astimezone(timezone.utc)
            
            if dt >= one_hour_ago_utc:
                count3 += 1
                
        except Exception as e:
            print(f"   Error parsing {timestamp}: {e}")
    
    print(f"   Count: {count3}")
    
    # Show some examples
    print(f"\n=== EXAMPLES ===")
    for (timestamp,) in timestamps[:3]:
        try:
            if '+00:00' in str(timestamp) or 'Z' in str(timestamp):
                dt = datetime.fromisoformat(str(timestamp).replace('Z', '+00:00'))
            else:
                dt = datetime.fromisoformat(str(timestamp))
                vietnam_tz = timezone(timedelta(hours=7))
                dt = dt.replace(tzinfo=vietnam_tz)
                dt = dt.astimezone(timezone.utc)
            
            is_after = dt >= one_hour_ago_utc
            print(f"   {timestamp} -> {dt} -> >= 1h ago: {is_after}")
            
        except Exception as e:
            print(f"   {timestamp} -> Error: {e}")
    
    conn.close()

if __name__ == "__main__":
    debug_time_comparison()
