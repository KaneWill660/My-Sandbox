#!/usr/bin/env python3
"""
Script kiểm tra dữ liệu đã import
"""

import sqlite3
from datetime import datetime, timedelta

def check_imported_data():
    """Kiểm tra dữ liệu đã import"""
    
    print("KIEM TRA DU LIEU DA IMPORT")
    print("=" * 50)
    
    conn = sqlite3.connect("coin_tracker.db")
    cursor = conn.cursor()
    
    # Lấy tất cả group
    cursor.execute("SELECT DISTINCT chat_id FROM coin_signals")
    chat_ids = cursor.fetchall()
    
    print(f"Bot hien tai co {len(chat_ids)} group:")
    for chat_id in chat_ids:
        print(f"  - Group ID: {chat_id[0]}")
    
    print()
    
    # Kiểm tra tin nhắn theo thời gian
    for chat_id in chat_ids:
        chat_id = chat_id[0]
        
        # Đếm tin nhắn theo ngày
        cursor.execute("""
            SELECT DATE(timestamp) as date, COUNT(*) as count
            FROM coin_signals 
            WHERE chat_id = ?
            GROUP BY DATE(timestamp)
            ORDER BY date DESC
            LIMIT 7
        """, (chat_id,))
        
        daily_counts = cursor.fetchall()
        
        print(f"Group {chat_id} - Tin nhan theo ngay (7 ngay gan nhat):")
        for date, count in daily_counts:
            print(f"  {date}: {count} tin nhan")
        
        # Lấy tin nhắn gần nhất
        cursor.execute("""
            SELECT contract_address, sender_username, timestamp
            FROM coin_signals 
            WHERE chat_id = ?
            ORDER BY timestamp DESC 
            LIMIT 5
        """, (chat_id,))
        
        recent = cursor.fetchall()
        
        print(f"\\n5 tin nhan gan nhat:")
        for contract, sender, timestamp in recent:
            print(f"  {timestamp}: {sender} - {contract[:20]}...")
        
        print()
    
    conn.close()
    
    print("HUONG DAN SU DUNG:")
    print("-" * 30)
    print("1. Go lenh /summary trong group")
    print("2. Bot se hien thi keo tu tin nhan lich su")
    print("3. Bot se tu dong doc tin nhan moi")

if __name__ == "__main__":
    check_imported_data()
