#!/usr/bin/env python3
"""
Demo script để hiển thị kết quả output của bot
"""

def demo_summary_output():
    """Demo kết quả lệnh /summary"""
    
    print("DEMO OUTPUT CUA BOT TELEGRAM")
    print("=" * 60)
    print()
    
    print("Khi ban go lenh: /summary")
    print("Bot se tra ve ket qua nhu sau:")
    print()
    print("-" * 60)
    
    # Demo output 1 - Có kèo
    demo_output_1 = """📊 **TỔNG HỢP KÈO 1 NGÀY QUA**

🪙 **0x1234...567890**
👤 Người gửi: @crypto_trader_2024
⏰ Thời gian: 15/12/2024 14:30
💰 Giá lúc gửi: $0.00012345
💰 Giá hiện tại: $0.00015678
📊 Thay đổi: 📈 +26.95%

🪙 **0xabcd...ef1234**
👤 Người gửi: @moon_hunter
⏰ Thời gian: 15/12/2024 16:45
💰 Giá lúc gửi: $0.00056789
💰 Giá hiện tại: $0.00043210
📊 Thay đổi: 📉 -23.89%

🪙 **0x9876...543210**
👤 Người gửi: @diamond_hands
⏰ Thời gian: 15/12/2024 18:20
💰 Giá lúc gửi: $0.00000123
💰 Giá hiện tại: $0.00000234
📊 Thay đổi: 📈 +90.24%"""
    
    print(demo_output_1)
    print()
    print("─" * 60)
    print()
    
    # Demo output 2 - Không có kèo
    print("📱 Khi không có kèo nào trong 1 ngày:")
    print()
    demo_output_2 = "Không có kèo nào trong 1 ngày qua."
    print(demo_output_2)
    print()
    print("─" * 60)
    print()
    
    # Demo output 3 - Lệnh với tham số
    print("📱 Khi bạn gõ: /summary 3")
    print("Bot sẽ hiển thị kèo trong 3 ngày qua:")
    print()
    
    demo_output_3 = """📊 **TỔNG HỢP KÈO 3 NGÀY QUA**

🪙 **0x1111...222222**
👤 Người gửi: @whale_alert
⏰ Thời gian: 13/12/2024 09:15
💰 Giá lúc gửi: $0.00000012
💰 Giá hiện tại: $0.00000045
📊 Thay đổi: 📈 +275.00%

🪙 **0x3333...444444**
👤 Người gửi: @pump_king
⏰ Thời gian: 14/12/2024 11:30
💰 Giá lúc gửi: $0.00023456
💰 Giá hiện tại: $0.00019876
📊 Thay đổi: 📉 -15.24%

🪙 **0x5555...666666**
👤 Người gửi: @hodl_master
⏰ Thời gian: 14/12/2024 20:45
💰 Giá lúc gửi: $0.00000111
💰 Giá hiện tại: $0.00000111
📊 Thay đổi: 📊 +0.00%"""
    
    print(demo_output_3)
    print()
    print("─" * 60)
    print()
    
    # Demo output 4 - Lệnh help
    print("📱 Khi bạn gõ: /help")
    print()
    
    demo_output_4 = """🤖 **COIN TRACKER BOT**

**Cách sử dụng:**
• Bot sẽ tự động theo dõi các tin nhắn chứa contract address (0x...)
• Gõ `/summary` để xem tổng hợp kèo 1 ngày qua
• Gõ `/summary 3` để xem tổng hợp 3 ngày qua (tối đa 30 ngày)

**Lệnh:**
• `/summary [số_ngày]` - Xem tổng hợp kèo
• `/help` - Hiển thị hướng dẫn

**Lưu ý:**
• Bot chỉ theo dõi contract addresses bắt đầu bằng 0x
• Mỗi contract chỉ hiển thị người gửi đầu tiên
• Giá được lấy từ DexScreener và CoinGecko"""
    
    print(demo_output_4)
    print()
    print("─" * 60)
    print()

def demo_message_processing():
    """Demo cách bot xử lý tin nhắn"""
    
    print("🔍 DEMO XỬ LÝ TIN NHẮN")
    print("=" * 60)
    print()
    
    sample_messages = [
        {
            "user": "@crypto_trader_2024",
            "message": "Check out this new token: 0x1234567890123456789012345678901234567890",
            "action": "✅ Bot phát hiện contract address và lưu vào database"
        },
        {
            "user": "@moon_hunter", 
            "message": "Pump incoming! 🚀 0xabcdefabcdefabcdefabcdefabcdefabcdefabcd",
            "action": "✅ Bot phát hiện contract address và lưu vào database"
        },
        {
            "user": "@hodl_master",
            "message": "Hello everyone, how are you today?",
            "action": "❌ Không có contract address, bot bỏ qua"
        },
        {
            "user": "@whale_alert",
            "message": "Multiple contracts: 0x1111111111111111111111111111111111111111 and 0x2222222222222222222222222222222222222222",
            "action": "✅ Bot phát hiện 2 contract addresses và lưu cả hai"
        }
    ]
    
    for i, msg in enumerate(sample_messages, 1):
        print(f"📨 Tin nhắn {i}:")
        print(f"👤 Người gửi: {msg['user']}")
        print(f"💬 Nội dung: {msg['message']}")
        print(f"🤖 Hành động: {msg['action']}")
        print()

def demo_database_structure():
    """Demo cấu trúc database"""
    
    print("🗄️ DEMO CẤU TRÚC DATABASE")
    print("=" * 60)
    print()
    
    print("📊 Bảng coin_signals:")
    print("┌────┬──────────────────────────────────────────┬──────────┬─────────────────┬─────────────┬─────────────────────┬─────────────────┐")
    print("│ ID │ Contract Address                         │ Sender   │ Username        │ Timestamp   │ Price at Signal     │ Created At      │")
    print("├────┼──────────────────────────────────────────┼──────────┼─────────────────┼─────────────┼─────────────────────┼─────────────────┤")
    print("│ 1  │ 0x1234567890123456789012345678901234567890 │ 12345    │ crypto_trader   │ 15/12 14:30 │ 0.00012345          │ 15/12 14:30:15  │")
    print("│ 2  │ 0xabcdefabcdefabcdefabcdefabcdefabcdefabcd │ 67890    │ moon_hunter     │ 15/12 16:45 │ 0.00056789          │ 15/12 16:45:22  │")
    print("│ 3  │ 0x9876543210987654321098765432109876543210 │ 11111    │ diamond_hands   │ 15/12 18:20 │ 0.00000123          │ 15/12 18:20:33  │")
    print("└────┴──────────────────────────────────────────┴──────────┴─────────────────┴─────────────┴─────────────────────┴─────────────────┘")
    print()
    
    print("🔍 Query để lấy kèo 1 ngày qua:")
    print("SELECT contract_address, sender_username, timestamp, price_at_signal")
    print("FROM coin_signals")
    print("WHERE timestamp >= datetime('now', '-1 day')")
    print("GROUP BY contract_address")
    print("ORDER BY MIN(timestamp) DESC;")
    print()

def main():
    """Hàm main"""
    demo_summary_output()
    print("\n" + "=" * 60 + "\n")
    demo_message_processing()
    print("\n" + "=" * 60 + "\n")
    demo_database_structure()
    
    print("🎯 TÓM TẮT:")
    print("• Bot tự động phát hiện contract addresses (0x...)")
    print("• Lưu thông tin vào SQLite database")
    print("• Lấy giá real-time từ API")
    print("• Tổng hợp kèo theo lệnh /summary")
    print("• Hiển thị % thay đổi giá từ lúc gửi đến hiện tại")
    print("• Mỗi contract chỉ hiển thị người gửi đầu tiên")

if __name__ == "__main__":
    main()
