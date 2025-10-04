#!/usr/bin/env python3
"""
Trading Manager - Quản lý workflow: Tạo tín hiệu → Vào lệnh → Tracking → Kết thúc → Tiếp tục
"""

import ccxt
import pandas as pd
import requests
import time
import threading
import signal
import sys
from datetime import datetime
from typing import Dict, List, Optional
from method1_rsi_ema import Method1RSIEMA
from method2_bollinger_macd import Method2BollingerMACD

class TradingManager:
    def __init__(self):
        self.symbol = 'BTCUSDT'
        self.timeframe = '5m'
        
        # Initialize methods
        self.method1 = Method1RSIEMA()
        self.method2 = Method2BollingerMACD()
        
        # Initialize exchange
        self.exchange = ccxt.binance({
            'enableRateLimit': True,
            'options': {'defaultType': 'spot'}
        })
        
        # Telegram config
        self.telegram_token = self.get_telegram_token()
        self.chat_id = '@tradingbotbykane'
        
        # Trading state
        self.is_trading = False  # True = đang tracking position, False = đang tìm tín hiệu
        self.current_position = None
        self.position_id_counter = 0
        self.trading_stats = {
            'total_signals': 0,
            'total_trades': 0,
            'profitable_trades': 0,
            'losing_trades': 0,
            'total_pnl': 0.0
        }
        
        # Control flags
        self.stop_trading = False
        self.trading_thread = None
        
        # Setup signal handler for Ctrl+C
        signal.signal(signal.SIGINT, self.signal_handler)
    
    def signal_handler(self, signum, frame):
        """Handle Ctrl+C signal"""
        if self.stop_trading:
            print("\n🛑 Force exit...")
            sys.exit(0)
        
        print("\n🛑 Received interrupt signal (Ctrl+C)")
        print("⏹️ Stopping Trading Manager...")
        self.stop_trading = True
        self.stop_trading_manager()
    
    def get_telegram_token(self):
        """Get Telegram bot token from .env file"""
        try:
            with open('.env', 'r', encoding='utf-8') as f:
                for line in f:
                    if line.startswith('TELEGRAM_BOT_TOKEN='):
                        return line.split('=', 1)[1].strip()
        except:
            pass
        return ''
    
    def send_telegram(self, message):
        """Send message to Telegram"""
        if not self.telegram_token:
            return False
        
        url = f"https://api.telegram.org/bot{self.telegram_token}/sendMessage"
        data = {
            'chat_id': self.chat_id,
            'text': message,
            'parse_mode': 'HTML'
        }
        
        try:
            response = requests.post(url, data=data, timeout=10)
            return response.status_code == 200
        except:
            return False
    
    def get_current_price(self):
        """Get current price"""
        try:
            ticker = self.exchange.fetch_ticker(self.symbol)
            return ticker['last']
        except Exception as e:
            print(f"Error getting current price: {e}")
            return None
    
    def find_signal(self):
        """Tìm tín hiệu từ cả 2 method"""
        print("🔍 Searching for trading signals...")
        
        # Test Method 1
        df1 = self.method1.fetch_data()
        signal1 = None
        if df1 is not None:
            signal1 = self.method1.analyze_method1(df1)
        
        # Test Method 2
        df2 = self.method2.fetch_data()
        signal2 = None
        if df2 is not None:
            signal2 = self.method2.analyze_method2(df2)
        
        # Chọn tín hiệu tốt nhất
        best_signal = None
        if signal1 and signal2:
            # Chọn tín hiệu có strength cao hơn
            if signal1['strength'] >= signal2['strength']:
                best_signal = signal1
            else:
                best_signal = signal2
        elif signal1:
            best_signal = signal1
        elif signal2:
            best_signal = signal2
        
        return best_signal
    
    def enter_position(self, signal: Dict):
        """Vào lệnh và bắt đầu tracking"""
        self.position_id_counter += 1
        position_id = f"TRADE_{self.position_id_counter}_{int(time.time())}"
        
        self.current_position = {
            'id': position_id,
            'direction': signal['direction'],
            'entry_price': signal['current_price'],
            'take_profit': signal['take_profit'],
            'stop_loss': signal['stop_loss'],
            'entry_time': datetime.now(),
            'method': signal.get('method', 'Unknown'),
            'strength': signal.get('strength', 0),
            'status': 'ACTIVE'
        }
        
        self.is_trading = True
        self.trading_stats['total_trades'] += 1
        
        # Gửi thông báo vào lệnh
        self.send_entry_notification()
        
        print(f"✅ Entered position: {position_id}")
        print(f"📊 Direction: {signal['direction']} at ${signal['current_price']:,.2f}")
        print(f"🎯 TP: ${signal['take_profit']:,.2f} | SL: ${signal['stop_loss']:,.2f}")
    
    def send_entry_notification(self):
        """Gửi thông báo vào lệnh"""
        pos = self.current_position
        
        direction_emoji = "🟢" if pos['direction'] == "LONG" else "🔴"
        direction_text = "MUA (LONG)" if pos['direction'] == "LONG" else "BÁN (SHORT)"
        
        # Tính toán khoảng cách từ entry price
        tp_distance = abs(pos['take_profit'] - pos['entry_price'])
        sl_distance = abs(pos['stop_loss'] - pos['entry_price'])
        tp_distance_pct = (tp_distance / pos['entry_price']) * 100
        sl_distance_pct = (sl_distance / pos['entry_price']) * 100
        
        # Hiển thị hướng di chuyển giá
        if pos['direction'] == 'LONG':
            tp_direction = "↑"  # Giá tăng
            sl_direction = "↓"  # Giá giảm
        else:  # SHORT
            tp_direction = "↓"  # Giá giảm
            sl_direction = "↑"  # Giá tăng
        
        message = f"""
{direction_emoji} <b>POSITION ENTERED - TRADING PAUSED</b> {direction_emoji}

📈 <b>Direction:</b> {direction_text}
💰 <b>Entry Price:</b> ${pos['entry_price']:,.2f}
🎯 <b>Strength:</b> {pos['strength']:.1%}
⚡ <b>Method:</b> {pos['method']}

🎯 <b>TAKE PROFIT:</b>
• Price: ${pos['take_profit']:,.2f} {tp_direction}
• Distance: ${tp_distance:,.2f} ({tp_distance_pct:.2f}%)

🛡️ <b>STOP LOSS:</b>
• Price: ${pos['stop_loss']:,.2f} {sl_direction}
• Distance: ${sl_distance:,.2f} ({sl_distance_pct:.2f}%)

📊 <b>Risk/Reward:</b> 1:{(tp_distance/sl_distance):.1f}

🆔 <b>Position ID:</b> {pos['id']}
⏰ <b>Entry Time:</b> {pos['entry_time'].strftime("%d/%m/%Y %H:%M:%S")}

⏸️ <b>STATUS:</b> Signal generation PAUSED
🎯 <b>Now tracking price for TP/SL...</b>

⚠️ <i>Đang theo dõi giá để đạt TP/SL. Sẽ không tạo tín hiệu mới!</i>"""
        
        self.send_telegram(message)
    
    def check_position(self):
        """Kiểm tra position hiện tại"""
        if not self.current_position or self.current_position['status'] != 'ACTIVE':
            return
        
        current_price = self.get_current_price()
        if current_price is None:
            return
        
        pos = self.current_position
        direction = pos['direction']
        entry_price = pos['entry_price']
        take_profit = pos['take_profit']
        stop_loss = pos['stop_loss']
        
        outcome = None
        
        # Check for TP/SL hit
        if direction == 'LONG':
            if current_price >= take_profit:
                outcome = 'TAKE_PROFIT'
            elif current_price <= stop_loss:
                outcome = 'STOP_LOSS'
        else:  # SHORT
            if current_price <= take_profit:
                outcome = 'TAKE_PROFIT'
            elif current_price >= stop_loss:
                outcome = 'STOP_LOSS'
        
        if outcome:
            # Calculate P&L
            if direction == 'LONG':
                pnl_percent = ((current_price - entry_price) / entry_price) * 100
            else:
                pnl_percent = ((entry_price - current_price) / entry_price) * 100
            
            # Update stats
            self.trading_stats['total_pnl'] += pnl_percent
            if pnl_percent > 0:
                self.trading_stats['profitable_trades'] += 1
            else:
                self.trading_stats['losing_trades'] += 1
            
            # Send outcome notification
            self.send_outcome_notification(current_price, outcome, pnl_percent)
            
            # Close position
            pos['status'] = outcome
            pos['exit_price'] = current_price
            pos['exit_time'] = datetime.now()
            pos['pnl_percent'] = pnl_percent
            
            # Resume signal generation
            self.is_trading = False
            self.current_position = None
            
            print(f"✅ Position closed: {outcome} | P&L: {pnl_percent:+.2f}%")
            print("🔄 Resuming signal generation...")
    
    def send_outcome_notification(self, current_price: float, outcome: str, pnl_percent: float):
        """Gửi thông báo kết quả lệnh"""
        pos = self.current_position
        
        if outcome == 'TAKE_PROFIT':
            emoji = "🎯"
            title = "TAKE PROFIT HIT!"
            color = "🟢"
            result = "PROFIT"
        else:  # STOP_LOSS
            emoji = "🛡️"
            title = "STOP LOSS HIT!"
            color = "🔴"
            result = "LOSS"
        
        # Calculate duration
        duration = datetime.now() - pos['entry_time']
        duration_str = f"{duration.seconds // 60}m {duration.seconds % 60}s"
        
        message = f"""
{emoji} <b>{title}</b> {emoji}

{color} <b>Result:</b> {result}
📈 <b>Direction:</b> {pos['direction']}
💰 <b>Entry Price:</b> ${pos['entry_price']:,.2f}
💵 <b>Exit Price:</b> ${current_price:,.2f}
📊 <b>P&L:</b> {pnl_percent:+.2f}%

⏰ <b>Duration:</b> {duration_str}
📊 <b>Method:</b> {pos['method']}
🆔 <b>Position ID:</b> {pos['id']}

⏰ <b>Time:</b> {datetime.now().strftime("%d/%m/%Y %H:%M:%S")}

🔄 <b>STATUS:</b> Signal generation RESUMED
🔍 <b>Now searching for next signal...</b>

🤖 <i>Trading Manager - Position Closed</i>"""
        
        self.send_telegram(message)
        self.send_telegram("-------------------------------------------------------------------------")
    
    def send_trading_summary(self):
        """Gửi thống kê trading (chỉ khi có hoạt động)"""
        stats = self.trading_stats
        
        # Chỉ gửi summary khi có hoạt động
        if stats['total_signals'] == 0 and stats['total_trades'] == 0:
            return
        
        win_rate = (stats['profitable_trades'] / stats['total_trades'] * 100) if stats['total_trades'] > 0 else 0
        
        message = f"""
📊 <b>TRADING SUMMARY</b> 📊

⏰ <b>Time:</b> {datetime.now().strftime("%d/%m/%Y %H:%M:%S")}

📈 <b>Statistics:</b>
• Total signals: {stats['total_signals']}
• Total trades: {stats['total_trades']}
• Profitable trades: {stats['profitable_trades']}
• Losing trades: {stats['losing_trades']}
• Win rate: {win_rate:.1f}%
• Total P&L: {stats['total_pnl']:+.2f}%

🔄 <b>Current Status:</b>
• Trading: {'ACTIVE (Position open)' if self.is_trading else 'SEARCHING (Looking for signals)'}
• Position: {self.current_position['id'] if self.current_position else 'None'}

🤖 <i>Trading Manager</i>"""
        
        self.send_telegram(message)
    
    def trading_loop(self, duration_minutes=60, signal_interval_minutes=5, tracking_interval_seconds=15):
        """Main trading loop"""
        print(f"🚀 Starting Trading Manager for {duration_minutes} minutes")
        print(f"🔍 Signal search interval: {signal_interval_minutes} minutes")
        print(f"🎯 Position tracking interval: {tracking_interval_seconds} seconds")
        
        # Send start notification
        start_msg = f"""
🚀 <b>TRADING MANAGER STARTED</b> 🚀

⏰ <b>Start time:</b> {datetime.now().strftime("%d/%m/%Y %H:%M:%S")}
⏱️ <b>Duration:</b> {duration_minutes} minutes
🔍 <b>Signal interval:</b> Every {signal_interval_minutes} minutes
🎯 <b>Tracking interval:</b> Every {tracking_interval_seconds} seconds

🤖 <i>Workflow: Find Signal → Enter Position → Track TP/SL → Close → Repeat</i>"""
        
        self.send_telegram(start_msg)
        self.send_telegram("-------------------------------------------------------------------------")
        
        start_time = time.time()
        end_time = start_time + (duration_minutes * 60)
        last_signal_check = 0
        
        while time.time() < end_time and not self.stop_trading:
            current_time = time.time()
            
            if not self.is_trading:
                # Đang tìm tín hiệu
                if current_time - last_signal_check >= (signal_interval_minutes * 60):
                    print("🔍 Checking for signals...")
                    signal = self.find_signal()
                    
                    if signal:
                        print(f"✅ Signal found: {signal['direction']} ({signal['strength']:.1%})")
                        self.trading_stats['total_signals'] += 1
                        self.enter_position(signal)
                    else:
                        print("⏳ No signal found, continuing search...")
                        # Không gửi thông báo Telegram khi không có tín hiệu
                    
                    last_signal_check = current_time
            else:
                # Đang tracking position
                print("🎯 Tracking position...")
                self.check_position()
            
            # Send summary every 10 minutes (chỉ khi có hoạt động)
            if int(current_time - start_time) % 600 == 0:  # Every 10 minutes
                if self.trading_stats['total_signals'] > 0 or self.trading_stats['total_trades'] > 0:
                    self.send_trading_summary()
            
            # Wait for next check
            time.sleep(tracking_interval_seconds)
        
        # Send final summary (chỉ khi có hoạt động)
        if self.trading_stats['total_signals'] > 0 or self.trading_stats['total_trades'] > 0:
            final_msg = f"""
🏁 <b>TRADING MANAGER COMPLETED</b> 🏁

⏰ <b>End time:</b> {datetime.now().strftime("%d/%m/%Y %H:%M:%S")}
⏱️ <b>Duration:</b> {duration_minutes} minutes

📊 <b>Final Statistics:</b>
• Total signals: {self.trading_stats['total_signals']}
• Total trades: {self.trading_stats['total_trades']}
• Profitable trades: {self.trading_stats['profitable_trades']}
• Losing trades: {self.trading_stats['losing_trades']}
• Total P&L: {self.trading_stats['total_pnl']:+.2f}%

🤖 <i>Trading Manager Session Ended</i>"""
            
            self.send_telegram(final_msg)
            self.send_telegram("-------------------------------------------------------------------------")
        else:
            # Chỉ gửi thông báo kết thúc đơn giản khi không có hoạt động
            final_msg = f"""
🏁 <b>TRADING MANAGER COMPLETED</b> 🏁

⏰ <b>End time:</b> {datetime.now().strftime("%d/%m/%Y %H:%M:%S")}
⏱️ <b>Duration:</b> {duration_minutes} minutes

📊 <b>No trading activity detected</b>
🔍 <b>Status:</b> No signals found during session

🤖 <i>Trading Manager Session Ended</i>"""
            
            self.send_telegram(final_msg)
        
        print("✅ Trading Manager completed!")
    
    def start_trading(self, duration_minutes=60, signal_interval_minutes=5, tracking_interval_seconds=15):
        """Start trading in separate thread"""
        if self.trading_thread and self.trading_thread.is_alive():
            print("⚠️ Trading already running!")
            return
        
        self.stop_trading = False
        self.trading_thread = threading.Thread(
            target=self.trading_loop,
            args=(duration_minutes, signal_interval_minutes, tracking_interval_seconds),
            daemon=True  # Daemon thread sẽ tự động dừng khi main thread dừng
        )
        self.trading_thread.start()
        print("🚀 Trading Manager started!")
        print("💡 Press Ctrl+C to stop trading")
    
    def stop_trading_manager(self):
        """Stop trading"""
        self.stop_trading = True
        if self.trading_thread and self.trading_thread.is_alive():
            print("⏳ Waiting for trading thread to stop...")
            self.trading_thread.join(timeout=5)  # Wait max 5 seconds
            if self.trading_thread.is_alive():
                print("⚠️ Thread did not stop gracefully")
            else:
                print("✅ Trading thread stopped")
        print("✅ Trading Manager stopped!")

def main():
    import sys
    
    manager = TradingManager()
    
    if len(sys.argv) > 1:
        if sys.argv[1] == '--start':
            duration = int(sys.argv[2]) if len(sys.argv) > 2 else 60
            signal_interval = int(sys.argv[3]) if len(sys.argv) > 3 else 5
            tracking_interval = int(sys.argv[4]) if len(sys.argv) > 4 else 15
            manager.start_trading(duration, signal_interval, tracking_interval)
        elif sys.argv[1] == '--summary':
            manager.send_trading_summary()
        elif sys.argv[1] == '--stop':
            manager.stop_trading_manager()
        else:
            print("Usage:")
            print("  python trading_manager.py --start 60 5 15    # Start trading for 60 minutes, signal every 5 minutes, track every 15 seconds")
            print("  python trading_manager.py --summary          # Send current trading summary")
            print("  python trading_manager.py --stop             # Stop trading")
    else:
        manager.start_trading(60, 5, 15)

if __name__ == "__main__":
    main()
