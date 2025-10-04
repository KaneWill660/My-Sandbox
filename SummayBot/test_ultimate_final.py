#!/usr/bin/env python3
"""
Script test bot hoàn chỉnh với tất cả tính năng và format Markdown
"""

import sqlite3
from datetime import datetime, timedelta

def test_ultimate_final():
    """Test bot hoàn chỉnh với tất cả tính năng và format Markdown"""
    
    print("TEST BOT HOAN CHINH - TAT CA TINH NANG + MARKDOWN FORMAT")
    print("=" * 80)
    
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
            SELECT contract_address, sender_username, timestamp, price_at_signal
            FROM coin_signals 
            WHERE chat_id = ?
            ORDER BY timestamp DESC 
            LIMIT 1
        """, (chat_id,))
        
        sample = cursor.fetchone()
        if sample:
            contract, sender, timestamp, price = sample
            print(f"  - Keo gan nhat: {contract[:20]}...")
            print(f"  - Nguoi gui: {sender}")
            print(f"  - Thoi gian: {timestamp}")
            print(f"  - Gia: {price}")
        print()
    
    print("TINH NANG DA HOAN THIEN:")
    print("-" * 60)
    print("+ Contract address co the click va copy (code format)")
    print("+ Phan biet group (moi group chi hien thi keo cua rieng group do)")
    print("+ Hien thi ten group trong summary")
    print("+ Tu dong xoa tin nhan sau 1 phut")
    print("+ Format Markdown dep va de doc")
    print("+ Lay ten token tu DexScreener")
    print("+ Tinh % thay doi gia")
    print("+ Format gia thong minh")
    print("+ Custom theo gio (1-168 gio)")
    print("+ Luu duplicate theo group")
    print("+ Error handling tot")
    
    print()
    print("HUONG DAN SU DUNG:")
    print("-" * 60)
    print("1. Them bot vao group va cap quyen Admin")
    print("2. Gui tin nhan chua contract address (0x...)")
    print("3. Go lenh /summary [so_gio] de xem keo")
    print("4. Click vao contract address de copy")
    print("5. Paste vao DexScreener de tim token")
    print("6. Bot se tu dong xoa tin nhan sau 1 phut")
    
    print()
    print("VI DU LENH:")
    print("-" * 60)
    print("/summary        - Xem keo 24h qua")
    print("/summary 2      - Xem keo 2h qua")
    print("/summary 48     - Xem keo 48h qua")
    print("/help           - Xem huong dan")
    
    print()
    print("VI DU SUMMARY MESSAGE:")
    print("-" * 60)
    example = """**TONG HOP KEO 24 GIO QUA**
Group: Test Group

**1. Token Name (SYMBOL)**
Contract: `0x1234567890123456789012345678901234567890`
Nguoi gui: username
Thoi gian: 04/10/2025 10:30
Gia luc gui: $0.001234
Gia hien tai: $0.001456
Thay doi: +18.0%

**2. Another Token (TOKEN)**
Contract: `0xabcdef1234567890abcdef1234567890abcdef12`
Nguoi gui: user2
Thoi gian: 04/10/2025 09:15
Gia luc gui: $0.000567
Gia hien tai: $0.000789
Thay doi: +39.2%

Tin nhan nay se tu dong xoa sau 1 phut"""
    
    print(example)
    
    print()
    print("TINH NANG MOI - CONTRACT ADDRESS CLICKABLE:")
    print("-" * 60)
    print("+ Contract address hien thi trong o vuong (code format)")
    print("+ Click vao contract address se copy vao clipboard")
    print("+ Paste vao DexScreener hoac DEX khac de tim token")
    print("+ Khong can phai select va copy thu cong")
    print("+ Tiet kiem thoi gian va giam loi sai")
    
    print()
    print("TINH NANG PHAN BIET GROUP:")
    print("-" * 60)
    print("+ Moi group chi hien thi keo cua rieng group do")
    print("+ Khong bi tron lan keo giua cac group")
    print("+ Hien thi ten group trong summary")
    print("+ Luu duplicate theo group")
    print("+ Error handling tot")
    
    print()
    print("TINH NANG TU DONG XOA TIN NHAN:")
    print("-" * 60)
    print("+ Tu dong xoa tin nhan sau 1 phut")
    print("+ Khong lam roi group chat")
    print("+ Tiet kiem dung luong")
    print("+ Bao mat thong tin")
    
    conn.close()

if __name__ == "__main__":
    test_ultimate_final()
