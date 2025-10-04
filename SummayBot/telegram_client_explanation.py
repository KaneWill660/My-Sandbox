#!/usr/bin/env python3
"""
Script giải thích về Telegram Client API
"""

def explain_telegram_client():
    """Giải thích về Telegram Client API"""
    
    print("TELEGRAM CLIENT API - DOC TIN NHAN LICH SU")
    print("=" * 60)
    
    print("GIOI THIEU:")
    print("-" * 30)
    print("+ Telegram Client API cho phep doc tin nhan lich su")
    print("+ Can dang nhap bang tai khoan Telegram")
    print("+ Co the doc tin nhan tu bat ky group nao")
    print("+ Phuc tap hon Bot API nhung manh me hon")
    
    print()
    print("CACH HOAT DONG:")
    print("-" * 30)
    print("1. Dang nhap bang tai khoan Telegram")
    print("2. Ket noi den group")
    print("3. Doc tin nhan lich su")
    print("4. Tim contract addresses")
    print("5. Luu vao database")
    
    print()
    print("THU VIEN CAN CAI DAT:")
    print("-" * 30)
    print("pip install telethon")
    print("pip install python-dotenv")
    
    print()
    print("CAU TRUC CODE:")
    print("-" * 30)
    print("from telethon import TelegramClient")
    print("from telethon.tl.functions.messages import GetHistoryRequest")
    print()
    print("# Dang nhap")
    print("client = TelegramClient('session', api_id, api_hash)")
    print("client.start()")
    print()
    print("# Doc tin nhan")
    print("messages = client.get_messages(group_entity, limit=1000)")
    print()
    print("# Tim contract addresses")
    print("for msg in messages:")
    print("    if '0x' in msg.text:")
    print("        # Luu vao database")
    print("        pass")
    
    print()
    print("UU DIEM:")
    print("-" * 30)
    print("+ Doc duoc tin nhan lich su")
    print("+ Khong can export thu cong")
    print("+ Tu dong hoa hoan toan")
    print("+ Co the doc tu nhieu group")
    
    print()
    print("NHUOC DIEM:")
    print("-" * 30)
    print("+ Can dang nhap bang tai khoan")
    print("+ Phuc tap hon Bot API")
    print("+ Co the bi gioi han rate limit")
    print("+ Can quan ly session")
    
    print()
    print("SO SANH BOT API vs CLIENT API:")
    print("-" * 30)
    print("BOT API:")
    print("  + Don gian, de su dung")
    print("  + Khong can dang nhap")
    print("  + Chi doc duoc tin nhan moi")
    print("  + Khong doc duoc tin nhan lich su")
    print()
    print("CLIENT API:")
    print("  + Phuc tap hon")
    print("  + Can dang nhap bang tai khoan")
    print("  + Doc duoc tin nhan lich su")
    print("  + Manh me hon, nhieu tinh nang hon")

if __name__ == "__main__":
    explain_telegram_client()
