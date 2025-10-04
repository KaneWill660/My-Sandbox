#!/usr/bin/env python3
"""
Hướng dẫn từng bước export chat history và import vào database
"""

def step_by_step_guide():
    """Hướng dẫn từng bước export chat history và import vào database"""
    
    print("HUONG DAN TUNG BUOC - EXPORT CHAT HISTORY VA IMPORT")
    print("=" * 70)
    
    print("BUOC 1: CAI DAT TELEGRAM DESKTOP")
    print("-" * 40)
    print("1. Truy cap: https://desktop.telegram.org/")
    print("2. Tai ve va cai dat Telegram Desktop")
    print("3. Dang nhap bang tai khoan Telegram cua ban")
    print("4. Dang nhap vao group can export")
    
    print()
    print("BUOC 2: EXPORT CHAT HISTORY")
    print("-" * 40)
    print("1. Vao group can export")
    print("2. Click vao ten group (o dau chat)")
    print("3. Chon 'Export chat history'")
    print("4. Chon cac tuy chon:")
    print("   - Format: JSON")
    print("   - Date range: All time")
    print("   - Media: Khong can (chi can text)")
    print("5. Click 'Export'")
    print("6. Download file JSON")
    print("7. Dat file JSON vao cung thu muc voi bot")
    
    print()
    print("BUOC 3: CHINH SUA SCRIPT IMPORT")
    print("-" * 40)
    print("1. Mo file import_chat_history.py")
    print("2. Thay doi cac tham so:")
    print("   - json_file = 'ten_file_cua_ban.json'")
    print("   - chat_id = -1001234567890  # Chat ID cua group")
    print("3. Luu file")
    
    print()
    print("BUOC 4: CHAY SCRIPT IMPORT")
    print("-" * 40)
    print("1. Mo Command Prompt")
    print("2. Di chuyen den thu muc bot:")
    print("   cd E:\\MySandbox\\SummayBot")
    print("3. Chay script import:")
    print("   python import_chat_history.py")
    print("4. Kiem tra ket qua")
    
    print()
    print("BUOC 5: KIEM TRA DU LIEU")
    print("-" * 40)
    print("1. Chay script kiem tra:")
    print("   python check_imported_data.py")
    print("2. Kiem tra so luong tin nhan da import")
    print("3. Kiem tra tin nhan theo ngay")
    
    print()
    print("BUOC 6: TEST BOT")
    print("-" * 40)
    print("1. Khoi dong bot:")
    print("   python telegram_coin_tracker_bot.py")
    print("2. Vao group va go lenh /summary")
    print("3. Bot se hien thi keo tu tin nhan lich su")
    print("4. Bot se tu dong doc tin nhan moi")
    
    print()
    print("LUU Y QUAN TRONG:")
    print("-" * 40)
    print("+ Chi lam 1 lan khi bat dau su dung bot")
    print("+ Sau do bot se tu dong doc tin nhan moi")
    print("+ Khong can export lai")
    print("+ Bot se ket hop du lieu cu va moi")
    print("+ Chat ID co the tim thay trong file JSON")
    
    print()
    print("TRO GIUP:")
    print("-" * 40)
    print("+ Neu gap loi, kiem tra file JSON co dung format khong")
    print("+ Kiem tra chat_id co dung khong")
    print("+ Kiem tra bot co quyen doc tin nhan khong")
    print("+ Kiem tra database co duoc tao khong")

if __name__ == "__main__":
    step_by_step_guide()
