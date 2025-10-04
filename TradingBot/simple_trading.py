#!/usr/bin/env python3
"""
Simple Trading Manager - Script đơn giản không có signal handler phức tạp
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
    
    print(f"🚀 Starting Simple Trading Manager...")
    print(f"⏱️ Duration: {duration} minutes")
    print(f"🔍 Signal interval: {signal_interval} minutes")
    print(f"🎯 Tracking interval: {tracking_interval} seconds")
    print(f"💡 Press Ctrl+C to stop")
    print("=" * 50)
    
    # Create trading manager (không setup signal handler)
    manager = TradingManager()
    
    # Override signal handler để tránh conflict
    import signal
    def simple_signal_handler(signum, frame):
        print("\n🛑 Stopping...")
        manager.stop_trading = True
        sys.exit(0)
    
    signal.signal(signal.SIGINT, simple_signal_handler)
    
    # Start trading
    manager.start_trading(duration, signal_interval, tracking_interval)
    
    # Keep main thread alive
    try:
        while manager.trading_thread.is_alive():
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n🛑 Stopping...")
        manager.stop_trading = True
    
    print("✅ Done!")

if __name__ == "__main__":
    main()

