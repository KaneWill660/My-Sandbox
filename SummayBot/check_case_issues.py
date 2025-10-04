#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sqlite3

def check_case_issues():
    """Check for case sensitivity issues in contract addresses"""
    
    print("=== CHECK CASE SENSITIVITY ISSUES ===")
    
    # Kết nối database
    conn = sqlite3.connect("coin_tracker.db")
    cursor = conn.cursor()
    
    # Lấy tất cả contract addresses
    cursor.execute("""
        SELECT contract_address, COUNT(*) as count
        FROM coin_signals 
        GROUP BY contract_address
        ORDER BY contract_address
    """)
    
    all_contracts = cursor.fetchall()
    
    print(f"Total unique contract addresses: {len(all_contracts)}")
    
    # Tìm các contract có case khác nhau
    case_issues = []
    seen_lower = set()
    
    for contract, count in all_contracts:
        lower_contract = contract.lower()
        if lower_contract in seen_lower:
            case_issues.append(contract)
        else:
            seen_lower.add(lower_contract)
    
    if case_issues:
        print(f"\nFound {len(case_issues)} contracts with case issues:")
        for contract in case_issues:
            print(f"  {contract}")
    else:
        print("\nNo case issues found")
    
    # Kiểm tra cụ thể contract mà user đề cập
    print(f"\n=== CHECKING SPECIFIC CONTRACTS ===")
    
    target_contracts = [
        "0x3a08a614ceb8b2380a022e5d35873fd2d8e64444",
        "0x3a08A614ceB8b2380a022E5D35873Fd2D8e64444"
    ]
    
    for contract in target_contracts:
        cursor.execute("""
            SELECT COUNT(*) FROM coin_signals 
            WHERE contract_address = ?
        """, (contract,))
        count = cursor.fetchone()[0]
        print(f"  {contract}: {count} records")
    
    # Kiểm tra với LOWER
    cursor.execute("""
        SELECT COUNT(*) FROM coin_signals 
        WHERE LOWER(contract_address) = LOWER(?)
    """, (target_contracts[0],))
    lower_count = cursor.fetchone()[0]
    print(f"  Lowercase version: {lower_count} records")
    
    # Hiển thị tất cả contract addresses để debug
    print(f"\n=== ALL CONTRACT ADDRESSES ===")
    for i, (contract, count) in enumerate(all_contracts, 1):
        print(f"{i:2d}. {contract} (count: {count})")
        if i >= 20:  # Chỉ hiển thị 20 đầu tiên
            print("...")
            break
    
    conn.close()

if __name__ == "__main__":
    check_case_issues()
