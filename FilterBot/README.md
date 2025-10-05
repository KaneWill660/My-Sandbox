# Telegram Flow Bot

Bot tự động lọc tin nhắn từ group Telegram và gửi về chat cá nhân của bạn.

## Tính năng

- 🔍 Lọc tin nhắn theo người dùng cụ thể trong group
- 📱 Trigger bằng tin nhắn từ Telegram cá nhân
- 📊 Hiển thị thống kê và nội dung tin nhắn
- 🔒 Sử dụng tài khoản cá nhân (không cần bot trong group)

## Cài đặt

### Bước 1: Cài đặt Python và thư viện

```bash
# Cài đặt Python 3.7+ nếu chưa có
# Tải từ: https://www.python.org/downloads/

# Cài đặt thư viện
pip install -r requirements.txt
```

### Bước 2: Lấy API Credentials

1. Truy cập https://my.telegram.org/apps
2. Đăng nhập bằng số điện thoại Telegram của bạn
3. Tạo ứng dụng mới:
   - App title: `Telegram Flow Bot`
   - Short name: `telegram_flow`
   - Platform: `Desktop`
4. Lưu lại `api_id` và `api_hash`

### Bước 3: Cấu hình

1. Mở file `config.json`
2. Thay thế các giá trị:
   ```json
   {
       "api_id": "12345678",
       "api_hash": "abcdef1234567890abcdef1234567890",
       "phone_number": "+84123456789"
   }
   ```

### Bước 4: Chạy bot

```bash
python telegram_flow.py
```

Lần đầu chạy, bot sẽ yêu cầu:
- Nhập mã xác thực từ Telegram
- Nhập mật khẩu 2FA (nếu có)

## Cách sử dụng

### Format tin nhắn trigger:

```
/filter <group_username> <target_user> [yyyy.mm.dd] [limit]
```

### Cách dừng bot:

1. **Từ Telegram:** Gửi tin nhắn `/stop` hoặc `/quit` vào chat cá nhân
2. **Từ Console:** Nhấn `Ctrl+C` 
3. **Từ Windows:** Double-click file `stop_bot.bat`

### Ví dụ:

```
/filter @mygroup username                    # Tin nhắn hôm nay (giới hạn 10000)
/filter @mygroup username 2024.12.15        # Tin nhắn ngày 15/12/2024
/filter @mygroup username 2024.12.15 5000   # Tin nhắn ngày 15/12/2024, giới hạn 5000
/filter @crypto_signals trader_pro 2024.12.10  # Tin nhắn ngày 10/12/2024
/filter @coin_group admin 2024.11.25 20000  # Tin nhắn ngày 25/11/2024, giới hạn 20000
```

### Giải thích:

- `@mygroup`: Username của group (có thể dùng @ hoặc không)
- `username`: Tên người dùng cần lọc (có thể là username, first_name, hoặc last_name)
- `2024.12.15`: Ngày cần lọc tin nhắn (tùy chọn, mặc định là hôm nay)
- `5000`: Số tin nhắn tối đa để kiểm tra (tùy chọn, mặc định 10000)

## Lưu ý quan trọng

⚠️ **Bảo mật:**
- Không chia sẻ file `config.json` với ai
- Không commit file config lên Git
- Sử dụng mật khẩu mạnh cho tài khoản Telegram

⚠️ **Quy định:**
- Chỉ sử dụng với group mà bạn có quyền truy cập
- Tuân thủ quy định của group
- Không spam hoặc lạm dụng

⚠️ **Rủi ro đầu tư:**
- Thông tin kèo coin chỉ mang tính tham khảo
- Luôn nghiên cứu kỹ trước khi đầu tư
- Chỉ đầu tư số tiền có thể chấp nhận mất

## Xử lý lỗi

### Lỗi "Invalid API credentials"
- Kiểm tra lại `api_id` và `api_hash` trong `config.json`
- Đảm bảo đã tạo ứng dụng trên https://my.telegram.org/apps

### Lỗi "Group not found"
- Kiểm tra username group có đúng không
- Đảm bảo bạn đã tham gia group đó

### Lỗi "No messages found"
- Kiểm tra tên người dùng có đúng không
- Thử tăng `limit` để kiểm tra nhiều tin nhắn hơn

## Hỗ trợ

Nếu gặp vấn đề, hãy kiểm tra:
1. File log `telegram_flow.log`
2. Kết nối internet
3. Quyền truy cập group
4. Cấu hình API credentials

## Cập nhật

Để cập nhật bot:
```bash
pip install --upgrade telethon
```

## License

MIT License - Sử dụng tự do cho mục đích cá nhân.
