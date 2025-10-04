# 🚀 Trading Manager Guide

## 📋 Tổng quan

**Trading Manager** quản lý workflow hoàn chỉnh:
1. **Tìm tín hiệu** từ 2 method (RSI+EMA, Bollinger+MACD)
2. **Vào lệnh** khi có tín hiệu tốt
3. **PAUSE** việc tạo tín hiệu mới
4. **Tracking giá** để xem TP/SL
5. **Kết thúc lệnh** khi đạt TP/SL
6. **RESUME** tìm tín hiệu tiếp theo

## 🔧 Cách sử dụng

### 1. Khởi động Trading Manager

```bash
# Cách 1: Script đơn giản nhất (KHUYẾN NGHỊ)
python easy_trading.py 60 5 15

# Cách 2: Script đơn giản
python simple_trading.py 60 5 15

# Cách 3: Script đầy đủ
python run_trading.py 60 5 15

# Cách 4: Sử dụng test_methods.py
python test_methods.py --trade 60 5 15

# Cách 5: Chạy trực tiếp
python trading_manager.py --start 60 5 15
```

### 2. Dừng Trading Manager

```bash
# Nhấn Ctrl+C trong terminal để dừng
# Hoặc đóng terminal
```

### 3. Xem thống kê trading

```bash
python test_methods.py --trading-summary
```

### 4. Dừng trading (nếu cần)

```bash
python trading_manager.py --stop
```

## 📱 Workflow Telegram

### 🔍 Khi tìm tín hiệu:
```
🚀 TRADING MANAGER STARTED 🚀

⏰ Start time: 15/10/2024 14:30:00
⏱️ Duration: 60 minutes
🔍 Signal interval: Every 5 minutes
🎯 Tracking interval: Every 15 seconds

🤖 Workflow: Find Signal → Enter Position → Track TP/SL → Close → Repeat
```

### ✅ Khi vào lệnh LONG:
```
🟢 POSITION ENTERED - TRADING PAUSED 🟢

📈 Direction: MUA (LONG)
💰 Entry Price: $45,123.45
🎯 Strength: 75.2%
⚡ Method: RSI + EMA Crossover

🎯 TAKE PROFIT:
• Price: $46,928.39 ↑
• Distance: $1,804.94 (4.00%)

🛡️ STOP LOSS:
• Price: $44,220.98 ↓
• Distance: $902.47 (2.00%)

📊 Risk/Reward: 1:2.0

🆔 Position ID: TRADE_1_1696091234
⏰ Entry Time: 15/10/2024 14:35:00

⏸️ STATUS: Signal generation PAUSED
🎯 Now tracking price for TP/SL...

⚠️ Đang theo dõi giá để đạt TP/SL. Sẽ không tạo tín hiệu mới!
```

### ✅ Khi vào lệnh SHORT:
```
🔴 POSITION ENTERED - TRADING PAUSED 🔴

📈 Direction: BÁN (SHORT)
💰 Entry Price: $45,123.45
🎯 Strength: 68.5%
⚡ Method: Bollinger + MACD

🎯 TAKE PROFIT:
• Price: $43,318.51 ↓
• Distance: $1,804.94 (4.00%)

🛡️ STOP LOSS:
• Price: $46,025.92 ↑
• Distance: $902.47 (2.00%)

📊 Risk/Reward: 1:2.0

🆔 Position ID: TRADE_2_1696091234
⏰ Entry Time: 15/10/2024 14:40:00

⏸️ STATUS: Signal generation PAUSED
🎯 Now tracking price for TP/SL...

⚠️ Đang theo dõi giá để đạt TP/SL. Sẽ không tạo tín hiệu mới!
```

### 🎯 Khi đạt Take Profit:
```
🎯 TAKE PROFIT HIT! 🎯

🟢 Result: PROFIT
📈 Direction: LONG
💰 Entry Price: $45,123.45
💵 Exit Price: $46,928.39
📊 P&L: +4.00%

⏰ Duration: 15m 30s
📊 Method: RSI + EMA Crossover
🆔 Position ID: TRADE_1_1696091234

⏰ Time: 15/10/2024 14:50:30

🔄 STATUS: Signal generation RESUMED
🔍 Now searching for next signal...

🤖 Trading Manager - Position Closed
```

### 🛡️ Khi đạt Stop Loss:
```
🛡️ STOP LOSS HIT! 🛡️

🔴 Result: LOSS
📈 Direction: LONG
💰 Entry Price: $45,123.45
💵 Exit Price: $44,220.98
📊 P&L: -2.00%

⏰ Duration: 5m 15s
📊 Method: Bollinger + MACD
🆔 Position ID: TRADE_2_1696091234

⏰ Time: 15/10/2024 14:40:15

🔄 STATUS: Signal generation RESUMED
🔍 Now searching for next signal...

🤖 Trading Manager - Position Closed
```

### 📊 Thống kê trading (chỉ khi có hoạt động):
```
📊 TRADING SUMMARY 📊

⏰ Time: 15/10/2024 15:30:00

📈 Statistics:
• Total signals: 5
• Total trades: 3
• Profitable trades: 2
• Losing trades: 1
• Win rate: 66.7%
• Total P&L: +6.00%

🔄 Current Status:
• Trading: SEARCHING (Looking for signals)
• Position: None

🤖 Trading Manager
```

### 🏁 Kết thúc khi không có hoạt động:
```
🏁 TRADING MANAGER COMPLETED 🏁

⏰ End time: 15/10/2024 15:30:00
⏱️ Duration: 60 minutes

📊 No trading activity detected
🔍 Status: No signals found during session

🤖 Trading Manager Session Ended
```

## ⚙️ Cấu hình

### Tham số chính:
- **Duration**: Thời gian chạy trading (phút)
- **Signal Interval**: Khoảng thời gian tìm tín hiệu (phút)
- **Tracking Interval**: Khoảng thời gian kiểm tra TP/SL (giây) - **Mặc định: 15 giây**

### Ví dụ cấu hình:
```bash
# Scalping nhanh: tìm tín hiệu mỗi 2 phút, tracking mỗi 15 giây
python test_methods.py --trade 120 2 15

# Trading chậm: tìm tín hiệu mỗi 10 phút, tracking mỗi 30 giây
python test_methods.py --trade 240 10 30

# Test ngắn: 30 phút, tìm tín hiệu mỗi 3 phút, tracking mỗi 15 giây
python test_methods.py --trade 30 3 15
```

## 🎯 Tính năng chính

### ✅ Tự động quản lý:
- **Pause/Resume** tín hiệu tự động
- **Tracking TP/SL** real-time
- **Thống kê** chi tiết
- **Thông báo** đầy đủ

### ✅ An toàn:
- **Chỉ 1 lệnh** tại một thời điểm
- **Không tạo tín hiệu mới** khi đang có lệnh
- **Theo dõi chặt chẽ** TP/SL

### ✅ Thông báo thông minh:
- **Chỉ thông báo** khi có tín hiệu thực sự
- **Không spam** khi không có hoạt động
- **Summary** chỉ khi có giao dịch

### ✅ Thông tin đầy đủ:
- **P&L** chính xác
- **Thời gian** giữ lệnh
- **Method** được sử dụng
- **Position ID** để tracking

## 🚀 Bắt đầu

1. **Chạy test** để đảm bảo hoạt động:
   ```bash
   python test_methods.py --data
   python test_methods.py --indicators
   ```

2. **Khởi động trading**:
   ```bash
   python easy_trading.py 60 5 15
   ```

3. **Theo dõi** qua Telegram

4. **Xem thống kê**:
   ```bash
   python test_methods.py --trading-summary
   ```

## ⚠️ Lưu ý

- **Chỉ 1 lệnh** tại một thời điểm
- **Tự động pause** khi có lệnh
- **Tự động resume** khi đóng lệnh
- **Tracking liên tục** TP/SL
- **Thống kê** real-time

**Trading Manager = Workflow hoàn chỉnh cho scalping! 🎯**
