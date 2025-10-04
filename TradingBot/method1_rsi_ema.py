#!/usr/bin/env python3
"""
SCALPING METHOD 1: RSI + EMA CROSSOVER
- RSI oversold/overbought confirmation
- EMA 5 cắt EMA 15
- Simple but effective
"""

import ccxt
import pandas as pd
import numpy as np
import requests
import time
from datetime import datetime
from typing import Optional, Dict

class Method1RSIEMA:
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
        
        # Method 1 parameters
        self.rsi_period = 14
        self.ema_short = 5
        self.ema_long = 15
        self.rsi_oversold = 30
        self.rsi_overbought = 70
        
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
    
    def calculate_rsi(self, df, period=14):
        """Calculate RSI"""
        delta = df['close'].diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
        rs = gain / loss
        rsi = 100 - (100 / (1 + rs))
        return rsi
    
    def calculate_ema(self, df, period):
        """Calculate EMA"""
        return df['close'].ewm(span=period).mean()
    
    def analyze_method1(self, df):
        """Analyze using RSI + EMA crossover method"""
        if len(df) < 50:
            return None
        
        # Calculate indicators
        df['rsi'] = self.calculate_rsi(df, self.rsi_period)
        df['ema_short'] = self.calculate_ema(df, self.ema_short)
        df['ema_long'] = self.calculate_ema(df, self.ema_long)
        
        latest = df.iloc[-1]
        prev = df.iloc[-2]
        
        current_price = latest['close']
        rsi = latest['rsi']
        ema_short = latest['ema_short']
        ema_long = latest['ema_long']
        
        # Previous values for crossover detection
        prev_ema_short = prev['ema_short']
        prev_ema_long = prev['ema_long']
        
        signal = None
        strength = 0
        
        # LONG Signal: RSI oversold + EMA bullish crossover
        if (rsi < self.rsi_oversold and 
            ema_short > ema_long and 
            prev_ema_short <= prev_ema_long and
            current_price > ema_short):
            
            # Calculate signal strength
            rsi_strength = (self.rsi_oversold - rsi) / self.rsi_oversold
            ema_strength = (ema_short - ema_long) / ema_long
            strength = (rsi_strength + ema_strength) / 2
            
            if strength > 0.3:  # Minimum threshold
                signal = 'LONG'
        
        # SHORT Signal: RSI overbought + EMA bearish crossover
        elif (rsi > self.rsi_overbought and 
              ema_short < ema_long and 
              prev_ema_short >= prev_ema_long and
              current_price < ema_short):
            
            # Calculate signal strength
            rsi_strength = (rsi - self.rsi_overbought) / (100 - self.rsi_overbought)
            ema_strength = (ema_long - ema_short) / ema_long
            strength = (rsi_strength + ema_strength) / 2
            
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
                'method': 'RSI + EMA Crossover',
                'direction': signal,
                'strength': strength,
                'current_price': current_price,
                'take_profit': take_profit,
                'stop_loss': stop_loss,
                'rsi': rsi,
                'ema_short': ema_short,
                'ema_long': ema_long,
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
{emoji} <b>METHOD 1: RSI + EMA CROSSOVER</b> {emoji}

📈 <b>Hướng:</b> {direction_text}
💰 <b>Giá hiện tại:</b> ${signal['current_price']:,.2f}
🎯 <b>Độ tin cậy:</b> {signal['strength']:.1%}
⚡ <b>Đòn bẩy:</b> 5X

🛡️ <b>Stop Loss:</b> ${signal['stop_loss']:,.2f} (2% spot)
🎯 <b>Take Profit:</b> ${signal['take_profit']:,.2f} (4% spot)

📊 <b>Indicators:</b>
• RSI: {signal['rsi']:.1f}
• EMA 5: ${signal['ema_short']:,.2f}
• EMA 15: ${signal['ema_long']:,.2f}

⏰ <b>Thời gian:</b> {signal['timestamp'].strftime("%d/%m/%Y %H:%M:%S")}

🤖 <i>Scalping Method 1 - RSI + EMA</i>"""
        
        return message
    
    def run_single_test(self):
        """Run single test"""
        print("🧪 Testing Method 1: RSI + EMA Crossover...")
        
        # Send start notification
        start_msg = f"""
🚀 <b>METHOD 1 TEST STARTED</b> 🚀

⏰ <b>Start time:</b> {datetime.now().strftime("%d/%m/%Y %H:%M:%S")}
📊 <b>Method:</b> RSI + EMA Crossover
🎯 <b>Target:</b> Detect scalping signals

🤖 <i>Testing RSI oversold/overbought + EMA crossover...</i>"""
        
        self.send_telegram(start_msg)
        
        # Fetch and analyze
        df = self.fetch_data()
        if df is None:
            print("❌ Failed to fetch data")
            return
        
        signal = self.analyze_method1(df)
        
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
🧪 <b>METHOD 1 TEST RESULT</b> 🧪

⏰ <b>Test time:</b> {datetime.now().strftime("%d/%m/%Y %H:%M:%S")}

⏳ <b>NO SIGNAL DETECTED</b>
📊 Market conditions not suitable for RSI + EMA method
🎯 RSI: {df.iloc[-1]['rsi']:.1f} (need <30 or >70)
📈 EMA 5: ${df.iloc[-1]['ema_short']:,.2f}
📈 EMA 15: ${df.iloc[-1]['ema_long']:,.2f}

🤖 <i>Scalping Method 1 - RSI + EMA</i>"""
            
            self.send_telegram(no_signal_msg)
        
        # Send separator
        self.send_telegram("-------------------------------------------------------------------------")

if __name__ == "__main__":
    bot = Method1RSIEMA()
    bot.run_single_test()
