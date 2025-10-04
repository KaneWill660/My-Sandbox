#!/usr/bin/env python3
"""
Script test lệnh summary từ command line
"""

import sqlite3
import asyncio
import aiohttp
from datetime import datetime, timezone, timedelta
import sys

class TestSummaryCMD:
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
        
        # Sử dụng local time để so sánh với database
        start_date = datetime.now() - timedelta(hours=hours)
        
        cursor.execute('''
            SELECT cs1.contract_address, cs1.sender_id, cs1.sender_username, 
                   cs1.timestamp, cs1.price_at_signal
            FROM coin_signals cs1
            INNER JOIN (
                SELECT contract_address, MIN(timestamp) as first_time
                FROM coin_signals 
                WHERE timestamp >= ? AND chat_id = ?
                GROUP BY contract_address
            ) cs2 ON cs1.contract_address = cs2.contract_address 
                   AND cs1.timestamp = cs2.first_time
            WHERE cs1.chat_id = ?
            ORDER BY cs1.timestamp DESC
        ''', (start_date.isoformat(), chat_id, chat_id))
        
        signals = cursor.fetchall()
        conn.close()
        
        # Chuyển đổi thành dict
        results = []
        for signal in signals:
            results.append({
                'contract_address': signal[0],
                'sender_id': signal[1],
                'sender_username': signal[2],
                'timestamp': signal[3],
                'price_at_signal': signal[4]
            })
        
        return results
    
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
            if hours < 24:
                print(f"Khong co keo nao trong {hours} gio qua.")
            else:
                days = hours // 24
                print(f"Khong co keo nao trong {days} ngay qua.")
            return
        
        # Tạo summary message
        if hours < 24:
            summary_text = f"TONG HOP KEO {hours} GIO QUA\n"
        else:
            days = hours // 24
            summary_text = f"TONG HOP KEO {days} NGAY QUA\n"
        
        summary_text += f"Group: Test Group\n\n"
        
        # Tạo danh sách
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
            
            # Tạo entry
            summary_text += f"{i}. {token_display}\n"
            summary_text += f"Contract: {contract}\n"
            summary_text += f"Nguoi gui: {sender}\n"
            summary_text += f"Thoi gian: {time_str}\n"
            summary_text += f"Gia luc gui: {self.format_price(price_at_signal)}\n"
            summary_text += f"Gia hien tai: {self.format_price(current_price)}\n"
            summary_text += f"Thay doi: {price_info}\n\n"
        
        summary_text += "Tin nhan nay se tu dong xoa sau 1 phut"
        
        # Hiển thị kết quả
        print(summary_text)
        
        # Kiểm tra độ dài
        message_length = len(summary_text)
        print(f"\nDo dai tin nhan: {message_length} ky tu")
        
        if message_length > 4000:
            chunks = (message_length + 3999) // 4000
            print(f"Se chia thanh {chunks} tin nhan")
        
        return len(signals)

def main():
    """Main function"""
    if len(sys.argv) < 2:
        print("Usage: python test_summary_cmd.py <chat_id> [hours]")
        print("Examples:")
        print("  python test_summary_cmd.py -1002385574544")
        print("  python test_summary_cmd.py -1002385574544 1")
        print("  python test_summary_cmd.py -1002385574544 24")
        print("  python test_summary_cmd.py -1002385574544 48")
        return
    
    try:
        chat_id = int(sys.argv[1])
        hours = int(sys.argv[2]) if len(sys.argv) > 2 else 24
    except ValueError:
        print("Error: Chat ID and hours must be numbers")
        return
    
    test = TestSummaryCMD()
    
    print("TESTING SUMMARY COMMAND")
    print("=" * 60)
    
    # Test summary
    count = asyncio.run(test.test_summary(chat_id, hours))
    
    print(f"\nKET QUA: {count} keo trong {hours} gio qua")

if __name__ == "__main__":
    main()
