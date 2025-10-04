#!/usr/bin/env python3
"""
Hướng dẫn export chat history và import vào database
"""

def export_import_guide():
    """Hướng dẫn export chat history và import vào database"""
    
    print("HUONG DAN EXPORT CHAT HISTORY VA IMPORT VAO DATABASE")
    print("=" * 70)
    
    print("BUOC 1: EXPORT CHAT HISTORY")
    print("-" * 40)
    print("1. Cai dat Telegram Desktop:")
    print("   + Tai ve tu: https://desktop.telegram.org/")
    print("   + Dang nhap bang tai khoan Telegram cua ban")
    print()
    print("2. Export chat history:")
    print("   + Vao group can export")
    print("   + Click vao ten group (o dau chat)")
    print("   + Chon 'Export chat history'")
    print("   + Chon cac tuy chon:")
    print("     * Format: JSON")
    print("     * Date range: All time")
    print("     * Media: Khong can (chi can text)")
    print("   + Click 'Export'")
    print("   + Download file JSON")
    
    print()
    print("BUOC 2: CHUAN BI FILE JSON")
    print("-" * 40)
    print("File JSON se co cau truc nhu sau:")
    print("""{
  "name": "Group Name",
  "type": "supergroup", 
  "id": -1001234567890,
  "messages": [
    {
      "id": 123,
      "date": "2025-10-03T10:30:00",
      "from": "username",
      "text": "Check this token: 0x1234567890123456789012345678901234567890"
    }
  ]
}""")
    
    print()
    print("BUOC 3: IMPORT VAO DATABASE")
    print("-" * 40)
    print("1. Dat file JSON vao cung thu muc voi bot")
    print("2. Chay script import:")
    print("   python import_chat_history.py")
    print("3. Bot se tu dong:")
    print("   + Doc file JSON")
    print("   + Tim contract addresses (0x...)")
    print("   + Luu vao database")
    print("   + Hien thi ket qua")
    
    print()
    print("BUOC 4: KIEM TRA KET QUA")
    print("-" * 40)
    print("1. Chay script kiem tra:")
    print("   python check_imported_data.py")
    print("2. Go lenh /summary trong group")
    print("3. Bot se hien thi keo tu tin nhan lich su")
    
    print()
    print("LUU Y QUAN TRONG:")
    print("-" * 40)
    print("+ Chi lam 1 lan khi bat dau su dung bot")
    print("+ Sau do bot se tu dong doc tin nhan moi")
    print("+ Khong can export lai")
    print("+ Bot se ket hop du lieu cu va moi")

if __name__ == "__main__":
    export_import_guide()
