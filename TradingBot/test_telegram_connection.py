#!/usr/bin/env python3
"""
Test Telegram bot connection
"""

import requests
import os

def test_telegram():
    """Test Telegram bot connection"""
    
    # Read bot token from .env file
    bot_token = ''
    chat_id = '@tradingbotbykane'
    
    try:
        with open('.env', 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if line.startswith('TELEGRAM_BOT_TOKEN='):
                    bot_token = line.split('=', 1)[1].strip()
                    break
    except Exception as e:
        print(f"Error reading .env file: {e}")
        return False
    
    print(f"Bot Token: {'*' * 20 if bot_token else 'NOT SET'}")
    print(f"Chat ID: {chat_id}")
    
    if not bot_token:
        print("\n❌ TELEGRAM_BOT_TOKEN not found in .env file")
        print("Please create .env file with:")
        print("TELEGRAM_BOT_TOKEN=8221353087:AAGm5quJTf6tpFk7_j5B8otV6fTAu0xNCPk")
        return False
    
    # Test message
    message = """
🧪 <b>TELEGRAM CONNECTION TEST</b> 🧪

✅ Bot is working correctly!
📱 Telegram notifications enabled

⏰ <b>Test time:</b> {time}

🤖 <i>Scalping Methods Bot</i>""".format(time="30/09/2025 21:00:00")
    
    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    data = {
        'chat_id': chat_id,
        'text': message,
        'parse_mode': 'HTML'
    }
    
    try:
        response = requests.post(url, data=data, timeout=10)
        
        if response.status_code == 200:
            result = response.json()
            if result.get('ok'):
                print("✅ Telegram message sent successfully!")
                print(f"Message ID: {result['result']['message_id']}")
                return True
            else:
                print(f"❌ Telegram API error: {result}")
                return False
        else:
            print(f"❌ HTTP Error {response.status_code}: {response.text}")
            
            # Try to get more details about the error
            try:
                error_data = response.json()
                if 'description' in error_data:
                    print(f"Error description: {error_data['description']}")
                    
                    # Common solutions
                    if "chat not found" in error_data['description'].lower():
                        print("\n💡 Solution: Bot chưa được thêm vào kênh @tradingbotbykane")
                        print("1. Tạo kênh @tradingbotbykane trên Telegram")
                        print("2. Thêm bot vào kênh với quyền admin")
                        print("3. Gửi tin nhắn test trong kênh")
                    elif "bot was blocked" in error_data['description'].lower():
                        print("\n💡 Solution: Bot bị block")
                        print("1. Unblock bot trên Telegram")
                        print("2. Thử lại")
                        
            except:
                pass
                
            return False
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Failed to send Telegram message: {e}")
        return False

if __name__ == "__main__":
    print("🧪 Testing Telegram Bot Connection...")
    print("=" * 50)
    test_telegram()

