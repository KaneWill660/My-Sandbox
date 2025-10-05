#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Wrapper script để chạy Telegram Flow Bot với encoding UTF-8
"""

import sys
import os

# Thiết lập encoding UTF-8 cho Windows
if sys.platform == "win32":
    import codecs
    import locale
    
    # Thiết lập locale
    try:
        locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')
    except:
        try:
            locale.setlocale(locale.LC_ALL, 'C.UTF-8')
        except:
            pass
    
    # Thiết lập stdout/stderr với UTF-8
    if hasattr(sys.stdout, 'detach'):
        sys.stdout = codecs.getwriter("utf-8")(sys.stdout.detach())
    if hasattr(sys.stderr, 'detach'):
        sys.stderr = codecs.getwriter("utf-8")(sys.stderr.detach())

# Import và chạy main script
try:
    from telegram_flow import main
    import asyncio
    
    print("🚀 Starting Telegram Flow Bot...")
    print("📱 Make sure you have configured config.json")
    print("💡 Send /filter message to your personal chat to start")
    print("=" * 50)
    
    # Chạy bot
    if __name__ == "__main__":
        try:
            asyncio.run(main())
        except KeyboardInterrupt:
            print("\n🛑 Bot stopped by user (Ctrl+C)")
        except AttributeError:
            # Fallback cho Python 3.7 cũ
            try:
                loop = asyncio.get_event_loop()
                loop.run_until_complete(main())
            except KeyboardInterrupt:
                print("\n🛑 Bot stopped by user (Ctrl+C)")
            
except ImportError as e:
    print(f"❌ Import error: {e}")
    print("Make sure telegram_flow.py is in the same directory")
    input("Press Enter to exit...")
except Exception as e:
    print(f"❌ Error: {e}")
    input("Press Enter to exit...")
