# HƯỚNG DẪN TEST LỆNH SUMMARY

## 📁 **Các file test:**

### 1. **test_summary_final.py** - Script chính
- Test lệnh summary từ command line
- Xử lý Unicode an toàn
- Hiển thị đầy đủ thông tin

### 2. **Batch files** - Dễ sử dụng
- `test_summary_1h.bat` - Test 1 giờ
- `test_summary_24h.bat` - Test 24 giờ  
- `test_summary_48h.bat` - Test 48 giờ

## 🚀 **Cách sử dụng:**

### **Option 1: Command line**
```bash
# Test 24 giờ (mặc định)
python test_summary_final.py -1002385574544

# Test 1 giờ
python test_summary_final.py -1002385574544 1

# Test 24 giờ
python test_summary_final.py -1002385574544 24

# Test 48 giờ
python test_summary_final.py -1002385574544 48
```

### **Option 2: Batch files**
- **Double-click** `test_summary_1h.bat` để test 1 giờ
- **Double-click** `test_summary_24h.bat` để test 24 giờ
- **Double-click** `test_summary_48h.bat` để test 48 giờ

## 📊 **Kết quả test:**

### **1 giờ qua:**
- ✅ **0 kèo** (không có kèo mới trong 1 giờ)
- ✅ **Logic đúng**: Chỉ lấy kèo trong 1 giờ qua

### **24 giờ qua:**
- ✅ **24 kèo** từ 00:00 đến 12:07
- ✅ **Thông tin đầy đủ**: Contract, người gửi, thời gian
- ✅ **Unicode safe**: Xử lý ký tự đặc biệt

### **48 giờ qua:**
- ✅ **24 kèo** (cùng kết quả với 24h vì không có kèo cũ hơn)
- ✅ **Logic đúng**: Lấy kèo trong 48 giờ qua

## 🔧 **Tùy chỉnh:**

### **Thay đổi Chat ID:**
```bash
python test_summary_final.py -1001234567890 24
```

### **Test group khác:**
```bash
python test_summary_final.py -1003186951947 24
```

## 📝 **Thông tin hiển thị:**

### **Mỗi kèo bao gồm:**
1. **Contract address** - Địa chỉ contract đầy đủ
2. **Người gửi** - Tên người gửi đầu tiên
3. **Thời gian** - Giờ:phút gửi tin nhắn
4. **Giá lúc gửi** - Giá tại thời điểm gửi (N/A nếu chưa có)

### **Thống kê:**
- **Tổng số kèo** trong khoảng thời gian
- **Độ dài tin nhắn** (nếu cần chia nhỏ)
- **Số chunks** nếu tin nhắn quá dài

## 🎯 **Ví dụ sử dụng:**

### **Test nhanh:**
```bash
# Test 24 giờ
python test_summary_final.py -1002385574544 24

# Test 1 giờ
python test_summary_final.py -1002385574544 1
```

### **Test với group khác:**
```bash
# Test group khác
python test_summary_final.py -1003186951947 24
```

## ✅ **Kết quả mong đợi:**

- **Bot hoạt động đúng** với timezone đã sửa
- **Lấy đúng kèo** trong khoảng thời gian chỉ định
- **Hiển thị đầy đủ** thông tin contract và người gửi
- **Xử lý Unicode** an toàn
- **Logic summary** chính xác

## 🚀 **Sẵn sàng test bot thật:**

Sau khi test thành công, bot sẽ hoạt động tương tự trong Telegram với:
- ✅ **Timezone đúng**
- ✅ **Logic chính xác**
- ✅ **Auto delete** sau 1 phút
- ✅ **Chia nhỏ tin nhắn** nếu quá dài
