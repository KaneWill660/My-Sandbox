from telethon import TelegramClient, events
from dotenv import load_dotenv
import os
import re
import hashlib
import MetaTrader5 as mt5
import asyncio
import sys
from telethon import events
import time
from telethon import TelegramClient
from telethon.network.connection.tcpfull import ConnectionTcpFull
from datetime import datetime, timezone
import subprocess

START_TIME = datetime.now(timezone.utc)

load_dotenv()

api_id = int(os.getenv("API_ID"))
api_hash = os.getenv("API_HASH")
group_username = os.getenv("GROUP_USERNAME")
session_name = os.getenv("SESSION_NAME")

SYMBOL_VOLUME = {
    "XAUUSDm": 0.01,
    #"ETHUSDm": 0.25,
    #"BTCUSDm": 0.02,
    #"USOILm": 0.01
}

SYMBOL_OFFSET = {
    "USOILm": 9
}

def adjust_price(symbol, price):
    offset = SYMBOL_OFFSET.get(symbol, 0)
    return price - offset

def place_order_mt5(signal):
    symbol = signal["symbol"]
    order_type = signal["type"]
    entry = signal["entry"]
    sl = signal["sl"]
    tp = signal["tp"][0]
    
    entry = adjust_price(symbol, entry)
    sl = adjust_price(symbol, sl)
    tp = adjust_price(symbol, tp)

    lot = SYMBOL_VOLUME.get(symbol, 0.01)

    # ===== connect =====
    if not mt5.initialize():
        print("* MT5 init failed")
        return

    # ===== select symbol =====
    if not mt5.symbol_select(symbol, True):
        print(f"* Cannot select {symbol}")
        return

    # ===== GET CURRENT PRICE =====
    tick = mt5.symbol_info_tick(symbol)
    if tick is None:
        print("* Cannot get tick")
        return

    bid = tick.bid
    ask = tick.ask

    print(f"* Current price: bid={bid}, ask={ask}")

    # ===== CHECK LIMIT LOGIC =====
    if order_type == "BUY":
        # BUY LIMIT phải thấp hơn giá hiện tại
        if entry >= ask:
            print("* BUY LIMIT sai: entry >= current price")
            return
        mt5_type = mt5.ORDER_TYPE_BUY_LIMIT

    else:  # SELL
        # SELL LIMIT phải cao hơn giá hiện tại
        if entry <= bid:
            print("* SELL LIMIT sai: entry <= current price")
            return
        mt5_type = mt5.ORDER_TYPE_SELL_LIMIT

    # ===== SEND ORDER =====
    request = {
        "action": mt5.TRADE_ACTION_PENDING,
        "symbol": symbol,
        "volume": lot,
        "type": mt5_type,
        "price": entry,
        "sl": sl,
        "tp": tp,
        "deviation": 20,
        "magic": 123456,
        "comment": "auto_bot",
        "type_time": mt5.ORDER_TIME_GTC,
        "type_filling": mt5.ORDER_FILLING_IOC,
    }

    print(f"* {symbol} {order_type} | ENTRY={entry:.2f} SL={sl:.2f} TP={tp:.2f} | ASK={ask:.2f} BID={bid:.2f}")
    result = mt5.order_send(request)

    if result.retcode != mt5.TRADE_RETCODE_DONE:
        print(f"* Order failed:", result.retcode)
    else:
        print(f"* Order placed:", result.order)

    mt5.shutdown()

def limit_pending_orders(symbol, max_orders=4):
    if not mt5.initialize():
        print("* MT5 init failed (limit)")
        return

    orders = mt5.orders_get(symbol=symbol)

    if orders is None:
        mt5.shutdown()
        return

    # lọc lệnh của bot
    bot_orders = [o for o in orders if o.magic == 123456]

    # nếu <= max thì thôi
    if len(bot_orders) <= max_orders:
        mt5.shutdown()
        return

    # sort theo thời gian (cũ → mới)
    bot_orders.sort(key=lambda x: x.time_setup)

    # số lệnh cần xoá
    to_delete = len(bot_orders) - max_orders

    for i in range(to_delete):
        order = bot_orders[i]

        request = {
            "action": mt5.TRADE_ACTION_REMOVE,
            "order": order.ticket,
        }

        result = mt5.order_send(request)

        if result.retcode == mt5.TRADE_RETCODE_DONE:
            print(f"* Removed old order {order.ticket}")
        else:
            print(f"* Remove failed {order.ticket}: {result.retcode}")

    mt5.shutdown()

def cancel_pending_orders(symbol):
    if not mt5.initialize():
        print("* MT5 init failed (cancel)")
        return

    orders = mt5.orders_get(symbol=symbol)

    if orders is None:
        print("* No pending orders")
        return

    for order in orders:
        request = {
            "action": mt5.TRADE_ACTION_REMOVE,
            "order": order.ticket,
        }

        result = mt5.order_send(request)

        if result.retcode == mt5.TRADE_RETCODE_DONE:
            print(f"* Canceled order {order.ticket}")
        else:
            print(f"* Cancel failed {order.ticket}: {result.retcode}")

    mt5.shutdown()

# ====== TELEGRAM CLIENT ======
#client = TelegramClient(session_name, api_id, api_hash)
client = TelegramClient(
    session_name,
    api_id,
    api_hash,
    connection=ConnectionTcpFull,
    connection_retries=9999,
    retry_delay=5,
    auto_reconnect=True
)

def parse_xau_special(text: str):
    text = text.upper()

    if "XAUUSD" not in text:
        return None

    # ===== detect BUY/SELL =====
    if "BUY XAUUSD" in text:
        order_type = "BUY"
    elif "SELL XAUUSD" in text:
        order_type = "SELL"
    else:
        return None

    # ===== ENTRY (range) =====
    entry_match = re.search(r"ENTRY:\s*([\d.]+)\s*-\s*([\d.]+)", text)
    if not entry_match:
        return None

    entry_1 = float(entry_match.group(1))
    entry_2 = float(entry_match.group(2))
    entry_low = entry_1 if entry_1 < entry_2 else entry_2
    entry_high = entry_1 if entry_1 > entry_2 else entry_2

    # BUY lấy giá thấp, SELL lấy giá cao
    entry = entry_low if order_type == "BUY" else entry_high

    # ===== SL =====
    sl_match = re.search(r"SL:\s*([\d.]+)", text)
    if not sl_match:
        return None

    sl = float(sl_match.group(1))

    # ===== TP1 (pip) =====
    tp_match = re.search(r"TP2:\s*([\d.]+)\s*PIP", text)
    if not tp_match:
        return None

    tp_pip = float(tp_match.group(1))

    # ===== convert pip -> price =====
    # XAU: 10 pip = 1 giá → 1 pip = 0.1
    tp_value = tp_pip * 0.1

    if order_type == "BUY":
        tp = entry + tp_value
    else:
        tp = entry - tp_value

    return [{
        "type": order_type,
        "symbol": "XAUUSDm",
        "entry": entry,
        "sl": sl,
        "tp": [round(tp, 2)]
    }]

# ====== PARSER ======
def parse_tradecoin_signal(text: str):
    # 🔥 ưu tiên XAU special trước
    xau_signal = parse_xau_special(text)
    if xau_signal:
        return xau_signal
    #==================================
    
    text = text.upper()
    results = []

    # ===== detect symbol =====
    symbol = None

    # if "ETHEREUM" in text or "(ETH/USD)" in text:
        # symbol = "ETHUSDm"
    # elif "BITCOIN" in text or "(BTC/USD)" in text:
        # symbol = "BTCUSDm"
    # elif "USOIL" in text or "WTI" in text:
        # symbol = "USOILm"
    # elif "XAU/USD" in text or "VÀNG" in text:
        # symbol = "XAUUSDm"

    if not symbol:
        return None

    # ===== helper =====
    def extract_block(pattern, order_type):
        match = re.search(pattern, text, re.DOTALL)
        if not match:
            return None

        return {
            "type": order_type,
            "symbol": symbol,
            "entry": float(match.group(1)),
            "sl": float(match.group(2)),
            "tp": [
                float(match.group(3)),
                float(match.group(4))
            ]
        }

    # ===== LONG =====
    long_pattern = r"LONG.*?ENTRY:\s*([\d.]+).*?SL:\s*([\d.]+).*?TP1:\s*([\d.]+).*?TP2:\s*([\d.]+)"
    long_signal = extract_block(long_pattern, "BUY")

    if long_signal:
        results.append(long_signal)

    # ===== SHORT =====
    short_pattern = r"SHORT.*?ENTRY:\s*([\d.]+).*?SL:\s*([\d.]+).*?TP1:\s*([\d.]+).*?TP2:\s*([\d.]+)"
    short_signal = extract_block(short_pattern, "SELL")

    if short_signal:
        results.append(short_signal)

    return results if results else None

async def run_mt5(signal):
    loop = asyncio.get_event_loop()
    await loop.run_in_executor(None, place_order_mt5, signal)

async def heartbeat():
    while True:
        print("* Bot alive", time.strftime("%H:%M:%S"))
        await asyncio.sleep(60)

client.loop.create_task(heartbeat())

# ====== DEDUP ======
processed_signals = set()

def get_signal_id(text):
    return hashlib.md5(text.encode()).hexdigest()

be_done_tickets = set()
def update_break_even():
    if not mt5.initialize():
        print("MT5 init fail (BE)")
        return

    # 🔥 đặt ở đây
    positions = mt5.positions_get()

    if not positions:
        mt5.shutdown()   # nhớ đóng MT5
        return  # skip nhanh

    # ===== xử lý tiếp =====
    for pos in positions:
        if pos.magic != 123456:
            continue

        symbol = pos.symbol
        entry = pos.price_open
        sl = pos.sl
        tp = pos.tp

        if tp == 0:
            continue

        tick = mt5.symbol_info_tick(symbol)
        if not tick:
            continue

        current_price = tick.bid if pos.type == mt5.ORDER_TYPE_BUY else tick.ask

        if pos.type == mt5.ORDER_TYPE_BUY:
            half_tp = entry + (tp - entry) / 2

            if current_price >= half_tp and sl < entry:
                new_sl = entry
            else:
                continue
        else:
            half_tp = entry - (entry - tp) / 2

            if current_price <= half_tp and sl > entry:
                new_sl = entry
            else:
                continue

        request = {
            "action": mt5.TRADE_ACTION_SLTP,
            "position": pos.ticket,
            "sl": new_sl,
            "tp": tp,
        }

        result = mt5.order_send(request)

        if result.retcode == mt5.TRADE_RETCODE_DONE:
            print(f"Move SL to BE for {symbol} #{pos.ticket}")
        else:
            print(f"BE failed {pos.ticket}: {result.retcode}")

    mt5.shutdown()

async def be_loop():
    loop = asyncio.get_event_loop()
    while True:
        await loop.run_in_executor(None, update_break_even)
        await asyncio.sleep(5)

# ====== Listener ======

ALLOWED_USER_ID = 936956659 
is_running = True

@client.on(events.NewMessage(pattern=r'^/stop$'))
async def stop_handler(event):
    global is_running

    if not event.is_private:
        return
    
    if event.sender_id != ALLOWED_USER_ID:
        return

    is_running = False
    await event.reply("✅ Bot stopped")
    print("* Bot stopped by user")


@client.on(events.NewMessage(pattern=r'^/start$'))
async def start_handler(event):
    global is_running

    if not event.is_private:
        return

    if event.sender_id != ALLOWED_USER_ID:
        return

    is_running = True
    await event.reply("✅ Bot resumed")
    print("* Bot resumed by user")
    
@client.on(events.NewMessage(pattern=r'^/exit$'))
async def exit_handler(event):
    global is_running

    if not event.is_private:
        return

    if event.sender_id != ALLOWED_USER_ID:
        return

    await event.reply("🛑 Bot is shutting down...") 
    print("* Bot exited by user")
    await client.disconnect()
    sys.exit(0)
    
# @client.on(events.NewMessage)
# async def debug_user(event):
    # print("Your ID:", event.sender_id)

@client.on(events.NewMessage(pattern=r'^/restart$'))
async def restart_handler(event):
    if not event.is_private:
        return

    if event.sender_id != ALLOWED_USER_ID:
        return

    await event.reply("🔄 Bot is restarting...")
    print("* Bot restarting...")

    # 🔥 chạy bot mới
    subprocess.Popen([sys.executable] + sys.argv)

    # 🔥 kill bot hiện tại
    await client.disconnect()
    os._exit(0)

@client.on(events.NewMessage(pattern=r'^/status$'))
async def status_handler(event):
    global is_running

    # chỉ nhận private
    if not event.is_private:
        return

    # chỉ bạn dùng
    if event.sender_id != ALLOWED_USER_ID:
        return

    # ===== BOT STATUS =====
    bot_status = "🟢 RUNNING" if is_running else "🔴 STOPPED"

    # ===== MT5 STATUS =====
    if not mt5.initialize():
        await event.reply(f"{bot_status}\n❌ MT5 not connected")
        return

    # lệnh đang mở
    positions = mt5.positions_get()
    total_positions = len(positions) if positions else 0

    # lệnh chờ
    orders = mt5.orders_get()
    total_orders = len(orders) if orders else 0

    # balance
    account = mt5.account_info()
    balance = account.balance if account else 0

    mt5.shutdown()

    # ===== RESPONSE =====
    msg = f"""
📊 BOT STATUS

🤖 Bot: {bot_status}
📈 Positions: {total_positions}
📌 Pending Orders: {total_orders}
💰 Balance: {balance:.2f}

"""
    await event.reply(msg)

from datetime import datetime, timezone
@client.on(events.NewMessage(pattern=r'^/report$'))
async def report_handler(event):
    if not event.is_private:
        return

    if event.sender_id != ALLOWED_USER_ID:
        return

    # ===== TIME RANGE (hôm nay) =====
    now = datetime.now()
    start_day = datetime(now.year, now.month, now.day)

    if not mt5.initialize():
        await event.reply("❌ MT5 not connected")
        return

    # ===== LẤY DEALS (lệnh đã đóng) =====
    deals = mt5.history_deals_get(start_day, now)

    if not deals:
        await event.reply("📊 Hôm nay chưa có giao dịch")
        mt5.shutdown()
        return

    # ===== THỐNG KÊ =====
    total = 0
    win = 0
    lose = 0
    profit = 0
    volume = 0

    for d in deals:
        # chỉ tính deal đóng lệnh
        if d.entry != mt5.DEAL_ENTRY_OUT:
            continue

        total += 1
        profit += d.profit
        volume += d.volume

        if d.profit > 0:
            win += 1
        else:
            lose += 1

    mt5.shutdown()

    # ===== TÍNH TOÁN =====
    winrate = (win / total * 100) if total > 0 else 0

    # ===== OUTPUT =====
    msg = f"""
📊 DAILY REPORT

📌 Total trades: {total}
✅ Win: {win}
❌ Lose: {lose}
📈 Winrate: {winrate:.1f}%

💰 Profit: {profit:.2f}
📦 Volume: {volume:.2f}
"""

    await event.reply(msg)

# ===== MAIN =====
async def main():
    await client.start()
    
    # 🔥 chạy BE loop nền
    client.loop.create_task(be_loop())
    
    GROUP_ID = -1001307184953
    @client.on(events.NewMessage(chats=GROUP_ID, incoming=True))
    async def handler(event):
        global is_running

        if not is_running:
            return
        try:
            if event.date < START_TIME:
                return
            text = event.raw_text
            
            print("Received at:", time.strftime("%H:%M:%S"))
            print("Message time:", event.date)
            if "ENTRY" not in text:
                return
            signal_id = get_signal_id(text)
            # ===== duplicate check =====
            if signal_id in processed_signals:
                print("* Duplicate signal")
                )
            signals = parse_tradecoin_signal(text)

            if not signals:
                return

            # ===== mark processed =====
            processed_signals.add(signal_id)

            # ===== lấy symbol (giả định cùng 1 cặp) =====
            symbol = signals[0]["symbol"]

            # ===== cancel pending cũ (1 lần duy nhất) =====
            cancel_pending_orders(symbol)

            # ===== đặt lệnh =====
            for s in signals:
                print("* TRADE:", s)
                await run_mt5(s)
            
            # * sau khi đặt xong → limit về 4 lệnh
            #limit_pending_orders(symbol, max_orders=4)

            print("------------------------------------------------------------\n")
        except Exception as e:
            print("* ERROR in handler:", e)

    print("Bot is running...")
    print("group_username: ", group_username)
    await client.run_until_disconnected()

# ===== RUN =====
client.loop.run_until_complete(main())
# asyncio.run(main())




