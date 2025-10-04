#!/usr/bin/env python3
"""
Test Binance data fetching to verify data accuracy
"""

import ccxt
import pandas as pd
import requests
from datetime import datetime
import time

class BinanceDataTester:
    def __init__(self):
        self.symbol = 'BTCUSDT'
        self.timeframe = '5m'
        self.limit = 10  # Just get last 10 candles for testing
        
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
    
    def fetch_binance_data(self):
        """Fetch data from Binance"""
        try:
            print(f"📊 Fetching {self.symbol} {self.timeframe} data from Binance...")
            ohlcv = self.exchange.fetch_ohlcv(self.symbol, self.timeframe, limit=self.limit)
            
            if not ohlcv:
                print("❌ No data received from Binance")
                return None
            
            # Convert to DataFrame
            df = pd.DataFrame(ohlcv, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
            df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
            df.set_index('timestamp', inplace=True)
            
            print(f"✅ Successfully fetched {len(df)} candles")
            return df
            
        except Exception as e:
            print(f"❌ Error fetching data: {e}")
            return None
    
    def get_current_price(self):
        """Get current price from ticker"""
        try:
            ticker = self.exchange.fetch_ticker(self.symbol)
            return ticker['last']
        except Exception as e:
            print(f"❌ Error getting current price: {e}")
            return None
    
    def verify_data_accuracy(self, df):
        """Verify data accuracy by comparing with current price"""
        if df is None or len(df) == 0:
            return False
        
        # Get current price
        current_price = self.get_current_price()
        if current_price is None:
            return False
        
        # Get latest candle data
        latest_candle = df.iloc[-1]
        latest_close = latest_candle['close']
        
        # Calculate price difference
        price_diff = abs(current_price - latest_close)
        price_diff_percent = (price_diff / current_price) * 100
        
        print(f"\n📊 DATA VERIFICATION:")
        print(f"Current Price: ${current_price:,.2f}")
        print(f"Latest Candle Close: ${latest_close:,.2f}")
        print(f"Price Difference: ${price_diff:,.2f} ({price_diff_percent:.3f}%)")
        
        # Data is considered accurate if difference is less than 0.1%
        is_accurate = price_diff_percent < 0.1
        
        if is_accurate:
            print("✅ Data is ACCURATE")
        else:
            print("⚠️ Data might be DELAYED or INACCURATE")
        
        return is_accurate, current_price, latest_close, price_diff_percent
    
    def analyze_data_quality(self, df):
        """Analyze data quality"""
        if df is None or len(df) == 0:
            return None
        
        print(f"\n📈 DATA QUALITY ANALYSIS:")
        print(f"Total candles: {len(df)}")
        print(f"Time range: {df.index[0]} to {df.index[-1]}")
        print(f"Timeframe: {self.timeframe}")
        
        # Check for missing data
        expected_interval = pd.Timedelta(minutes=5) if self.timeframe == '5m' else pd.Timedelta(hours=1)
        time_diffs = df.index.to_series().diff().dropna()
        missing_periods = (time_diffs > expected_interval * 1.5).sum()
        
        print(f"Missing periods: {missing_periods}")
        
        # Price statistics
        latest = df.iloc[-1]
        print(f"\n💰 LATEST CANDLE:")
        print(f"Open: ${latest['open']:,.2f}")
        print(f"High: ${latest['high']:,.2f}")
        print(f"Low: ${latest['low']:,.2f}")
        print(f"Close: ${latest['close']:,.2f}")
        print(f"Volume: {latest['volume']:,.0f}")
        
        # Price change
        if len(df) > 1:
            prev_close = df.iloc[-2]['close']
            price_change = latest['close'] - prev_close
            price_change_percent = (price_change / prev_close) * 100
            print(f"Price change: ${price_change:,.2f} ({price_change_percent:+.2f}%)")
        
        return {
            'total_candles': len(df),
            'time_range': f"{df.index[0]} to {df.index[-1]}",
            'missing_periods': missing_periods,
            'latest_price': latest['close'],
            'price_change_percent': price_change_percent if len(df) > 1 else 0
        }
    
    def send_data_report(self, df, is_accurate, current_price, latest_close, price_diff_percent, quality_data):
        """Send data report to Telegram"""
        if not self.telegram_token:
            return
        
        accuracy_status = "✅ ACCURATE" if is_accurate else "⚠️ DELAYED"
        accuracy_emoji = "✅" if is_accurate else "⚠️"
        
        message = f"""
{accuracy_emoji} <b>BINANCE DATA TEST REPORT</b> {accuracy_emoji}

⏰ <b>Test time:</b> {datetime.now().strftime("%d/%m/%Y %H:%M:%S")}

📊 <b>Data Accuracy:</b> {accuracy_status}
💰 <b>Current Price:</b> ${current_price:,.2f}
📈 <b>Latest Candle:</b> ${latest_close:,.2f}
📊 <b>Difference:</b> {price_diff_percent:.3f}%

📈 <b>Data Quality:</b>
• Total candles: {quality_data['total_candles']}
• Time range: {quality_data['time_range']}
• Missing periods: {quality_data['missing_periods']}
• Price change: {quality_data['price_change_percent']:+.2f}%

🎯 <b>Symbol:</b> {self.symbol}
⏱️ <b>Timeframe:</b> {self.timeframe}

🤖 <i>Binance Data Verification</i>"""
        
        self.send_telegram(message)
        self.send_telegram("-------------------------------------------------------------------------")
    
    def run_data_test(self):
        """Run complete data test"""
        print("🧪 BINANCE DATA TEST")
        print("=" * 50)
        
        # Send start notification
        start_msg = f"""
🧪 <b>BINANCE DATA TEST STARTED</b> 🧪

⏰ <b>Start time:</b> {datetime.now().strftime("%d/%m/%Y %H:%M:%S")}
🎯 <b>Symbol:</b> {self.symbol}
⏱️ <b>Timeframe:</b> {self.timeframe}
📊 <b>Testing:</b> Data accuracy and quality

🤖 <i>Verifying Binance data connection...</i>"""
        
        self.send_telegram(start_msg)
        
        # Fetch data
        df = self.fetch_binance_data()
        
        if df is None:
            error_msg = """
❌ <b>BINANCE DATA TEST FAILED</b> ❌

⏰ <b>Test time:</b> {time}

❌ <b>Error:</b> Failed to fetch data from Binance
🔧 <b>Possible causes:</b>
• Network connection issues
• Binance API rate limiting
• Invalid symbol or timeframe

🤖 <i>Binance Data Verification</i>""".format(time=datetime.now().strftime("%d/%m/%Y %H:%M:%S"))
            
            self.send_telegram(error_msg)
            return
        
        # Verify accuracy
        is_accurate, current_price, latest_close, price_diff_percent = self.verify_data_accuracy(df)
        
        # Analyze quality
        quality_data = self.analyze_data_quality(df)
        
        # Send report
        self.send_data_report(df, is_accurate, current_price, latest_close, price_diff_percent, quality_data)
        
        print("\n✅ Data test completed!")
        return df

def main():
    tester = BinanceDataTester()
    tester.run_data_test()

if __name__ == "__main__":
    main()

