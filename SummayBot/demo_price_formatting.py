#!/usr/bin/env python3
"""
Demo script hien thi cach format gia thong minh
"""

def format_price(price):
    """Format gia mot cach thong minh - hien thi du so co nghia"""
    if price is None or price == 0:
        return "N/A"
    
    # Neu gia >= 1, hien thi 2-4 chu so thap phan
    if price >= 1:
        return f"${price:.4f}".rstrip('0').rstrip('.')
    
    # Neu gia < 1, tim so chu so co nghia dau tien
    price_str = f"{price:.15f}"
    
    # Tim vi tri chu so khac 0 dau tien sau dau phay
    decimal_part = price_str.split('.')[1]
    first_non_zero = 0
    for i, char in enumerate(decimal_part):
        if char != '0':
            first_non_zero = i
            break
    
    # Hien thi tu chu so co nghia dau tien + 4 chu so nua
    significant_digits = first_non_zero + 4
    
    # Gioi han toi da 8 chu so thap phan
    significant_digits = min(significant_digits, 8)
    
    formatted = f"${price:.{significant_digits}f}".rstrip('0').rstrip('.')
    
    # Neu qua dai (>12 ky tu), rut gon
    if len(formatted) > 12:
        # Hien thi dang scientific notation cho so rat nho
        if price < 0.000001:
            return f"${price:.2e}"
        else:
            # Rut gon bang cach bo bot so 0 cuoi
            return f"${price:.6f}".rstrip('0').rstrip('.')
    
    return formatted

def main():
    print("DEMO FORMAT GIA THONG MINH")
    print("=" * 60)
    print()
    
    # Cac vi du gia khac nhau
    test_prices = [
        0.000000123456789,  # Rat nho
        0.00000123456789,   # Nho
        0.0000123456789,    # Nho vua
        0.000123456789,     # Nho vua
        0.00123456789,      # Nho
        0.0123456789,       # Nho
        0.123456789,        # Trung binh
        1.23456789,         # Lon
        12.3456789,         # Lon
        123.456789,         # Rat lon
        1234.56789,         # Rat rat lon
    ]
    
    print("SO SANH FORMAT GIA:")
    print("-" * 60)
    print(f"{'Gia goc':<20} {'Format cu':<20} {'Format moi':<20}")
    print("-" * 60)
    
    for price in test_prices:
        old_format = f"${price:.6f}" if price < 1 else f"${price:.4f}"
        new_format = format_price(price)
        print(f"{price:<20} {old_format:<20} {new_format:<20}")
    
    print()
    print("=" * 60)
    print()
    
    print("DEMO BANG VOI GIA THUC TE:")
    print("-" * 60)
    
    # Demo bang voi gia thuc te
    demo_data = [
        ("0x1234...7890", "crypto_trader", "15/12 14:30", 0.000000123456789, 0.000000156789012, "+27.0%"),
        ("0xabcd...1234", "moon_hunter", "15/12 16:45", 0.00056789, 0.00043210, "-23.9%"),
        ("0x9876...3210", "diamond_hands", "15/12 18:20", 0.00000123, 0.00000234, "+90.2%"),
        ("0x1111...2222", "whale_alert", "15/12 20:15", 0.00000000012, 0.00000000045, "+275.0%"),
        ("0x3333...4444", "pump_king", "15/12 22:30", 0.00023456, 0.00019876, "-15.2%"),
        ("0x5555...6666", "hodl_master", "15/12 23:45", 1.23456789, 1.45678901, "+18.0%"),
    ]
    
    print("TONG HOP KEO 1 NGAY QUA")
    print()
    print("```")
    print(f"{'Contract':<12} {'Nguoi gui':<15} {'Thoi gian':<12} {'Gia gui':<15} {'Gia hien tai':<15} {'Thay doi':<10}")
    print("-" * 85)
    
    for contract, sender, time, price_signal, price_current, change in demo_data:
        price_signal_str = format_price(price_signal)
        price_current_str = format_price(price_current)
        print(f"{contract:<12} {sender:<15} {time:<12} {price_signal_str:<15} {price_current_str:<15} {change:<10}")
    
    print("```")
    print()
    
    print("UU DIEM CUA FORMAT GIA MOI:")
    print("+ Hien thi du so co nghia - khong qua dai")
    print("+ Tu dong chon so chu so thap phan phu hop")
    print("+ Scientific notation cho so rat nho")
    print("+ Bo bot so 0 khong can thiet")
    print("+ De doc va so sanh hon")
    print()
    
    print("QUY TAC FORMAT:")
    print("• Gia >= $1: Hien thi 2-4 chu so thap phan")
    print("• Gia < $1: Hien thi tu chu so co nghia dau tien + 4 chu so")
    print("• Gia < $0.000001: Dung scientific notation (1.23e-07)")
    print("• Toi da 8 chu so thap phan")
    print("• Toi da 12 ky tu cho moi gia")

if __name__ == "__main__":
    main()
