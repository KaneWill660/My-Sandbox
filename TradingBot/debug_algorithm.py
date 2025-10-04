#!/usr/bin/env python3
"""
Debug Algorithm - Kiểm tra thuật toán có hoạt động đúng không
"""

import ccxt
import pandas as pd
import ta
from datetime import datetime
from method1_rsi_ema import Method1RSIEMA
from method2_bollinger_macd import Method2BollingerMACD

def debug_method1():
    """Debug Method 1 - RSI + EMA"""
    print("🔍 DEBUGGING METHOD 1: RSI + EMA")
    print("=" * 50)
    
    method1 = Method1RSIEMA()
    df = method1.fetch_data()
    
    if df is None:
        print("❌ Failed to fetch data")
        return
    
    print(f"📊 Data points: {len(df)}")
    print(f"💰 Current price: ${df['close'].iloc[-1]:,.2f}")
    
    # Calculate indicators manually
    df['rsi'] = method1.calculate_rsi(df, method1.rsi_period)
    df['ema_short'] = method1.calculate_ema(df, method1.ema_short)
    df['ema_long'] = method1.calculate_ema(df, method1.ema_long)
    
    latest = df.iloc[-1]
    prev = df.iloc[-2]
    
    print(f"\n📈 INDICATORS:")
    print(f"RSI: {latest['rsi']:.2f}")
    print(f"EMA 5: ${latest['ema_short']:,.2f}")
    print(f"EMA 15: ${latest['ema_long']:,.2f}")
    print(f"EMA 5 (prev): ${prev['ema_short']:,.2f}")
    print(f"EMA 15 (prev): ${prev['ema_long']:,.2f}")
    
    # Check conditions step by step
    print(f"\n🟢 LONG CONDITIONS:")
    rsi_oversold = latest['rsi'] < method1.rsi_oversold
    ema_bullish = latest['ema_short'] > latest['ema_long']
    ema_crossover = prev['ema_short'] <= prev['ema_long']
    price_above_ema = latest['close'] > latest['ema_short']
    
    print(f"RSI < 30: {latest['rsi']:.2f} < 30 = {rsi_oversold}")
    print(f"EMA 5 > EMA 15: {latest['ema_short']:,.2f} > {latest['ema_long']:,.2f} = {ema_bullish}")
    print(f"EMA crossover: {prev['ema_short']:,.2f} <= {prev['ema_long']:,.2f} = {ema_crossover}")
    print(f"Price > EMA 5: {latest['close']:,.2f} > {latest['ema_short']:,.2f} = {price_above_ema}")
    
    if rsi_oversold and ema_bullish and ema_crossover and price_above_ema:
        rsi_strength = (method1.rsi_oversold - latest['rsi']) / method1.rsi_oversold
        ema_strength = (latest['ema_short'] - latest['ema_long']) / latest['ema_long']
        strength = (rsi_strength + ema_strength) / 2
        print(f"✅ LONG signal strength: {strength:.3f}")
        if strength > 0.2:
            print(f"🚀 LONG SIGNAL ACTIVE!")
        else:
            print(f"⚠️ Signal too weak (need > 0.2)")
    else:
        print(f"❌ LONG conditions not met")
    
    print(f"\n🔴 SHORT CONDITIONS:")
    rsi_overbought = latest['rsi'] > method1.rsi_overbought
    ema_bearish = latest['ema_short'] < latest['ema_long']
    ema_crossover_short = prev['ema_short'] >= prev['ema_long']
    price_below_ema = latest['close'] < latest['ema_short']
    
    print(f"RSI > 70: {latest['rsi']:.2f} > 70 = {rsi_overbought}")
    print(f"EMA 5 < EMA 15: {latest['ema_short']:,.2f} < {latest['ema_long']:,.2f} = {ema_bearish}")
    print(f"EMA crossover: {prev['ema_short']:,.2f} >= {prev['ema_long']:,.2f} = {ema_crossover_short}")
    print(f"Price < EMA 5: {latest['close']:,.2f} < {latest['ema_short']:,.2f} = {price_below_ema}")
    
    if rsi_overbought and ema_bearish and ema_crossover_short and price_below_ema:
        rsi_strength = (latest['rsi'] - method1.rsi_overbought) / (100 - method1.rsi_overbought)
        ema_strength = (latest['ema_long'] - latest['ema_short']) / latest['ema_long']
        strength = (rsi_strength + ema_strength) / 2
        print(f"✅ SHORT signal strength: {strength:.3f}")
        if strength > 0.2:
            print(f"🚀 SHORT SIGNAL ACTIVE!")
        else:
            print(f"⚠️ Signal too weak (need > 0.2)")
    else:
        print(f"❌ SHORT conditions not met")
    
    # Test the actual method
    print(f"\n🧪 TESTING ACTUAL METHOD:")
    signal = method1.analyze_method1(df)
    if signal:
        print(f"✅ Method returned: {signal['direction']} (Strength: {signal['strength']:.1%})")
    else:
        print(f"❌ Method returned: None")

def debug_method2():
    """Debug Method 2 - Bollinger + MACD"""
    print("\n🔍 DEBUGGING METHOD 2: BOLLINGER + MACD")
    print("=" * 50)
    
    method2 = Method2BollingerMACD()
    df = method2.fetch_data()
    
    if df is None:
        print("❌ Failed to fetch data")
        return
    
    print(f"📊 Data points: {len(df)}")
    print(f"💰 Current price: ${df['close'].iloc[-1]:,.2f}")
    
    # Calculate indicators manually
    df['bb_upper'], df['bb_middle'], df['bb_lower'] = method2.calculate_bollinger_bands(df, method2.bb_period, method2.bb_std)
    df['macd'], df['macd_signal'], df['macd_histogram'] = method2.calculate_macd(df, method2.macd_fast, method2.macd_slow, method2.macd_signal)
    
    latest = df.iloc[-1]
    prev = df.iloc[-2]
    
    print(f"\n📊 INDICATORS:")
    print(f"BB Upper: ${latest['bb_upper']:,.2f}")
    print(f"BB Middle: ${latest['bb_middle']:,.2f}")
    print(f"BB Lower: ${latest['bb_lower']:,.2f}")
    print(f"MACD: {latest['macd']:.4f}")
    print(f"MACD Signal: {latest['macd_signal']:.4f}")
    print(f"MACD Histogram: {latest['macd_histogram']:.4f}")
    
    # Calculate BB position
    bb_position = (latest['close'] - latest['bb_lower']) / (latest['bb_upper'] - latest['bb_lower'])
    print(f"BB Position: {bb_position:.3f} (0=lower, 1=upper)")
    
    # Check conditions step by step
    print(f"\n🟢 LONG CONDITIONS:")
    bb_low = bb_position < 0.2
    macd_bullish = latest['macd'] > latest['macd_signal']
    macd_crossover = prev['macd'] <= prev['macd_signal']
    macd_hist_positive = latest['macd_histogram'] > 0
    
    print(f"BB Position < 0.2: {bb_position:.3f} < 0.2 = {bb_low}")
    print(f"MACD > Signal: {latest['macd']:.4f} > {latest['macd_signal']:.4f} = {macd_bullish}")
    print(f"MACD crossover: {prev['macd']:.4f} <= {prev['macd_signal']:.4f} = {macd_crossover}")
    print(f"MACD Hist > 0: {latest['macd_histogram']:.4f} > 0 = {macd_hist_positive}")
    
    if bb_low and macd_bullish and macd_crossover and macd_hist_positive:
        bb_strength = (0.2 - bb_position) / 0.2
        macd_strength = abs(latest['macd_histogram']) / abs(latest['macd']) if latest['macd'] != 0 else 0
        strength = (bb_strength + macd_strength) / 2
        print(f"✅ LONG signal strength: {strength:.3f}")
        if strength > 0.2:
            print(f"🚀 LONG SIGNAL ACTIVE!")
        else:
            print(f"⚠️ Signal too weak (need > 0.2)")
    else:
        print(f"❌ LONG conditions not met")
    
    print(f"\n🔴 SHORT CONDITIONS:")
    bb_high = bb_position > 0.8
    macd_bearish = latest['macd'] < latest['macd_signal']
    macd_crossover_short = prev['macd'] >= prev['macd_signal']
    macd_hist_negative = latest['macd_histogram'] < 0
    
    print(f"BB Position > 0.8: {bb_position:.3f} > 0.8 = {bb_high}")
    print(f"MACD < Signal: {latest['macd']:.4f} < {latest['macd_signal']:.4f} = {macd_bearish}")
    print(f"MACD crossover: {prev['macd']:.4f} >= {prev['macd_signal']:.4f} = {macd_crossover_short}")
    print(f"MACD Hist < 0: {latest['macd_histogram']:.4f} < 0 = {macd_hist_negative}")
    
    if bb_high and macd_bearish and macd_crossover_short and macd_hist_negative:
        bb_strength = (bb_position - 0.8) / 0.2
        macd_strength = abs(latest['macd_histogram']) / abs(latest['macd']) if latest['macd'] != 0 else 0
        strength = (bb_strength + macd_strength) / 2
        print(f"✅ SHORT signal strength: {strength:.3f}")
        if strength > 0.2:
            print(f"🚀 SHORT SIGNAL ACTIVE!")
        else:
            print(f"⚠️ Signal too weak (need > 0.2)")
    else:
        print(f"❌ SHORT conditions not met")
    
    # Test the actual method
    print(f"\n🧪 TESTING ACTUAL METHOD:")
    signal = method2.analyze_method2(df)
    if signal:
        print(f"✅ Method returned: {signal['direction']} (Strength: {signal['strength']:.1%})")
    else:
        print(f"❌ Method returned: None")

def check_data_quality():
    """Check if data is good quality"""
    print("🔍 CHECKING DATA QUALITY")
    print("=" * 50)
    
    exchange = ccxt.binance({
        'enableRateLimit': True,
        'options': {'defaultType': 'spot'}
    })
    
    try:
        # Fetch data
        ohlcv = exchange.fetch_ohlcv('BTCUSDT', '5m', limit=100)
        df = pd.DataFrame(ohlcv, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
        df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
        df.set_index('timestamp', inplace=True)
        
        print(f"✅ Data fetched successfully")
        print(f"📊 Data points: {len(df)}")
        print(f"💰 Price range: ${df['close'].min():,.2f} - ${df['close'].max():,.2f}")
        print(f"📈 Price change: {((df['close'].iloc[-1] - df['close'].iloc[0]) / df['close'].iloc[0] * 100):+.2f}%")
        
        # Check for missing data
        expected_interval = pd.Timedelta('5 minutes')
        missing_periods = 0
        for i in range(1, len(df)):
            time_diff = df.index[i] - df.index[i-1]
            if time_diff > expected_interval + pd.Timedelta('1 minute'):
                missing_periods += 1
        
        print(f"📊 Missing periods: {missing_periods}")
        
        if missing_periods > 5:
            print("⚠️ Too many missing periods - data quality poor")
        else:
            print("✅ Data quality good")
            
    except Exception as e:
        print(f"❌ Error fetching data: {e}")

def main():
    print("🐛 ALGORITHM DEBUG TOOL")
    print("=" * 60)
    
    # Check data quality first
    check_data_quality()
    
    # Debug both methods
    debug_method1()
    debug_method2()
    
    print("\n" + "=" * 60)
    print("🎯 SUMMARY:")
    print("If no signals found, possible issues:")
    print("1. Market conditions not suitable")
    print("2. Indicators not calculating correctly")
    print("3. Threshold still too high")
    print("4. Data quality issues")
    print("5. Algorithm logic errors")

if __name__ == "__main__":
    main()

