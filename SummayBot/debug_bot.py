#!/usr/bin/env python3
"""
Script debug để kiểm tra bot hoạt động trong nhiều group
"""

import sqlite3
from datetime import datetime, timedelta

def check_bot_activity():
    """Kiểm tra hoạt động của bot trong các group"""
    
    print("KIEM TRA HOAT DONG BOT")
    print("=" * 50)
    
    # Kết nối database
    conn = sqlite3.connect("coin_tracker.db")
    cursor = conn.cursor()
    
    # Lấy danh sách tất cả group
    cursor.execute("SELECT DISTINCT chat_id FROM coin_signals")
    chat_ids = cursor.fetchall()
    
    print(f"Bot da hoat dong trong {len(chat_ids)} group(s):")
    print()
    
    for chat_id in chat_ids:
        chat_id = chat_id[0]
        
        # Đếm số tin nhắn trong group này
        cursor.execute("SELECT COUNT(*) FROM coin_signals WHERE chat_id = ?", (chat_id,))
        count = cursor.fetchone()[0]
        
        # Lấy tin nhắn gần nhất
        cursor.execute("""
            SELECT timestamp, sender_username, contract_address 
            FROM coin_signals 
            WHERE chat_id = ? 
            ORDER BY timestamp DESC 
            LIMIT 1
        """, (chat_id,))
        
        latest = cursor.fetchone()
        
        print(f"Group ID: {chat_id}")
        print(f"   So tin nhan: {count}")
        if latest:
            print(f"   Tin nhan gan nhat: {latest[0]}")
            print(f"   Nguoi gui: {latest[1]}")
            print(f"   Contract: {latest[2][:20]}...")
        print()
    
    conn.close()
    
    print("HUONG DAN FIX:")
    print("-" * 30)
    print("1. Kiem tra bot co quyen Admin trong group thu 2")
    print("2. Dam bao bot duoc them dung cach")
    print("3. Gui tin nhan chua contract address (0x...) trong group thu 2")
    print("4. Kiem tra log bot de xem co loi gi khong")
    print()
    
    print("CAC BUOC KIEM TRA:")
    print("-" * 30)
    print("1. Vao group thu 2")
    print("2. Kiem tra bot co trong danh sach thanh vien")
    print("3. Cap quyen Admin cho bot")
    print("4. Gui tin nhan: 'Test contract: 0x1234567890123456789012345678901234567890'")
    print("5. Chay lai script nay de kiem tra")

def check_recent_activity():
    """Kiểm tra hoạt động gần đây"""
    
    print("\nHOAT DONG GAN DAY (24h qua)")
    print("=" * 50)
    
    conn = sqlite3.connect("coin_tracker.db")
    cursor = conn.cursor()
    
    # Lấy tin nhắn trong 24h qua
    yesterday = datetime.now() - timedelta(days=1)
    cursor.execute("""
        SELECT chat_id, timestamp, sender_username, contract_address
        FROM coin_signals 
        WHERE timestamp >= ?
        ORDER BY timestamp DESC
    """, (yesterday.isoformat(),))
    
    recent = cursor.fetchall()
    
    if recent:
        print(f"Co {len(recent)} tin nhan trong 24h qua:")
        print()
        
        for row in recent:
            chat_id, timestamp, sender, contract = row
            print(f"Group: {chat_id}")
            print(f"   {timestamp}")
            print(f"   {sender}")
            print(f"   {contract[:30]}...")
            print()
    else:
        print("Khong co hoat dong nao trong 24h qua")
        print("   Bot co the da dung hoac khong nhan duoc tin nhan")
    
    conn.close()

if __name__ == "__main__":
    check_bot_activity()
    check_recent_activity()
