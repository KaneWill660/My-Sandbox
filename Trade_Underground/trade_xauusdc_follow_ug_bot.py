from telethon import TelegramClient, events
from dotenv import load_dotenv
import os
import re
import hashlib
import MetaTrader5 as mt5
import asyncio
import time

load_dotenv()

api_id = int(os.getenv("API_ID"))
api_hash = os.getenv("API_HASH")
group_username = os.getenv("GROUP_USERNAME")
session_name = os.getenv("SESSION_NAME")
ALLOWED_USER_ID = 936876659 

delta_entry = 2
delta_tp = 0 #default
offset_tp = 1.5 #offset to TP1 is 1

volume_1 = 0.7
volume_2 = 0.2
volume_3 = 0.1

SYMBOL_VOLUME = {
    "XAUUSDc": 0.5,
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
    tps = signal["tp"][:2]  # 🔥 chỉ TP1, TP2

    if not mt5.initialize():
        print("* MT5 init failed")
        return

    info = mt5.symbol_info(symbol)
    if info is None:
        print("* Cannot get symbol info")
        return

    if not mt5.symbol_select(symbol, True):
        print(f"* Cannot select {symbol}")
        return

    tick = mt5.symbol_info_tick(symbol)
    if tick is None:
        print("* Cannot get tick")
        return

    bid = tick.bid
    ask = tick.ask

    # ===== normalize giá =====
    digits = info.digits
    entry = round(entry, digits)
    sl = round(sl, digits)
    tps = [round(tp, digits) for tp in tps]
    tp1 = tps[0]
    tp2 = tps[1]
    # 🔥 TP3 = TP2 + 5 giá
    if order_type == "BUY":
        tp3 = tp2 + 5
    else:
        tp3 = tp2 - 5

    tp3 = round(tp3, digits)

    print(f"* {symbol} {order_type} | ENTRY={entry} SL={sl} TP={tps} | ASK={ask} BID={bid}")

    # ===== skip nếu giá đã chạm TP1 quá 1 giá (offset_tp)=====
    if order_type == "BUY":
        if ask >= (tp1+delta_tp+offset_tp):
            msg = f"* BUY_LIMIT: Skip {symbol}: giá đã chạm/gần TP1 | ENTRY={entry} SL={sl} TP={tp1+delta_tp+offset_tp} | ASK={ask} BID={bid}"
            print(msg)
            notify(msg)
            mt5.shutdown()
            return
    else:  # SELL
        if bid <= (tp1-delta_tp-offset_tp):
            msg = f"* SELL_LIMIT: Skip {symbol}: giá đã chạm/gần TP1 | ENTRY={entry} SL={sl} TP={tp1-delta_tp-offset_tp} | ASK={ask} BID={bid}"
            print(msg)
            notify(msg)
            mt5.shutdown()
            return

    # ===== check LIMIT logic =====
    if order_type == "BUY":
        if entry >= ask:
            msg = f"* BUY LIMIT invalid | {symbol} | entry={entry} ask={ask}"
            print(msg)
            notify(msg)
            mt5.shutdown()
            return
        mt5_type = mt5.ORDER_TYPE_BUY_LIMIT
    else:
        if entry <= bid:
            msg = f"* SELL LIMIT invalid | {symbol} | entry={entry} ask={ask}"
            print(msg)
            notify(msg)
            mt5.shutdown()
            return
        mt5_type = mt5.ORDER_TYPE_SELL_LIMIT

    # ===== đặt 3 lệnh TP1 + TP2 + TP3 =====
    orders_to_place = [
        {
            "tp": tp1,
            "volume": volume_1,
            "comment": "TP1"
        },
        {
            "tp": tp2,
            "volume": volume_2,
            "comment": "TP2"
        },
        {
            "tp": tp3,
            "volume": volume_3,
            "comment": "TP3"
        }
    ]
    for o in orders_to_place:

        request = {
            "action": mt5.TRADE_ACTION_PENDING,
            "symbol": symbol,
            "volume": o["volume"],
            "type": mt5_type,
            "price": entry,
            "sl": sl,
            "tp": o["tp"],
            "deviation": 20,
            "magic": 123456,
            "comment": o["comment"],
            "type_time": mt5.ORDER_TIME_GTC,
            "type_filling": mt5.ORDER_FILLING_IOC,
        }

        result = mt5.order_send(request)

        if result.retcode != mt5.TRADE_RETCODE_DONE:

            msg = (
                f"❌ {order_type}_LIMIT: Order failed "
                f"{symbol} "
                f"comment={o['comment']} "
                f"vol={o['volume']} "
                f"entry={entry} "
                f"tp={o['tp']} "
                f"retcode={result.retcode} "
                f"reason={result.comment}"
            )

            print(msg)
            notify(msg)

        else:

            msg = (
                f"✅ {order_type}_LIMIT: Order placed "
                f"{symbol} "
                f"comment={o['comment']} "
                f"vol={o['volume']} "
                f"entry={entry} "
                f"tp={o['tp']} "
                f"ticket={result.order}"
            )

            print(msg)
            notify(msg)

    mt5.shutdown()

def move_sl_to_be_after_tp1():
    if not mt5.initialize():
        return

    positions = mt5.positions_get()
    if not positions:
        mt5.shutdown()
        return

    # ===== check có TP1 không =====
    tp1_exists = any(p.comment == "TP1" for p in positions)

    # 👉 nếu TP1 vẫn còn → chưa hit
    if tp1_exists:
        mt5.shutdown()
        return

    # 👉 TP1 đã biến mất → bắt đầu BE TP2/TP3
    for p in positions:
        entry = p.price_open
        sl = p.sl
        tp = p.tp

        # 🔥 nếu SL đã gần entry thì bỏ
        if abs(sl - entry) < 0.01:
            continue

        request = {
            "action": mt5.TRADE_ACTION_SLTP,
            "position": p.ticket,
            "sl": entry,
            "tp": tp,
        }

        result = mt5.order_send(request)

        if result.retcode == mt5.TRADE_RETCODE_DONE:
            msg = f"* BE successed {p.ticket}: SL={entry}"
            print(msg)
            notify(msg)
        else:
            msg = f"* BE failed {p.ticket}: {result.retcode}"
            print(msg)
            notify(msg)

    mt5.shutdown()

def move_sl_to_be():
    if not mt5.initialize():
        return

    positions = mt5.positions_get()
    if not positions:
        mt5.shutdown()
        return

    for p in positions:
        entry = p.price_open
        sl = p.sl
        tp = p.tp

        # 🔥 nếu SL đã gần entry thì bỏ
        if abs(sl - entry) < 0.01:
            continue

        request = {
            "action": mt5.TRADE_ACTION_SLTP,
            "position": p.ticket,
            "sl": entry,
            "tp": tp,
        }

        result = mt5.order_send(request)

        if result.retcode == mt5.TRADE_RETCODE_DONE:
            print(f"* BE {p.ticket}: SL={entry}")
        else:
            print(f"* BE failed {p.ticket}: {result.retcode}")

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
    connection_retries=9999,
    retry_delay=5,
    auto_reconnect=True
)

def parse_xau_special(text: str):
    global delta_tp
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
    entry_match = re.search(r"ENTRY:\s*([\d.]+)(?:\s*-\s*([\d.]+))?", text)
    if not entry_match:
        return None

    entry = 0
    if entry_match.group(2):
        entry_1 = float(entry_match.group(1))
        entry_2 = float(entry_match.group(2))
        
        entry_low = entry_1 if entry_1 < entry_2 else entry_2
        entry_high = entry_1 if entry_1 > entry_2 else entry_2
        delta_tp = entry_high - entry_low - delta_entry
        
        # + delta_entry ở BUY, -delta_entry ở SELL để dễ match lệnh hơn
        entry_low = entry_low + delta_entry
        entry_high = entry_high - delta_entry
        
        # BUY lấy giá thấp, SELL lấy giá cao
        entry = entry_low if order_type == "BUY" else entry_high
    else:
        entry_1 = float(entry_match.group(1))
        delta_tp = 0
        entry = entry_1
    
    # ===== SL =====
    sl_match = re.search(r"SL:\s*([\d.]+)", text)
    if not sl_match:
        return None

    sl = float(sl_match.group(1))

    # ===== TP1 + TP2 (pip) =====
    tp1_match = re.search(r"TP1:\s*([\d.]+)\s*PIP", text)
    tp2_match = re.search(r"TP2:\s*([\d.]+)\s*PIP", text)

    if not tp1_match or not tp2_match:
        return None

    tp1_pip = float(tp1_match.group(1))
    tp2_pip = float(tp2_match.group(1))

    # ===== convert pip -> price =====
    # XAU: 1 pip = 0.1
    tp1_val = tp1_pip * 0.1
    tp2_val = tp2_pip * 0.1

    if order_type == "BUY":
        tp1 = entry + tp1_val
        tp2 = entry + tp2_val
    else:
        tp1 = entry - tp1_val
        tp2 = entry - tp2_val

    return [{
        "type": order_type,
        "symbol": "XAUUSDc",
        "entry": round(entry, 2),
        "sl": round(sl, 2),
        "tp": [round(tp1, 2), round(tp2, 2)]  # 🔥 chỉ 2 TP
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
        # symbol = "XAUUSDc"

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

def cancel_pending_if_tp_hit():
    if not mt5.initialize():
        notify("* MT5 init failed in cancel_pending_if_tp_hit")
        return

    orders = mt5.orders_get()

    if not orders:
        mt5.shutdown()
        return

    should_cancel = False
    # ===== check TP reached =====
    for o in orders:

        # chỉ xử lý lệnh bot
        if o.magic != 123456:
            continue

        symbol = o.symbol

        tick = mt5.symbol_info_tick(symbol)
        if tick is None:
            continue

        bid = tick.bid
        ask = tick.ask

        tp = o.tp
        # ===== BUY LIMIT =====
        if o.type == mt5.ORDER_TYPE_BUY_LIMIT:
            if ask >= (tp+delta_tp+offset_tp):
                should_cancel = True
                print(f"* BUY LIMIT: TP reached before fill BUY {symbol}, Ticket={o.ticket}, ASK={ask}, TP={tp+delta_tp+offset_tp}")
                notify(f"* BUY LIMIT: TP reached before fill BUY {symbol}, Ticket={o.ticket}, ASK={ask}, TP={tp+delta_tp+offset_tp}")
                break

        # ===== SELL LIMIT =====
        elif o.type == mt5.ORDER_TYPE_SELL_LIMIT:
            if bid <= (tp-delta_tp-offset_tp):
                should_cancel = True
                print(f"* SELL LIMIT: TP reached before fill SELL {symbol}, Ticket={o.ticket}, BID={bid}, TP={tp-delta_tp-offset_tp}")
                notify(f"* SELL LIMIT: TP reached before fill SELL {symbol}, Ticket={o.ticket}, BID={bid}, TP={tp-delta_tp-offset_tp}")
                break

    # ===== cancel ALL pending =====
    if should_cancel:
        for o in orders:
            if o.magic != 123456:
                continue

            request = {
                "action": mt5.TRADE_ACTION_REMOVE,
                "order": o.ticket,
            }
            result = mt5.order_send(request)
            if result.retcode == mt5.TRADE_RETCODE_DONE:
                print(f"🗑 Canceled pending {o.ticket}")
                notify(f"🗑 Pending canceled {o.symbol}, Ticket={o.ticket}")
            else:
                print(f"* Cancel failed {o.ticket}: {result.retcode}")
                notify(f"* Cancel failed {o.ticket}: {result.retcode}")
    mt5.shutdown()
    
async def run_mt5(signal):
    loop = asyncio.get_event_loop()
    await loop.run_in_executor(None, place_order_mt5, signal)

async def heartbeat():
    while True:
        # print("* Bot alive", time.strftime("%H:%M:%S"))
        loop = asyncio.get_event_loop()
        await loop.run_in_executor(None, move_sl_to_be_after_tp1)
        await loop.run_in_executor(
            None,
            cancel_pending_if_tp_hit
        )
        await asyncio.sleep(5)

client.loop.create_task(heartbeat())

# ====== DEDUP ======
processed_signals = set()

def get_signal_id(text):
    return hashlib.md5(text.encode()).hexdigest()

# ====== Listener ======

is_running = True

@client.on(events.NewMessage(pattern=r'^/offset1$'))
async def set_offet_tp_1_handler(event):
    global offset_tp

    if not event.is_private:
        return
    
    if event.sender_id != ALLOWED_USER_ID:
        return

    offset_tp = offset_tp + 0.5
    await event.reply("✅ set offset_tp = {offset_tp}")
    print("✅ set offset_tp = {offset_tp}")

@client.on(events.NewMessage(pattern=r'^/offset2$'))
async def set_offet_tp_2_handler(event):
    global offset_tp

    if not event.is_private:
        return
    
    if event.sender_id != ALLOWED_USER_ID:
        return

    offset_tp = offset_tp - 0.5
    await event.reply("✅ Set offset_tp = {offset_tp}")
    print("✅ Set offset_tp = {offset_tp}")    

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

@client.on(events.NewMessage(pattern=r'^/be$'))
async def be_handler(event):
    if not event.is_private:
        return

    if event.sender_id != ALLOWED_USER_ID:
        return

    await event.reply("🔄 Bot is move to entry...")
    print("* Bot move to entry...")

    move_sl_to_be()
    
    mt5.shutdown()

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
    balance = (balance / 100)
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
    profit = (profit / 100) # quy ra USD 
    volume = (volume / 100) # quy ra lot 

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
    
@client.on(events.NewMessage(pattern=r'^/report2$'))
async def report2_handler(event):
    if not event.is_private:
        return

    if event.sender_id != ALLOWED_USER_ID:
        return

    # ===== TIME RANGE (hôm nay) =====
    now = datetime.now()
    start_day = datetime(now.year, now.month, now.day-1)

    if not mt5.initialize():
        await event.reply("❌ MT5 not connected")
        return

    # ===== LẤY DEALS (lệnh đã đóng) =====
    deals = mt5.history_deals_get(start_day, now)

    if not deals:
        await event.reply("📊 2 Hôm nay chưa có giao dịch")
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
    profit = (profit / 100) # quy ra USD 
    volume = (volume / 100) # quy ra lot 

    # ===== OUTPUT =====
    msg = f"""
📊 2 DAYs REPORT

📌 Total trades: {total}
✅ Win: {win}
❌ Lose: {lose}
📈 Winrate: {winrate:.1f}%

💰 Profit: {profit:.2f}
📦 Volume: {volume:.2f}
"""

    await event.reply(msg)    

MAIN_LOOP = None
async def send_telegram_message(msg):
    try:
        await client.send_message(ALLOWED_USER_ID, msg)
    except Exception as e:
        print("* Send telegram failed:", e)

def notify(msg):
    global MAIN_LOOP

    try:
        asyncio.run_coroutine_threadsafe(
            send_telegram_message(msg),
            MAIN_LOOP
        )
    except Exception as e:
        print("* Notify failed:", e)

@client.on(events.NewMessage(chats=group_username))
async def handler(event):
    try:
        text = event.raw_text
        signal_id = get_signal_id(text)
        print("* received message")
        notify(f"* received message")

        # ===== duplicate check =====
        if signal_id in processed_signals:
            print("* Duplicate signal")
            return

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

client.start()
MAIN_LOOP = client.loop
print("\nBot is listening...")
print("group_username: ", group_username)
client.run_until_disconnected()

# @client.on(events.newmessage('/stop'))
# async def stop_handler(event):
    # print("* stop...")
    # await event.reply("🛑 stopping bot...")
    # await client.disconnect()

