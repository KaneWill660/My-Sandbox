#!/usr/bin/env python3
"""
Script đơn giản để tìm chat_id
"""

import sqlite3

def find_chat_id_from_database():
    """Tìm chat_id từ database"""
    
    print("TIM CHAT_ID TU DATABASE")
    print("=" * 40)
    
    try:
        conn = sqlite3.connect("coin_tracker.db")
        cursor = conn.cursor()
        
        # Lấy tất cả chat_id
        cursor.execute("SELECT DISTINCT chat_id FROM coin_signals")
        chat_ids = cursor.fetchall()
        
        if chat_ids:
            print("Cac chat_id da co trong database:")
            for chat_id in chat_ids:
                print(f"  - {chat_id[0]}")
        else:
            print("Khong co chat_id nao trong database")
            print("Hay them bot vao group va gui tin nhan truoc")
        
        conn.close()
        
    except Exception as e:
        print(f"Loi: {e}")

if __name__ == "__main__":
    find_chat_id_from_database()
