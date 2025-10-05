#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Telegram Flow - Tự động lọc tin nhắn từ group và gửi về chat cá nhân
"""

import asyncio
import json
import os
import sys
import re
import aiohttp
from datetime import datetime, timedelta
from telethon import TelegramClient, events
from telethon.tl.types import PeerChannel, PeerUser
import logging

# Thiết lập encoding cho Windows
if sys.platform == "win32":
    import codecs
    sys.stdout = codecs.getwriter("utf-8")(sys.stdout.detach())
    sys.stderr = codecs.getwriter("utf-8")(sys.stderr.detach())

# Thiết lập logging với encoding UTF-8
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('telegram_flow.log', encoding='utf-8'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class TelegramFlow:
    def __init__(self, config_file='config.json'):
        self.config_file = config_file
        self.config = self.load_config()
        self.client = None
        
    def load_config(self):
        """Load cấu hình từ file config.json"""
        try:
            with open(self.config_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            logger.error(f"Không tìm thấy file {self.config_file}")
            return None
        except json.JSONDecodeError:
            logger.error(f"File {self.config_file} không đúng định dạng JSON")
            return None
    
    async def start_client(self):
        """Khởi tạo Telegram client"""
        try:
            self.client = TelegramClient(
                'telegram_flow_session',
                self.config['api_id'],
                self.config['api_hash']
            )
            
            await self.client.start()
            logger.info("Successfully connected to Telegram")
            return True
        except Exception as e:
            logger.error(f"Error connecting to Telegram: {e}")
            return False
    
    async def get_group_messages(self, group_username, target_date=None, limit=10000):
        """Lấy tin nhắn từ group theo ngày"""
        try:
            # Lấy entity của group
            group = await self.client.get_entity(group_username)
            logger.info(f"Successfully connected to group: {group_username}")
            
            # Nếu không có target_date, lấy tin nhắn hôm nay (UTC+7)
            if target_date is None:
                from datetime import timezone, timedelta
                utc_plus_7 = timezone(timedelta(hours=7))
                target_date = datetime.now(utc_plus_7).date()
                logger.info(f"No target date specified, using today's date (UTC+7): {target_date}")
                
                # Tính toán thời gian bắt đầu và kết thúc của ngày hôm nay (UTC+7)
                start_time_local = datetime.combine(target_date, datetime.min.time()).replace(tzinfo=utc_plus_7)
                end_time_local = datetime.combine(target_date, datetime.max.time()).replace(tzinfo=utc_plus_7)
                
                logger.info(f"Today's range (UTC+7): {start_time_local} to {end_time_local}")
                
                messages = []
                message_count = 0
                #consecutive_old_messages = 0
                
                async for message in self.client.iter_messages(group, limit=limit):
                    message_count += 1
                    message_date_local = message.date.astimezone(utc_plus_7)
                    
                    # Log một số tin nhắn đầu tiên để debug
                    if message_count <= 5:
                        logger.info(f"Message {message_count}: UTC={message.date}, UTC+7={message_date_local}")
                    
                    # Kiểm tra tin nhắn có trong ngày hôm nay không (theo UTC+7)
                    if start_time_local <= message_date_local <= end_time_local:
                        messages.append({
                            'id': message.id,
                            'text': message.text or '',
                            'date': message_date_local,
                            'sender_id': message.sender_id,
                            'sender_username': getattr(message.sender, 'username', None) if message.sender else None,
                            'sender_first_name': getattr(message.sender, 'first_name', None) if message.sender else None,
                            'sender_last_name': getattr(message.sender, 'last_name', None) if message.sender else None
                        })
                        #consecutive_old_messages = 0  # Reset counter
                    else:
                        #consecutive_old_messages += 1
                        
                        # Nếu tin nhắn cũ hơn ngày hôm nay, dừng lại
                        if message_date_local < start_time_local:
                            logger.info(f"Stopping at message {message_count} - too old: {message_date_local}")
                            break
                        
                        # Nếu có quá nhiều tin nhắn cũ liên tiếp, dừng lại
                        #if consecutive_old_messages >= 100:
                        #    logger.info(f"Stopping at message {message_count} - too many consecutive old messages ({consecutive_old_messages})")
                        #    break
                
                logger.info(f"Retrieved {len(messages)} messages from today ({target_date}) in group {group_username}")
                logger.info(f"Processed {message_count} messages total, stopped early for efficiency")
                return messages
            
            # Tính toán thời gian bắt đầu và kết thúc của ngày (UTC+7)
            from datetime import timezone, timedelta
            utc_plus_7 = timezone(timedelta(hours=7))
            
            # Ngày bắt đầu và kết thúc theo UTC+7
            start_time_local = datetime.combine(target_date, datetime.min.time()).replace(tzinfo=utc_plus_7)
            end_time_local = datetime.combine(target_date, datetime.max.time()).replace(tzinfo=utc_plus_7)
            
            logger.info(f"Target date (UTC+7): {target_date}")
            logger.info(f"UTC+7 range: {start_time_local} to {end_time_local}")
            
            # Lấy tin nhắn trong khoảng thời gian
            messages = []
            message_count = 0
            #consecutive_old_messages = 0  # Đếm số tin nhắn cũ liên tiếp
            
            async for message in self.client.iter_messages(group, limit=limit):
                message_count += 1
                # Convert message date từ UTC sang UTC+7 để kiểm tra
                message_date_local = message.date.astimezone(utc_plus_7)
                
                # Log một số tin nhắn đầu tiên để debug
                if message_count <= 5:
                    logger.info(f"Message {message_count}: UTC={message.date}, UTC+7={message_date_local}")
                
                # Kiểm tra tin nhắn có trong ngày target không (theo UTC+7)
                if start_time_local <= message_date_local <= end_time_local:
                    messages.append({
                        'id': message.id,
                        'text': message.text or '',
                        'date': message_date_local,  # Đã convert sang UTC+7
                        'sender_id': message.sender_id,
                        'sender_username': getattr(message.sender, 'username', None) if message.sender else None,
                        'sender_first_name': getattr(message.sender, 'first_name', None) if message.sender else None,
                        'sender_last_name': getattr(message.sender, 'last_name', None) if message.sender else None
                    })
                    #consecutive_old_messages = 0  # Reset counter khi tìm thấy tin nhắn trong ngày
                else:
                    #consecutive_old_messages += 1
                    
                    # Nếu tin nhắn cũ hơn ngày target (theo UTC+7), dừng lại
                    if message_date_local < start_time_local:
                        logger.info(f"Stopping at message {message_count} - too old: {message_date_local}")
                        break
                    
                    # Nếu có quá nhiều tin nhắn cũ liên tiếp (không trong ngày target), dừng lại
                    # Ngưỡng dừng sớm: 100 tin nhắn cũ liên tiếp
                    #early_stop_threshold = 100
                    #if consecutive_old_messages >= early_stop_threshold:
                    #    logger.info(f"Stopping at message {message_count} - too many consecutive old messages ({consecutive_old_messages})")
                    #    logger.info(f"Early stop threshold: {early_stop_threshold} consecutive old messages")
                    #    break
                    
            
            logger.info(f"Retrieved {len(messages)} messages from group {group_username} on {target_date} (UTC+7)")
            logger.info(f"Processed {message_count} messages total, stopped early for efficiency")
            return messages
            
        except Exception as e:
            logger.error(f"Error retrieving messages from group: {e}")
            return []
    
    async def get_group_messages_recent(self, group_username, limit=1000):
        """Lấy tất cả tin nhắn gần đây (không filter theo ngày)"""
        try:
            # Lấy entity của group
            group = await self.client.get_entity(group_username)
            logger.info(f"Successfully connected to group: {group_username}")
            
            from datetime import timezone, timedelta
            utc_plus_7 = timezone(timedelta(hours=7))
            
            messages = []
            async for message in self.client.iter_messages(group, limit=limit):
                message_date_local = message.date.astimezone(utc_plus_7)
                
                messages.append({
                    'id': message.id,
                    'text': message.text or '',
                    'date': message_date_local,
                    'sender_id': message.sender_id,
                    'sender_username': getattr(message.sender, 'username', None) if message.sender else None,
                    'sender_first_name': getattr(message.sender, 'first_name', None) if message.sender else None,
                    'sender_last_name': getattr(message.sender, 'last_name', None) if message.sender else None
                })
            
            logger.info(f"Retrieved {len(messages)} recent messages from group {group_username}")
            return messages
            
        except Exception as e:
            logger.error(f"Error retrieving recent messages from group: {e}")
            return []
    
    def detect_contract_addresses(self, text):
        """Phát hiện contract address trong text (EVM và Solana)"""
        contracts = []
        
        # EVM contract address (0x + 40 hex characters)
        evm_pattern = r'0x[a-fA-F0-9]{40}'
        evm_matches = re.findall(evm_pattern, text)
        for match in evm_matches:
            contracts.append({
                'address': match,
                'type': 'EVM',
                'chain': 'Ethereum/BSC/Polygon/etc'
            })
        
        # Solana contract address (Base58, 32-44 characters)
        solana_pattern = r'[1-9A-HJ-NP-Za-km-z]{32,44}'
        solana_matches = re.findall(solana_pattern, text)
        for match in solana_matches:
            # Kiểm tra không phải EVM address
            if not match.startswith('0x') and len(match) >= 32:
                contracts.append({
                    'address': match,
                    'type': 'Solana',
                    'chain': 'Solana'
                })
        
        return contracts
    
    def format_market_cap(self, market_cap):
        """Format market cap để dễ đọc hơn"""
        try:
            if market_cap == 'N/A' or market_cap is None:
                return 'N/A'
            
            # Convert to float
            cap = float(market_cap)
            
            if cap >= 1_000_000_000:  # 1 tỉ trở lên
                return f"{cap / 1_000_000_000:.1f}B"
            elif cap >= 1_000_000:  # 1 triệu trở lên
                return f"{cap / 1_000_000:.1f}M"
            elif cap >= 1_000:  # 1 nghìn trở lên
                return f"{cap / 1_000:.0f}K"
            else:
                return f"{cap:.0f}"
                
        except (ValueError, TypeError):
            return str(market_cap)
    
    async def get_current_token_price(self, contract_address):
        """Lấy giá token hiện tại từ DexScreener API (không cần historical data)"""
        try:
            logger.info(f"Getting current price for contract: {contract_address}")
            
            async with aiohttp.ClientSession() as session:
                # Lấy thông tin token hiện tại
                current_url = f"https://api.dexscreener.com/latest/dex/tokens/{contract_address}"
                logger.info(f"Requesting: {current_url}")
                
                async with session.get(current_url) as response:
                    logger.info(f"Current price API response status: {response.status}")
                    
                    if response.status == 200:
                        current_data = await response.json()
                        #logger.info(f"Current price API response: {current_data}")
                        
                        # Kiểm tra xem có token nào được tìm thấy không
                        if 'pairs' not in current_data or not current_data['pairs']:
                            logger.warning(f"No pairs found for contract: {contract_address}")
                            return {
                                'current_price': 'N/A',
                                'current_market_cap': 'N/A',
                                'error': 'No pairs found on DexScreener'
                            }
                        
                        # Lấy pair đầu tiên (thường là pair chính)
                        main_pair = current_data['pairs'][0]
                        current_price = main_pair.get('priceUsd', 'N/A')
                        current_market_cap = main_pair.get('marketCap', 'N/A')
                        
                        logger.info(f"Found price: {current_price}, market cap: {current_market_cap}")
                        
                        return {
                            'current_price': current_price,
                            'current_market_cap': current_market_cap
                        }
                    else:
                        logger.error(f"DexScreener API error: {response.status}")
                        error_text = await response.text()
                        logger.error(f"Error response: {error_text}")
                        return {
                            'current_price': 'N/A',
                            'current_market_cap': 'N/A',
                            'error': f'API error: {response.status}'
                        }
                        
        except Exception as e:
            logger.error(f"Error getting current token price: {e}")
            return {
                'current_price': 'N/A',
                'current_market_cap': 'N/A',
                'error': str(e)
            }
    
    async def get_token_price_data(self, contract_address, message_timestamp):
        """Lấy giá token từ DexScreener API"""
        try:
            logger.info(f"Getting price data for contract: {contract_address}")
            
            async with aiohttp.ClientSession() as session:
                # Lấy thông tin token hiện tại
                current_url = f"https://api.dexscreener.com/latest/dex/tokens/{contract_address}"
                logger.info(f"Requesting: {current_url}")
                
                async with session.get(current_url) as response:
                    logger.info(f"Current price API response status: {response.status}")
                    
                    if response.status == 200:
                        current_data = await response.json()
                        #logger.info(f"Current price API response: {current_data}")
                        
                        # Kiểm tra xem có token nào được tìm thấy không
                        if 'pairs' not in current_data or not current_data['pairs']:
                            logger.warning(f"No pairs found for contract: {contract_address}")
                            return {
                                'current_price': 'N/A',
                                'current_market_cap': 'N/A',
                                'historical_price': None,
                                'price_change_percent': None,
                                'error': 'No pairs found on DexScreener'
                            }
                        
                        # Lấy pair đầu tiên (thường là pair chính)
                        main_pair = current_data['pairs'][0]
                        current_price = main_pair.get('priceUsd', 'N/A')
                        current_market_cap = main_pair.get('marketCap', 'N/A')
                        
                        logger.info(f"Found price: {current_price}, market cap: {current_market_cap}")
                        
                        # Lấy OHLCV data 5 phút
                        ohlcv_url = f"https://api.dexscreener.com/latest/dex/tokens/{contract_address}/ohlc/5m"
                        logger.info(f"Requesting OHLCV: {ohlcv_url}")
                        
                        async with session.get(ohlcv_url) as ohlcv_response:
                            logger.info(f"OHLCV API response status: {ohlcv_response.status}")
                            
                            if ohlcv_response.status == 200:
                                ohlcv_data = await ohlcv_response.json()
                                logger.info(f"OHLCV 5m data received: {len(ohlcv_data.get('ohlcv', []))} candles")
                                
                                # Tìm giá gần nhất với thời điểm tin nhắn
                                historical_price = self.find_historical_price(ohlcv_data, message_timestamp)
                                
                                # Tính phần trăm tăng/giảm
                                price_change_percent = self.calculate_price_change(historical_price, current_price)
                                
                                return {
                                    'current_price': current_price,
                                    'current_market_cap': current_market_cap,
                                    'historical_price': historical_price,
                                    'price_change_percent': price_change_percent,
                                    'ohlcv': ohlcv_data,
                                    'message_timestamp': message_timestamp
                                }
                            else:
                                logger.warning(f"OHLCV 5m API error: {ohlcv_response.status} - No historical data available")
                                return {
                                    'current_price': current_price,
                                    'current_market_cap': current_market_cap,
                                    'historical_price': None,
                                    'price_change_percent': None,
                                    'warning': f'Token có thể mới hoặc chưa có trading history đủ lâu để tạo dữ liệu historical (OHLCV 5m API: {ohlcv_response.status})'
                                }
                    else:
                        logger.error(f"DexScreener API error: {response.status}")
                        error_text = await response.text()
                        logger.error(f"Error response: {error_text}")
                        return {
                            'current_price': 'N/A',
                            'current_market_cap': 'N/A',
                            'historical_price': None,
                            'price_change_percent': None,
                            'error': f'API error: {response.status}'
                        }
                        
        except Exception as e:
            logger.error(f"Error getting token price data: {e}")
            return {
                'current_price': 'N/A',
                'current_market_cap': 'N/A',
                'historical_price': None,
                'price_change_percent': None,
                'error': str(e)
            }
    
    def find_historical_price(self, ohlcv_data, message_timestamp):
        """Tìm giá gần nhất với thời điểm tin nhắn"""
        try:
            if not ohlcv_data or 'ohlcv' not in ohlcv_data:
                return None
            
            # Convert message timestamp to UTC for comparison
            message_utc = message_timestamp.astimezone(timezone.utc)
            message_unix = int(message_utc.timestamp())
            
            # Tìm candle gần nhất
            closest_candle = None
            min_diff = float('inf')
            
            for candle in ohlcv_data['ohlcv']:
                candle_time = candle.get('timestamp', 0)
                diff = abs(candle_time - message_unix)
                if diff < min_diff:
                    min_diff = diff
                    closest_candle = candle
            
            if closest_candle:
                return closest_candle.get('close', None)
            
            return None
            
        except Exception as e:
            logger.error(f"Error finding historical price: {e}")
            return None
    
    def calculate_price_change(self, historical_price, current_price):
        """Tính phần trăm tăng/giảm giá"""
        try:
            if not historical_price or not current_price:
                return None
            
            # Convert to float
            hist_price = float(historical_price)
            curr_price = float(current_price)
            
            if hist_price == 0:
                return None
            
            # Tính phần trăm thay đổi
            change_percent = ((curr_price - hist_price) / hist_price) * 100
            return round(change_percent, 2)
            
        except Exception as e:
            logger.error(f"Error calculating price change: {e}")
            return None
    
    async def send_contract_analysis(self, contract_messages, target_user):
        """Gửi phân tích contract address về Saved Messages"""
        try:
            logger.info(f"Starting to send contract analysis for {len(contract_messages)} messages")
            
            # Lấy entity của chat cá nhân (Saved Messages)
            me = await self.client.get_me()
            logger.info(f"Sending contract analysis to Saved Messages for user: {me.username}")
            
            if not contract_messages:
                content = f"🔍 **Contract Analysis từ {target_user}**\n"
                content += f"📅 Thời gian: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}\n"
                content += f"📊 Tổng số tin nhắn: 0\n\n"
                content += "❌ Không tìm thấy contract address nào từ người dùng này."
                await self.client.send_message(me, content)
                return
            
            # Gửi tin nhắn header
            header = f"🔍 **Contract Analysis từ {target_user}**\n"
            header += f"📅 Thời gian: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}\n"
            header += f"📊 Tổng số tin nhắn: {len(contract_messages)}\n"
            header += f"⏰ Sắp xếp theo thời gian tăng dần\n\n"
            header += "📝 **Phân tích Contract:**\n\n"
            
            await self.client.send_message(me, header)
            
            # Gửi từng contract analysis
            for i, msg_data in enumerate(contract_messages, 1):
                try:
                    msg = msg_data['message']
                    contracts = msg_data['contracts']
                    
                    content = f"**{i}.** {msg['date'].strftime('%d/%m/%Y %H:%M')} (UTC+7)\n"
                    
                    # Hiển thị tên người gửi nếu có
                    sender_name = ""
                    if msg.get('sender_username'):
                        sender_name = f"@{msg['sender_username']}"
                    elif msg.get('sender_first_name'):
                        sender_name = msg['sender_first_name']
                        if msg.get('sender_last_name'):
                            sender_name += f" {msg['sender_last_name']}"
                    
                    if sender_name:
                        content += f"👤 {sender_name}\n"
                    
                    content += f"💬 {msg['text'][:200]}{'...' if len(msg['text']) > 200 else ''}\n\n"
                    
                    for contract in contracts:
                        # Lấy giá token hiện tại
                        price_data = await self.get_current_token_price(contract['address'])
                        if price_data:
                            content += f"🔗 Contract : {contract['address']}\n"
                            content += f"💰 Giá hiện tại: ${price_data['current_price']}\n"
                            formatted_market_cap = self.format_market_cap(price_data['current_market_cap'])
                            content += f"📈 Market Cap: ${formatted_market_cap}\n"
                        else:
                            content += f"🔗 Contract : {contract['address']}\n"
                            content += f"❌ Không thể lấy giá token\n"
                        
                        content += "\n"
                    
                    # Chia nhỏ tin nhắn nếu quá dài
                    if len(content) > 4000:
                        parts = [content[i:i+4000] for i in range(0, len(content), 4000)]
                        for part in parts:
                            await self.client.send_message(me, part)
                            await asyncio.sleep(0.5)
                    else:
                        await self.client.send_message(me, content)
                        await asyncio.sleep(0.5)
                        
                except Exception as e:
                    logger.error(f"Error sending contract analysis {i}: {e}")
                    continue
            
            logger.info("Contract analysis sent successfully to Saved Messages")
            
        except Exception as e:
            logger.error(f"Error sending contract analysis: {e}")
    
    def filter_messages_with_contracts(self, messages, target_user):
        """Lọc tin nhắn có contract address từ người dùng cụ thể (loại bỏ trùng lặp)"""
        contract_messages = []
        seen_contracts = set()  # Set để track contract đã thấy
        
        logger.info(f"Searching for contract addresses from user: '{target_user}' in {len(messages)} messages")
        
        for msg in messages:
            # Kiểm tra người gửi
            sender_match = False
            if msg['sender_username'] and target_user.lower() in msg['sender_username'].lower():
                sender_match = True
            elif msg['sender_first_name'] and target_user.lower() in msg['sender_first_name'].lower():
                sender_match = True
            elif msg['sender_last_name'] and target_user.lower() in msg['sender_last_name'].lower():
                sender_match = True
            
            if sender_match:
                # Phát hiện contract address trong tin nhắn
                contracts = self.detect_contract_addresses(msg['text'])
                if contracts:
                    # Lọc bỏ contract đã thấy trước đó (không phân biệt hoa thường)
                    unique_contracts = []
                    for contract in contracts:
                        address_lower = contract['address'].lower()
                        if address_lower not in seen_contracts:
                            unique_contracts.append(contract)
                            seen_contracts.add(address_lower)
                    
                    # Chỉ thêm tin nhắn nếu có contract mới
                    if unique_contracts:
                        contract_messages.append({
                            'message': msg,
                            'contracts': unique_contracts
                        })
                        logger.info(f"Found {len(unique_contracts)} new contracts in message from {target_user}")
        
        logger.info(f"Found {len(contract_messages)} messages with unique contracts from {target_user}")
        return contract_messages
    
    def filter_all_messages_with_contracts(self, messages):
        """Lọc tất cả tin nhắn có contract address từ toàn bộ group (loại bỏ trùng lặp)"""
        contract_messages = []
        seen_contracts = set()  # Set để track contract đã thấy
        
        logger.info(f"Searching for contract addresses from all users in {len(messages)} messages")
        
        for msg in messages:
            # Phát hiện contract address trong tin nhắn
            contracts = self.detect_contract_addresses(msg['text'])
            if contracts:
                # Lọc bỏ contract đã thấy trước đó (không phân biệt hoa thường)
                unique_contracts = []
                for contract in contracts:
                    address_lower = contract['address'].lower()
                    if address_lower not in seen_contracts:
                        unique_contracts.append(contract)
                        seen_contracts.add(address_lower)
                
                # Chỉ thêm tin nhắn nếu có contract mới
                if unique_contracts:
                    contract_messages.append({
                        'message': msg,
                        'contracts': unique_contracts
                    })
                    logger.info(f"Found {len(unique_contracts)} new contracts in message from {msg.get('sender_username', 'Unknown')}")
        
        logger.info(f"Found {len(contract_messages)} messages with unique contracts from all users")
        return contract_messages
    
    def filter_messages_by_user(self, messages, target_user):
        """Lọc tin nhắn theo người dùng cụ thể"""
        filtered_messages = []
        
        logger.info(f"Searching for user: '{target_user}' in {len(messages)} messages")
        
        for msg in messages:
            # Debug: Log thông tin người gửi
            sender_info = f"Username: {msg['sender_username']}, First: {msg['sender_first_name']}, Last: {msg['sender_last_name']}"
            logger.info(f"Message from: {sender_info}")
            
            # Kiểm tra theo username, first_name, hoặc last_name
            match_found = False
            
            if msg['sender_username'] and target_user.lower() in msg['sender_username'].lower():
                match_found = True
                logger.info(f"Match found by username: {msg['sender_username']}")
            elif msg['sender_first_name'] and target_user.lower() in msg['sender_first_name'].lower():
                match_found = True
                logger.info(f"Match found by first name: {msg['sender_first_name']}")
            elif msg['sender_last_name'] and target_user.lower() in msg['sender_last_name'].lower():
                match_found = True
                logger.info(f"Match found by last name: {msg['sender_last_name']}")
            
            if match_found:
                filtered_messages.append(msg)
        
        logger.info(f"Filtered {len(filtered_messages)} messages from {target_user}")
        return filtered_messages
    
    async def send_filtered_messages(self, messages, target_user):
        """Gửi tin nhắn đã lọc về Saved Messages"""
        try:
            logger.info(f"Starting to send {len(messages)} messages for {target_user}")
            
            # Lấy entity của chat cá nhân (Saved Messages)
            me = await self.client.get_me()
            logger.info(f"Sending to Saved Messages for user: {me.username}")
            
            if not messages:
                content = f"🔍 **Tin nhắn từ {target_user}**\n"
                content += f"📅 Thời gian: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}\n"
                content += f"📊 Tổng số tin nhắn: 0\n\n"
                content += "❌ Không tìm thấy tin nhắn nào từ người dùng này."
                await self.client.send_message(me, content)
                logger.info("Sent empty result message to Saved Messages")
                return
            
            # Gửi tin nhắn header
            header = f"🔍 **Tin nhắn từ {target_user}**\n"
            header += f"📅 Thời gian: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}\n"
            header += f"📊 Tổng số tin nhắn: {len(messages)}\n"
            header += f"⏰ Sắp xếp theo thời gian tăng dần (từ cũ đến mới)\n\n"
            header += "📝 **Nội dung tin nhắn:**\n\n"
            
            logger.info("Sending header message to Saved Messages")
            await self.client.send_message(me, header)
            logger.info("Header message sent successfully to Saved Messages")
            
            # Gửi từng tin nhắn riêng biệt
            sent_count = 0
            for i, msg in enumerate(messages, 1):
                try:
                    logger.info(f"Processing message {i}/{len(messages)}")
                    
                    if msg['text']:
                        content = f"**{i}.** {msg['date'].strftime('%d/%m/%Y %H:%M')} (UTC+7)\n"
                        content += f"💬 {msg['text']}"
                        logger.info(f"Message {i} has text: {len(msg['text'])} characters")
                    else:
                        content = f"**{i}.** {msg['date'].strftime('%d/%m/%Y %H:%M')} (UTC+7)\n"
                        content += f"💬 [Tin nhắn không có text - có thể chứa media]"
                        logger.info(f"Message {i} has no text")
                    
                    # Chia nhỏ tin nhắn nếu quá dài (Telegram giới hạn 4096 ký tự)
                    if len(content) > 4000:
                        logger.info(f"Message {i} is too long, splitting...")
                        # Chia thành nhiều phần
                        parts = [content[i:i+4000] for i in range(0, len(content), 4000)]
                        for j, part in enumerate(parts):
                            await self.client.send_message(me, part)
                            logger.info(f"Sent part {j+1}/{len(parts)} of message {i} to Saved Messages")
                            await asyncio.sleep(0.5)  # Tránh spam
                    else:
                        await self.client.send_message(me, content)
                        logger.info(f"Sent message {i} successfully to Saved Messages")
                        await asyncio.sleep(0.3)  # Tránh spam
                    
                    sent_count += 1
                        
                except Exception as e:
                    logger.error(f"Error sending message {i}: {e}")
                    continue
            
            logger.info(f"Successfully sent {sent_count}/{len(messages)} messages to Saved Messages")
            
        except Exception as e:
            logger.error(f"Error in send_filtered_messages: {e}")
            # Gửi thông báo lỗi
            try:
                me = await self.client.get_me()
                await self.client.send_message(me, f"❌ Lỗi khi gửi tin nhắn: {str(e)}")
            except:
                pass
    
    async def handle_trigger_message(self, event):
        """Xử lý tin nhắn trigger"""
        try:
            message_text = event.message.text.strip()
            
            # Kiểm tra lệnh dừng bot
            if message_text == '/stop' or message_text == '/quit':
                await event.reply("🛑 Bot will stop in 3 seconds...")
                logger.info("🛑 Stop command received from user")
                await asyncio.sleep(3)
                await self.client.disconnect()
                return
            
            # Kiểm tra lệnh debug
            if message_text == '/debug':
                await event.reply("🔧 Debug mode enabled. Next /filter command will show detailed info.")
                return
            
            # Kiểm tra lệnh test
            if message_text == '/test':
                await event.reply("🧪 Test message - bot is working!")
                return
            
            # Kiểm tra lệnh hiển thị thời gian
            if message_text == '/time':
                from datetime import timezone, timedelta
                utc_plus_7 = timezone(timedelta(hours=7))
                current_time = datetime.now(utc_plus_7)
                current_time_utc = current_time.astimezone(timezone.utc)
                await event.reply(f"🕐 Thời gian hiện tại (UTC+7): {current_time.strftime('%d/%m/%Y %H:%M:%S')}\n🕐 Thời gian hiện tại (UTC): {current_time_utc.strftime('%d/%m/%Y %H:%M:%S')}")
                return
            
            # Kiểm tra lệnh giải thích timezone
            if message_text == '/timezone':
                from datetime import timezone, timedelta
                utc_plus_7 = timezone(timedelta(hours=7))
                current_time = datetime.now(utc_plus_7)
                current_time_utc = current_time.astimezone(timezone.utc)
                
                explanation = f"🌍 **Giải thích Timezone:**\n\n"
                explanation += f"📅 Ngày hôm nay (UTC+7): {current_time.strftime('%d/%m/%Y')}\n"
                explanation += f"📅 Ngày hôm nay (UTC): {current_time_utc.strftime('%d/%m/%Y')}\n\n"
                explanation += f"🕐 Thời gian hiện tại (UTC+7): {current_time.strftime('%H:%M:%S')}\n"
                explanation += f"🕐 Thời gian hiện tại (UTC): {current_time_utc.strftime('%H:%M:%S')}\n\n"
                explanation += f"💡 **Ví dụ:**\n"
                explanation += f"• Tin nhắn lúc 18:00 UTC ngày 3/10\n"
                explanation += f"• = 01:00 UTC+7 ngày 4/10\n"
                explanation += f"• Bot sẽ lấy tin nhắn này khi filter ngày 4/10 (UTC+7)\n\n"
                explanation += f"🔍 **Khi filter ngày hôm nay (UTC+7):**\n"
                explanation += f"• Bot sẽ lấy tin nhắn từ 17:00 UTC ngày hôm qua\n"
                explanation += f"• Đến 16:59 UTC ngày hôm nay"
                
                await event.reply(explanation)
                return
            
            # Kiểm tra lệnh test với ngày hôm qua
            if message_text == '/testyesterday':
                from datetime import timedelta
                yesterday = (datetime.now() - timedelta(days=1)).date()
                await event.reply(f"🔄 Testing with yesterday's date: {yesterday}")
                
                # Test với group và user mẫu
                test_messages = await self.get_group_messages("@BNNMEMECHATT", yesterday, 100)
                await event.reply(f"📊 Found {len(test_messages)} messages from yesterday")
                
                if test_messages:
                    # Lấy 5 tin nhắn đầu tiên để test
                    sample_messages = test_messages[:5]
                    await self.send_filtered_messages(sample_messages, "SampleUser")
                    await event.reply("✅ Sent sample messages to Saved Messages!")
                return
            
            # Kiểm tra lệnh test với tên người dùng khác nhau
            if message_text.startswith('/testuser'):
                parts = message_text.split()
                if len(parts) < 2:
                    await event.reply("❌ Format: /testuser <username>")
                    return
                
                test_username = parts[1]
                await event.reply(f"🔄 Testing with username: {test_username}")
                
                # Test với group
                test_messages = await self.get_group_messages("@BNNMEMECHATT", None, 100)
                await event.reply(f"📊 Found {len(test_messages)} messages in group")
                
                # Test filter
                filtered_messages = self.filter_messages_by_user(test_messages, test_username)
                # Sắp xếp theo thời gian tăng dần
                filtered_messages.sort(key=lambda x: x['date'])
                await event.reply(f"🎯 Found {len(filtered_messages)} messages from {test_username}")
                
                if filtered_messages:
                    await self.send_filtered_messages(filtered_messages, test_username)
                    await event.reply("✅ Sent filtered messages to Saved Messages!")
                return
            
            # Kiểm tra lệnh test lấy tin nhắn gần đây
            if message_text == '/testrecent':
                await event.reply("🔄 Testing recent messages from group...")
                
                # Test với group - lấy tất cả tin nhắn gần đây (không filter theo ngày)
                test_messages = await self.get_group_messages_recent("@BNNMEMECHATT", 50)
                await event.reply(f"📊 Found {len(test_messages)} recent messages in group")
                
                if test_messages:
                    # Sắp xếp theo thời gian tăng dần
                    test_messages.sort(key=lambda x: x['date'])
                    # Lấy 5 tin nhắn đầu tiên để test
                    sample_messages = test_messages[:5]
                    await self.send_filtered_messages(sample_messages, "RecentMessages")
                    await event.reply("✅ Sent sample recent messages to Saved Messages!")
                else:
                    await event.reply("❌ No recent messages found!")
                return
            
            # Kiểm tra lệnh test với ngày cụ thể
            if message_text.startswith('/testdate'):
                parts = message_text.split()
                if len(parts) < 2:
                    await event.reply("❌ Format: /testdate yyyy.mm.dd")
                    return
                
                try:
                    test_date = datetime.strptime(parts[1], '%Y.%m.%d').date()
                    await event.reply(f"🔄 Testing with date: {test_date}")
                    
                    # Test với group
                    test_messages = await self.get_group_messages("@BNNMEMECHATT", test_date, 100)
                    await event.reply(f"📊 Found {len(test_messages)} messages on {test_date}")
                    
                    if test_messages:
                        # Sắp xếp theo thời gian tăng dần
                        test_messages.sort(key=lambda x: x['date'])
                        # Lấy 5 tin nhắn đầu tiên để test
                        sample_messages = test_messages[:5]
                        await self.send_filtered_messages(sample_messages, "DateTest")
                        await event.reply("✅ Sent sample messages to Saved Messages!")
                    else:
                        await event.reply("❌ No messages found on this date!")
                        
                except ValueError:
                    await event.reply("❌ Format ngày không đúng! Sử dụng: yyyy.mm.dd")
                return
            
            # Kiểm tra lệnh test contract API
            if message_text.startswith('/testcontract'):
                parts = message_text.split()
                if len(parts) < 2:
                    await event.reply("❌ Format: /testcontract <contract_address> [yyyy.mm.dd hh:mm]")
                    return
                
                contract_address = parts[1]
                
                # Xử lý thời gian cụ thể nếu có
                target_datetime = datetime.now()
                if len(parts) >= 3:
                    try:
                        # Parse format: yyyy.mm.dd hh:mm
                        date_time_str = f"{parts[2]} {parts[3] if len(parts) > 3 else '00:00'}"
                        target_datetime = datetime.strptime(date_time_str, '%Y.%m.%d %H:%M')
                        
                        # Convert to UTC+7 timezone
                        from datetime import timezone, timedelta
                        utc_plus_7 = timezone(timedelta(hours=7))
                        target_datetime = target_datetime.replace(tzinfo=utc_plus_7)
                        
                    except ValueError:
                        await event.reply("❌ Format thời gian không đúng! Sử dụng: yyyy.mm.dd hh:mm")
                        return
                
                await event.reply(f"🔄 Testing contract API for: {contract_address}")
                await event.reply(f"⏰ Target time: {target_datetime.strftime('%d/%m/%Y %H:%M')} (UTC+7)")
                
                # Test API
                price_data = await self.get_token_price_data(contract_address, target_datetime)
                
                if price_data:
                    result = f"✅ **API Test Result:**\n"
                    result += f"🔗 Contract: `{contract_address}`\n"
                    result += f"⏰ Thời gian yêu cầu: {target_datetime.strftime('%d/%m/%Y %H:%M')} (UTC+7)\n"
                    result += f"💰 Giá hiện tại: ${price_data['current_price']}\n"
                    formatted_market_cap = self.format_market_cap(price_data['current_market_cap'])
                    result += f"📈 Market Cap: ${formatted_market_cap}\n"
                    
                    if 'error' in price_data:
                        result += f"❌ Lỗi: {price_data['error']}\n"
                    elif 'warning' in price_data:
                        result += f"⚠️ Cảnh báo: {price_data['warning']}\n"
                    
                    if price_data['historical_price']:
                        result += f"📊 Giá lúc {target_datetime.strftime('%H:%M')}: ${price_data['historical_price']}\n"
                    
                    if price_data['price_change_percent'] is not None:
                        result += f"📈 Thay đổi: {price_data['price_change_percent']}%\n"
                    
                    await event.reply(result)
                else:
                    await event.reply(f"❌ Không thể lấy dữ liệu từ API cho contract: {contract_address}")
                return
            
            # Kiểm tra lệnh test gửi tin nhắn
            if message_text == '/testmsg':
                test_messages = [
                    {
                        'text': 'Đây là tin nhắn test 1',
                        'date': datetime.now()
                    },
                    {
                        'text': 'Đây là tin nhắn test 2 với nội dung dài hơn để kiểm tra xem bot có gửi được không',
                        'date': datetime.now()
                    }
                ]
                await self.send_filtered_messages(test_messages, "TestUser")
                await event.reply("✅ Đã gửi tin nhắn test vào Saved Messages!")
                return
            
            # Kiểm tra lệnh list users trong group
            if message_text.startswith('/listusers'):
                parts = message_text.split()
                if len(parts) < 2:
                    await event.reply("❌ Format: /listusers <group_username>")
                    return
                
                group_username = parts[1]
                await event.reply(f"🔄 Đang lấy danh sách người dùng từ {group_username}...")
                
                try:
                    # Lấy tin nhắn gần đây để xem có những ai
                    messages = await self.get_group_messages(group_username, None, 50)
                    
                    # Tạo danh sách người dùng unique
                    users = {}
                    for msg in messages:
                        if msg['sender_username']:
                            users[msg['sender_username']] = {
                                'username': msg['sender_username'],
                                'first_name': msg['sender_first_name'],
                                'last_name': msg['sender_last_name']
                            }
                    
                    # Gửi danh sách
                    if users:
                        user_list = "👥 **Danh sách người dùng trong group:**\n\n"
                        for i, (username, info) in enumerate(users.items(), 1):
                            user_list += f"**{i}.** @{username}\n"
                            if info['first_name']:
                                user_list += f"   Tên: {info['first_name']}"
                            if info['last_name']:
                                user_list += f" {info['last_name']}"
                            user_list += "\n\n"
                        
                        # Chia nhỏ nếu quá dài
                        if len(user_list) > 4000:
                            parts = [user_list[i:i+4000] for i in range(0, len(user_list), 4000)]
                            for part in parts:
                                await self.client.send_message(await self.client.get_me(), part)
                                await asyncio.sleep(0.5)
                        else:
                            await self.client.send_message(await self.client.get_me(), user_list)
                        
                        await event.reply(f"✅ Đã gửi danh sách {len(users)} người dùng vào Saved Messages!")
                    else:
                        await event.reply("❌ Không tìm thấy người dùng nào trong group")
                        
                except Exception as e:
                    await event.reply(f"❌ Lỗi: {str(e)}")
                return
            
            # Kiểm tra lệnh filter_contract
            # Format: /filter_contract <group_username> [target_user] [date] [limit]
            if message_text.startswith('/filter_contract'):
                parts = message_text.split()
                if len(parts) < 2:
                    await event.reply("❌ Format không đúng!\nSử dụng: /filter_contract <group_username> [target_user] [yyyy.mm.dd] [limit]")
                    return
                
                group_username = parts[1]
                target_user = parts[2] if len(parts) > 2 and not parts[2].startswith('202') else None
                
                # Xử lý ngày và limit
                target_date = None
                limit = 50000  # Tăng limit mặc định
                
                # Xác định vị trí của ngày và limit trong parts
                date_index = 3 if target_user else 2
                limit_index = 4 if target_user else 3
                
                if len(parts) > date_index:
                    try:
                        # Kiểm tra xem tham số có phải là ngày không
                        target_date = datetime.strptime(parts[date_index], '%Y.%m.%d').date()
                        logger.info(f"Contract filter target date (UTC+7): {target_date}")
                        
                        # Nếu có tham số tiếp theo, đó là limit
                        if len(parts) > limit_index:
                            try:
                                limit = int(parts[limit_index])
                                logger.info(f"Custom limit: {limit}")
                            except ValueError:
                                await event.reply("❌ Limit phải là số!")
                                return
                                
                    except ValueError:
                        # Nếu không phải ngày, có thể là limit
                        try:
                            limit = int(parts[date_index])
                            logger.info(f"Custom limit: {limit}")
                        except ValueError:
                            await event.reply("❌ Format không đúng!\nSử dụng: /filter_contract <group_username> [target_user] [yyyy.mm.dd] [limit]")
                            return
                
                # Thông báo tìm kiếm
                if target_user:
                    if target_date:
                        await event.reply(f"🔄 Đang tìm kiếm contract address từ {target_user} trong {group_username} ngày {target_date}...")
                    else:
                        await event.reply(f"🔄 Đang tìm kiếm contract address từ {target_user} trong {group_username} hôm nay...")
                else:
                    if target_date:
                        await event.reply(f"🔄 Đang tìm kiếm tất cả contract address trong {group_username} ngày {target_date}...")
                    else:
                        await event.reply(f"🔄 Đang tìm kiếm tất cả contract address trong {group_username} hôm nay...")
                
                # Lấy tin nhắn từ group
                messages = await self.get_group_messages(group_username, target_date, limit)
                
                # Gửi thông tin debug về số tin nhắn
                await event.reply(f"📊 Tìm thấy {len(messages)} tin nhắn trong group")
                
                # Lọc tin nhắn có contract address
                if target_user:
                    # Filter theo user cụ thể (logic cũ)
                    contract_messages = self.filter_messages_with_contracts(messages, target_user)
                else:
                    # Lấy tất cả contract từ toàn bộ group
                    contract_messages = self.filter_all_messages_with_contracts(messages)
                
                # Sắp xếp theo thời gian tăng dần
                contract_messages.sort(key=lambda x: x['message']['date'])
                
                # Gửi kết quả
                await self.send_contract_analysis(contract_messages, target_user)
                
                # Gửi thông tin debug
                debug_info = f"🔧 **Contract Debug Info:**\n"
                debug_info += f"📊 Tổng tin nhắn trong group: {len(messages)}\n"
                debug_info += f"🎯 Tin nhắn có contract từ {target_user}: {len(contract_messages)}\n"
                
                total_contracts = sum(len(msg['contracts']) for msg in contract_messages)
                debug_info += f"🔗 Tổng số contract address: {total_contracts}\n"
                
                await event.reply(debug_info)
                await event.reply(f"✅ Hoàn thành! Đã tìm thấy {len(contract_messages)} tin nhắn có contract từ {target_user}\n⏰ Tin nhắn đã được sắp xếp theo thời gian tăng dần\n📱 Kiểm tra Saved Messages để xem phân tích contract!")
                
                return
            
            # Kiểm tra format tin nhắn trigger
            # Format: /filter <group_username> <target_user> [date] [limit]
            if not message_text.startswith('/filter'):
                return
            
            parts = message_text.split()
            if len(parts) < 3:
                await event.reply("❌ Format không đúng!\nSử dụng: /filter <group_username> <target_user> [yyyy.mm.dd] [limit]")
                return
            
            group_username = parts[1]
            target_user = parts[2]
            
            # Xử lý ngày
            target_date = None
            limit = 10000  # Mặc định
            
            if len(parts) > 3:
                # Kiểm tra xem tham số thứ 3 có phải là ngày không
                try:
                    # Parse format yyyy.mm.dd (được hiểu là UTC+7)
                    target_date = datetime.strptime(parts[3], '%Y.%m.%d').date()
                    logger.info(f"Target date (UTC+7): {target_date}")
                    
                    # Nếu có tham số thứ 4, đó là limit
                    if len(parts) > 4:
                        try:
                            limit = int(parts[4])
                            logger.info(f"Custom limit: {limit}")
                        except ValueError:
                            await event.reply("❌ Limit phải là số!")
                            return
                            
                except ValueError:
                    # Nếu không phải ngày, có thể là limit
                    try:
                        limit = int(parts[3])
                        logger.info(f"Custom limit: {limit}")
                    except ValueError:
                        await event.reply("❌ Format không đúng!\nSử dụng: /filter <group_username> <target_user> [yyyy.mm.dd] [limit]")
                        return
            
            # Thông báo tìm kiếm
            if target_date:
                await event.reply(f"🔄 Đang tìm kiếm tin nhắn từ {target_user} trong {group_username} ngày {target_date}...")
            else:
                await event.reply(f"🔄 Đang tìm kiếm tin nhắn từ {target_user} trong {group_username} hôm nay...")
            
            # Lấy tin nhắn từ group
            messages = await self.get_group_messages(group_username, target_date, limit)
            
            # Gửi thông tin debug về số tin nhắn
            await event.reply(f"📊 Tìm thấy {len(messages)} tin nhắn trong group")
            
            # Lọc tin nhắn theo người dùng
            filtered_messages = self.filter_messages_by_user(messages, target_user)
            
            # Sắp xếp tin nhắn theo thời gian tăng dần (từ cũ đến mới)
            filtered_messages.sort(key=lambda x: x['date'])
            
            # Gửi kết quả
            await self.send_filtered_messages(filtered_messages, target_user)
            
            # Gửi thông tin debug
            debug_info = f"🔧 **Debug Info:**\n"
            debug_info += f"📊 Tổng tin nhắn trong group: {len(messages)}\n"
            debug_info += f"🎯 Tin nhắn từ {target_user}: {len(filtered_messages)}\n"
            debug_info += f"📝 Tin nhắn có text: {sum(1 for msg in filtered_messages if msg['text'])}\n"
            debug_info += f"📎 Tin nhắn chỉ có media: {sum(1 for msg in filtered_messages if not msg['text'])}\n"
            
            await event.reply(debug_info)
            await event.reply(f"✅ Hoàn thành! Đã tìm thấy {len(filtered_messages)} tin nhắn từ {target_user}\n⏰ Tin nhắn đã được sắp xếp theo thời gian tăng dần\n📱 Kiểm tra Saved Messages để xem nội dung!")
            
        except Exception as e:
            logger.error(f"Error handling trigger message: {e}")
            await event.reply(f"❌ Lỗi: {str(e)}")
    
    async def run(self):
        """Chạy bot"""
        if not self.config:
            logger.error("Cannot load configuration")
            return
        
        if not await self.start_client():
            return
        
        # Đăng ký event handler cho tin nhắn trigger
        @self.client.on(events.NewMessage(from_users='me'))
        async def trigger_handler(event):
            await self.handle_trigger_message(event)
        
        logger.info("🤖 Bot is ready! Send /filter or /filter_contract message to start...")
        logger.info("📝 Format: /filter <group_username> <target_user> [yyyy.mm.dd] [limit]")
        logger.info("🔗 Format: /filter_contract <group_username> [target_user] [yyyy.mm.dd] [limit]")
        logger.info("💡 Example: /filter @mygroup username 2024.12.15 5000")
        logger.info("💡 Example: /filter_contract @mygroup username 2024.12.15")
        logger.info("📅 Default: No date = today's messages only (UTC+7)")
        logger.info("🧪 Commands: /test (test bot), /time (show time), /timezone (explain timezone), /testmsg (test messages), /testyesterday (test yesterday), /testuser (test username), /testrecent (test recent), /testdate (test date), /testcontract (test contract API), /listusers (list users), /debug (debug mode), /stop (stop bot)")
        logger.info("🛑 Commands: /stop or /quit to stop bot, Ctrl+C to force stop")
        
        try:
            # Chạy bot với xử lý interrupt
            await self.client.run_until_disconnected()
        except KeyboardInterrupt:
            logger.info("🛑 Bot stopped by user")
        except Exception as e:
            logger.error(f"Bot error: {e}")
        finally:
            # Đảm bảo client được đóng đúng cách
            if self.client:
                await self.client.disconnect()
                logger.info("📱 Disconnected from Telegram")

async def main():
    """Hàm main"""
    flow = TelegramFlow()
    await flow.run()

if __name__ == "__main__":
    # Tương thích với Python 3.7
    try:
        asyncio.run(main())
    except AttributeError:
        # Fallback cho Python 3.7 cũ
        loop = asyncio.get_event_loop()
        loop.run_until_complete(main())
