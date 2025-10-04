# 🤖 Telegram Coin Tracker Bot

Bot Telegram tự động theo dõi và tổng hợp các kèo coin/token trong group chat.

## ✨ Tính năng

- 🔍 **Tự động phát hiện** contract addresses (0x...)
- 💰 **Theo dõi giá** real-time từ DexScreener và CoinGecko
- 📊 **Tổng hợp kèo** theo thời gian tùy chỉnh
- 👤 **Hiển thị người gửi** đầu tiên cho mỗi contract
- 📈 **Tính % thay đổi** giá từ lúc gửi đến hiện tại
- 💾 **Lưu trữ** lịch sử trong SQLite database

## 🚀 Cài đặt

### 1. Tạo Telegram Bot

1. Mở Telegram và tìm `@BotFather`
2. Gửi lệnh `/newbot`
3. Đặt tên cho bot (ví dụ: "Coin Tracker Bot")
4. Đặt username cho bot (ví dụ: "coin_tracker_bot")
5. Lưu lại **BOT TOKEN** được cung cấp

### 2. Cài đặt dependencies

```bash
pip install -r requirements.txt
```

### 3. Cấu hình bot

Mở file `config.py` và thay `YOUR_BOT_TOKEN` bằng token thật:

```python
BOT_TOKEN = "1234567890:ABCdefGHIjklMNOpqrsTUVwxyz"
```

### 4. Chạy bot

```bash
python telegram_coin_tracker_bot.py
```

## 📱 Cách sử dụng

### Thêm bot vào group

1. Thêm bot vào group Telegram của bạn
2. Cấp quyền **Admin** cho bot (để đọc tin nhắn)
3. Bot sẽ tự động theo dõi các tin nhắn chứa contract addresses

### Lệnh bot

- `/summary` - Xem tổng hợp kèo 1 ngày qua
- `/summary 3` - Xem tổng hợp 3 ngày qua (tối đa 30 ngày)
- `/help` - Hiển thị hướng dẫn

### Ví dụ output

```
📊 TỔNG HỢP KÈO 1 NGÀY QUA

🪙 0x1234...567890
👤 Người gửi: @username
⏰ Thời gian: 15/12/2024 14:30
💰 Giá lúc gửi: $0.00012345
💰 Giá hiện tại: $0.00015678
📊 Thay đổi: 📈 +26.95%
```

## 🔧 Cấu hình nâng cao

### Thay đổi API giá

Trong `config.py`, bạn có thể thêm API khác:

```python
PRICE_APIS = {
    'dexscreener': 'https://api.dexscreener.com/latest/dex/tokens/',
    'coingecko': 'https://api.coingecko.com/api/v3/simple/token_price/ethereum',
    'your_api': 'https://your-api.com/price/'
}
```

### Thay đổi pattern contract

Để hỗ trợ các chain khác (không chỉ EVM):

```python
CONTRACT_PATTERN = r'0x[a-fA-F0-9]{40}|[A-Za-z0-9]{32,44}'  # EVM + Solana
```

## 🗄️ Database

Bot sử dụng SQLite để lưu trữ:

- **contract_address**: Địa chỉ contract
- **sender_id**: ID người gửi
- **sender_username**: Username người gửi
- **timestamp**: Thời gian gửi
- **price_at_signal**: Giá lúc gửi
- **message_id**: ID tin nhắn

## ⚠️ Lưu ý quan trọng

1. **Quyền Admin**: Bot cần quyền đọc tin nhắn trong group
2. **Rate Limiting**: API có giới hạn request, bot sẽ xử lý tự động
3. **Privacy**: Bot chỉ lưu thông tin công khai (username, contract addresses)
4. **Backup**: Nên backup file `coin_tracker.db` định kỳ

## 🐛 Troubleshooting

### Bot không phản hồi
- Kiểm tra BOT_TOKEN có đúng không
- Đảm bảo bot có quyền Admin trong group
- Kiểm tra log để xem lỗi

### Không lấy được giá
- API có thể bị rate limit
- Contract address có thể không tồn tại trên DEX
- Kiểm tra kết nối internet

### Database lỗi
- Xóa file `coin_tracker.db` để reset
- Kiểm tra quyền ghi file trong thư mục

## 📄 License

MIT License - Sử dụng tự do cho mục đích cá nhân và thương mại.

## 🤝 Đóng góp

Mọi đóng góp đều được chào đón! Tạo issue hoặc pull request để cải thiện bot.
