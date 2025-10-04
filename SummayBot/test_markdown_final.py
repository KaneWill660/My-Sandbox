#!/usr/bin/env python3
"""
Script test Markdown format hoàn chỉnh cho bot
"""

import sqlite3
from datetime import datetime, timedelta

def test_markdown_final():
    """Test Markdown format hoàn chỉnh cho bot"""
    
    print("TEST MARKDOWN FORMAT HOAN CHINH")
    print("=" * 50)
    
    # Kết nối database
    conn = sqlite3.connect("coin_tracker.db")
    cursor = conn.cursor()
    
    # Lấy kèo gần nhất
    cursor.execute("""
        SELECT contract_address, sender_username, timestamp, price_at_signal
        FROM coin_signals 
        ORDER BY timestamp DESC 
        LIMIT 1
    """)
    
    signal = cursor.fetchone()
    
    if not signal:
        print("Khong co keo nao trong database")
        return
    
    contract, sender, timestamp, price = signal
    
    # Format thời gian
    if isinstance(timestamp, str):
        try:
            timestamp = datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
            time_str = timestamp.strftime('%d/%m/%Y %H:%M')
        except:
            time_str = timestamp
    else:
        time_str = timestamp.strftime('%d/%m/%Y %H:%M')
    
    # Format giá
    price_str = f"${price}" if price else "N/A"
    
    # Tạo summary message với Markdown format
    summary_text = f"""**TONG HOP KEO 24 GIO QUA**
Group: Test Group

**1. Token Name (SYMBOL)**
Contract: `{contract}`
Nguoi gui: {sender}
Thoi gian: {time_str}
Gia luc gui: {price_str}
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
    
    print("SUMMARY MESSAGE (MARKDOWN FORMAT):")
    print("-" * 40)
    print(summary_text)
    print()
    
    print("TINH NANG MARKDOWN:")
    print("-" * 40)
    print("+ **Bold text** - Ten token va so thu tu")
    print("+ `Code format` - Contract address co the click va copy")
    print("+ Tu dong xoa sau 1 phut")
    print("+ Phan biet group")
    print("+ Format gia thong minh")
    print("+ Tinh % thay doi gia")
    
    print()
    print("HUONG DAN SU DUNG:")
    print("-" * 40)
    print("1. Trong Telegram, contract address se hien thi trong o vuong")
    print("2. Click vao contract address se copy vao clipboard")
    print("3. Paste vao DexScreener hoac DEX khac de tim token")
    print("4. Bot se tu dong xoa tin nhan sau 1 phut")
    print("5. Moi group chi hien thi keo cua rieng group do")
    
    conn.close()

if __name__ == "__main__":
    test_markdown_final()
