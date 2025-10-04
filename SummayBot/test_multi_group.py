#!/usr/bin/env python3
"""
Script test bot với nhiều group
"""

import sqlite3
from datetime import datetime, timedelta

def test_group_separation():
    """Test xem bot có phân biệt group không"""
    
    print("TEST PHAN BIET GROUP")
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
    
    # Test lấy kèo từ từng group
    for chat_id in chat_ids:
        chat_id = chat_id[0]
        
        # Đếm kèo trong 24h qua
        yesterday = datetime.now() - timedelta(days=1)
        cursor.execute("""
            SELECT COUNT(*) FROM coin_signals 
            WHERE chat_id = ? AND timestamp >= ?
        """, (chat_id, yesterday.isoformat()))
        
        count = cursor.fetchone()[0]
        
        print(f"Group {chat_id}: {count} keo trong 24h qua")
        
        # Lấy 1 kèo mẫu
        cursor.execute("""
            SELECT contract_address, sender_username, timestamp
            FROM coin_signals 
            WHERE chat_id = ?
            ORDER BY timestamp DESC 
            LIMIT 1
        """, (chat_id,))
        
        sample = cursor.fetchone()
        if sample:
            print(f"  - Keo gan nhat: {sample[0][:20]}...")
            print(f"  - Nguoi gui: {sample[1]}")
            print(f"  - Thoi gian: {sample[2]}")
        print()
    
    conn.close()
    
    print("HUONG DAN THEM BOT VAO GROUP THU 2:")
    print("-" * 40)
    print("1. Vao group thu 2")
    print("2. Nhan vao ten group -> Edit -> Add Members")
    print("3. Tim bot cua ban va them vao")
    print("4. Cap quyen Admin cho bot:")
    print("   - Vao group settings")
    print("   - Chon bot -> Admin rights")
    print("   - Bat 'Delete messages' va 'Read messages'")
    print("5. Gui tin nhan test:")
    print("   'Test contract: 0x1234567890123456789012345678901234567890'")
    print("6. Chay lai script nay de kiem tra")

def simulate_summary_command(chat_id):
    """Mô phỏng lệnh summary cho group cụ thể"""
    
    print(f"\nMO PHONG LENH /summary CHO GROUP {chat_id}")
    print("=" * 50)
    
    conn = sqlite3.connect("coin_tracker.db")
    cursor = conn.cursor()
    
    # Lấy kèo trong 24h qua cho group này
    yesterday = datetime.now() - timedelta(days=1)
    cursor.execute("""
        SELECT contract_address, sender_username, timestamp, price_at_signal
        FROM coin_signals 
        WHERE chat_id = ? AND timestamp >= ?
        ORDER BY timestamp DESC
    """, (chat_id, yesterday.isoformat()))
    
    signals = cursor.fetchall()
    
    if not signals:
        print(f"Khong co keo nao trong group {chat_id}")
        return
    
    print(f"Co {len(signals)} keo trong group {chat_id}:")
    print()
    
    for i, signal in enumerate(signals, 1):
        contract, sender, timestamp, price = signal
        print(f"{i}. Contract: {contract[:30]}...")
        print(f"   Nguoi gui: {sender}")
        print(f"   Thoi gian: {timestamp}")
        print(f"   Gia: {price}")
        print()
    
    conn.close()

if __name__ == "__main__":
    test_group_separation()
    
    # Test summary cho group hiện tại
    conn = sqlite3.connect("coin_tracker.db")
    cursor = conn.cursor()
    cursor.execute("SELECT DISTINCT chat_id FROM coin_signals")
    chat_ids = cursor.fetchall()
    conn.close()
    
    if chat_ids:
        simulate_summary_command(chat_ids[0][0])
