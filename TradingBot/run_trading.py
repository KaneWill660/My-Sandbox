#!/usr/bin/env python3
"""
Run Trading Manager - Script đơn giản để chạy trading manager
"""

import sys
import time
import signal
from trading_manager import TradingManager

def signal_handler(signum, frame):
    """Handle Ctrl+C signal"""
    print("\n🛑 Received interrupt signal (Ctrl+C)")
    print("⏹️ Stopping Trading Manager...")
    if 'manager' in globals():
        manager.stop_trading = True
        manager.stop_trading_manager()
    sys.exit(0)

def main():
    # Setup signal handler
    signal.signal(signal.SIGINT, signal_handler)
    
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
    
    print(f"🚀 Starting Trading Manager...")
    print(f"⏱️ Duration: {duration} minutes")
    print(f"🔍 Signal interval: {signal_interval} minutes")
    print(f"🎯 Tracking interval: {tracking_interval} seconds")
    print(f"💡 Press Ctrl+C to stop")
    print("=" * 50)
    
    # Create and start trading manager
    global manager
    manager = TradingManager()
    manager.start_trading(duration, signal_interval, tracking_interval)
    
    # Keep main thread alive
    try:
        while manager.trading_thread.is_alive():
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n🛑 Keyboard interrupt received...")
        manager.stop_trading = True
        manager.stop_trading_manager()
    
    print("✅ Program ended!")

if __name__ == "__main__":
    main()
