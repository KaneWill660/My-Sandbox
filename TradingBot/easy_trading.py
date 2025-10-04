#!/usr/bin/env python3
"""
Easy Trading Manager - Chạy trading đơn giản, dễ dừng
"""

import sys
import time
from trading_manager import TradingManager

def main():
    # Parse arguments
    duration = 60
    signal_interval = 5
    tracking_interval = 15
    
    if len(sys.argv) > 1:
        duration = int(sys.argv[1])
    if len(sys.argv) > 2:
        signal_interval = int(sys.argv[2])
    if len(sys.argv) > 3:
        tracking_interval = int(sys.argv[3])
    
    print(f"🚀 Starting Easy Trading Manager...")
    print(f"⏱️ Duration: {duration} minutes")
    print(f"🔍 Signal interval: {signal_interval} minutes")
    print(f"🎯 Tracking interval: {tracking_interval} seconds")
    print(f"💡 Press Ctrl+C to stop")
    print("=" * 50)
    
    # Create trading manager
    manager = TradingManager()
    
    # Start trading
    manager.start_trading(duration, signal_interval, tracking_interval)
    
    # Simple loop - dễ dừng
    try:
        while True:
            time.sleep(1)
            if not manager.trading_thread.is_alive():
                break
    except KeyboardInterrupt:
        print("\n🛑 Ctrl+C pressed. Stopping...")
        manager.stop_trading = True
        print("✅ Stopped!")
        return
    
    print("✅ Trading completed!")

if __name__ == "__main__":
    main()

