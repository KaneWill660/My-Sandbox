#!/usr/bin/env python3
"""
Test Signal Frequency - Test tần suất tín hiệu với threshold mới
"""

import ccxt
import pandas as pd
import time
from datetime import datetime, timedelta
from method1_rsi_ema import Method1RSIEMA
from method2_bollinger_macd import Method2BollingerMACD

def test_signal_frequency(duration_minutes=60):
    """Test tần suất tín hiệu trong thời gian nhất định"""
    
    print(f"🧪 TESTING SIGNAL FREQUENCY FOR {duration_minutes} MINUTES")
    print("=" * 60)
    
    # Initialize methods
    method1 = Method1RSIEMA()
    method2 = Method2BollingerMACD()
    
    signals_found = 0
    method1_signals = 0
    method2_signals = 0
    total_checks = 0
    
    start_time = time.time()
    end_time = start_time + (duration_minutes * 60)
    
    print(f"⏰ Start time: {datetime.now().strftime('%H:%M:%S')}")
    print(f"⏰ End time: {(datetime.now() + timedelta(minutes=duration_minutes)).strftime('%H:%M:%S')}")
    print(f"🔍 Checking every 5 minutes...")
    print("=" * 60)
    
    while time.time() < end_time:
        current_time = datetime.now()
        print(f"🔍 Check #{total_checks + 1} - {current_time.strftime('%H:%M:%S')}")
        
        # Test Method 1
        df1 = method1.fetch_data()
        if df1 is not None:
            signal1 = method1.analyze_method1(df1)
            if signal1:
                method1_signals += 1
                signals_found += 1
                print(f"  ✅ Method 1: {signal1['direction']} (Strength: {signal1['strength']:.1%})")
            else:
                print(f"  ❌ Method 1: No signal")
        else:
            print(f"  ❌ Method 1: Failed to fetch data")
        
        # Test Method 2
        df2 = method2.fetch_data()
        if df2 is not None:
            signal2 = method2.analyze_method2(df2)
            if signal2:
                method2_signals += 1
                signals_found += 1
                print(f"  ✅ Method 2: {signal2['direction']} (Strength: {signal2['strength']:.1%})")
            else:
                print(f"  ❌ Method 2: No signal")
        else:
            print(f"  ❌ Method 2: Failed to fetch data")
        
        total_checks += 1
        
        # Wait 5 minutes
        if time.time() < end_time:
            print(f"  ⏳ Waiting 5 minutes...")
            time.sleep(300)  # 5 minutes
    
    # Results
    print("\n" + "=" * 60)
    print("📊 TEST RESULTS:")
    print(f"⏰ Duration: {duration_minutes} minutes")
    print(f"🔍 Total checks: {total_checks}")
    print(f"✅ Total signals found: {signals_found}")
    print(f"📈 Method 1 signals: {method1_signals}")
    print(f"📊 Method 2 signals: {method2_signals}")
    
    if total_checks > 0:
        signal_rate = (signals_found / total_checks) * 100
        print(f"📊 Signal rate: {signal_rate:.1f}% per check")
        print(f"📊 Expected signals per hour: {signal_rate * 12:.1f}")
        print(f"📊 Expected signals per day: {signal_rate * 288:.1f}")
    
    print("=" * 60)
    
    if signals_found == 0:
        print("❌ NO SIGNALS FOUND!")
        print("💡 Suggestions:")
        print("  1. Reduce MIN_SIGNAL_STRENGTH further (0.2 or 0.1)")
        print("  2. Check if indicators are calculating correctly")
        print("  3. Try different timeframes (1m, 3m)")
        print("  4. Check market conditions (low volatility?)")
    elif signals_found < total_checks * 0.1:
        print("⚠️ LOW SIGNAL FREQUENCY!")
        print("💡 Consider reducing MIN_SIGNAL_STRENGTH to 0.2")
    else:
        print("✅ GOOD SIGNAL FREQUENCY!")

def quick_test():
    """Quick test - check current conditions"""
    print("🚀 QUICK SIGNAL TEST")
    print("=" * 40)
    
    method1 = Method1RSIEMA()
    method2 = Method2BollingerMACD()
    
    # Test Method 1
    print("📈 Testing Method 1...")
    df1 = method1.fetch_data()
    if df1 is not None:
        signal1 = method1.analyze_method1(df1)
        if signal1:
            print(f"✅ Method 1: {signal1['direction']} (Strength: {signal1['strength']:.1%})")
        else:
            print("❌ Method 1: No signal")
    else:
        print("❌ Method 1: Failed to fetch data")
    
    # Test Method 2
    print("📊 Testing Method 2...")
    df2 = method2.fetch_data()
    if df2 is not None:
        signal2 = method2.analyze_method2(df2)
        if signal2:
            print(f"✅ Method 2: {signal2['direction']} (Strength: {signal2['strength']:.1%})")
        else:
            print("❌ Method 2: No signal")
    else:
        print("❌ Method 2: Failed to fetch data")
    
    print("=" * 40)

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1:
        if sys.argv[1] == "--quick":
            quick_test()
        else:
            duration = int(sys.argv[1])
            test_signal_frequency(duration)
    else:
        print("Usage:")
        print("  python test_signal_frequency.py --quick     # Quick test")
        print("  python test_signal_frequency.py 60          # Test for 60 minutes")
        print("  python test_signal_frequency.py 120         # Test for 120 minutes")

