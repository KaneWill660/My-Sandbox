#!/usr/bin/env python3
"""
Test indicators calculation on 5m data to verify accuracy
"""

import ccxt
import pandas as pd
import numpy as np
import requests
from datetime import datetime

class Indicators5mTester:
    def __init__(self):
        self.symbol = 'BTCUSDT'
        self.timeframe = '5m'  # 5 minute timeframe
        self.limit = 100
        
        # Initialize exchange
        self.exchange = ccxt.binance({
            'enableRateLimit': True,
            'options': {'defaultType': 'spot'}
        })
        
        # Telegram config
        self.telegram_token = self.get_telegram_token()
        self.chat_id = '@tradingbotbykane'
    
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
    
    def send_telegram(self, message):
        """Send message to Telegram"""
        if not self.telegram_token:
            print("Telegram not configured")
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
    
    def fetch_5m_data(self):
        """Fetch 5m OHLCV data"""
        try:
            print(f"📊 Fetching {self.symbol} {self.timeframe} data...")
            ohlcv = self.exchange.fetch_ohlcv(self.symbol, self.timeframe, limit=self.limit)
            
            if not ohlcv:
                print("❌ No data received")
                return None
            
            # Convert to DataFrame
            df = pd.DataFrame(ohlcv, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
            df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
            df.set_index('timestamp', inplace=True)
            
            print(f"✅ Successfully fetched {len(df)} candles")
            print(f"📅 Time range: {df.index[0]} to {df.index[-1]}")
            print(f"⏱️ Timeframe: {self.timeframe}")
            
            return df
            
        except Exception as e:
            print(f"❌ Error fetching data: {e}")
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
    
    def test_all_indicators(self, df):
        """Test all indicators on 5m data"""
        if df is None or len(df) < 50:
            print("❌ Insufficient data for indicator calculation")
            return None
        
        print(f"\n🧮 CALCULATING INDICATORS ON {self.timeframe} DATA:")
        
        # Calculate all indicators
        df['rsi'] = self.calculate_rsi(df, 14)
        df['ema_5'] = self.calculate_ema(df, 5)
        df['ema_15'] = self.calculate_ema(df, 15)
        df['bb_upper'], df['bb_middle'], df['bb_lower'] = self.calculate_bollinger_bands(df, 20, 2)
        df['macd'], df['macd_signal'], df['macd_histogram'] = self.calculate_macd(df, 12, 26, 9)
        
        # Get latest values
        latest = df.iloc[-1]
        
        print(f"📊 LATEST INDICATORS VALUES:")
        print(f"RSI (14): {latest['rsi']:.2f}")
        print(f"EMA 5: ${latest['ema_5']:,.2f}")
        print(f"EMA 15: ${latest['ema_15']:,.2f}")
        print(f"BB Upper: ${latest['bb_upper']:,.2f}")
        print(f"BB Middle: ${latest['bb_middle']:,.2f}")
        print(f"BB Lower: ${latest['bb_lower']:,.2f}")
        print(f"MACD: {latest['macd']:.6f}")
        print(f"MACD Signal: {latest['macd_signal']:.6f}")
        print(f"MACD Histogram: {latest['macd_histogram']:.6f}")
        
        # Check for valid values
        valid_indicators = []
        if not pd.isna(latest['rsi']):
            valid_indicators.append("RSI")
        if not pd.isna(latest['ema_5']):
            valid_indicators.append("EMA 5")
        if not pd.isna(latest['ema_15']):
            valid_indicators.append("EMA 15")
        if not pd.isna(latest['bb_upper']):
            valid_indicators.append("Bollinger Bands")
        if not pd.isna(latest['macd']):
            valid_indicators.append("MACD")
        
        print(f"\n✅ Valid indicators: {', '.join(valid_indicators)}")
        
        return latest
    
    def analyze_signal_conditions(self, latest):
        """Analyze current signal conditions"""
        print(f"\n🎯 SIGNAL CONDITIONS ANALYSIS:")
        
        # RSI conditions
        rsi = latest['rsi']
        if rsi < 30:
            rsi_condition = "OVERSOLD (LONG signal possible)"
        elif rsi > 70:
            rsi_condition = "OVERBOUGHT (SHORT signal possible)"
        else:
            rsi_condition = "NEUTRAL"
        print(f"RSI: {rsi:.1f} - {rsi_condition}")
        
        # EMA conditions
        ema_5 = latest['ema_5']
        ema_15 = latest['ema_15']
        price = latest['close']
        
        if ema_5 > ema_15 and price > ema_5:
            ema_condition = "BULLISH (LONG signal possible)"
        elif ema_5 < ema_15 and price < ema_5:
            ema_condition = "BEARISH (SHORT signal possible)"
        else:
            ema_condition = "NEUTRAL"
        print(f"EMA: {ema_condition}")
        
        # Bollinger Bands conditions
        bb_upper = latest['bb_upper']
        bb_lower = latest['bb_lower']
        bb_position = (price - bb_lower) / (bb_upper - bb_lower)
        
        if bb_position < 0.2:
            bb_condition = "NEAR LOWER BAND (LONG signal possible)"
        elif bb_position > 0.8:
            bb_condition = "NEAR UPPER BAND (SHORT signal possible)"
        else:
            bb_condition = "MIDDLE RANGE"
        print(f"Bollinger: {bb_condition} (Position: {bb_position:.1%})")
        
        # MACD conditions
        macd = latest['macd']
        macd_signal = latest['macd_signal']
        macd_hist = latest['macd_histogram']
        
        if macd > macd_signal and macd_hist > 0:
            macd_condition = "BULLISH (LONG signal possible)"
        elif macd < macd_signal and macd_hist < 0:
            macd_condition = "BEARISH (SHORT signal possible)"
        else:
            macd_condition = "NEUTRAL"
        print(f"MACD: {macd_condition}")
        
        return {
            'rsi_condition': rsi_condition,
            'ema_condition': ema_condition,
            'bb_condition': bb_condition,
            'macd_condition': macd_condition,
            'bb_position': bb_position
        }
    
    def send_indicators_report(self, latest, conditions):
        """Send indicators report to Telegram"""
        if not self.telegram_token:
            return
        
        message = f"""
🧮 <b>INDICATORS TEST ON 5M DATA</b> 🧮

⏰ <b>Test time:</b> {datetime.now().strftime("%d/%m/%Y %H:%M:%S")}
🎯 <b>Symbol:</b> {self.symbol}
⏱️ <b>Timeframe:</b> {self.timeframe}

📊 <b>Latest Indicators:</b>
• RSI (14): {latest['rsi']:.2f}
• EMA 5: ${latest['ema_5']:,.2f}
• EMA 15: ${latest['ema_15']:,.2f}
• BB Upper: ${latest['bb_upper']:,.2f}
• BB Middle: ${latest['bb_middle']:,.2f}
• BB Lower: ${latest['bb_lower']:,.2f}
• MACD: {latest['macd']:.6f}
• MACD Signal: {latest['macd_signal']:.6f}
• MACD Hist: {latest['macd_histogram']:.6f}

🎯 <b>Signal Conditions:</b>
• RSI: {conditions['rsi_condition']}
• EMA: {conditions['ema_condition']}
• Bollinger: {conditions['bb_condition']}
• MACD: {conditions['macd_condition']}

💰 <b>Current Price:</b> ${latest['close']:,.2f}

🤖 <i>5M Indicators Verification</i>"""
        
        self.send_telegram(message)
        self.send_telegram("-------------------------------------------------------------------------")
    
    def run_indicators_test(self):
        """Run complete indicators test"""
        print("🧮 INDICATORS TEST ON 5M DATA")
        print("=" * 50)
        
        # Send start notification
        start_msg = f"""
🧮 <b>INDICATORS TEST STARTED</b> 🧮

⏰ <b>Start time:</b> {datetime.now().strftime("%d/%m/%Y %H:%M:%S")}
🎯 <b>Symbol:</b> {self.symbol}
⏱️ <b>Timeframe:</b> {self.timeframe}
📊 <b>Testing:</b> RSI, EMA, Bollinger, MACD on 5m data

🤖 <i>Calculating indicators on 5-minute candles...</i>"""
        
        self.send_telegram(start_msg)
        
        # Fetch 5m data
        df = self.fetch_5m_data()
        
        if df is None:
            error_msg = """
❌ <b>INDICATORS TEST FAILED</b> ❌

⏰ <b>Test time:</b> {time}

❌ <b>Error:</b> Failed to fetch 5m data from Binance

🤖 <i>5M Indicators Verification</i>""".format(time=datetime.now().strftime("%d/%m/%Y %H:%M:%S"))
            
            self.send_telegram(error_msg)
            return
        
        # Test indicators
        latest = self.test_all_indicators(df)
        
        if latest is None:
            return
        
        # Analyze signal conditions
        conditions = self.analyze_signal_conditions(latest)
        
        # Send report
        self.send_indicators_report(latest, conditions)
        
        print("\n✅ Indicators test completed!")
        return latest

def main():
    tester = Indicators5mTester()
    tester.run_indicators_test()

if __name__ == "__main__":
    main()

