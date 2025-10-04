import asyncio
import re
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Optional
import aiohttp
import sqlite3
from telegram import Update, Bot
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
from telegram import ParseMode
import json

# Cấu hình logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

class CoinTrackerBot:
    def __init__(self, bot_token: str):
        self.bot_token = bot_token
        self.db_path = "coin_tracker.db"
        self.init_database()
        
        # Regex để detect contract addresses
        self.contract_pattern = re.compile(r'0x[a-fA-F0-9]{40}')
        
        # API endpoints cho giá coin
        self.price_apis = {
            'coingecko': 'https://api.coingecko.com/api/v3/simple/token_price/ethereum',
            'dexscreener': 'https://api.dexscreener.com/latest/dex/tokens/'
        }
    
    def init_database(self):
        """Khởi tạo database SQLite"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS coin_signals (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                contract_address TEXT NOT NULL,
                sender_id INTEGER NOT NULL,
                sender_username TEXT,
                message_id INTEGER NOT NULL,
                chat_id INTEGER NOT NULL,
                timestamp DATETIME NOT NULL,
                price_at_signal REAL,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        
        cursor.execute('''
            CREATE INDEX IF NOT EXISTS idx_contract_address ON coin_signals(contract_address);
        ''')
        
        cursor.execute('''
            CREATE INDEX IF NOT EXISTS idx_timestamp ON coin_signals(timestamp);
        ''')
        
        conn.commit()
        conn.close()
    
    async def get_token_info(self, contract_address: str) -> Dict:
        """Lấy thông tin token từ DexScreener (tên và giá)"""
        try:
            # Thử DexScreener API trước (tốt cho các token mới)
            async with aiohttp.ClientSession() as session:
                url = f"{self.price_apis['dexscreener']}{contract_address}"
                async with session.get(url) as response:
                    if response.status == 200:
                        data = await response.json()
                        if data.get('pairs') and len(data['pairs']) > 0:
                            # Lấy pair có liquidity cao nhất
                            best_pair = max(data['pairs'], key=lambda x: float(x.get('liquidity', {}).get('usd', 0)))
                            
                            # Lấy thông tin token
                            base_token = best_pair.get('baseToken', {})
                            token_name = base_token.get('name', 'Unknown')
                            token_symbol = base_token.get('symbol', 'UNKNOWN')
                            price = float(best_pair.get('priceUsd', 0))
                            
                            return {
                                'name': token_name,
                                'symbol': token_symbol,
                                'price': price,
                                'source': 'dexscreener'
                            }
            
            # Fallback: Thử CoinGecko API (chỉ lấy giá)
            async with aiohttp.ClientSession() as session:
                url = f"{self.price_apis['coingecko']}?contract_addresses={contract_address}&vs_currencies=usd"
                async with session.get(url) as response:
                    if response.status == 200:
                        data = await response.json()
                        if contract_address.lower() in data:
                            price = float(data[contract_address.lower()]['usd'])
                            return {
                                'name': 'Unknown',
                                'symbol': 'UNKNOWN',
                                'price': price,
                                'source': 'coingecko'
                            }
        
        except Exception as e:
            logger.error(f"Error getting token info for {contract_address}: {e}")
        
        return {
            'name': 'Unknown',
            'symbol': 'UNKNOWN',
            'price': None,
            'source': 'none'
        }
    
    async def get_token_price(self, contract_address: str) -> Optional[float]:
        """Lấy giá token hiện tại (backward compatibility)"""
        token_info = await self.get_token_info(contract_address)
        return token_info.get('price')
    
    def save_coin_signal(self, contract_address: str, sender_id: int, sender_username: str, 
                        message_id: int, chat_id: int, timestamp: datetime, price: Optional[float]):
        """Lưu thông tin kèo vào database - chỉ lưu lần sớm nhất cho mỗi contract"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Convert contract address về lowercase để tránh duplicate do case sensitivity
        contract_address = contract_address.lower()
        
        # Kiểm tra xem contract này đã tồn tại trong group này chưa
        cursor.execute('''
            SELECT id, timestamp FROM coin_signals 
            WHERE LOWER(contract_address) = ? AND chat_id = ?
        ''', (contract_address, chat_id))
        
        existing = cursor.fetchone()
        
        if existing:
            # Đã tồn tại, kiểm tra xem lần này có sớm hơn không
            existing_id, existing_timestamp = existing
            
            # So sánh timestamp (UTC)
            if isinstance(timestamp, str):
                try:
                    new_timestamp = datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
                except:
                    # Nếu không parse được, không lưu
                    conn.close()
                    return
            else:
                new_timestamp = timestamp
            
            if isinstance(existing_timestamp, str):
                try:
                    existing_timestamp = datetime.fromisoformat(existing_timestamp.replace('Z', '+00:00'))
                except:
                    # Nếu không parse được existing timestamp, lưu mới
                    pass
            
            # Nếu timestamp mới sớm hơn, cập nhật
            if new_timestamp < existing_timestamp:
                cursor.execute('''
                    UPDATE coin_signals 
                    SET sender_id = ?, sender_username = ?, message_id = ?, 
                        timestamp = ?, price_at_signal = ?
                    WHERE id = ?
                ''', (sender_id, sender_username, message_id, timestamp, price, existing_id))
                conn.commit()
                print(f"Updated signal for contract {contract_address} with earlier timestamp")
            else:
                print(f"Contract {contract_address} already exists with earlier timestamp, skipping")
            
            conn.close()
            return
        
        # Chưa tồn tại, lưu mới
        cursor.execute('''
            INSERT INTO coin_signals 
            (contract_address, sender_id, sender_username, message_id, chat_id, timestamp, price_at_signal)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (contract_address, sender_id, sender_username, message_id, chat_id, timestamp, price))
        
        conn.commit()
        conn.close()
        print(f"Saved new signal for contract {contract_address} from user {sender_username}")
    
    
    def format_price(self, price: float) -> str:
        """Format giá một cách thông minh - hiển thị đủ số có nghĩa"""
        if price is None or price == 0:
            return "N/A"
        
        # Nếu giá >= 1, hiển thị 2-4 chữ số thập phân
        if price >= 1:
            return f"${price:.4f}".rstrip('0').rstrip('.')
        
        # Nếu giá < 1, tìm số chữ số có nghĩa đầu tiên
        price_str = f"{price:.15f}"
        
        # Tìm vị trí chữ số khác 0 đầu tiên sau dấu phẩy
        decimal_part = price_str.split('.')[1]
        first_non_zero = 0
        for i, char in enumerate(decimal_part):
            if char != '0':
                first_non_zero = i
                break
        
        # Hiển thị từ chữ số có nghĩa đầu tiên + 4 chữ số nữa
        significant_digits = first_non_zero + 4
        
        # Giới hạn tối đa 8 chữ số thập phân
        significant_digits = min(significant_digits, 8)
        
        formatted = f"${price:.{significant_digits}f}".rstrip('0').rstrip('.')
        
        # Nếu quá dài (>12 ký tự), rút gọn
        if len(formatted) > 12:
            # Hiển thị dạng scientific notation cho số rất nhỏ
            if price < 0.000001:
                return f"${price:.2e}"
            else:
                # Rút gọn bằng cách bỏ bớt số 0 cuối
                return f"${price:.6f}".rstrip('0').rstrip('.')
        
        return formatted
    
    def schedule_message_deletion(self, update: Update, messages: List, delay: int = 60):
        """Lên lịch xóa tin nhắn sau một khoảng thời gian"""
        import threading
        import time
        
        def delete_messages():
            time.sleep(delay)  # Đợi delay giây
            try:
                for msg in messages:
                    if msg and msg.message_id:
                        update.message.bot.delete_message(
                            chat_id=update.message.chat_id,
                            message_id=msg.message_id
                        )
            except Exception as e:
                logger.error(f"Error deleting messages: {e}")
        
        # Chạy trong thread riêng để không block bot
        thread = threading.Thread(target=delete_messages)
        thread.daemon = True
        thread.start()
    
    def get_coin_signals(self, hours: int = 24, chat_id: int = None) -> List[Dict]:
        """Lấy danh sách kèo trong khoảng thời gian (theo giờ) cho group cụ thể"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Sử dụng UTC time để so sánh với database
        from datetime import timezone
        start_date = datetime.now(timezone.utc) - timedelta(hours=hours)
        
        # Lấy tất cả records và filter trong Python (vì SQL string comparison không đúng)
        if chat_id:
            cursor.execute('''
                SELECT contract_address, sender_id, sender_username, timestamp, price_at_signal
                FROM coin_signals 
                WHERE chat_id = ?
                ORDER BY timestamp DESC
            ''', (chat_id,))
        else:
            cursor.execute('''
                SELECT contract_address, sender_id, sender_username, timestamp, price_at_signal
                FROM coin_signals 
                ORDER BY timestamp DESC
            ''')
        
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
                        valid_signals.append({
                            'contract_address': contract_address,
                            'sender_id': sender_id,
                            'sender_username': sender_username,
                            'timestamp': timestamp,
                            'price_at_signal': price_at_signal,
                            'first_signal_time': timestamp
                        })
                        seen_contracts.add(contract_address)
                        
            except Exception as e:
                # Nếu không parse được timestamp, bỏ qua
                continue
        
        results = valid_signals
        
        conn.close()
        return results
    
    def process_message(self, update: Update, context: CallbackContext):
        """Xử lý tin nhắn để tìm contract addresses"""
        if not update.message or not update.message.text:
            return
        
        message_text = update.message.text
        contract_addresses = self.contract_pattern.findall(message_text)
        
        if not contract_addresses:
            return
        
        # Lấy giá hiện tại cho mỗi contract
        for contract in contract_addresses:
            # Sử dụng asyncio.run để chạy async function
            current_price = asyncio.run(self.get_token_price(contract))
            
            # Lưu thông tin kèo (sử dụng UTC time)
            from datetime import timezone
            utc_timestamp = update.message.date.replace(tzinfo=timezone.utc)
            
            self.save_coin_signal(
                contract_address=contract,
                sender_id=update.message.from_user.id,
                sender_username=update.message.from_user.username or update.message.from_user.first_name,
                message_id=update.message.message_id,
                chat_id=update.message.chat_id,
                timestamp=utc_timestamp,
                price=current_price
            )
            
            logger.info(f"Saved signal for contract {contract} from user {update.message.from_user.username}")
    
    def summary_command(self, update: Update, context: CallbackContext):
        """Xử lý lệnh /summary"""
        # Parse arguments (mặc định 24 giờ)
        hours = 24
        if context.args and len(context.args) > 0:
            try:
                hours = int(context.args[0])
                hours = max(1, min(hours, 168))  # Giới hạn từ 1-168 giờ (7 ngày)
            except ValueError:
                hours = 24
        
        # Lấy danh sách kèo từ group hiện tại
        current_chat_id = update.message.chat_id
        signals = self.get_coin_signals(hours, current_chat_id)
        
        if not signals:
            if hours < 24:
                msg = update.message.reply_text(f"Khong co keo nao trong {hours} gio qua.")
            else:
                days = hours // 24
                msg = update.message.reply_text(f"Khong co keo nao trong {days} ngay qua.")
            
            # Tự động xóa tin nhắn "không có kèo nào" sau 1 phút
            self.schedule_message_deletion(update, [msg], delay=60)
            return
        
        # Tạo summary message dạng bảng
        if hours < 24:
            summary_text = f"TONG HOP KEO {hours} GIO QUA\n"
        else:
            days = hours // 24
            summary_text = f"TONG HOP KEO {days} NGAY QUA\n"
        
        # Thêm thông tin group
        chat_title = update.message.chat.title or f"Group {current_chat_id}"
        summary_text += f"📱 Group: {chat_title}\n\n"
        
        # Tạo danh sách dễ đọc cho Telegram
        for i, signal in enumerate(signals, 1):
            contract = signal['contract_address']
            sender = signal['sender_username'] or f"User_{signal['sender_id']}"
            timestamp = signal['timestamp']
            price_at_signal = signal['price_at_signal']
            
            # Lấy thông tin token (tên và giá)
            token_info = asyncio.run(self.get_token_info(contract))
            current_price = token_info.get('price')
            token_name = token_info.get('name', 'Unknown')
            token_symbol = token_info.get('symbol', 'UNKNOWN')
            
            # Format tên token
            if token_name != 'Unknown':
                token_display = f"{token_name} ({token_symbol})"
            else:
                token_display = f"Unknown ({token_symbol})"
            
            # Xử lý giá và % thay đổi
            price_info = ""
            if price_at_signal and current_price:
                # Có cả hai giá - tính % thay đổi
                change_percent = ((current_price - price_at_signal) / price_at_signal) * 100
                change_emoji = "📈" if change_percent > 0 else "📉"
                price_info = f"{change_emoji} {change_percent:+.1f}%"
            
            # Format thời gian - convert UTC sang UTC+7 để hiển thị
            if isinstance(timestamp, str):
                # Nếu timestamp là string, parse thành datetime
                from datetime import datetime, timezone
                try:
                    # Thử parse với timezone info trước
                    if '+00:00' in timestamp or 'Z' in timestamp:
                        # Có timezone info, parse bình thường
                        dt = datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
                    else:
                        # Không có timezone info, giả sử là UTC+7 (data cũ từ import)
                        dt = datetime.fromisoformat(timestamp)
                        # Thêm timezone UTC+7
                        vietnam_tz = timezone(timedelta(hours=7))
                        dt = dt.replace(tzinfo=vietnam_tz)
                        # Convert sang UTC
                        dt = dt.astimezone(timezone.utc)
                    
                    # Convert UTC sang UTC+7 để hiển thị
                    vietnam_tz = timezone(timedelta(hours=7))
                    local_time = dt.astimezone(vietnam_tz)
                    time_str = local_time.strftime('%H:%M')
                except:
                    time_str = timestamp  # Giữ nguyên nếu không parse được
            else:
                # Convert UTC sang UTC+7
                from datetime import timezone
                vietnam_tz = timezone(timedelta(hours=7))
                local_time = timestamp.astimezone(vietnam_tz)
                time_str = local_time.strftime('%H:%M')
            # Tạo entry cho mỗi token
            summary_text += f"{i}. {token_display}\n"
            summary_text += f"Contract: `{contract}`\n"
            summary_text += f"Nguoi gui: {sender}\n"
            summary_text += f"Thoi gian: {time_str}\n"
            
            # Chỉ hiển thị giá lúc gửi nếu có
            if price_at_signal:
                price_signal_str = self.format_price(price_at_signal)
                summary_text += f"Gia luc gui: {price_signal_str}\n"
            
            # Chỉ hiển thị giá hiện tại nếu có
            if current_price:
                price_current_str = self.format_price(current_price)
                summary_text += f"Gia hien tai: {price_current_str}\n"
            
            # Chỉ hiển thị % thay đổi nếu có
            if price_info:
                summary_text += f"Thay doi: {price_info}\n"
            
            summary_text += "\n"
        
        # Thêm thông báo tin nhắn sẽ bị xóa
        summary_text += "⏰ Tin nhắn này sẽ tự động xóa sau 1 phút"
        
        # Gửi message (chia nhỏ nếu quá dài)
        sent_messages = []
        try:
            if len(summary_text) > 4000:
                # Chia thành nhiều message
                chunks = [summary_text[i:i+4000] for i in range(0, len(summary_text), 4000)]
                for chunk in chunks:
                    try:
                        msg = update.message.reply_text(chunk, parse_mode='Markdown')
                        sent_messages.append(msg)
                    except Exception as e:
                        # Nếu lỗi Markdown, thử gửi không có parse_mode
                        try:
                            msg = update.message.reply_text(chunk)
                            sent_messages.append(msg)
                        except Exception as e2:
                            print(f"Lỗi gửi tin nhắn: {e2}")
            else:
                try:
                    msg = update.message.reply_text(summary_text, parse_mode='Markdown')
                    sent_messages.append(msg)
                except Exception as e:
                    # Nếu lỗi Markdown, thử gửi không có parse_mode
                    try:
                        msg = update.message.reply_text(summary_text)
                        sent_messages.append(msg)
                    except Exception as e2:
                        print(f"Lỗi gửi tin nhắn: {e2}")
            
            # Tự động xóa tin nhắn sau 1 phút (chỉ nếu gửi thành công)
            if sent_messages:
                self.schedule_message_deletion(update, sent_messages, delay=60)
                
        except Exception as e:
            print(f"Lỗi xử lý tin nhắn: {e}")
            # Gửi tin nhắn lỗi đơn giản
            try:
                error_msg = update.message.reply_text("Lỗi tạo summary. Vui lòng thử lại sau.")
                self.schedule_message_deletion(update, [error_msg], delay=60)
            except:
                pass
    
    def chatid_command(self, update: Update, context: CallbackContext):
        """Lệnh hiển thị chat_id"""
        chat_id = update.message.chat_id
        chat_type = update.message.chat.type
        chat_title = update.message.chat.title or "Private Chat"
        
        chatid_text = f"""CHAT INFORMATION

Chat ID: `{chat_id}`
Chat Type: {chat_type}
Chat Title: {chat_title}

Su dung chat_id nay trong script import_chat_history.py:
json_file = 'your_file.json'
chat_id = {chat_id}
        """
        
        msg = update.message.reply_text(chatid_text, parse_mode='Markdown')
        
        # Tự động xóa tin nhắn sau 1 phút
        self.schedule_message_deletion(update, [msg], delay=60)
    
    def help_command(self, update: Update, context: CallbackContext):
        """Lệnh help"""
        help_text = """
COIN TRACKER BOT

Cach su dung:
• Bot se tu dong theo doi cac tin nhan chua contract address (0x...)
• Go /summary de xem tong hop keo 24 gio qua
• Go /summary 6 de xem tong hop 6 gio qua
• Go /summary 48 de xem tong hop 2 ngay qua (toi da 168 gio = 7 ngay)

Lenh:
• /summary [so_gio] - Xem tong hop keo theo gio
• /chatid - Hien thi chat_id cua group
• /help - Hien thi huong dan

Vi du:
• /summary - 24 gio qua
• /summary 6 - 6 gio qua  
• /summary 12 - 12 gio qua
• /summary 48 - 2 ngay qua
• /summary 168 - 7 ngay qua

Luu y:
• Bot chi theo doi contract addresses bat dau bang 0x
• Moi contract chi hien thi nguoi gui dau tien
• Gia duoc lay tu DexScreener va CoinGecko
• Toi da 168 gio (7 ngay) cho moi lan query
• Tin nhan summary tu dong xoa sau 1 phut
        """
        update.message.reply_text(help_text)
    
    def clear_old_bot_messages(self, bot):
        """Thông báo bot đã khởi động và sẵn sàng"""
        try:
            print("Bot đã khởi động thành công!")
            print("Bot sẽ tự động xóa tin nhắn summary sau 1 phút.")
            
        except Exception as e:
            print(f"Lỗi khi khởi tạo bot: {e}")

def main():
    # Import config
    try:
        from config import BOT_TOKEN
    except ImportError:
        print("Khong tim thay file config.py!")
        return
    
    if BOT_TOKEN == "YOUR_BOT_TOKEN":
        print("Vui long thay YOUR_BOT_TOKEN bang token that tu BotFather trong file config.py!")
        return
    
    # Khởi tạo bot
    bot = CoinTrackerBot(BOT_TOKEN)
    
    # Tạo updater với drop_pending_updates để tránh conflict
    updater = Updater(token=BOT_TOKEN, use_context=True)
    dispatcher = updater.dispatcher
    
    # Xóa tin nhắn cũ của bot khi khởi động
    bot.clear_old_bot_messages(updater.bot)
    
    # Thêm error handler
    def error_handler(update, context):
        """Xử lý lỗi"""
        logger.error(f"Update {update} caused error {context.error}")
    
    # Thêm handlers
    dispatcher.add_handler(CommandHandler("summary", bot.summary_command))
    dispatcher.add_handler(CommandHandler("chatid", bot.chatid_command))
    dispatcher.add_handler(CommandHandler("help", bot.help_command))
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, bot.process_message))
    dispatcher.add_error_handler(error_handler)
    
    # Chạy bot
    print("Bot dang chay...")
    print("Nhan Ctrl+C de dung bot")
    try:
        # Drop pending updates để tránh conflict
        updater.start_polling(drop_pending_updates=True)
        updater.idle()
    except KeyboardInterrupt:
        print("\nBot da dung!")
        updater.stop()
    except Exception as e:
        print(f"Loi khi chay bot: {e}")
        print("Thu chay lai sau 5 giay...")
        import time
        time.sleep(5)

if __name__ == '__main__':
    main()
