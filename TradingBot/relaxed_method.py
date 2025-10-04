#!/usr/bin/env python3
"""
Relaxed Method - Method đơn giản hơn, dễ vào lệnh
"""

import ccxt
import pandas as pd
import ta
from datetime import datetime

class RelaxedMethod:
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
    
    def analyze_relaxed(self, df):
        """Relaxed analysis - điều kiện đơn giản hơn"""
        if len(df) < 20:
            return None
        
        # Calculate indicators
        df['rsi'] = ta.momentum.RSIIndicator(df['close'], window=14).rsi()
        df['ema_5'] = ta.trend.EMAIndicator(df['close'], window=5).ema_indicator()
        df['ema_15'] = ta.trend.EMAIndicator(df['close'], window=15).ema_indicator()
        
        latest = df.iloc[-1]
        prev = df.iloc[-2]
        
        current_price = latest['close']
        rsi = latest['rsi']
        ema_5 = latest['ema_5']
        ema_15 = latest['ema_15']
        prev_ema_5 = prev['ema_5']
        prev_ema_15 = prev['ema_15']
        
        signal = None
        strength = 0
        
        # RELAXED LONG: RSI < 40 OR EMA crossover
        if rsi < 40 or (ema_5 > ema_15 and prev_ema_5 <= prev_ema_15):
            signal = 'LONG'
            if rsi < 40:
                strength = (40 - rsi) / 40  # 0 to 1
            else:
                strength = 0.5  # EMA crossover
                
        # RELAXED SHORT: RSI > 60 OR EMA crossover
        elif rsi > 60 or (ema_5 < ema_15 and prev_ema_5 >= prev_ema_15):
            signal = 'SHORT'
            if rsi > 60:
                strength = (rsi - 60) / 40  # 0 to 1
            else:
                strength = 0.5  # EMA crossover
        
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
                'method': 'Relaxed RSI+EMA'
            }
        
        return None

def test_relaxed_method():
    """Test relaxed method"""
    print("🧪 TESTING RELAXED METHOD")
    print("=" * 40)
    
    method = RelaxedMethod()
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
    prev = df.iloc[-2]
    
    print(f"📈 RSI: {latest['rsi']:.2f}")
    print(f"📈 EMA 5: ${latest['ema_5']:,.2f}")
    print(f"📈 EMA 15: ${latest['ema_15']:,.2f}")
    
    # Check relaxed conditions
    print(f"\n🟢 RELAXED LONG CONDITIONS:")
    rsi_long = latest['rsi'] < 40
    ema_long = latest['ema_5'] > latest['ema_15'] and prev['ema_5'] <= prev['ema_15']
    
    print(f"RSI < 40: {latest['rsi']:.2f} < 40 = {rsi_long}")
    print(f"EMA crossover: {prev['ema_5']:,.2f} <= {prev['ema_15']:,.2f} → {latest['ema_5']:,.2f} > {latest['ema_15']:,.2f} = {ema_long}")
    
    if rsi_long or ema_long:
        print(f"✅ LONG condition met!")
    else:
        print(f"❌ LONG condition not met")
    
    print(f"\n🔴 RELAXED SHORT CONDITIONS:")
    rsi_short = latest['rsi'] > 60
    ema_short = latest['ema_5'] < latest['ema_15'] and prev['ema_5'] >= prev['ema_15']
    
    print(f"RSI > 60: {latest['rsi']:.2f} > 60 = {rsi_short}")
    print(f"EMA crossover: {prev['ema_5']:,.2f} >= {prev['ema_15']:,.2f} → {latest['ema_5']:,.2f} < {latest['ema_15']:,.2f} = {ema_short}")
    
    if rsi_short or ema_short:
        print(f"✅ SHORT condition met!")
    else:
        print(f"❌ SHORT condition not met")
    
    # Test the method
    signal = method.analyze_relaxed(df)
    if signal:
        print(f"\n✅ Method returned: {signal['direction']} (Strength: {signal['strength']:.1%})")
        print(f"💰 Entry: ${signal['current_price']:,.2f}")
        print(f"🎯 TP: ${signal['take_profit']:,.2f}")
        print(f"🛡️ SL: ${signal['stop_loss']:,.2f}")
    else:
        print(f"\n❌ Method returned: None")

if __name__ == "__main__":
    test_relaxed_method()

