#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from datetime import datetime, timezone, timedelta

def test_timezone_conversion():
    """Test conversion từ UTC+7 sang UTC"""
    
    print("=== TEST TIMEZONE CONVERSION ===")
    
    # Test data từ JSON
    json_date = "2025-10-04T12:40:17"
    print(f"JSON date (UTC+7): {json_date}")
    
    # Parse date từ JSON
    dt = datetime.fromisoformat(json_date)
    print(f"Parsed datetime (no timezone): {dt}")
    
    # Thêm timezone UTC+7
    vietnam_tz = timezone(timedelta(hours=7))
    dt_utc7 = dt.replace(tzinfo=vietnam_tz)
    print(f"With UTC+7 timezone: {dt_utc7}")
    
    # Convert sang UTC (trừ 7 giờ)
    dt_utc = dt_utc7.astimezone(timezone.utc)
    print(f"Converted to UTC: {dt_utc}")
    
    # So sánh
    print(f"\nTime difference: {dt_utc7.hour - dt_utc.hour} hours")
    print(f"UTC+7: {dt_utc7.strftime('%H:%M')}")
    print(f"UTC:   {dt_utc.strftime('%H:%M')}")
    
    # Test với nhiều thời điểm khác nhau
    print(f"\n=== TEST MULTIPLE TIMES ===")
    test_times = [
        "2025-10-04T00:00:00",  # Midnight
        "2025-10-04T12:00:00",  # Noon
        "2025-10-04T23:59:59",  # End of day
        "2025-10-04T07:30:15",  # Morning
        "2025-10-04T18:45:30",  # Evening
    ]
    
    for time_str in test_times:
        dt = datetime.fromisoformat(time_str)
        dt_utc7 = dt.replace(tzinfo=timezone(timedelta(hours=7)))
        dt_utc = dt_utc7.astimezone(timezone.utc)
        
        print(f"{time_str} (UTC+7) -> {dt_utc.strftime('%Y-%m-%dT%H:%M:%S')} (UTC)")
    
    # Test edge case - qua ngày
    print(f"\n=== TEST EDGE CASE - CROSS DAY ===")
    edge_times = [
        "2025-10-04T01:00:00",  # 1 AM UTC+7 -> 6 PM previous day UTC
        "2025-10-04T06:00:00",  # 6 AM UTC+7 -> 11 PM previous day UTC
        "2025-10-04T07:00:00",  # 7 AM UTC+7 -> 12 AM same day UTC
    ]
    
    for time_str in edge_times:
        dt = datetime.fromisoformat(time_str)
        dt_utc7 = dt.replace(tzinfo=timezone(timedelta(hours=7)))
        dt_utc = dt_utc7.astimezone(timezone.utc)
        
        print(f"{time_str} (UTC+7) -> {dt_utc.strftime('%Y-%m-%dT%H:%M:%S')} (UTC)")

if __name__ == "__main__":
    test_timezone_conversion()
