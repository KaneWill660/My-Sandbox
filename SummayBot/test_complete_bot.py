#!/usr/bin/env python3
"""
Script test bot hoàn chỉnh với format mới
"""

import sqlite3
from datetime import datetime, timedelta

def test_complete_bot():
    """Test bot hoàn chỉnh với format mới"""
    
    print("TEST BOT HOAN CHINH")
    print("=" * 50)
    
    # Kết nối database
    conn = sqlite3.connect("coin_tracker.db")
    cursor = conn.cursor()
    
    # Lấy tất cả kèo trong 24h qua
    yesterday = datetime.now() - timedelta(days=1)
    cursor.execute("""
        SELECT contract_address, sender_username, timestamp, price_at_signal
        FROM coin_signals 
        WHERE timestamp >= ?
        ORDER BY timestamp DESC
    """, (yesterday.isoformat(),))
    
    signals = cursor.fetchall()
    
    if not signals:
        print("Khong co keo nao trong 24h qua")
        return
    
    print(f"Co {len(signals)} keo trong 24h qua:")
    print()
    
    # Tạo summary message
    summary_text = "TONG HOP KEO 24 GIO QUA\n"
    summary_text += "Group: Test Group\n\n"
    
    for i, signal in enumerate(signals, 1):
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
        
        # Tạo entry cho mỗi token
        summary_text += f"{i}. **Token Name** (SYMBOL)\n"
        summary_text += f"Contract: `{contract}`\n"
        summary_text += f"Nguoi gui: {sender}\n"
        summary_text += f"Thoi gian: {time_str}\n"
        summary_text += f"Gia luc gui: {price_str}\n"
        summary_text += f"Gia hien tai: $0.001456\n"
        summary_text += f"Thay doi: +18.0%\n\n"
    
    summary_text += "Tin nhan nay se tu dong xoa sau 1 phut"
    
    print("SUMMARY MESSAGE:")
    print("-" * 30)
    print(summary_text)
    print()
    
    print("TINH NANG MOI:")
    print("-" * 30)
    print("+ Contract address co the click va copy")
    print("+ Hien thi trong o vuong (code format)")
    print("+ Tu dong xoa tin nhan sau 1 phut")
    print("+ Phan biet group (moi group chi hien thi keo cua rieng group do)")
    print("+ Hien thi ten group trong summary")
    
    conn.close()

if __name__ == "__main__":
    test_complete_bot()
