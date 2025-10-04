#!/usr/bin/env python3
"""
Check Current Trading Conditions - Kiểm tra điều kiện hiện tại
"""

import ccxt
import pandas as pd
import ta
from datetime import datetime
from method1_rsi_ema import Method1RSIEMA
from method2_bollinger_macd import Method2BollingerMACD

def get_current_conditions():
    """Lấy và hiển thị điều kiện hiện tại"""
    
    print("🔍 CHECKING CURRENT TRADING CONDITIONS")
    print("=" * 60)
    
    # Initialize methods
    method1 = Method1RSIEMA()
    method2 = Method2BollingerMACD()
    
    # Get current data
    print("📊 Fetching current data...")
    df1 = method1.fetch_data()
    df2 = method2.fetch_data()
    
    if df1 is None or df2 is None:
        print("❌ Failed to fetch data")
        return
    
    current_price = df1['close'].iloc[-1]
    current_time = df1.index[-1]
    
    print(f"💰 Current Price: ${current_price:,.2f}")
    print(f"⏰ Time: {current_time.strftime('%d/%m/%Y %H:%M:%S')}")
    print("=" * 60)
    
    # Check Method 1 (RSI + EMA)
    print("📈 METHOD 1: RSI + EMA CROSSOVER")
    print("-" * 40)
    
    # Calculate indicators for Method 1
    df1['rsi'] = method1.calculate_rsi(df1, method1.rsi_period)
    df1['ema_short'] = method1.calculate_ema(df1, method1.ema_short)
    df1['ema_long'] = method1.calculate_ema(df1, method1.ema_long)
    
    latest1 = df1.iloc[-1]
    prev1 = df1.iloc[-2]
    
    rsi = latest1['rsi']
    ema_short = latest1['ema_short']
    ema_long = latest1['ema_long']
    prev_ema_short = prev1['ema_short']
    prev_ema_long = prev1['ema_long']
    
    print(f"📊 RSI: {rsi:.2f}")
    print(f"📊 EMA 5: ${ema_short:,.2f}")
    print(f"📊 EMA 15: ${ema_long:,.2f}")
    print(f"📊 EMA 5 (prev): ${prev_ema_short:,.2f}")
    print(f"📊 EMA 15 (prev): ${prev_ema_long:,.2f}")
    
    # Check LONG conditions
    print("\n🟢 LONG Conditions:")
    long_rsi = rsi < method1.rsi_oversold
    long_ema_cross = ema_short > ema_long
    long_ema_prev = prev_ema_short <= prev_ema_long
    long_price = current_price > ema_short
    
    print(f"  RSI < 30: {rsi:.2f} < 30 = {long_rsi} {'✅' if long_rsi else '❌'}")
    print(f"  EMA 5 > EMA 15: {ema_short:,.2f} > {ema_long:,.2f} = {long_ema_cross} {'✅' if long_ema_cross else '❌'}")
    print(f"  EMA crossover: {prev_ema_short:,.2f} ≤ {prev_ema_long:,.2f} = {long_ema_prev} {'✅' if long_ema_prev else '❌'}")
    print(f"  Price > EMA 5: {current_price:,.2f} > {ema_short:,.2f} = {long_price} {'✅' if long_price else '❌'}")
    
    if long_rsi and long_ema_cross and long_ema_prev and long_price:
        rsi_strength = (method1.rsi_oversold - rsi) / method1.rsi_oversold
        ema_strength = (ema_short - ema_long) / ema_long
        long_strength = (rsi_strength + ema_strength) / 2
        print(f"  🎯 LONG Signal Strength: {long_strength:.3f} ({long_strength*100:.1f}%)")
        if long_strength > 0.3:
            print(f"  ✅ LONG SIGNAL ACTIVE! (Strength: {long_strength:.1%})")
        else:
            print(f"  ⚠️ LONG signal too weak (Need > 0.3)")
    else:
        print(f"  ❌ LONG conditions not met")
    
    # Check SHORT conditions
    print("\n🔴 SHORT Conditions:")
    short_rsi = rsi > method1.rsi_overbought
    short_ema_cross = ema_short < ema_long
    short_ema_prev = prev_ema_short >= prev_ema_long
    short_price = current_price < ema_short
    
    print(f"  RSI > 70: {rsi:.2f} > 70 = {short_rsi} {'✅' if short_rsi else '❌'}")
    print(f"  EMA 5 < EMA 15: {ema_short:,.2f} < {ema_long:,.2f} = {short_ema_cross} {'✅' if short_ema_cross else '❌'}")
    print(f"  EMA crossover: {prev_ema_short:,.2f} ≥ {prev_ema_long:,.2f} = {short_ema_prev} {'✅' if short_ema_prev else '❌'}")
    print(f"  Price < EMA 5: {current_price:,.2f} < {ema_short:,.2f} = {short_price} {'✅' if short_price else '❌'}")
    
    if short_rsi and short_ema_cross and short_ema_prev and short_price:
        rsi_strength = (rsi - method1.rsi_overbought) / (100 - method1.rsi_overbought)
        ema_strength = (ema_long - ema_short) / ema_long
        short_strength = (rsi_strength + ema_strength) / 2
        print(f"  🎯 SHORT Signal Strength: {short_strength:.3f} ({short_strength*100:.1f}%)")
        if short_strength > 0.3:
            print(f"  ✅ SHORT SIGNAL ACTIVE! (Strength: {short_strength:.1%})")
        else:
            print(f"  ⚠️ SHORT signal too weak (Need > 0.3)")
    else:
        print(f"  ❌ SHORT conditions not met")
    
    print("\n" + "=" * 60)
    
    # Check Method 2 (Bollinger + MACD)
    print("📊 METHOD 2: BOLLINGER BANDS + MACD")
    print("-" * 40)
    
    # Calculate indicators for Method 2
    df2['bb_upper'], df2['bb_middle'], df2['bb_lower'] = method2.calculate_bollinger_bands(df2, method2.bb_period, method2.bb_std)
    df2['macd'], df2['macd_signal'], df2['macd_histogram'] = method2.calculate_macd(df2, method2.macd_fast, method2.macd_slow, method2.macd_signal)
    
    latest2 = df2.iloc[-1]
    prev2 = df2.iloc[-2]
    
    bb_upper = latest2['bb_upper']
    bb_middle = latest2['bb_middle']
    bb_lower = latest2['bb_lower']
    macd = latest2['macd']
    macd_signal = latest2['macd_signal']
    macd_hist = latest2['macd_histogram']
    prev_macd = prev2['macd']
    prev_macd_signal = prev2['macd_signal']
    
    print(f"📊 BB Upper: ${bb_upper:,.2f}")
    print(f"📊 BB Middle: ${bb_middle:,.2f}")
    print(f"📊 BB Lower: ${bb_lower:,.2f}")
    print(f"📊 MACD: {macd:.4f}")
    print(f"📊 MACD Signal: {macd_signal:.4f}")
    print(f"📊 MACD Histogram: {macd_hist:.4f}")
    
    # Calculate BB position
    bb_position = (current_price - bb_lower) / (bb_upper - bb_lower)
    print(f"📊 BB Position: {bb_position:.3f} (0=lower, 1=upper)")
    
    # Check LONG conditions
    print("\n🟢 LONG Conditions:")
    long_bb = bb_position < 0.2
    long_macd = macd > macd_signal
    long_macd_cross = prev_macd <= prev_macd_signal
    long_hist = macd_hist > 0
    
    print(f"  BB Position < 0.2: {bb_position:.3f} < 0.2 = {long_bb} {'✅' if long_bb else '❌'}")
    print(f"  MACD > Signal: {macd:.4f} > {macd_signal:.4f} = {long_macd} {'✅' if long_macd else '❌'}")
    print(f"  MACD crossover: {prev_macd:.4f} ≤ {prev_macd_signal:.4f} = {long_macd_cross} {'✅' if long_macd_cross else '❌'}")
    print(f"  MACD Hist > 0: {macd_hist:.4f} > 0 = {long_hist} {'✅' if long_hist else '❌'}")
    
    if long_bb and long_macd and long_macd_cross and long_hist:
        bb_strength = (0.2 - bb_position) / 0.2
        macd_strength = abs(macd_hist) / abs(macd) if macd != 0 else 0
        long_strength = (bb_strength + macd_strength) / 2
        print(f"  🎯 LONG Signal Strength: {long_strength:.3f} ({long_strength*100:.1f}%)")
        if long_strength > 0.3:
            print(f"  ✅ LONG SIGNAL ACTIVE! (Strength: {long_strength:.1%})")
        else:
            print(f"  ⚠️ LONG signal too weak (Need > 0.3)")
    else:
        print(f"  ❌ LONG conditions not met")
    
    # Check SHORT conditions
    print("\n🔴 SHORT Conditions:")
    short_bb = bb_position > 0.8
    short_macd = macd < macd_signal
    short_macd_cross = prev_macd >= prev_macd_signal
    short_hist = macd_hist < 0
    
    print(f"  BB Position > 0.8: {bb_position:.3f} > 0.8 = {short_bb} {'✅' if short_bb else '❌'}")
    print(f"  MACD < Signal: {macd:.4f} < {macd_signal:.4f} = {short_macd} {'✅' if short_macd else '❌'}")
    print(f"  MACD crossover: {prev_macd:.4f} ≥ {prev_macd_signal:.4f} = {short_macd_cross} {'✅' if short_macd_cross else '❌'}")
    print(f"  MACD Hist < 0: {macd_hist:.4f} < 0 = {short_hist} {'✅' if short_hist else '❌'}")
    
    if short_bb and short_macd and short_macd_cross and short_hist:
        bb_strength = (bb_position - 0.8) / 0.2
        macd_strength = abs(macd_hist) / abs(macd) if macd != 0 else 0
        short_strength = (bb_strength + macd_strength) / 2
        print(f"  🎯 SHORT Signal Strength: {short_strength:.3f} ({short_strength*100:.1f}%)")
        if short_strength > 0.3:
            print(f"  ✅ SHORT SIGNAL ACTIVE! (Strength: {short_strength:.1%})")
        else:
            print(f"  ⚠️ SHORT signal too weak (Need > 0.3)")
    else:
        print(f"  ❌ SHORT conditions not met")
    
    print("\n" + "=" * 60)
    print("🎯 SUMMARY:")
    
    # Check if any signal is active
    method1_signal = method1.analyze_method1(df1)
    method2_signal = method2.analyze_method2(df2)
    
    if method1_signal:
        print(f"✅ METHOD 1 SIGNAL: {method1_signal['direction']} (Strength: {method1_signal['strength']:.1%})")
    else:
        print("❌ METHOD 1: No signal")
    
    if method2_signal:
        print(f"✅ METHOD 2 SIGNAL: {method2_signal['direction']} (Strength: {method2_signal['strength']:.1%})")
    else:
        print("❌ METHOD 2: No signal")
    
    if method1_signal or method2_signal:
        print("🚀 BOT WOULD ENTER POSITION!")
    else:
        print("⏳ BOT WAITING FOR SIGNAL...")
    
    print("=" * 60)

if __name__ == "__main__":
    get_current_conditions()

