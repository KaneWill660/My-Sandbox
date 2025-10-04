# 🔧 HƯỚNG DẪN FIX LỖI CÀI ĐẶT

## ❌ Lỗi gặp phải:
```
ImportError: cannot import name 'Application' from 'telegram.ext'
```

## ✅ Giải pháp:

### 1. Gỡ cài đặt phiên bản cũ:
```bash
pip uninstall python-telegram-bot
```

### 2. Cài đặt phiên bản tương thích với Python 3.7:
```bash
pip install python-telegram-bot==13.15
```

### 3. Cài đặt các dependencies khác:
```bash
pip install aiohttp==3.9.1
```

### 4. Chạy bot:
```bash
python telegram_coin_tracker_bot.py
```

## 📋 Thay đổi đã thực hiện:

### ✅ **Code đã được sửa để tương thích:**
- ✅ Thay `Application` → `Updater`
- ✅ Thay `ContextTypes.DEFAULT_TYPE` → `CallbackContext`
- ✅ Thay `filters` → `Filters`
- ✅ Thay `async/await` → `asyncio.run()` cho các hàm cần thiết
- ✅ Bỏ markdown formatting để tránh lỗi Unicode

### ✅ **Requirements.txt đã cập nhật:**
```
python-telegram-bot==13.15
aiohttp==3.9.1
```

## 🚀 Cách sử dụng sau khi fix:

### 1. Tạo bot với BotFather:
- Tìm `@BotFather` trên Telegram
- Gửi `/newbot`
- Đặt tên và username cho bot
- Lưu lại BOT TOKEN

### 2. Cấu hình bot:
- Mở file `config.py`
- Thay `YOUR_BOT_TOKEN` bằng token thật

### 3. Chạy bot:
```bash
python telegram_coin_tracker_bot.py
```

### 4. Thêm bot vào group:
- Thêm bot vào group Telegram
- Cấp quyền Admin cho bot
- Bot sẽ tự động theo dõi tin nhắn

## 📱 Lệnh bot:

- `/summary` - Xem kèo 24 giờ qua
- `/summary 6` - Xem kèo 6 giờ qua
- `/summary 48` - Xem kèo 2 ngày qua
- `/help` - Hiển thị hướng dẫn

## ⚠️ Lưu ý:

- ✅ Bot tương thích với Python 3.7
- ✅ Sử dụng python-telegram-bot v13.15
- ✅ Không cần markdown formatting
- ✅ Hiển thị contract address đầy đủ
- ✅ Lấy tên token từ DexScreener API

## 🐛 Nếu vẫn gặp lỗi:

1. **Kiểm tra Python version:**
   ```bash
   python --version
   ```

2. **Kiểm tra packages đã cài:**
   ```bash
   pip list | grep telegram
   ```

3. **Cài đặt lại từ đầu:**
   ```bash
   pip uninstall python-telegram-bot aiohttp
   pip install python-telegram-bot==13.15 aiohttp==3.9.1
   ```

4. **Chạy setup script:**
   ```bash
   python setup_bot.py
   ```
