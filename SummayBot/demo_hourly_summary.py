#!/usr/bin/env python3
"""
Demo script hien thi cach su dung lenh summary theo gio
"""

def main():
    print("DEMO LENH SUMMARY THEO GIO")
    print("=" * 60)
    print()
    
    print("THAY DOI CHINH:")
    print("-" * 30)
    print("+ Truoc: /summary [so_ngay]")
    print("+ Sau:   /summary [so_gio]")
    print("+ Mac dinh: 24 gio thay vi 1 ngay")
    print("+ Gioi han: 1-168 gio (7 ngay)")
    print()
    
    print("CAC LENH MOI:")
    print("-" * 30)
    
    commands = [
        ("/summary", "24 gio qua (mac dinh)"),
        ("/summary 6", "6 gio qua"),
        ("/summary 12", "12 gio qua"),
        ("/summary 24", "24 gio qua (1 ngay)"),
        ("/summary 48", "48 gio qua (2 ngay)"),
        ("/summary 72", "72 gio qua (3 ngay)"),
        ("/summary 168", "168 gio qua (7 ngay)"),
    ]
    
    for cmd, desc in commands:
        print(f"{cmd:<15} - {desc}")
    
    print()
    print("=" * 60)
    print()
    
    print("DEMO OUTPUT:")
    print("-" * 30)
    
    # Demo 6 giờ
    print("Khi go: /summary 6")
    print("Output:")
    print()
    demo_6h = """TONG HOP KEO 6 GIO QUA

```
Contract     Nguoi gui       Thoi gian    Gia gui         Gia hien tai    Thay doi  
-------------------------------------------------------------------------------------
0x1234...7890 crypto_trader   15/12 14:30  $0.00000012     $0.00000016     +27.0%    
0xabcd...1234 moon_hunter     15/12 16:45  $0.0005679      $0.0004321      -23.9%    
0x9876...3210 diamond_hands   15/12 18:20  $0.00000123     $0.00000234     +90.2%    
```"""
    print(demo_6h)
    print()
    
    # Demo 12 giờ
    print("Khi go: /summary 12")
    print("Output:")
    print()
    demo_12h = """TONG HOP KEO 12 GIO QUA

```
Contract     Nguoi gui       Thoi gian    Gia gui         Gia hien tai    Thay doi  
-------------------------------------------------------------------------------------
0x1234...7890 crypto_trader   15/12 14:30  $0.00000012     $0.00000016     +27.0%    
0xabcd...1234 moon_hunter     15/12 16:45  $0.0005679      $0.0004321      -23.9%    
0x9876...3210 diamond_hands   15/12 18:20  $0.00000123     $0.00000234     +90.2%    
0x1111...2222 whale_alert     15/12 20:15  $0.00000000012  $0.00000000045  +275.0%   
0x3333...4444 pump_king       15/12 22:30  $0.0002346      $0.0001988      -15.2%    
```"""
    print(demo_12h)
    print()
    
    # Demo 48 giờ (2 ngày)
    print("Khi go: /summary 48")
    print("Output:")
    print()
    demo_48h = """TONG HOP KEO 2 NGAY QUA

```
Contract     Nguoi gui       Thoi gian    Gia gui         Gia hien tai    Thay doi  
-------------------------------------------------------------------------------------
0x1111...2222 whale_alert     13/12 09:15  $0.00000000012  $0.00000000045  +275.0%   
0x3333...4444 pump_king       14/12 11:30  $0.0002346      $0.0001988      -15.2%    
0x5555...6666 hodl_master     14/12 20:45  $0.00000111     $0.00000111     +0.0%     
0x7777...8888 moon_boy        15/12 08:20  $0.000045       $0.000067       +48.9%    
0x9999...0000 diamond_king    15/12 12:15  $0.000123       $0.000098       -20.3%    
```"""
    print(demo_48h)
    print()
    
    print("=" * 60)
    print()
    
    print("UU DIEM CUA VIEC SU DUNG GIO:")
    print("-" * 40)
    print("+ Linh hoat hon - co the xem keo trong thoi gian ngan")
    print("+ Phu hop voi trading - 6h, 12h, 24h la cac khung thoi gian quan trong")
    print("+ De tinh toan - 48h = 2 ngay, 72h = 3 ngay")
    print("+ Gioi han hop ly - toi da 168h (7 ngay)")
    print("+ Mac dinh 24h thay vi 1 ngay - chinh xac hon")
    print()
    
    print("CAC TRUONG HOP SU DUNG:")
    print("-" * 40)
    print("• /summary 6   - Xem keo trong 6h qua (sang -> chieu)")
    print("• /summary 12  - Xem keo trong 12h qua (nua ngay)")
    print("• /summary 24  - Xem keo trong 24h qua (1 ngay)")
    print("• /summary 48  - Xem keo trong 48h qua (2 ngay)")
    print("• /summary 168 - Xem keo trong 168h qua (1 tuan)")
    print()
    
    print("THONG BAO KHI KHONG CO KEO:")
    print("-" * 40)
    print("• /summary 6   -> 'Khong co keo nao trong 6 gio qua.'")
    print("• /summary 24  -> 'Khong co keo nao trong 24 gio qua.'")
    print("• /summary 48  -> 'Khong co keo nao trong 2 ngay qua.'")
    print("• /summary 168 -> 'Khong co keo nao trong 7 ngay qua.'")

if __name__ == "__main__":
    main()
