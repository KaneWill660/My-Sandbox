# 🎯 **SCALPING METHODS TESTING GUIDE**

## 📋 **2 PHƯƠNG PHÁP SCALPING ĐƯỢC TEST**

### **📈 METHOD 1: RSI + EMA CROSSOVER**
- **RSI**: Oversold (<30) / Overbought (>70)
- **EMA**: EMA 5 cắt EMA 15
- **Logic**: RSI xác nhận + EMA trend
- **Ưu điểm**: Đơn giản, ít false signal
- **Phù hợp**: Thị trường có trend rõ ràng

### **📊 METHOD 2: BOLLINGER BANDS + MACD**
- **Bollinger**: Price chạm bands (<20% hoặc >80%)
- **MACD**: Momentum crossover
- **Logic**: Volatility + Momentum
- **Ưu điểm**: Bắt được breakout tốt
- **Phù hợp**: Thị trường sideway/breakout

## 🚀 **CÁCH SỬ DỤNG**

### **1. Test cả 2 phương pháp cùng lúc:**
```bash
python test_methods.py --single
```

### **2. Test liên tục để so sánh:**
```bash
# Test 1 giờ, mỗi 5 phút
python test_methods.py --continuous 60 5

# Test 6 giờ, mỗi 10 phút
python test_methods.py --continuous 360 10
```

### **3. Test từng phương pháp riêng:**
```bash
# Chỉ test Method 1 (RSI + EMA)
python test_methods.py --method1

# Chỉ test Method 2 (Bollinger + MACD)
python test_methods.py --method2
```

## 📊 **PHÂN TÍCH KẾT QUẢ**

### **Signal Rate (Tỷ lệ tín hiệu):**
- **< 5%**: Phương pháp quá thận trọng
- **5-15%**: Tỷ lệ hợp lý cho scalping
- **> 15%**: Có thể quá nhiều false signals

### **Signal Strength (Độ mạnh tín hiệu):**
- **> 60%**: Tín hiệu rất mạnh
- **40-60%**: Tín hiệu tốt
- **< 40%**: Tín hiệu yếu

### **Direction Balance:**
- **LONG vs SHORT**: Nên cân bằng
- **Không quá lệch** về một hướng

## 🎯 **CẤU HÌNH HIỆN TẠI**

### **Risk Management:**
- **Đòn bẩy**: 5X
- **Take Profit**: 20% (4% spot)
- **Stop Loss**: 10% (2% spot)
- **Risk/Reward**: 1:2

### **Timeframe:**
- **5 phút** cho cả 2 phương pháp
- **100 candles** để tính toán indicators

## 📱 **TELEGRAM NOTIFICATIONS**

Bot sẽ gửi:
- ✅ **Start notification** khi bắt đầu test
- ✅ **Signal notifications** khi phát hiện tín hiệu
- ✅ **Comparison results** khi kết thúc test
- ✅ **Separator lines** để dễ theo dõi

## 🔧 **TỐI ƯU HÓA**

### **Nếu Method 1 hiệu quả hơn:**
- Tăng trọng số RSI và EMA
- Giảm ngưỡng signal strength
- Thêm confirmation indicators

### **Nếu Method 2 hiệu quả hơn:**
- Tăng trọng số Bollinger và MACD
- Điều chỉnh BB parameters
- Thêm volume confirmation

### **Nếu cả 2 đều không hiệu quả:**
- Giảm ngưỡng signal strength
- Thử timeframe khác (3m, 15m)
- Kết hợp cả 2 phương pháp

## 📈 **KẾ HOẠCH TEST**

### **Phase 1: Single Tests (1-2 ngày)**
- Test từng phương pháp riêng biệt
- Xem phương pháp nào tạo nhiều tín hiệu hơn

### **Phase 2: Continuous Tests (3-7 ngày)**
- Test liên tục để so sánh hiệu quả
- Phân tích signal rate và strength

### **Phase 3: Optimization (1 tuần)**
- Tối ưu phương pháp tốt nhất
- Điều chỉnh parameters
- Test với real trading conditions

## 🎯 **MỤC TIÊU**

- **Signal Rate**: 10-20% (2-4 tín hiệu/ngày)
- **Signal Strength**: >50%
- **Win Rate**: >60%
- **Risk/Reward**: 1:2 hoặc tốt hơn

**Hãy bắt đầu với single test để xem phương pháp nào hoạt động tốt hơn! 🚀**

