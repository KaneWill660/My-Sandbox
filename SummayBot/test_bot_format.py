#!/usr/bin/env python3
"""
Script test bot với format mới
"""

import sqlite3
from datetime import datetime, timedelta

def test_bot_format():
    """Test bot với format contract address mới"""
    
    print("TEST BOT FORMAT MOI")
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
    
    print("KEO GAN NHAT:")
    print("-" * 30)
    print(f"Contract: {contract}")
    print(f"Nguoi gui: {sender}")
    print(f"Thoi gian: {timestamp}")
    print(f"Gia: {price}")
    print()
    
    print("FORMAT MOI (co the click va copy):")
    print("-" * 30)
    new_format = f"""1. **Token Name** (SYMBOL)
Contract: `{contract}`
Nguoi gui: {sender}
Thoi gian: {timestamp}
Gia luc gui: ${price}
Gia hien tai: $0.001456
Thay doi: +18.0%"""
    
    print(new_format)
    print()
    
    print("HUONG DAN SU DUNG:")
    print("-" * 30)
    print("1. Trong Telegram, contract address se hien thi trong o vuong")
    print("2. Click vao contract address se copy vao clipboard")
    print("3. Paste vao DexScreener hoac DEX khac de tim token")
    print("4. Bot se tu dong xoa tin nhan sau 1 phut")
    
    conn.close()

if __name__ == "__main__":
    test_bot_format()
