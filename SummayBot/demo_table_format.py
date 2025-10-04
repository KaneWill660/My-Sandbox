#!/usr/bin/env python3
"""
Demo script hien thi ket qua output dang bang cua bot
"""

def main():
    print("DEMO OUTPUT DANG BANG CUA BOT TELEGRAM")
    print("=" * 80)
    print()
    
    print("Khi ban go lenh: /summary")
    print("Bot se tra ve ket qua dang bang nhu sau:")
    print()
    print("-" * 80)
    
    # Demo output dang bang
    demo_output = """TONG HOP KEO 1 NGAY QUA

```
Contract     Nguoi gui       Thoi gian    Gia gui      Gia hien tai  Thay doi  
--------------------------------------------------------------------------------
0x1234...7890 crypto_trader  15/12 14:30  $0.000123   $0.000156     +26.9%
0xabcd...1234 moon_hunter    15/12 16:45  $0.000567   $0.000432     -23.9%
0x9876...3210 diamond_hands  15/12 18:20  $0.000001   $0.000002     +90.2%
0x1111...2222 whale_alert    15/12 20:15  $0.000000   $0.000000     +275.0%
0x3333...4444 pump_king      15/12 22:30  $0.000234   $0.000198     -15.2%
```"""
    
    print(demo_output)
    print()
    print("-" * 80)
    print()
    
    print("Khi ban go: /summary 3")
    print("Bot se hien thi keo trong 3 ngay qua dang bang:")
    print()
    
    demo_output_3_days = """TONG HOP KEO 3 NGAY QUA

```
Contract     Nguoi gui       Thoi gian    Gia gui      Gia hien tai  Thay doi  
--------------------------------------------------------------------------------
0x1111...2222 whale_alert    13/12 09:15  $0.000000   $0.000000     +275.0%
0x3333...4444 pump_king      14/12 11:30  $0.000234   $0.000198     -15.2%
0x5555...6666 hodl_master    14/12 20:45  $0.000001   $0.000001     +0.0%
0x7777...8888 moon_boy       15/12 08:20  $0.000045   $0.000067     +48.9%
0x9999...0000 diamond_king   15/12 12:15  $0.000123   $0.000098     -20.3%
```"""
    
    print(demo_output_3_days)
    print()
    print("-" * 80)
    print()
    
    print("SO SANH FORMAT CU VA MOI:")
    print()
    print("FORMAT CU (doc):")
    print("-" * 40)
    old_format = """0x1234...567890
Nguoi gui: @crypto_trader_2024
Thoi gian: 15/12/2024 14:30
Gia luc gui: $0.00012345
Gia hien tai: $0.00015678
Thay doi: +26.95%

0xabcd...ef1234
Nguoi gui: @moon_hunter
Thoi gian: 15/12/2024 16:45
Gia luc gui: $0.00056789
Gia hien tai: $0.00043210
Thay doi: -23.89%"""
    print(old_format)
    print()
    
    print("FORMAT MOI (bang):")
    print("-" * 40)
    new_format = """```
Contract     Nguoi gui       Thoi gian    Gia gui      Gia hien tai  Thay doi  
--------------------------------------------------------------------------------
0x1234...7890 crypto_trader  15/12 14:30  $0.000123   $0.000156     +26.9%
0xabcd...1234 moon_hunter    15/12 16:45  $0.000567   $0.000432     -23.9%
```"""
    print(new_format)
    print()
    
    print("UU DIEM CUA FORMAT BANG:")
    print("+ De doc hon - tat ca thong tin trong 1 hang")
    print("+ Tiet kiem khong gian - nhieu keo hon trong 1 message")
    print("+ De so sanh - cac cot duoc can chinh")
    print("+ Chuyen nghiep hon - giong cac bang thong ke")
    print("+ Nhanh hon - khong can scroll nhieu")
    print()
    
    print("CAC COT TRONG BANG:")
    print("• Contract: Dia chi contract (rut gon)")
    print("• Nguoi gui: Username nguoi gui dau tien")
    print("• Thoi gian: Ngay/gio gui")
    print("• Gia gui: Gia luc gui keo")
    print("• Gia hien tai: Gia hien tai")
    print("• Thay doi: % thay doi voi emoji")

if __name__ == "__main__":
    main()
