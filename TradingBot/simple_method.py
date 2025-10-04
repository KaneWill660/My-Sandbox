#!/usr/bin/env python3
"""
Simple Method - Method đơn giản để test
"""

import ccxt
import pandas as pd
import ta
from datetime import datetime

class SimpleMethod:
    def __init__(self):
        self.symbol = 'BTCUSDT'
        self.timeframe = '5m'
        self.exchange = ccxt.binance({
            'enableRateLimit': True,
            'options': {'defaultType': 'spot'}
        })
    
    def fetch_data(self):
        """Fetch OHLCV data"""
        try:
            ohlcv = self.exchange.fetch_ohlcv(self.symbol, self.timeframe, limit=100)
            df = pd.DataFrame(ohlcv, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
            df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
            df.set_index('timestamp', inplace=True)
            return df
        except Exception as e:
            print(f"Error fetching data: {e}")
            return None
    
    def analyze_simple(self, df):
        """Simple analysis - chỉ cần RSI oversold/overbought"""
        if len(df) < 20:
            return None
        
        # Calculate RSI
        df['rsi'] = ta.momentum.RSIIndicator(df['close'], window=14).rsi()
        
        latest = df.iloc[-1]
        current_price = latest['close']
        rsi = latest['rsi']
        
        signal = None
        strength = 0
        
        # Very simple conditions
        if rsi < 30:  # Oversold
            signal = 'LONG'
            strength = (30 - rsi) / 30  # 0 to 1
        elif rsi > 70:  # Overbought
            signal = 'SHORT'
            strength = (rsi - 70) / 30  # 0 to 1
        
        if signal and strength > 0.1:  # Very low threshold
            return {
                'direction': signal,
                'strength': strength,
                'current_price': current_price,
                'rsi': rsi,
                'method': 'Simple RSI'
            }
        
        return None

def test_simple_method():
    """Test simple method"""
    print("🧪 TESTING SIMPLE METHOD")
    print("=" * 40)
    
    method = SimpleMethod()
    df = method.fetch_data()
    
    if df is None:
        print("❌ Failed to fetch data")
        return
    
    print(f"📊 Data points: {len(df)}")
    print(f"💰 Current price: ${df['close'].iloc[-1]:,.2f}")
    
    # Calculate RSI
    df['rsi'] = ta.momentum.RSIIndicator(df['close'], window=14).rsi()
    latest = df.iloc[-1]
    
    print(f"📈 RSI: {latest['rsi']:.2f}")
    
    # Test simple conditions
    if latest['rsi'] < 30:
        print(f"🟢 RSI OVERSOLD: {latest['rsi']:.2f} < 30")
        strength = (30 - latest['rsi']) / 30
        print(f"🎯 LONG signal strength: {strength:.3f}")
        if strength > 0.1:
            print(f"🚀 SIMPLE LONG SIGNAL!")
        else:
            print(f"⚠️ Signal too weak")
    elif latest['rsi'] > 70:
        print(f"🔴 RSI OVERBOUGHT: {latest['rsi']:.2f} > 70")
        strength = (latest['rsi'] - 70) / 30
        print(f"🎯 SHORT signal strength: {strength:.3f}")
        if strength > 0.1:
            print(f"🚀 SIMPLE SHORT SIGNAL!")
        else:
            print(f"⚠️ Signal too weak")
    else:
        print(f"⚪ RSI NEUTRAL: {latest['rsi']:.2f} (30-70)")
    
    # Test the method
    signal = method.analyze_simple(df)
    if signal:
        print(f"\n✅ Method returned: {signal['direction']} (Strength: {signal['strength']:.1%})")
    else:
        print(f"\n❌ Method returned: None")

if __name__ == "__main__":
    test_simple_method()

