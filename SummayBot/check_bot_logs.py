#!/usr/bin/env python3
"""
Script kiểm tra log bot
"""

import os
import glob
from datetime import datetime

def check_bot_logs():
    """Kiểm tra log bot"""
    
    print("KIEM TRA LOG BOT")
    print("=" * 50)
    
    # Tìm file log
    log_files = glob.glob("*.log")
    
    if log_files:
        print(f"Tim thay {len(log_files)} file log:")
        for log_file in log_files:
            print(f"  - {log_file}")
        
        # Đọc log file gần nhất
        latest_log = max(log_files, key=os.path.getmtime)
        print(f"\nDoc log file gan nhat: {latest_log}")
        
        try:
            with open(latest_log, 'r', encoding='utf-8') as f:
                lines = f.readlines()
                
            print(f"Co {len(lines)} dong log")
            
            # Hiển thị 10 dòng cuối
            print("\n10 dong log gan nhat:")
            for line in lines[-10:]:
                print(f"  {line.strip()}")
                
        except Exception as e:
            print(f"Loi doc file log: {e}")
    else:
        print("Khong tim thay file log nao")
    
    print()
    print("HUONG DAN FIX:")
    print("-" * 30)
    print("1. Kiem tra bot co trong group moi khong")
    print("2. Cap quyen Admin cho bot")
    print("3. Gui tin nhan test chua contract address")
    print("4. Go lenh /summary de kiem tra")
    print("5. Neu van khong co, kiem tra log bot")
    print("6. Restart bot neu can thiet")

if __name__ == "__main__":
    check_bot_logs()
