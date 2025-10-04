#!/usr/bin/env python3
"""
Easy Signals - Method đơn giản, dễ vào lệnh
"""

import ccxt
import pandas as pd
import ta
from datetime import datetime

class EasySignals:
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
            ohlcv = self.exchange.fetch_ohlcv(self.symbol, self.timeframe, limit=50)
            df = pd.DataFrame(ohlcv, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
            df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
            df.set_index('timestamp', inplace=True)
            return df
        except Exception as e:
            print(f"Error fetching data: {e}")
            return None
    
    def analyze_easy(self, df):
        """Easy analysis - chỉ cần 1-2 điều kiện"""
        if len(df) < 20:
            return None
        
        # Calculate indicators
        df['rsi'] = ta.momentum.RSIIndicator(df['close'], window=14).rsi()
        df['ema_5'] = ta.trend.EMAIndicator(df['close'], window=5).ema_indicator()
        df['ema_15'] = ta.trend.EMAIndicator(df['close'], window=15).ema_indicator()
        
        latest = df.iloc[-1]
        current_price = latest['close']
        rsi = latest['rsi']
        ema_5 = latest['ema_5']
        ema_15 = latest['ema_15']
        
        signal = None
        strength = 0
        
        # EASY LONG: RSI < 50 (below middle) OR EMA 5 > EMA 15
        if rsi < 50 or ema_5 > ema_15:
            signal = 'LONG'
            if rsi < 50:
                strength = (50 - rsi) / 50  # 0 to 1
            else:
                strength = 0.6  # EMA bullish
                
        # EASY SHORT: RSI > 50 (above middle) OR EMA 5 < EMA 15
        elif rsi > 50 or ema_5 < ema_15:
            signal = 'SHORT'
            if rsi > 50:
                strength = (rsi - 50) / 50  # 0 to 1
            else:
                strength = 0.6  # EMA bearish
        
        if signal and strength > 0.1:  # Very low threshold
            # Calculate TP/SL
            leverage = 5
            if signal == 'LONG':
                take_profit = current_price * (1 + 0.04)  # 4% spot
                stop_loss = current_price * (1 - 0.02)    # 2% spot
            else:
                take_profit = current_price * (1 - 0.04)  # 4% spot
                stop_loss = current_price * (1 + 0.02)    # 2% spot
            
            return {
                'direction': signal,
                'strength': strength,
                'current_price': current_price,
                'take_profit': take_profit,
                'stop_loss': stop_loss,
                'rsi': rsi,
                'ema_5': ema_5,
                'ema_15': ema_15,
                'method': 'Easy RSI+EMA'
            }
        
        return None

def test_easy_signals():
    """Test easy signals"""
    print("🧪 TESTING EASY SIGNALS")
    print("=" * 40)
    
    method = EasySignals()
    df = method.fetch_data()
    
    if df is None:
        print("❌ Failed to fetch data")
        return
    
    print(f"📊 Data points: {len(df)}")
    print(f"💰 Current price: ${df['close'].iloc[-1]:,.2f}")
    
    # Calculate indicators
    df['rsi'] = ta.momentum.RSIIndicator(df['close'], window=14).rsi()
    df['ema_5'] = ta.trend.EMAIndicator(df['close'], window=5).ema_indicator()
    df['ema_15'] = ta.trend.EMAIndicator(df['close'], window=15).ema_indicator()
    
    latest = df.iloc[-1]
    
    print(f"📈 RSI: {latest['rsi']:.2f}")
    print(f"📈 EMA 5: ${latest['ema_5']:,.2f}")
    print(f"📈 EMA 15: ${latest['ema_15']:,.2f}")
    
    # Check easy conditions
    print(f"\n🟢 EASY LONG CONDITIONS:")
    rsi_long = latest['rsi'] < 50
    ema_long = latest['ema_5'] > latest['ema_15']
    
    print(f"RSI < 50: {latest['rsi']:.2f} < 50 = {rsi_long}")
    print(f"EMA 5 > EMA 15: {latest['ema_5']:,.2f} > {latest['ema_15']:,.2f} = {ema_long}")
    
    if rsi_long or ema_long:
        print(f"✅ LONG condition met!")
    else:
        print(f"❌ LONG condition not met")
    
    print(f"\n🔴 EASY SHORT CONDITIONS:")
    rsi_short = latest['rsi'] > 50
    ema_short = latest['ema_5'] < latest['ema_15']
    
    print(f"RSI > 50: {latest['rsi']:.2f} > 50 = {rsi_short}")
    print(f"EMA 5 < EMA 15: {latest['ema_5']:,.2f} < {latest['ema_15']:,.2f} = {ema_short}")
    
    if rsi_short or ema_short:
        print(f"✅ SHORT condition met!")
    else:
        print(f"❌ SHORT condition not met")
    
    # Test the method
    signal = method.analyze_easy(df)
    if signal:
        print(f"\n✅ Method returned: {signal['direction']} (Strength: {signal['strength']:.1%})")
        print(f"💰 Entry: ${signal['current_price']:,.2f}")
        print(f"🎯 TP: ${signal['take_profit']:,.2f}")
        print(f"🛡️ SL: ${signal['stop_loss']:,.2f}")
    else:
        print(f"\n❌ Method returned: None")

if __name__ == "__main__":
    test_easy_signals()

