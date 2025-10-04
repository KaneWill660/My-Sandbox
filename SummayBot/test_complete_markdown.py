#!/usr/bin/env python3
"""
Script test bot hoàn chỉnh với Markdown format
"""

import sqlite3
from datetime import datetime, timedelta

def test_complete_markdown():
    """Test bot hoàn chỉnh với Markdown format"""
    
    print("TEST BOT HOAN CHINH - MARKDOWN FORMAT")
    print("=" * 60)
    
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
    
    # Tạo summary message với Markdown format
    summary_text = "**TONG HOP KEO 24 GIO QUA**\n"
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
        summary_text += f"**{i}. Token Name (SYMBOL)**\n"
        summary_text += f"Contract: `{contract}`\n"
        summary_text += f"Nguoi gui: {sender}\n"
        summary_text += f"Thoi gian: {time_str}\n"
        summary_text += f"Gia luc gui: {price_str}\n"
        summary_text += f"Gia hien tai: $0.001456\n"
        summary_text += f"Thay doi: +18.0%\n\n"
    
    summary_text += "Tin nhan nay se tu dong xoa sau 1 phut"
    
    print("SUMMARY MESSAGE (MARKDOWN FORMAT):")
    print("-" * 40)
    print(summary_text)
    print()
    
    print("TINH NANG DA HOAN THIEN:")
    print("-" * 40)
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
    print("-" * 40)
    print("1. Them bot vao group va cap quyen Admin")
    print("2. Gui tin nhan chua contract address (0x...)")
    print("3. Go lenh /summary [so_gio] de xem keo")
    print("4. Click vao contract address de copy")
    print("5. Paste vao DexScreener de tim token")
    print("6. Bot se tu dong xoa tin nhan sau 1 phut")
    
    print()
    print("VI DU LENH:")
    print("-" * 40)
    print("/summary        - Xem keo 24h qua")
    print("/summary 2      - Xem keo 2h qua")
    print("/summary 48     - Xem keo 48h qua")
    print("/help           - Xem huong dan")
    
    conn.close()

if __name__ == "__main__":
    test_complete_markdown()
