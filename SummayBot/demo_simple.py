#!/usr/bin/env python3
"""
Demo script don gian de hien thi ket qua output cua bot
"""

def main():
    print("DEMO OUTPUT CUA BOT TELEGRAM")
    print("=" * 60)
    print()
    
    print("Khi ban go lenh: /summary")
    print("Bot se tra ve ket qua nhu sau:")
    print()
    print("-" * 60)
    
    # Demo output 1 - Co keo
    demo_output_1 = """TONG HOP KEO 1 NGAY QUA

0x1234...567890
Nguoi gui: @crypto_trader_2024
Thoi gian: 15/12/2024 14:30
Gia luc gui: $0.00012345
Gia hien tai: $0.00015678
Thay doi: +26.95%

0xabcd...ef1234
Nguoi gui: @moon_hunter
Thoi gian: 15/12/2024 16:45
Gia luc gui: $0.00056789
Gia hien tai: $0.00043210
Thay doi: -23.89%

0x9876...543210
Nguoi gui: @diamond_hands
Thoi gian: 15/12/2024 18:20
Gia luc gui: $0.00000123
Gia hien tai: $0.00000234
Thay doi: +90.24%"""
    
    print(demo_output_1)
    print()
    print("-" * 60)
    print()
    
    # Demo output 2 - Khong co keo
    print("Khi khong co keo nao trong 1 ngay:")
    print()
    demo_output_2 = "Khong co keo nao trong 1 ngay qua."
    print(demo_output_2)
    print()
    print("-" * 60)
    print()
    
    # Demo output 3 - Lenh voi tham so
    print("Khi ban go: /summary 3")
    print("Bot se hien thi keo trong 3 ngay qua:")
    print()
    
    demo_output_3 = """TONG HOP KEO 3 NGAY QUA

0x1111...222222
Nguoi gui: @whale_alert
Thoi gian: 13/12/2024 09:15
Gia luc gui: $0.00000012
Gia hien tai: $0.00000045
Thay doi: +275.00%

0x3333...444444
Nguoi gui: @pump_king
Thoi gian: 14/12/2024 11:30
Gia luc gui: $0.00023456
Gia hien tai: $0.00019876
Thay doi: -15.24%

0x5555...666666
Nguoi gui: @hodl_master
Thoi gian: 14/12/2024 20:45
Gia luc gui: $0.00000111
Gia hien tai: $0.00000111
Thay doi: +0.00%"""
    
    print(demo_output_3)
    print()
    print("-" * 60)
    print()
    
    # Demo output 4 - Lenh help
    print("Khi ban go: /help")
    print()
    
    demo_output_4 = """COIN TRACKER BOT

Cach su dung:
• Bot se tu dong theo doi cac tin nhan chua contract address (0x...)
• Go /summary de xem tong hop keo 1 ngay qua
• Go /summary 3 de xem tong hop 3 ngay qua (toi da 30 ngay)

Lenh:
• /summary [so_ngay] - Xem tong hop keo
• /help - Hien thi huong dan

Luu y:
• Bot chi theo doi contract addresses bat dau bang 0x
• Moi contract chi hien thi nguoi gui dau tien
• Gia duoc lay tu DexScreener va CoinGecko"""
    
    print(demo_output_4)
    print()
    print("-" * 60)
    print()
    
    print("DEMO XU LY TIN NHAN")
    print("=" * 60)
    print()
    
    sample_messages = [
        {
            "user": "@crypto_trader_2024",
            "message": "Check out this new token: 0x1234567890123456789012345678901234567890",
            "action": "Bot phat hien contract address va luu vao database"
        },
        {
            "user": "@moon_hunter", 
            "message": "Pump incoming! 0xabcdefabcdefabcdefabcdefabcdefabcdefabcd",
            "action": "Bot phat hien contract address va luu vao database"
        },
        {
            "user": "@hodl_master",
            "message": "Hello everyone, how are you today?",
            "action": "Khong co contract address, bot bo qua"
        },
        {
            "user": "@whale_alert",
            "message": "Multiple contracts: 0x1111111111111111111111111111111111111111 and 0x2222222222222222222222222222222222222222",
            "action": "Bot phat hien 2 contract addresses va luu ca hai"
        }
    ]
    
    for i, msg in enumerate(sample_messages, 1):
        print(f"Tin nhan {i}:")
        print(f"Nguoi gui: {msg['user']}")
        print(f"Noi dung: {msg['message']}")
        print(f"Hanh dong: {msg['action']}")
        print()
    
    print("TOM TAT:")
    print("• Bot tu dong phat hien contract addresses (0x...)")
    print("• Luu thong tin vao SQLite database")
    print("• Lay gia real-time tu API")
    print("• Tong hop keo theo lenh /summary")
    print("• Hien thi % thay doi gia tu luc gui den hien tai")
    print("• Moi contract chi hien thi nguoi gui dau tien")

if __name__ == "__main__":
    main()
