#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sqlite3
from datetime import datetime, timezone, timedelta

def check_data_source():
    """Kiểm tra nguồn gốc của data trong database"""
    
    print("=== CHECK DATA SOURCE ===")
    
    # Kết nối database
    conn = sqlite3.connect("coin_tracker.db")
    cursor = conn.cursor()
    
    # Kiểm tra tất cả records
    cursor.execute("""
        SELECT id, contract_address, sender_username, timestamp, price_at_signal
        FROM coin_signals 
        ORDER BY timestamp DESC
    """)
    
    records = cursor.fetchall()
    
    print(f"Total records: {len(records)}")
    print("=" * 80)
    
    # Phân loại data
    imported_data = []  # sender_id = 0 (từ import)
    bot_data = []       # sender_id != 0 (từ bot real-time)
    
    for record in records:
        id_val, contract, username, timestamp, price = record
        
        # Kiểm tra sender_id để phân biệt
        cursor.execute("SELECT sender_id FROM coin_signals WHERE id = ?", (id_val,))
        sender_id = cursor.fetchone()[0]
        
        if sender_id == 0:
            imported_data.append(record)
        else:
            bot_data.append(record)
    
    print(f"Imported data (sender_id = 0): {len(imported_data)} records")
    print(f"Bot data (sender_id != 0): {len(bot_data)} records")
    
    print(f"\n=== IMPORTED DATA (first 5) ===")
    for i, (id_val, contract, username, timestamp, price) in enumerate(imported_data[:5], 1):
        print(f"{i}. {contract[:20]}... | {username.encode('ascii', 'ignore').decode('ascii')} | {timestamp} | Price: {price}")
    
    print(f"\n=== BOT DATA (first 5) ===")
    for i, (id_val, contract, username, timestamp, price) in enumerate(bot_data[:5], 1):
        print(f"{i}. {contract[:20]}... | {username.encode('ascii', 'ignore').decode('ascii')} | {timestamp} | Price: {price}")
    
    # Kiểm tra timestamp format của từng loại
    print(f"\n=== TIMESTAMP FORMAT ANALYSIS ===")
    
    if imported_data:
        print(f"Imported data timestamp format:")
        sample_imported = imported_data[0][3]
        print(f"  Sample: {sample_imported}")
        print(f"  Has timezone: {'+00:00' in str(sample_imported)}")
    
    if bot_data:
        print(f"Bot data timestamp format:")
        sample_bot = bot_data[0][3]
        print(f"  Sample: {sample_bot}")
        print(f"  Has timezone: {'+00:00' in str(sample_bot)}")
    
    conn.close()

if __name__ == "__main__":
    check_data_source()
