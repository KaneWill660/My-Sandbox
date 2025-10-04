#!/usr/bin/env python3
"""
Script test lệnh summary cuối cùng
"""

import sqlite3
from datetime import datetime, timedelta
import sys

def safe_print(text):
    """In text an toàn với Unicode"""
    try:
        print(text)
    except UnicodeEncodeError:
        # Thay thế ký tự Unicode bằng ký tự an toàn
        safe_text = text.encode('ascii', 'replace').decode('ascii')
        print(safe_text)

def test_summary_final(chat_id, hours=24):
    """Test summary cuối cùng"""
    
    safe_print(f"TEST SUMMARY - GROUP {chat_id}")
    safe_print(f"Thoi gian: {hours} gio qua")
    safe_print("=" * 60)
    
    # Kết nối database
    conn = sqlite3.connect("coin_tracker.db")
    cursor = conn.cursor()
    
    # Tính thời gian (sử dụng UTC như bot)
    from datetime import timezone
    start_date = datetime.now(timezone.utc) - timedelta(hours=hours)
    
    # Lấy tất cả records và filter trong Python (vì SQL string comparison không đúng)
    cursor.execute('''
        SELECT contract_address, sender_id, sender_username, timestamp, price_at_signal
        FROM coin_signals 
        WHERE chat_id = ?
        ORDER BY timestamp DESC
    ''', (chat_id,))
    
    # Parse và filter timestamps
    valid_signals = []
    seen_contracts = set()
    
    for row in cursor.fetchall():
        contract_address, sender_id, sender_username, timestamp, price_at_signal = row
        
        # Parse timestamp
        try:
            if isinstance(timestamp, str):
                if '+00:00' in timestamp or 'Z' in timestamp:
                    # Có timezone info
                    dt = datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
                else:
                    # Không có timezone info, giả sử là UTC+7 (data cũ)
                    dt = datetime.fromisoformat(timestamp)
                    vietnam_tz = timezone(timedelta(hours=7))
                    dt = dt.replace(tzinfo=vietnam_tz)
                    dt = dt.astimezone(timezone.utc)
            else:
                dt = timestamp
            
            # Kiểm tra xem có trong khoảng thời gian không
            if dt >= start_date:
                # Chỉ lấy lần đầu tiên cho mỗi contract
                if contract_address not in seen_contracts:
                    valid_signals.append((contract_address, sender_id, sender_username, timestamp, price_at_signal))
                    seen_contracts.add(contract_address)
                    
        except Exception as e:
            # Nếu không parse được timestamp, bỏ qua
            continue
    
    signals = valid_signals
    conn.close()
    
    if not signals:
        if hours < 24:
            safe_print(f"Khong co keo nao trong {hours} gio qua.")
        else:
            days = hours // 24
            safe_print(f"Khong co keo nao trong {days} ngay qua.")
        return 0
    
    # Hiển thị thông tin
    safe_print(f"Tim thay {len(signals)} keo:")
    safe_print("")
    
    for i, signal in enumerate(signals, 1):
        contract = signal[0]
        sender = signal[2] or f"User_{signal[1]}"
        timestamp = signal[3]
        price_at_signal = signal[4]
        
        # Format thời gian - convert UTC sang UTC+7 để hiển thị
        if isinstance(timestamp, str):
            try:
                # Thử parse với timezone info trước
                if '+00:00' in timestamp or 'Z' in timestamp:
                    # Có timezone info, parse bình thường
                    date_obj = datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
                else:
                    # Không có timezone info, giả sử là UTC+7 (data cũ từ import)
                    date_obj = datetime.fromisoformat(timestamp)
                    # Thêm timezone UTC+7
                    vietnam_tz = timezone(timedelta(hours=7))
                    date_obj = date_obj.replace(tzinfo=vietnam_tz)
                    # Convert sang UTC
                    date_obj = date_obj.astimezone(timezone.utc)
                
                # Convert UTC sang UTC+7 để hiển thị
                vietnam_tz = timezone(timedelta(hours=7))
                local_time = date_obj.astimezone(vietnam_tz)
                time_str = local_time.strftime("%H:%M")
            except:
                time_str = "Unknown"
        else:
            # Convert UTC sang UTC+7
            vietnam_tz = timezone(timedelta(hours=7))
            local_time = timestamp.astimezone(vietnam_tz)
            time_str = local_time.strftime("%H:%M")
        
        # Lấy thông tin token hiện tại (tên và giá)
        try:
            import asyncio
            import aiohttp
            
            async def get_token_info(contract_address):
                """Lấy thông tin token từ DexScreener"""
                try:
                    async with aiohttp.ClientSession() as session:
                        url = f"https://api.dexscreener.com/latest/dex/tokens/{contract_address}"
                        async with session.get(url, timeout=10) as response:
                            if response.status == 200:
                                data = await response.json()
                                if data.get('pairs') and len(data['pairs']) > 0:
                                    pair = data['pairs'][0]
                                    return {
                                        'name': pair.get('baseToken', {}).get('name', 'Unknown'),
                                        'symbol': pair.get('baseToken', {}).get('symbol', 'UNKNOWN'),
                                        'price': float(pair.get('priceUsd', 0))
                                    }
                except Exception as e:
                    print(f"Error fetching token info: {e}")
                return {'name': 'Unknown', 'symbol': 'UNKNOWN', 'price': None}
            
            # Lấy thông tin token
            token_info = asyncio.run(get_token_info(contract))
            current_price = token_info.get('price')
            token_name = token_info.get('name', 'Unknown')
            token_symbol = token_info.get('symbol', 'UNKNOWN')
            
        except Exception as e:
            print(f"Error getting token info: {e}")
            token_name = 'Unknown'
            token_symbol = 'UNKNOWN'
            current_price = None
        
        # Format tên token
        if token_name != 'Unknown':
            token_display = f"{token_name} ({token_symbol})"
        else:
            token_display = f"Unknown ({token_symbol})"
        
        # Hiển thị thông tin cơ bản
        safe_print(f"{i}. {token_display}")
        safe_print(f"   Contract: {contract}")
        safe_print(f"   Nguoi gui: {sender}")
        safe_print(f"   Thoi gian: {time_str}")
        
        # Chỉ hiển thị giá lúc gửi nếu có
        if price_at_signal:
            price_signal_str = f"{price_at_signal:.8f}".rstrip('0').rstrip('.')
            safe_print(f"   Gia luc gui: {price_signal_str}")
        
        # Chỉ hiển thị giá hiện tại nếu có
        if current_price:
            price_current_str = f"{current_price:.8f}".rstrip('0').rstrip('.')
            safe_print(f"   Gia hien tai: {price_current_str}")
        
        # Chỉ hiển thị % thay đổi nếu có cả hai giá
        if price_at_signal and current_price:
            change_percent = ((current_price - price_at_signal) / price_at_signal) * 100
            change_emoji = "📈" if change_percent > 0 else "📉"
            safe_print(f"   Thay doi: {change_emoji} {change_percent:+.1f}%")
        
        safe_print("")
    
    return len(signals)

def main():
    """Main function"""
    if len(sys.argv) < 2:
        print("Usage: python test_summary_final.py <chat_id> [hours]")
        print("Examples:")
        print("  python test_summary_final.py -1002385574544")
        print("  python test_summary_final.py -1002385574544 1")
        print("  python test_summary_final.py -1002385574544 24")
        print("  python test_summary_final.py -1002385574544 48")
        return
    
    try:
        chat_id = int(sys.argv[1])
        hours = int(sys.argv[2]) if len(sys.argv) > 2 else 24
    except ValueError:
        print("Error: Chat ID and hours must be numbers")
        return
    
    safe_print("TESTING SUMMARY COMMAND - FINAL")
    safe_print("=" * 60)
    
    # Test summary
    count = test_summary_final(chat_id, hours)
    
    safe_print(f"KET QUA: {count} keo trong {hours} gio qua")

if __name__ == "__main__":
    main()
