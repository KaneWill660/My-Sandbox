#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sqlite3

def check_price_data():
    """Check price data in database"""
    
    print("=== CHECK PRICE DATA ===")
    
    # Kết nối database
    conn = sqlite3.connect("coin_tracker.db")
    cursor = conn.cursor()
    
    # Kiểm tra price_at_signal
    cursor.execute("""
        SELECT contract_address, sender_username, timestamp, price_at_signal
        FROM coin_signals 
        ORDER BY timestamp DESC 
        LIMIT 10
    """)
    
    records = cursor.fetchall()
    
    print("Top 10 records:")
    print("=" * 80)
    
    for contract, username, timestamp, price_at_signal in records:
        print(f"Contract: {contract[:20]}...")
        print(f"User: {username.encode('ascii', 'ignore').decode('ascii')}")
        print(f"Time: {timestamp}")
        print(f"Price at signal: {price_at_signal}")
        print("-" * 40)
    
    # Thống kê price_at_signal
    cursor.execute("""
        SELECT 
            COUNT(*) as total,
            COUNT(price_at_signal) as with_price,
            COUNT(*) - COUNT(price_at_signal) as without_price
        FROM coin_signals
    """)
    
    stats = cursor.fetchone()
    total, with_price, without_price = stats
    
    print(f"\n=== PRICE STATISTICS ===")
    print(f"Total records: {total}")
    print(f"With price_at_signal: {with_price}")
    print(f"Without price_at_signal: {without_price}")
    
    if without_price > 0:
        print(f"\n❌ Problem: {without_price} records have NULL price_at_signal")
        print(f"   This causes both prices to show the same value")
    else:
        print(f"\n✅ All records have price_at_signal")
    
    conn.close()

if __name__ == "__main__":
    check_price_data()
