#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sqlite3
import os

def clear_database():
    """Clear toàn bộ database hiện tại"""
    
    db_path = "coin_tracker.db"
    
    if not os.path.exists(db_path):
        print(f"Database {db_path} không tồn tại!")
        return
    
    # Kết nối database
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    try:
        # Lấy thông tin trước khi xóa
        cursor.execute("SELECT COUNT(*) FROM coin_signals")
        count_before = cursor.fetchone()[0]
        
        print(f"=== CLEAR DATABASE ===")
        print(f"Database: {db_path}")
        print(f"So records hien tai: {count_before}")
        
        if count_before == 0:
            print("Database da trong, khong can clear!")
            conn.close()
            return
        
        # Xác nhận từ user
        confirm = input(f"\nBan co chac chan muon xoa {count_before} records? (yes/no): ")
        
        if confirm.lower() not in ['yes', 'y', 'có', 'co']:
            print("Huy bo thao tac clear database!")
            conn.close()
            return
        
        # Xóa tất cả records
        cursor.execute("DELETE FROM coin_signals")
        
        # Reset auto-increment counter
        cursor.execute("DELETE FROM sqlite_sequence WHERE name='coin_signals'")
        
        conn.commit()
        
        # Kiểm tra kết quả
        cursor.execute("SELECT COUNT(*) FROM coin_signals")
        count_after = cursor.fetchone()[0]
        
        print(f"\nDa clear database thanh cong!")
        print(f"So records sau khi clear: {count_after}")
        
        # Hiển thị thông tin database
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = cursor.fetchall()
        print(f"\nCac bang con lai trong database:")
        for table in tables:
            print(f"- {table[0]}")
        
    except Exception as e:
        print(f"Loi khi clear database: {e}")
        conn.rollback()
    
    finally:
        conn.close()

def clear_database_force():
    """Clear database mà không cần xác nhận (dùng cho script tự động)"""
    
    db_path = "coin_tracker.db"
    
    if not os.path.exists(db_path):
        print(f"Database {db_path} không tồn tại!")
        return
    
    # Kết nối database
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    try:
        # Lấy thông tin trước khi xóa
        cursor.execute("SELECT COUNT(*) FROM coin_signals")
        count_before = cursor.fetchone()[0]
        
        print(f"=== CLEAR DATABASE (FORCE) ===")
        print(f"Database: {db_path}")
        print(f"So records hien tai: {count_before}")
        
        if count_before == 0:
            print("Database da trong!")
            conn.close()
            return
        
        # Xóa tất cả records
        cursor.execute("DELETE FROM coin_signals")
        
        # Reset auto-increment counter
        cursor.execute("DELETE FROM sqlite_sequence WHERE name='coin_signals'")
        
        conn.commit()
        
        # Kiểm tra kết quả
        cursor.execute("SELECT COUNT(*) FROM coin_signals")
        count_after = cursor.fetchone()[0]
        
        print(f"Da clear database thanh cong!")
        print(f"So records sau khi clear: {count_after}")
        
    except Exception as e:
        print(f"Loi khi clear database: {e}")
        conn.rollback()
    
    finally:
        conn.close()

def show_database_info():
    """Hiển thị thông tin database hiện tại"""
    
    db_path = "coin_tracker.db"
    
    if not os.path.exists(db_path):
        print(f"Database {db_path} không tồn tại!")
        return
    
    # Kết nối database
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    try:
        print(f"=== DATABASE INFO ===")
        print(f"Database: {db_path}")
        print(f"Kich thuoc file: {os.path.getsize(db_path)} bytes")
        
        # Đếm records
        cursor.execute("SELECT COUNT(*) FROM coin_signals")
        total_count = cursor.fetchone()[0]
        print(f"Tong so records: {total_count}")
        
        if total_count > 0:
            # Thống kê theo chat_id
            cursor.execute("""
                SELECT chat_id, COUNT(*) as count 
                FROM coin_signals 
                GROUP BY chat_id 
                ORDER BY count DESC
            """)
            chat_stats = cursor.fetchall()
            
            print(f"\nThong ke theo group:")
            for chat_id, count in chat_stats:
                print(f"- Chat ID {chat_id}: {count} records")
            
            # Thống kê theo ngày
            cursor.execute("""
                SELECT DATE(timestamp) as date, COUNT(*) as count 
                FROM coin_signals 
                GROUP BY DATE(timestamp) 
                ORDER BY date DESC 
                LIMIT 10
            """)
            date_stats = cursor.fetchall()
            
            print(f"\nThong ke theo ngay (10 ngay gan nhat):")
            for date, count in date_stats:
                print(f"- {date}: {count} records")
        
        # Hiển thị cấu trúc bảng
        cursor.execute("PRAGMA table_info(coin_signals)")
        columns = cursor.fetchall()
        
        print(f"\nCau truc bang coin_signals:")
        for col in columns:
            print(f"- {col[1]} ({col[2]})")
        
    except Exception as e:
        print(f"Loi khi doc thong tin database: {e}")
    
    finally:
        conn.close()

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1:
        command = sys.argv[1].lower()
        
        if command == "force":
            clear_database_force()
        elif command == "info":
            show_database_info()
        else:
            print("Usage: python clear_database.py [force|info]")
            print("  force: Clear database mà không cần xác nhận")
            print("  info:  Hiển thị thông tin database")
            print("  (no args): Clear database với xác nhận")
    else:
        clear_database()
