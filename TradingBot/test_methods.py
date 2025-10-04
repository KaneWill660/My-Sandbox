#!/usr/bin/env python3
"""
Test both scalping methods and compare results
"""

import time
from datetime import datetime
from method1_rsi_ema import Method1RSIEMA
from method2_bollinger_macd import Method2BollingerMACD
from test_binance_data import BinanceDataTester
from test_indicators_5m import Indicators5mTester
from position_tracker import PositionTracker
from trading_manager import TradingManager

class MethodTester:
    def __init__(self):
        self.method1 = Method1RSIEMA()
        self.method2 = Method2BollingerMACD()
        self.results = {
            'method1': {'signals': 0, 'total_tests': 0},
            'method2': {'signals': 0, 'total_tests': 0}
        }
    
    def send_comparison_message(self):
        """Send comparison results to Telegram"""
        if not self.method1.telegram_token:
            return
        
        method1_rate = (self.results['method1']['signals'] / self.results['method1']['total_tests'] * 100) if self.results['method1']['total_tests'] > 0 else 0
        method2_rate = (self.results['method2']['signals'] / self.results['method2']['total_tests'] * 100) if self.results['method2']['total_tests'] > 0 else 0
        
        message = f"""
📊 <b>METHOD COMPARISON RESULTS</b> 📊

⏰ <b>Test completed:</b> {datetime.now().strftime("%d/%m/%Y %H:%M:%S")}

📈 <b>Method 1: RSI + EMA Crossover</b>
• Signals detected: {self.results['method1']['signals']}
• Total tests: {self.results['method1']['total_tests']}
• Signal rate: {method1_rate:.1f}%

📊 <b>Method 2: Bollinger + MACD</b>
• Signals detected: {self.results['method2']['signals']}
• Total tests: {self.results['method2']['total_tests']}
• Signal rate: {method2_rate:.1f}%

🏆 <b>Winner:</b> {"Method 1" if method1_rate > method2_rate else "Method 2" if method2_rate > method1_rate else "Tie"}

🤖 <i>Scalping Methods Comparison</i>"""
        
        self.method1.send_telegram(message)
        self.method1.send_telegram("-------------------------------------------------------------------------")
    
    def run_continuous_test(self, duration_minutes=60, interval_minutes=5):
        """Run continuous test for both methods"""
        print(f"🚀 Starting continuous test for {duration_minutes} minutes")
        print(f"⏱️ Testing every {interval_minutes} minutes")
        
        # Send start notification
        start_msg = f"""
🚀 <b>CONTINUOUS TEST STARTED</b> 🚀

⏰ <b>Start time:</b> {datetime.now().strftime("%d/%m/%Y %H:%M:%S")}
⏱️ <b>Duration:</b> {duration_minutes} minutes
🔄 <b>Interval:</b> Every {interval_minutes} minutes
📊 <b>Methods:</b> RSI+EMA vs Bollinger+MACD

🤖 <i>Testing both scalping methods continuously...</i>"""
        
        self.method1.send_telegram(start_msg)
        self.method1.send_telegram("-------------------------------------------------------------------------")
        
        start_time = time.time()
        end_time = start_time + (duration_minutes * 60)
        test_count = 0
        
        while time.time() < end_time:
            test_count += 1
            current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            print(f"\n🔄 Test #{test_count} - {current_time}")
            
            # Test Method 1
            print("📈 Testing Method 1: RSI + EMA...")
            df1 = self.method1.fetch_data()
            if df1 is not None:
                signal1 = self.method1.analyze_method1(df1)
                self.results['method1']['total_tests'] += 1
                if signal1:
                    self.results['method1']['signals'] += 1
                    print(f"✅ Method 1 signal: {signal1['direction']} ({signal1['strength']:.1%})")
                    message1 = self.method1.format_signal_message(signal1)
                    self.method1.send_telegram(message1)
                else:
                    print("⏳ Method 1: No signal")
            
            # Test Method 2
            print("📊 Testing Method 2: Bollinger + MACD...")
            df2 = self.method2.fetch_data()
            if df2 is not None:
                signal2 = self.method2.analyze_method2(df2)
                self.results['method2']['total_tests'] += 1
                if signal2:
                    self.results['method2']['signals'] += 1
                    print(f"✅ Method 2 signal: {signal2['direction']} ({signal2['strength']:.1%})")
                    message2 = self.method2.format_signal_message(signal2)
                    self.method2.send_telegram(message2)
                else:
                    print("⏳ Method 2: No signal")
            
            # Wait for next interval
            if time.time() < end_time:
                wait_seconds = interval_minutes * 60
                print(f"⏳ Waiting {interval_minutes} minutes for next test...")
                time.sleep(wait_seconds)
        
        # Send final comparison
        self.send_comparison_message()
        
        print(f"\n📊 Final Results:")
        print(f"Method 1 (RSI+EMA): {self.results['method1']['signals']}/{self.results['method1']['total_tests']} signals")
        print(f"Method 2 (BB+MACD): {self.results['method2']['signals']}/{self.results['method2']['total_tests']} signals")
    
    def run_single_test(self):
        """Run single test for both methods"""
        print("🧪 Running single test for both methods...")
        
        # Test Method 1
        print("\n📈 Testing Method 1: RSI + EMA Crossover...")
        self.method1.run_single_test()
        
        # Wait a bit
        time.sleep(2)
        
        # Test Method 2
        print("\n📊 Testing Method 2: Bollinger Bands + MACD...")
        self.method2.run_single_test()

def main():
    import sys
    
    tester = MethodTester()
    
    if len(sys.argv) > 1:
        if sys.argv[1] == '--continuous':
            duration = int(sys.argv[2]) if len(sys.argv) > 2 else 60
            interval = int(sys.argv[3]) if len(sys.argv) > 3 else 5
            tester.run_continuous_test(duration, interval)
        elif sys.argv[1] == '--method1':
            tester.method1.run_single_test()
        elif sys.argv[1] == '--method2':
            tester.method2.run_single_test()
        elif sys.argv[1] == '--data':
            data_tester = BinanceDataTester()
            data_tester.run_data_test()
        elif sys.argv[1] == '--indicators':
            indicators_tester = Indicators5mTester()
            indicators_tester.run_indicators_test()
        elif sys.argv[1] == '--track':
            duration = int(sys.argv[2]) if len(sys.argv) > 2 else 60
            interval = int(sys.argv[3]) if len(sys.argv) > 3 else 30
            tracker = PositionTracker()
            tracker.run_tracker(duration, interval)
        elif sys.argv[1] == '--positions':
            tracker = PositionTracker()
            tracker.send_positions_summary()
        elif sys.argv[1] == '--trade':
            duration = int(sys.argv[2]) if len(sys.argv) > 2 else 60
            signal_interval = int(sys.argv[3]) if len(sys.argv) > 3 else 5
            tracking_interval = int(sys.argv[4]) if len(sys.argv) > 4 else 15
            manager = TradingManager()
            manager.start_trading(duration, signal_interval, tracking_interval)
            
            # Keep main thread alive and wait for Ctrl+C
            try:
                while manager.trading_thread.is_alive():
                    time.sleep(1)
            except KeyboardInterrupt:
                print("\n🛑 Stopping trading...")
                manager.stop_trading_manager()
        elif sys.argv[1] == '--trading-summary':
            manager = TradingManager()
            manager.send_trading_summary()
        else:
            print("Usage:")
            print("  python test_methods.py --single          # Test both methods once")
            print("  python test_methods.py --continuous 60 5 # Test for 60 minutes every 5 minutes")
            print("  python test_methods.py --method1         # Test only method 1")
            print("  python test_methods.py --method2         # Test only method 2")
            print("  python test_methods.py --data            # Test Binance data accuracy")
            print("  python test_methods.py --indicators      # Test indicators on 5m data")
            print("  python test_methods.py --track 60 30     # Track positions for 60 minutes, check every 30 seconds")
            print("  python test_methods.py --positions       # Show current positions summary")
            print("  python test_methods.py --trade 60 5 15   # Start trading manager: 60min duration, 5min signal interval, 15sec tracking")
            print("  python test_methods.py --trading-summary # Show trading statistics")
    else:
        tester.run_single_test()

if __name__ == "__main__":
    main()
