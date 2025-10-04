#!/usr/bin/env python3
"""
Position Tracker - Track active positions and notify when TP/SL is hit
"""

import ccxt
import pandas as pd
import requests
import time
from datetime import datetime
from typing import Dict, List, Optional

class PositionTracker:
    def __init__(self):
        self.symbol = 'BTCUSDT'
        self.timeframe = '5m'
        
        # Initialize exchange
        self.exchange = ccxt.binance({
            'enableRateLimit': True,
            'options': {'defaultType': 'spot'}
        })
        
        # Telegram config
        self.telegram_token = self.get_telegram_token()
        self.chat_id = '@tradingbotbykane'
        
        # Active positions tracking
        self.active_positions = {}
        self.position_id_counter = 0
    
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
    
    def add_position(self, signal_data: Dict) -> str:
        """Add a new position to track"""
        self.position_id_counter += 1
        position_id = f"POS_{self.position_id_counter}_{int(time.time())}"
        
        position = {
            'id': position_id,
            'direction': signal_data['direction'],
            'entry_price': signal_data['current_price'],
            'take_profit': signal_data['take_profit'],
            'stop_loss': signal_data['stop_loss'],
            'entry_time': datetime.now(),
            'method': signal_data.get('method', 'Unknown'),
            'strength': signal_data.get('strength', 0),
            'status': 'ACTIVE'
        }
        
        self.active_positions[position_id] = position
        
        print(f"✅ Added position {position_id}: {position['direction']} at ${position['entry_price']:,.2f}")
        return position_id
    
    def check_positions(self):
        """Check all active positions for TP/SL hits"""
        if not self.active_positions:
            return
        
        current_price = self.get_current_price()
        if current_price is None:
            return
        
        positions_to_remove = []
        
        for position_id, position in self.active_positions.items():
            if position['status'] != 'ACTIVE':
                continue
            
            direction = position['direction']
            entry_price = position['entry_price']
            take_profit = position['take_profit']
            stop_loss = position['stop_loss']
            
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
                
                # Send notification
                self.send_outcome_notification(position, current_price, outcome, pnl_percent)
                
                # Mark position as closed
                position['status'] = outcome
                position['exit_price'] = current_price
                position['exit_time'] = datetime.now()
                position['pnl_percent'] = pnl_percent
                
                positions_to_remove.append(position_id)
        
        # Remove closed positions
        for position_id in positions_to_remove:
            del self.active_positions[position_id]
    
    def send_outcome_notification(self, position: Dict, current_price: float, outcome: str, pnl_percent: float):
        """Send TP/SL hit notification"""
        direction = position['direction']
        entry_price = position['entry_price']
        take_profit = position['take_profit']
        stop_loss = position['stop_loss']
        method = position['method']
        entry_time = position['entry_time']
        
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
        duration = datetime.now() - entry_time
        duration_str = f"{duration.seconds // 60}m {duration.seconds % 60}s"
        
        message = f"""
{emoji} <b>{title}</b> {emoji}

{color} <b>Result:</b> {result}
📈 <b>Direction:</b> {direction}
💰 <b>Entry Price:</b> ${entry_price:,.2f}
💵 <b>Exit Price:</b> ${current_price:,.2f}
📊 <b>P&L:</b> {pnl_percent:+.2f}%

🎯 <b>Targets:</b>
• Take Profit: ${take_profit:,.2f}
• Stop Loss: ${stop_loss:,.2f}

⏰ <b>Duration:</b> {duration_str}
📊 <b>Method:</b> {method}
🆔 <b>Position ID:</b> {position['id']}

⏰ <b>Time:</b> {datetime.now().strftime("%d/%m/%Y %H:%M:%S")}

🤖 <i>Position Tracker - TP/SL Alert</i>"""
        
        self.send_telegram(message)
        self.send_telegram("-------------------------------------------------------------------------")
    
    def get_active_positions_summary(self):
        """Get summary of active positions"""
        if not self.active_positions:
            return "No active positions"
        
        summary = f"Active Positions: {len(self.active_positions)}\n"
        for position_id, position in self.active_positions.items():
            direction = position['direction']
            entry_price = position['entry_price']
            tp = position['take_profit']
            sl = position['stop_loss']
            method = position['method']
            
            summary += f"• {position_id}: {direction} ${entry_price:,.2f} | TP: ${tp:,.2f} | SL: ${sl:,.2f} | {method}\n"
        
        return summary
    
    def send_positions_summary(self):
        """Send active positions summary to Telegram"""
        if not self.active_positions:
            message = """
📊 <b>POSITIONS SUMMARY</b> 📊

⏰ <b>Time:</b> {time}

📈 <b>Active Positions:</b> 0
✅ All positions closed

🤖 <i>Position Tracker</i>""".format(time=datetime.now().strftime("%d/%m/%Y %H:%M:%S"))
        else:
            summary = self.get_active_positions_summary()
            message = f"""
📊 <b>POSITIONS SUMMARY</b> 📊

⏰ <b>Time:</b> {datetime.now().strftime("%d/%m/%Y %H:%M:%S")}

📈 <b>Active Positions:</b> {len(self.active_positions)}

{summary}

🤖 <i>Position Tracker</i>"""
        
        self.send_telegram(message)
    
    def run_tracker(self, duration_minutes=60, check_interval_seconds=30):
        """Run position tracker"""
        print(f"🎯 Starting Position Tracker for {duration_minutes} minutes")
        print(f"⏱️ Checking every {check_interval_seconds} seconds")
        
        # Send start notification
        start_msg = f"""
🎯 <b>POSITION TRACKER STARTED</b> 🎯

⏰ <b>Start time:</b> {datetime.now().strftime("%d/%m/%Y %H:%M:%S")}
⏱️ <b>Duration:</b> {duration_minutes} minutes
🔄 <b>Check interval:</b> Every {check_interval_seconds} seconds
📊 <b>Symbol:</b> {self.symbol}

🤖 <i>Monitoring active positions for TP/SL hits...</i>"""
        
        self.send_telegram(start_msg)
        
        start_time = time.time()
        end_time = start_time + (duration_minutes * 60)
        
        while time.time() < end_time:
            # Check positions
            self.check_positions()
            
            # Send summary every 10 minutes
            if int(time.time() - start_time) % 600 == 0:  # Every 10 minutes
                self.send_positions_summary()
            
            # Wait for next check
            time.sleep(check_interval_seconds)
        
        # Send final summary
        final_msg = f"""
🏁 <b>POSITION TRACKER COMPLETED</b> 🏁

⏰ <b>End time:</b> {datetime.now().strftime("%d/%m/%Y %H:%M:%S")}
⏱️ <b>Duration:</b> {duration_minutes} minutes

📊 <b>Final Status:</b>
{self.get_active_positions_summary()}

🤖 <i>Position Tracker Session Ended</i>"""
        
        self.send_telegram(final_msg)
        self.send_telegram("-------------------------------------------------------------------------")
        
        print("✅ Position tracker completed!")

def main():
    import sys
    
    tracker = PositionTracker()
    
    if len(sys.argv) > 1:
        if sys.argv[1] == '--track':
            duration = int(sys.argv[2]) if len(sys.argv) > 2 else 60
            interval = int(sys.argv[3]) if len(sys.argv) > 3 else 30
            tracker.run_tracker(duration, interval)
        elif sys.argv[1] == '--summary':
            tracker.send_positions_summary()
        else:
            print("Usage:")
            print("  python position_tracker.py --track 60 30    # Track for 60 minutes, check every 30 seconds")
            print("  python position_tracker.py --summary        # Send current positions summary")
    else:
        tracker.run_tracker(60, 30)

if __name__ == "__main__":
    main()

