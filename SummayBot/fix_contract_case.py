#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sqlite3
from datetime import datetime, timezone, timedelta

def fix_contract_case():
    """Fix contract address case sensitivity issues"""
    
    print("=== FIX CONTRACT CASE SENSITIVITY ===")
    
    # Kết nối database
    conn = sqlite3.connect("coin_tracker.db")
    cursor = conn.cursor()
    
    # Tìm các contract addresses có case khác nhau
    cursor.execute("""
        SELECT LOWER(contract_address) as lower_contract, 
               COUNT(DISTINCT contract_address) as case_variants,
               GROUP_CONCAT(DISTINCT contract_address) as variants
        FROM coin_signals 
        GROUP BY LOWER(contract_address)
        HAVING COUNT(DISTINCT contract_address) > 1
        ORDER BY case_variants DESC
    """)
    
    case_issues = cursor.fetchall()
    
    if case_issues:
        print(f"Found {len(case_issues)} contracts with case sensitivity issues:")
        for lower_contract, count, variants in case_issues:
            print(f"  {lower_contract[:20]}... | Variants: {count} | {variants}")
    else:
        print("No case sensitivity issues found!")
        conn.close()
        return
    
    print(f"\n=== FIXING CASE ISSUES ===")
    
    for lower_contract, count, variants in case_issues:
        print(f"\nFixing contract: {lower_contract[:20]}...")
        
        # Lấy tất cả records cho contract này
        cursor.execute("""
            SELECT id, contract_address, sender_id, sender_username, 
                   message_id, chat_id, timestamp, price_at_signal
            FROM coin_signals 
            WHERE LOWER(contract_address) = ?
            ORDER BY timestamp ASC
        """, (lower_contract,))
        
        records = cursor.fetchall()
        
        print(f"  Found {len(records)} records")
        
        # Lấy record sớm nhất (đầu tiên)
        earliest_record = records[0]
        earliest_id = earliest_record[0]
        
        print(f"  Earliest record ID: {earliest_id}")
        print(f"  Earliest timestamp: {earliest_record[6]}")
        
        # Xóa tất cả records khác
        other_ids = [record[0] for record in records[1:]]
        if other_ids:
            placeholders = ','.join(['?' for _ in other_ids])
            cursor.execute(f"""
                DELETE FROM coin_signals 
                WHERE id IN ({placeholders})
            """, other_ids)
            print(f"  Deleted {len(other_ids)} duplicate records")
        
        # Cập nhật record sớm nhất với contract address lowercase
        cursor.execute("""
            UPDATE coin_signals 
            SET contract_address = ?
            WHERE id = ?
        """, (lower_contract, earliest_id))
        print(f"  Updated contract address to lowercase: {lower_contract[:20]}...")
    
    # Commit changes
    conn.commit()
    
    # Verify fix
    print(f"\n=== VERIFYING FIX ===")
    cursor.execute("""
        SELECT LOWER(contract_address) as lower_contract, 
               COUNT(DISTINCT contract_address) as case_variants
        FROM coin_signals 
        GROUP BY LOWER(contract_address)
        HAVING COUNT(DISTINCT contract_address) > 1
    """)
    
    remaining_issues = cursor.fetchall()
    
    if remaining_issues:
        print(f"❌ Still have {len(remaining_issues)} case issues")
    else:
        print("✅ All case sensitivity issues fixed!")
    
    # Show final stats
    cursor.execute("SELECT COUNT(*) FROM coin_signals")
    total_records = cursor.fetchone()[0]
    print(f"Total records after fix: {total_records}")
    
    cursor.execute("SELECT COUNT(DISTINCT LOWER(contract_address)) FROM coin_signals")
    unique_contracts = cursor.fetchone()[0]
    print(f"Unique contracts (case-insensitive): {unique_contracts}")
    
    conn.close()

if __name__ == "__main__":
    fix_contract_case()
