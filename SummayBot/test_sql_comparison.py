#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sqlite3
from datetime import datetime, timezone, timedelta

def test_sql_comparison():
    """Test SQL comparison logic"""
    
    print("=== TEST SQL COMPARISON ===")
    
    # Kết nối database
    conn = sqlite3.connect("coin_tracker.db")
    cursor = conn.cursor()
    
    # Lấy thời gian hiện tại
    now_utc = datetime.now(timezone.utc)
    one_hour_ago_utc = now_utc - timedelta(hours=1)
    
    print(f"Current UTC time: {now_utc}")
    print(f"1 hour ago UTC: {one_hour_ago_utc}")
    
    # Convert thành string
    start_date_str = one_hour_ago_utc.strftime('%Y-%m-%d %H:%M:%S')
    print(f"Start date string: {start_date_str}")
    
    # Lấy một vài timestamps từ database
    cursor.execute("""
        SELECT timestamp, contract_address 
        FROM coin_signals 
        ORDER BY timestamp DESC 
        LIMIT 10
    """)
    
    records = cursor.fetchall()
    
    print(f"\nTop 10 timestamps from database:")
    for timestamp, contract in records:
        print(f"  {timestamp} | {contract[:20]}...")
        
        # Test string comparison
        is_after_str = str(timestamp) >= start_date_str
        print(f"    String comparison: {is_after_str}")
        
        # Test manual parsing
        try:
            if '+00:00' in str(timestamp) or 'Z' in str(timestamp):
                dt = datetime.fromisoformat(str(timestamp).replace('Z', '+00:00'))
            else:
                dt = datetime.fromisoformat(str(timestamp))
                vietnam_tz = timezone(timedelta(hours=7))
                dt = dt.replace(tzinfo=vietnam_tz)
                dt = dt.astimezone(timezone.utc)
            
            is_after_manual = dt >= one_hour_ago_utc
            print(f"    Manual comparison: {is_after_manual}")
            
        except Exception as e:
            print(f"    Error: {e}")
        
        print()
    
    # Test SQL query
    print(f"=== SQL QUERY TEST ===")
    cursor.execute("""
        SELECT COUNT(*) FROM coin_signals 
        WHERE timestamp >= ?
    """, (start_date_str,))
    count = cursor.fetchone()[0]
    print(f"SQL query count: {count}")
    
    # Manual count
    manual_count = 0
    for timestamp, contract in records:
        try:
            if '+00:00' in str(timestamp) or 'Z' in str(timestamp):
                dt = datetime.fromisoformat(str(timestamp).replace('Z', '+00:00'))
            else:
                dt = datetime.fromisoformat(str(timestamp))
                vietnam_tz = timezone(timedelta(hours=7))
                dt = dt.replace(tzinfo=vietnam_tz)
                dt = dt.astimezone(timezone.utc)
            
            if dt >= one_hour_ago_utc:
                manual_count += 1
                
        except Exception as e:
            pass
    
    print(f"Manual count: {manual_count}")
    
    conn.close()

if __name__ == "__main__":
    test_sql_comparison()
