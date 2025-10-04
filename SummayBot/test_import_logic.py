#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sqlite3
from datetime import datetime, timezone, timedelta

def test_import_logic():
    """Test logic import để đảm bảo chỉ import lần sớm nhất"""
    
    print("=== TEST IMPORT LOGIC ===")
    
    # Kết nối database
    conn = sqlite3.connect("coin_tracker.db")
    cursor = conn.cursor()
    
    # Kiểm tra duplicate contracts
    cursor.execute("""
        SELECT contract_address, COUNT(*) as count, 
               MIN(timestamp) as earliest, MAX(timestamp) as latest
        FROM coin_signals 
        GROUP BY contract_address 
        HAVING COUNT(*) > 1
        ORDER BY count DESC
    """)
    
    duplicates = cursor.fetchall()
    
    if duplicates:
        print(f"Found {len(duplicates)} contracts with duplicates:")
        for contract, count, earliest, latest in duplicates:
            print(f"  {contract[:20]}... | Count: {count} | Earliest: {earliest} | Latest: {latest}")
    else:
        print("No duplicate contracts found - import logic working correctly!")
    
    # Kiểm tra tất cả contracts
    cursor.execute("""
        SELECT contract_address, COUNT(*) as count
        FROM coin_signals 
        GROUP BY contract_address 
        ORDER BY count DESC
        LIMIT 10
    """)
    
    all_contracts = cursor.fetchall()
    
    print(f"\nTop 10 contracts by count:")
    for contract, count in all_contracts:
        print(f"  {contract[:20]}... | Count: {count}")
    
    # Kiểm tra timestamp order cho một contract cụ thể
    if all_contracts:
        test_contract = all_contracts[0][0]
        print(f"\n=== DETAILED CHECK FOR {test_contract[:20]}... ===")
        
        cursor.execute("""
            SELECT sender_username, timestamp, price_at_signal
            FROM coin_signals 
            WHERE contract_address = ?
            ORDER BY timestamp ASC
        """, (test_contract,))
        
        records = cursor.fetchall()
        
        for i, (username, timestamp, price) in enumerate(records, 1):
            print(f"  {i}. {username} | {timestamp} | Price: {price}")
    
    # Kiểm tra logic "chỉ lưu lần sớm nhất"
    print(f"\n=== CHECKING EARLIEST TIMESTAMP LOGIC ===")
    
    cursor.execute("""
        SELECT contract_address, MIN(timestamp) as earliest_time
        FROM coin_signals 
        GROUP BY contract_address
        ORDER BY earliest_time DESC
        LIMIT 5
    """)
    
    earliest_records = cursor.fetchall()
    
    for contract, earliest_time in earliest_records:
        # Lấy record với timestamp sớm nhất
        cursor.execute("""
            SELECT sender_username, timestamp, price_at_signal
            FROM coin_signals 
            WHERE contract_address = ? AND timestamp = ?
        """, (contract, earliest_time))
        
        record = cursor.fetchone()
        if record:
            username, timestamp, price = record
            print(f"  {contract[:20]}... | Earliest: {username} | {timestamp} | Price: {price}")
    
    conn.close()
    
    print(f"\n=== SUMMARY ===")
    if duplicates:
        print(f"Found {len(duplicates)} contracts with duplicates")
        print(f"   Import logic needs fixing")
    else:
        print(f"No duplicates found")
        print(f"   Import logic working correctly")
        print(f"   Each contract has only the earliest timestamp")

if __name__ == "__main__":
    test_import_logic()
