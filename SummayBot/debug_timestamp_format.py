#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sqlite3
from datetime import datetime, timezone, timedelta

def debug_timestamp_format():
    """Debug timestamp format trong database"""
    
    print("=== DEBUG TIMESTAMP FORMAT ===")
    
    # Kết nối database
    conn = sqlite3.connect("coin_tracker.db")
    cursor = conn.cursor()
    
    # Lấy tất cả timestamps để kiểm tra format
    cursor.execute("""
        SELECT timestamp, COUNT(*) as count 
        FROM coin_signals 
        GROUP BY timestamp 
        ORDER BY timestamp DESC 
        LIMIT 10
    """)
    
    records = cursor.fetchall()
    
    print("Top 10 timestamp formats:")
    print("=" * 80)
    
    for timestamp, count in records:
        print(f"Raw: {timestamp} (count: {count})")
        
        # Test parsing
        if isinstance(timestamp, str):
            print(f"  Type: string")
            
            # Test 1: Parse as ISO with timezone
            try:
                dt1 = datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
                print(f"  Parse with timezone: {dt1}")
                print(f"  Timezone info: {dt1.tzinfo}")
            except Exception as e:
                print(f"  Parse with timezone failed: {e}")
            
            # Test 2: Parse as naive datetime
            try:
                dt2 = datetime.fromisoformat(timestamp)
                print(f"  Parse naive: {dt2}")
                print(f"  Timezone info: {dt2.tzinfo}")
                
                # Add UTC timezone
                dt2_utc = dt2.replace(tzinfo=timezone.utc)
                print(f"  Add UTC timezone: {dt2_utc}")
                
                # Convert to UTC+7
                vietnam_tz = timezone(timedelta(hours=7))
                dt2_utc7 = dt2_utc.astimezone(vietnam_tz)
                print(f"  Convert to UTC+7: {dt2_utc7}")
                
            except Exception as e:
                print(f"  Parse naive failed: {e}")
        else:
            print(f"  Type: {type(timestamp)}")
            print(f"  Value: {timestamp}")
        
        print("-" * 40)
    
    # Kiểm tra tất cả unique formats
    cursor.execute("""
        SELECT DISTINCT 
            CASE 
                WHEN timestamp LIKE '%+00:00' THEN 'with_timezone'
                WHEN timestamp LIKE '%T%' THEN 'iso_format'
                ELSE 'other_format'
            END as format_type,
            COUNT(*) as count
        FROM coin_signals 
        GROUP BY format_type
    """)
    
    format_stats = cursor.fetchall()
    
    print(f"\nTimestamp format statistics:")
    for format_type, count in format_stats:
        print(f"- {format_type}: {count} records")
    
    conn.close()

if __name__ == "__main__":
    debug_timestamp_format()
