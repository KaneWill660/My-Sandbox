#!/usr/bin/env python3
"""
Script test lệnh summary đơn giản
"""

import sqlite3
from datetime import datetime, timedelta
import sys

def test_summary_simple(chat_id, hours=24):
    """Test summary đơn giản"""
    
    print(f"TEST SUMMARY - GROUP {chat_id}")
    print(f"Thoi gian: {hours} gio qua")
    print("=" * 60)
    
    # Kết nối database
    conn = sqlite3.connect("coin_tracker.db")
    cursor = conn.cursor()
    
    # Tính thời gian
    start_date = datetime.now() - timedelta(hours=hours)
    
    # Lấy signals
    cursor.execute('''
        SELECT cs1.contract_address, cs1.sender_id, cs1.sender_username, 
               cs1.timestamp, cs1.price_at_signal
        FROM coin_signals cs1
        INNER JOIN (
            SELECT contract_address, MIN(timestamp) as first_time
            FROM coin_signals 
            WHERE timestamp >= ? AND chat_id = ?
            GROUP BY contract_address
        ) cs2 ON cs1.contract_address = cs2.contract_address 
               AND cs1.timestamp = cs2.first_time
        WHERE cs1.chat_id = ?
        ORDER BY cs1.timestamp DESC
    ''', (start_date.isoformat(), chat_id, chat_id))
    
    signals = cursor.fetchall()
    conn.close()
    
    if not signals:
        if hours < 24:
            print(f"Khong co keo nao trong {hours} gio qua.")
        else:
            days = hours // 24
            print(f"Khong co keo nao trong {days} ngay qua.")
        return 0
    
    # Tạo summary
    if hours < 24:
        summary_text = f"TONG HOP KEO {hours} GIO QUA\n"
    else:
        days = hours // 24
        summary_text = f"TONG HOP KEO {days} NGAY QUA\n"
    
    summary_text += f"Group: Test Group\n\n"
    
    # Tạo danh sách
    for i, signal in enumerate(signals, 1):
        contract = signal[0]
        sender = signal[2] or f"User_{signal[1]}"
        timestamp = signal[3]
        price_at_signal = signal[4]
        
        # Format thời gian
        if isinstance(timestamp, str):
            try:
                date_obj = datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
                time_str = date_obj.strftime("%H:%M")
            except:
                time_str = "Unknown"
        else:
            time_str = timestamp.strftime("%H:%M")
        
        # Tạo entry
        summary_text += f"{i}. Contract: {contract[:20]}...\n"
        summary_text += f"   Nguoi gui: {sender}\n"
        summary_text += f"   Thoi gian: {time_str}\n"
        summary_text += f"   Gia luc gui: {price_at_signal or 'N/A'}\n\n"
    
    summary_text += "Tin nhan nay se tu dong xoa sau 1 phut"
    
    # Hiển thị kết quả
    print(summary_text)
    
    # Kiểm tra độ dài
    message_length = len(summary_text)
    print(f"\nDo dai tin nhan: {message_length} ky tu")
    
    if message_length > 4000:
        chunks = (message_length + 3999) // 4000
        print(f"Se chia thanh {chunks} tin nhan")
    
    return len(signals)

def main():
    """Main function"""
    if len(sys.argv) < 2:
        print("Usage: python test_summary_simple.py <chat_id> [hours]")
        print("Examples:")
        print("  python test_summary_simple.py -1002385574544")
        print("  python test_summary_simple.py -1002385574544 1")
        print("  python test_summary_simple.py -1002385574544 24")
        print("  python test_summary_simple.py -1002385574544 48")
        return
    
    try:
        chat_id = int(sys.argv[1])
        hours = int(sys.argv[2]) if len(sys.argv) > 2 else 24
    except ValueError:
        print("Error: Chat ID and hours must be numbers")
        return
    
    print("TESTING SUMMARY COMMAND - SIMPLE")
    print("=" * 60)
    
    # Test summary
    count = test_summary_simple(chat_id, hours)
    
    print(f"\nKET QUA: {count} keo trong {hours} gio qua")

if __name__ == "__main__":
    main()
