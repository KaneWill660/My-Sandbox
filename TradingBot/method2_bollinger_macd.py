#!/usr/bin/env python3
"""
SCALPING METHOD 2: BOLLINGER BANDS + MACD
- Bollinger Bands squeeze/expansion
- MACD momentum confirmation
- Good for breakout trading
"""

import ccxt
import pandas as pd
import numpy as np
import requests
import time
from datetime import datetime
from typing import Optional, Dict

class Method2BollingerMACD:
    def __init__(self):
        self.symbol = 'BTCUSDT'
        self.timeframe = '5m'
        self.limit = 100
        
        # Initialize exchange
        self.exchange = ccxt.binance({
            'enableRateLimit': True,
            'options': {'defaultType': 'spot'}
        })
        
        # Telegram config
        self.telegram_token = self.get_telegram_token()
        self.chat_id = '@tradingbotbykane'
        
        # Method 2 parameters
        self.bb_period = 20
        self.bb_std = 2
        self.macd_fast = 12
        self.macd_slow = 26
        self.macd_signal = 9
        
        # Risk management
        self.leverage = 5
        self.take_profit_percent = 20.0  # 20% leverage = 4% spot
        self.stop_loss_percent = 10.0    # 10% leverage = 2% spot
    
    def get_telegram_token(self):
        """Get Telegram bot token from .env file"""
        try:
            with open('.env', 'r', encoding='utf-8') as f:
                for line in f:
                    if line.startswith('TELEGRAM_BOT_TOKEN='):
                        return line.split('=', 1)[1].strip()
        except:
            pass
        return ''
    
    def fetch_data(self):
        """Fetch 5m OHLCV data"""
        try:
            ohlcv = self.exchange.fetch_ohlcv(self.symbol, self.timeframe, limit=self.limit)
            df = pd.DataFrame(ohlcv, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
            df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
            df.set_index('timestamp', inplace=True)
            return df
        except Exception as e:
            print(f"Error fetching data: {e}")
            return None
    
    def calculate_bollinger_bands(self, df, period=20, std=2):
        """Calculate Bollinger Bands"""
        sma = df['close'].rolling(window=period).mean()
        std_dev = df['close'].rolling(window=period).std()
        
        upper_band = sma + (std_dev * std)
        lower_band = sma - (std_dev * std)
        
        return upper_band, sma, lower_band
    
    def calculate_macd(self, df, fast=12, slow=26, signal=9):
        """Calculate MACD"""
        ema_fast = df['close'].ewm(span=fast).mean()
        ema_slow = df['close'].ewm(span=slow).mean()
        
        macd = ema_fast - ema_slow
        macd_signal = macd.ewm(span=signal).mean()
        macd_histogram = macd - macd_signal
        
        return macd, macd_signal, macd_histogram
    
    def analyze_method2(self, df):
        """Analyze using Bollinger Bands + MACD method"""
        if len(df) < 50:
            return None
        
        # Calculate indicators
        df['bb_upper'], df['bb_middle'], df['bb_lower'] = self.calculate_bollinger_bands(df, self.bb_period, self.bb_std)
        df['macd'], df['macd_signal'], df['macd_histogram'] = self.calculate_macd(df, self.macd_fast, self.macd_slow, self.macd_signal)
        
        latest = df.iloc[-1]
        prev = df.iloc[-2]
        
        current_price = latest['close']
        bb_upper = latest['bb_upper']
        bb_middle = latest['bb_middle']
        bb_lower = latest['bb_lower']
        macd = latest['macd']
        macd_signal = latest['macd_signal']
        macd_hist = latest['macd_histogram']
        
        # Previous values
        prev_macd = prev['macd']
        prev_macd_signal = prev['macd_signal']
        
        signal = None
        strength = 0
        
        # Calculate BB position (0 = lower band, 1 = upper band)
        bb_position = (current_price - bb_lower) / (bb_upper - bb_lower)
        
        # LONG Signal: Price near lower BB + MACD bullish crossover
        if (bb_position < 0.2 and  # Price near lower band
            macd > macd_signal and  # MACD above signal
            prev_macd <= prev_macd_signal and  # MACD crossover
            macd_hist > 0):  # MACD histogram positive
            
            # Calculate signal strength
            bb_strength = (0.2 - bb_position) / 0.2  # Closer to lower band = stronger
            macd_strength = abs(macd_hist) / abs(macd) if macd != 0 else 0
            strength = (bb_strength + macd_strength) / 2
            
            if strength > 0.3:  # Minimum threshold
                signal = 'LONG'
        
        # SHORT Signal: Price near upper BB + MACD bearish crossover
        elif (bb_position > 0.8 and  # Price near upper band
              macd < macd_signal and  # MACD below signal
              prev_macd >= prev_macd_signal and  # MACD crossover
              macd_hist < 0):  # MACD histogram negative
            
            # Calculate signal strength
            bb_strength = (bb_position - 0.8) / 0.2  # Closer to upper band = stronger
            macd_strength = abs(macd_hist) / abs(macd) if macd != 0 else 0
            strength = (bb_strength + macd_strength) / 2
            
            if strength > 0.3:  # Minimum threshold
                signal = 'SHORT'
        
        if signal:
            # Calculate TP/SL
            if signal == 'LONG':
                take_profit = current_price * (1 + self.take_profit_percent / 100 / self.leverage)
                stop_loss = current_price * (1 - self.stop_loss_percent / 100 / self.leverage)
            else:
                take_profit = current_price * (1 - self.take_profit_percent / 100 / self.leverage)
                stop_loss = current_price * (1 + self.stop_loss_percent / 100 / self.leverage)
            
            return {
                'method': 'Bollinger Bands + MACD',
                'direction': signal,
                'strength': strength,
                'current_price': current_price,
                'take_profit': take_profit,
                'stop_loss': stop_loss,
                'bb_upper': bb_upper,
                'bb_middle': bb_middle,
                'bb_lower': bb_lower,
                'bb_position': bb_position,
                'macd': macd,
                'macd_signal': macd_signal,
                'macd_histogram': macd_hist,
                'timestamp': datetime.now()
            }
        
        return None
    
    def send_telegram(self, message):
        """Send message to Telegram"""
        if not self.telegram_token:
            return False
        
        url = f"https://api.telegram.org/bot{self.telegram_token}/sendMessage"
        data = {
            'chat_id': self.chat_id,
            'text': message,
            'parse_mode': 'HTML'
        }
        
        try:
            response = requests.post(url, data=data, timeout=10)
            return response.status_code == 200
        except:
            return False
    
    def format_signal_message(self, signal):
        """Format signal for Telegram"""
        direction = signal['direction']
        emoji = "🟢" if direction == "LONG" else "🔴"
        direction_text = "MUA (LONG)" if direction == "LONG" else "BÁN (SHORT)"
        
        message = f"""
{emoji} <b>METHOD 2: BOLLINGER + MACD</b> {emoji}

📈 <b>Hướng:</b> {direction_text}
💰 <b>Giá hiện tại:</b> ${signal['current_price']:,.2f}
🎯 <b>Độ tin cậy:</b> {signal['strength']:.1%}
⚡ <b>Đòn bẩy:</b> 5X

🛡️ <b>Stop Loss:</b> ${signal['stop_loss']:,.2f} (2% spot)
🎯 <b>Take Profit:</b> ${signal['take_profit']:,.2f} (4% spot)

📊 <b>Indicators:</b>
• BB Upper: ${signal['bb_upper']:,.2f}
• BB Middle: ${signal['bb_middle']:,.2f}
• BB Lower: ${signal['bb_lower']:,.2f}
• BB Position: {signal['bb_position']:.1%}
• MACD: {signal['macd']:.4f}
• MACD Signal: {signal['macd_signal']:.4f}
• MACD Hist: {signal['macd_histogram']:.4f}

⏰ <b>Thời gian:</b> {signal['timestamp'].strftime("%d/%m/%Y %H:%M:%S")}

🤖 <i>Scalping Method 2 - Bollinger + MACD</i>"""
        
        return message
    
    def run_single_test(self):
        """Run single test"""
        print("🧪 Testing Method 2: Bollinger Bands + MACD...")
        
        # Send start notification
        start_msg = f"""
🚀 <b>METHOD 2 TEST STARTED</b> 🚀

⏰ <b>Start time:</b> {datetime.now().strftime("%d/%m/%Y %H:%M:%S")}
📊 <b>Method:</b> Bollinger Bands + MACD
🎯 <b>Target:</b> Detect breakout signals

🤖 <i>Testing BB squeeze/expansion + MACD momentum...</i>"""
        
        self.send_telegram(start_msg)
        
        # Fetch and analyze
        df = self.fetch_data()
        if df is None:
            print("❌ Failed to fetch data")
            return
        
        signal = self.analyze_method2(df)
        
        if signal:
            print(f"✅ Signal detected: {signal['direction']} with strength {signal['strength']:.1%}")
            message = self.format_signal_message(signal)
            self.send_telegram(message)
            
            # Add to position tracker
            try:
                from position_tracker import PositionTracker
                tracker = PositionTracker()
                position_id = tracker.add_position(signal)
                print(f"📊 Position added to tracker: {position_id}")
            except Exception as e:
                print(f"⚠️ Could not add to position tracker: {e}")
        else:
            print("⏳ No signal detected")
            no_signal_msg = f"""
🧪 <b>METHOD 2 TEST RESULT</b> 🧪

⏰ <b>Test time:</b> {datetime.now().strftime("%d/%m/%Y %H:%M:%S")}

⏳ <b>NO SIGNAL DETECTED</b>
📊 Market conditions not suitable for BB + MACD method
📈 BB Position: {signal['bb_position']:.1%} (need <20% or >80%)
📊 MACD: {signal['macd']:.4f}
📊 MACD Signal: {signal['macd_signal']:.4f}

🤖 <i>Scalping Method 2 - Bollinger + MACD</i>"""
            
            self.send_telegram(no_signal_msg)
        
        # Send separator
        self.send_telegram("-------------------------------------------------------------------------")

if __name__ == "__main__":
    bot = Method2BollingerMACD()
    bot.run_single_test()
