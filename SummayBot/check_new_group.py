#!/usr/bin/env python3
"""
Script kiểm tra group mới
"""

import sqlite3
from datetime import datetime, timedelta

def check_new_group():
    """Kiểm tra group mới"""
    
    print("KIEM TRA GROUP MOI")
    print("=" * 50)
    
    # Kết nối database
    conn = sqlite3.connect("coin_tracker.db")
    cursor = conn.cursor()
    
    # Lấy tất cả group
    cursor.execute("SELECT DISTINCT chat_id FROM coin_signals")
    chat_ids = cursor.fetchall()
    
    print(f"Bot hien tai co {len(chat_ids)} group:")
    for chat_id in chat_ids:
        print(f"  - Group ID: {chat_id[0]}")
    
    print()
    
    # Kiểm tra tin nhắn gần đây
    yesterday = datetime.now() - timedelta(days=1)
    cursor.execute("""
        SELECT chat_id, COUNT(*) as count, MAX(timestamp) as latest
        FROM coin_signals 
        WHERE timestamp >= ?
        GROUP BY chat_id
    """, (yesterday.isoformat(),))
    
    recent = cursor.fetchall()
    
    if recent:
        print("TIN NHAN GAN DAY (24h qua):")
        for chat_id, count, latest in recent:
            print(f"  Group {chat_id}: {count} tin nhan, gan nhat: {latest}")
    else:
        print("Khong co tin nhan nao trong 24h qua")
    
    print()
    print("HUONG DAN FIX:")
    print("-" * 30)
    print("1. Kiem tra bot co trong group moi khong")
    print("2. Cap quyen Admin cho bot")
    print("3. Gui tin nhan test chua contract address")
    print("4. Go lenh /summary de kiem tra")
    print("5. Neu van khong co, kiem tra log bot")
    
    conn.close()

if __name__ == "__main__":
    check_new_group()
