#!/usr/bin/env python3
"""
Hướng dẫn hoàn chỉnh lấy chat_id của group
"""

def chat_id_guide_complete():
    """Hướng dẫn hoàn chỉnh lấy chat_id của group"""
    
    print("HUONG DAN HOAN CHINH - LAY CHAT_ID CUA GROUP")
    print("=" * 60)
    
    print("PHUONG PHAP 1: SU DUNG BOT (KHUYEN NGHI)")
    print("-" * 40)
    print("1. Them bot vao group")
    print("2. Cap quyen Admin cho bot")
    print("3. Go lenh /chatid trong group")
    print("4. Bot se hien thi chat_id")
    print("5. Chat_id se tu dong xoa sau 1 phut")
    
    print()
    print("PHUONG PHAP 2: TU FILE JSON EXPORT")
    print("-" * 40)
    print("1. Export chat history tu Telegram Desktop")
    print("2. Mo file JSON")
    print("3. Tim field 'id' trong file:")
    print("""{
  "name": "Group Name",
  "type": "supergroup",
  "id": -1001234567890,  <-- Day la chat_id
  "messages": [...]
}""")
    print("4. Chat_id se co dang: -1001234567890")
    
    print()
    print("PHUONG PHAP 3: TU DATABASE")
    print("-" * 40)
    print("1. Chay script:")
    print("   python find_chat_id_simple.py")
    print("2. Script se hien thi tat ca chat_id da co")
    print("3. Su dung chat_id phu hop")
    
    print()
    print("PHUONG PHAP 4: TU BOT LOG")
    print("-" * 40)
    print("1. Them bot vao group")
    print("2. Cap quyen Admin cho bot")
    print("3. Gui tin nhan trong group")
    print("4. Bot se log chat_id trong console")
    print("5. Chat_id se hien thi trong log")
    
    print()
    print("PHUONG PHAP 5: TU TELEGRAM API")
    print("-" * 40)
    print("1. Su dung @userinfobot")
    print("2. Forward tin nhan tu group den @userinfobot")
    print("3. Bot se hien thi thong tin group")
    print("4. Chat_id se hien thi trong ket qua")
    
    print()
    print("DINH DANG CHAT_ID:")
    print("-" * 40)
    print("+ Group: -1001234567890")
    print("+ Channel: -1001234567890")
    print("+ Private chat: 123456789")
    print("+ Bot chat: 123456789")
    
    print()
    print("LUU Y:")
    print("-" * 40)
    print("+ Chat_id cua group luon bat dau bang -100")
    print("+ Chat_id cua channel luon bat dau bang -100")
    print("+ Chat_id cua private chat la so duong")
    print("+ Chat_id cua bot chat la so duong")
    
    print()
    print("SU DUNG CHAT_ID:")
    print("-" * 40)
    print("1. Mo file import_chat_history.py")
    print("2. Thay doi chat_id:")
    print("   chat_id = -1001234567890  # Chat ID cua group")
    print("3. Luu file")
    print("4. Chay script import")
    
    print()
    print("KHUYEN NGHI:")
    print("-" * 40)
    print("+ Su dung phuong phap 1 (bot /chatid) - nhanh nhat")
    print("+ Su dung phuong phap 2 (file JSON) - chinh xac nhat")
    print("+ Su dung phuong phap 3 (database) - de kiem tra")
    print("+ Su dung phuong phap 4 (bot log) - khi can debug")
    print("+ Su dung phuong phap 5 (API) - khi khong co bot")

if __name__ == "__main__":
    chat_id_guide_complete()
