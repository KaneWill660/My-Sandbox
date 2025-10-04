# Database Management Guide

## Scripts có sẵn

### 1. `clear_database.py` - Script chính để quản lý database

**Cách sử dụng:**
```bash
# Xem thông tin database
python clear_database.py info

# Clear database với xác nhận
python clear_database.py

# Clear database không cần xác nhận (force mode)
python clear_database.py force
```

### 2. Batch files để dễ sử dụng

- `db_info.bat` - Xem thông tin database
- `clear_db.bat` - Clear database với xác nhận  
- `clear_db_force.bat` - Clear database không cần xác nhận

## Chức năng

### Xem thông tin database (`info`)
- Kích thước file database
- Tổng số records
- Thống kê theo group (chat_id)
- Thống kê theo ngày (10 ngày gần nhất)
- Cấu trúc bảng coin_signals

### Clear database
- Xóa tất cả records trong bảng `coin_signals`
- Reset auto-increment counter
- Hiển thị số records trước và sau khi clear
- Có chế độ force (không cần xác nhận) cho script tự động

## Lưu ý

- Script sẽ chỉ xóa dữ liệu trong bảng `coin_signals`
- Cấu trúc bảng và các bảng khác sẽ được giữ nguyên
- Luôn backup database trước khi clear nếu cần thiết
- Sử dụng force mode cẩn thận vì không có xác nhận

## Ví dụ sử dụng

```bash
# Kiểm tra database hiện tại
python clear_database.py info

# Clear database để bắt đầu fresh
python clear_database.py force

# Import dữ liệu mới
python clear_and_import_utc.py

# Kiểm tra lại
python clear_database.py info
```
