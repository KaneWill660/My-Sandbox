#!/usr/bin/env python3
"""
Script test summary với dữ liệu đã import
"""

import sqlite3
import asyncio
import aiohttp
from datetime import datetime, timezone, timedelta

class TestSummary:
    def __init__(self, db_path="coin_tracker.db"):
        self.db_path = db_path
        self.price_apis = {
            'dexscreener': 'https://api.dexscreener.com/latest/dex/tokens/',
            'coingecko': 'https://api.coingecko.com/api/v3/simple/token_price/ethereum'
        }
    
    async def get_token_info(self, contract_address: str):
        """Lấy thông tin token từ DexScreener"""
        try:
            async with aiohttp.ClientSession() as session:
                url = f"{self.price_apis['dexscreener']}{contract_address}"
                async with session.get(url) as response:
                    if response.status == 200:
                        data = await response.json()
                        if data.get('pairs') and len(data['pairs']) > 0:
                            # Lấy pair có liquidity cao nhất
                            best_pair = max(data['pairs'], key=lambda x: float(x.get('liquidity', {}).get('usd', 0)))
                            return {
                                'name': best_pair.get('baseToken', {}).get('name', 'Unknown'),
                                'symbol': best_pair.get('baseToken', {}).get('symbol', 'UNKNOWN'),
                                'price': float(best_pair.get('priceUsd', 0))
                            }
        except Exception as e:
            print(f"Loi lay thong tin token {contract_address}: {e}")
        
        return {'name': 'Unknown', 'symbol': 'UNKNOWN', 'price': 0}
    
    def get_coin_signals(self, chat_id, hours=24):
        """Lấy coin signals từ database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Tính thời gian bắt đầu
        start_date = datetime.now(timezone.utc) - timedelta(hours=hours)
        
        # Lấy signals từ database
        cursor.execute('''
            SELECT contract_address, sender_username, sender_id, timestamp, price_at_signal
            FROM coin_signals 
            WHERE chat_id = ? AND timestamp >= ?
            ORDER BY timestamp ASC
        ''', (chat_id, start_date.isoformat()))
        
        signals = cursor.fetchall()
        conn.close()
        
        # Chuyển đổi thành dict và loại bỏ duplicate
        unique_signals = {}
        for signal in signals:
            contract = signal[0]
            if contract not in unique_signals:
                unique_signals[contract] = {
                    'contract_address': contract,
                    'sender_username': signal[1],
                    'sender_id': signal[2],
                    'timestamp': signal[3],
                    'price_at_signal': signal[4]
                }
        
        return list(unique_signals.values())
    
    def format_price(self, price):
        """Format giá cho dễ đọc"""
        if price is None or price == 0:
            return "N/A"
        
        if price >= 1:
            return f"${price:.4f}"
        elif price >= 0.01:
            return f"${price:.6f}"
        elif price >= 0.0001:
            return f"${price:.8f}"
        else:
            return f"${price:.2e}"
    
    async def test_summary(self, chat_id, hours=24):
        """Test summary cho group"""
        print(f"TEST SUMMARY - GROUP {chat_id}")
        print(f"Thoi gian: {hours} gio qua")
        print("=" * 60)
        
        # Lấy signals
        signals = self.get_coin_signals(chat_id, hours)
        
        if not signals:
            print("Khong co keo nao trong thoi gian nay!")
            return
        
        print(f"Tim thay {len(signals)} keo:")
        print()
        
        # Xử lý từng signal
        for i, signal in enumerate(signals, 1):
            contract = signal['contract_address']
            sender = signal['sender_username'] or f"User_{signal['sender_id']}"
            timestamp = signal['timestamp']
            price_at_signal = signal['price_at_signal']
            
            # Lấy thông tin token
            token_info = await self.get_token_info(contract)
            current_price = token_info.get('price')
            token_name = token_info.get('name', 'Unknown')
            token_symbol = token_info.get('symbol', 'UNKNOWN')
            
            # Format tên token
            if token_name != 'Unknown':
                token_display = f"{token_name} ({token_symbol})"
            else:
                token_display = f"Unknown ({token_symbol})"
            
            # Xử lý giá
            if not price_at_signal and current_price:
                price_at_signal = current_price
                price_info = "Gia hien tai"
            elif price_at_signal and current_price:
                change_percent = ((current_price - price_at_signal) / price_at_signal) * 100
                price_info = f"{change_percent:+.1f}%"
            else:
                price_info = "N/A"
            
            # Format thời gian
            if isinstance(timestamp, str):
                try:
                    date_obj = datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
                    time_str = date_obj.strftime("%H:%M")
                except:
                    time_str = "Unknown"
            else:
                time_str = timestamp.strftime("%H:%M")
            
            # Hiển thị kết quả
            print(f"{i}. {token_display}")
            print(f"   Contract: {contract}")
            print(f"   Nguoi gui: {sender} ({time_str})")
            print(f"   Gia luc gui: {self.format_price(price_at_signal)}")
            print(f"   Gia hien tai: {self.format_price(current_price)}")
            print(f"   Thay doi: {price_info}")
            print()

if __name__ == "__main__":
    test = TestSummary()
    
    # Test với group đã import
    chat_id = -1002385574544
    
    print("TESTING BOT SUMMARY WITH IMPORTED DATA")
    print("=" * 60)
    
    # Test 24 giờ
    asyncio.run(test.test_summary(chat_id, 24))
    
    print("\n" + "=" * 60)
    
    # Test 48 giờ
    asyncio.run(test.test_summary(chat_id, 48))
