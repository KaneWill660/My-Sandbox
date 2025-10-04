# 🚀 HƯỚNG DẪN CẤU HÌNH BOT

## ✅ Bot đã chạy thành công!

Bot hiện tại đang hiển thị thông báo:
```
Vui long thay YOUR_BOT_TOKEN bang token that tu BotFather!
```

## 📋 Bước tiếp theo:

### 1. Tạo Telegram Bot với BotFather

1. **Mở Telegram** và tìm `@BotFather`
2. **Gửi lệnh:** `/newbot`
3. **Đặt tên bot:** Ví dụ: "Coin Tracker Bot"
4. **Đặt username:** Ví dụ: "coin_tracker_bot"
5. **Lưu lại BOT TOKEN** được cung cấp

### 2. Cấu hình Bot Token

1. **Mở file `config.py`**
2. **Thay dòng:**
   ```python
   BOT_TOKEN = "YOUR_BOT_TOKEN"
   ```
3. **Thành:**
   ```python
   BOT_TOKEN = "1234567890:ABCdefGHIjklMNOpqrsTUVwxyz"
   ```
   (Thay bằng token thật từ BotFather)

### 3. Chạy Bot

```bash
python telegram_coin_tracker_bot.py
```

Bot sẽ hiển thị:
```
Bot dang chay...
```

### 4. Thêm Bot vào Group

1. **Thêm bot vào group** Telegram của bạn
2. **Cấp quyền Admin** cho bot (để đọc tin nhắn)
3. **Bot sẽ tự động** theo dõi tin nhắn chứa contract addresses

## 📱 Cách sử dụng Bot

### Lệnh chính:
- `/summary` - Xem kèo 24 giờ qua
- `/summary 6` - Xem kèo 6 giờ qua
- `/summary 12` - Xem kèo 12 giờ qua
- `/summary 48` - Xem kèo 2 ngày qua
- `/help` - Hiển thị hướng dẫn

### Ví dụ sử dụng:
1. **Gửi tin nhắn** chứa contract address: `0x1234...`
2. **Bot tự động** lưu thông tin kèo
3. **Gõ `/summary`** để xem tổng hợp
4. **Copy contract** để paste lên DexScreener

## 🎯 Tính năng Bot

- ✅ **Tự động phát hiện** contract addresses (0x...)
- ✅ **Lưu thông tin** người gửi, thời gian, giá
- ✅ **Lấy tên token** từ DexScreener API
- ✅ **Hiển thị contract đầy đủ** để copy
- ✅ **Tính % thay đổi** giá từ lúc gửi đến hiện tại
- ✅ **Filter theo giờ** (1-168 giờ)

## 📊 Ví dụ Output

```
TONG HOP KEO 6 GIO QUA

1. PEPE (PEPE)
Contract: 0x6982508145454Ce325dDbE47a25d4ec3d2311933
Nguoi gui: crypto_trader
Thoi gian: 15/12/2024 14:30
Gia luc gui: $0.00000012
Gia hien tai: $0.00000016
Thay doi: 📈 +27.0%

2. Shiba Inu (SHIB)
Contract: 0x95aD61b0a150d79219dCF64E1E6Cc01f0B64C4cE
Nguoi gui: moon_hunter
Thoi gian: 15/12/2024 16:45
Gia luc gui: $0.0005679
Gia hien tai: $0.0004321
Thay doi: 📉 -23.9%
```

## ⚠️ Lưu ý quan trọng

- ✅ **Bot cần quyền Admin** trong group để đọc tin nhắn
- ✅ **Chỉ theo dõi** contract addresses bắt đầu bằng 0x
- ✅ **Mỗi contract** chỉ hiển thị người gửi đầu tiên
- ✅ **Giá được lấy** từ DexScreener và CoinGecko
- ✅ **Tối đa 168 giờ** (7 ngày) cho mỗi lần query

## 🐛 Troubleshooting

### Bot không phản hồi:
- Kiểm tra BOT_TOKEN có đúng không
- Đảm bảo bot có quyền Admin trong group
- Kiểm tra log để xem lỗi

### Không lấy được giá:
- API có thể bị rate limit
- Contract address có thể không tồn tại
- Kiểm tra kết nối internet

### Database lỗi:
- Xóa file `coin_tracker.db` để reset
- Kiểm tra quyền ghi file

## 🎉 Chúc mừng!

Bot của bạn đã sẵn sàng sử dụng! Hãy cấu hình BOT_TOKEN và bắt đầu theo dõi các kèo coin trong group!
