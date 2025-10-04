# HƯỚNG DẪN IMPORT CHAT HISTORY

## 📁 **Các file import:**

### 1. **import_with_options.py** - Interactive mode
- Yêu cầu user chọn option
- Phù hợp cho người dùng mới

### 2. **import_auto.py** - Auto mode  
- Tự động với command line arguments
- Phù hợp cho script automation

### 3. **import_clear.bat** - Batch file (Clear old data)
- Double-click để chạy
- Xóa hết data cũ rồi import

### 4. **import_keep.bat** - Batch file (Keep old data)
- Double-click để chạy  
- Giữ nguyên data cũ, chỉ thêm mới

## 🚀 **Cách sử dụng:**

### **Option 1: Interactive mode**
```bash
python import_with_options.py
```
- Chọn 1: Clear hết data cũ
- Chọn 2: Giữ nguyên data cũ

### **Option 2: Auto mode**
```bash
# Clear hết data cũ
python import_auto.py clear

# Giữ nguyên data cũ  
python import_auto.py keep
```

### **Option 3: Batch files**
- **Double-click** `import_clear.bat` để clear và import
- **Double-click** `import_keep.bat` để keep và import

## ⚙️ **Cấu hình:**

### **File JSON:**
- Đường dẫn: `.\data\result.json`
- Format: Export từ Telegram Desktop

### **Chat ID:**
- Mặc định: `-1002385574544`
- Có thể thay đổi trong script

## 📊 **Kết quả:**

### **Clear mode:**
- ✅ Xóa hết data cũ của group
- ✅ Import toàn bộ data mới
- ✅ Không có duplicate

### **Keep mode:**
- ✅ Giữ nguyên data cũ
- ✅ Chỉ thêm data mới
- ✅ Bỏ qua duplicate

## 🔧 **Tùy chỉnh:**

### **Thay đổi file JSON:**
```python
json_file = r".\data\your_file.json"
```

### **Thay đổi Chat ID:**
```python
chat_id = -1001234567890  # Chat ID của group khác
```

## 📝 **Lưu ý:**

1. **Backup database** trước khi clear
2. **Kiểm tra Chat ID** trước khi import
3. **File JSON** phải có format đúng
4. **Bot cần restart** sau khi import

## 🎯 **Ví dụ sử dụng:**

### **Import lần đầu:**
```bash
python import_auto.py clear
```

### **Import thêm data:**
```bash
python import_auto.py keep
```

### **Import group khác:**
1. Sửa `chat_id` trong script
2. Chạy `python import_auto.py clear`
