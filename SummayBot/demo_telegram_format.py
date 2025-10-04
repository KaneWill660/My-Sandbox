#!/usr/bin/env python3
"""
Demo script hien thi format moi de doc tren Telegram
"""

def main():
    print("DEMO FORMAT MOI CHO TELEGRAM")
    print("=" * 60)
    print()
    
    print("THAY DOI CHINH:")
    print("-" * 30)
    print("+ Bo format bang monospace")
    print("+ Su dung danh sach de doc")
    print("+ Them emoji va markdown")
    print("+ Contract trong code block")
    print("+ De copy paste hon")
    print()
    
    print("DEMO FORMAT MOI:")
    print("-" * 30)
    
    demo_output = """TONG HOP KEO 6 GIO QUA

1. PEPE (PEPE)
Contract: 0x6982508145454Ce325dDbE47a25d4ec3d2311933
Nguoi gui: crypto_trader
Thoi gian: 15/12/2024 14:30
Gia luc gui: $0.00000012
Gia hien tai: $0.00000016
Thay doi: +27.0%

2. Shiba Inu (SHIB)
Contract: 0x95aD61b0a150d79219dCF64E1E6Cc01f0B64C4cE
Nguoi gui: moon_hunter
Thoi gian: 15/12/2024 16:45
Gia luc gui: $0.0005679
Gia hien tai: $0.0004321
Thay doi: -23.9%

3. DogeCoin (DOGE)
Contract: 0x4206931337dc273a630d328dA6441786BfaD668f
Nguoi gui: diamond_hands
Thoi gian: 15/12/2024 18:20
Gia luc gui: $0.00000123
Gia hien tai: $0.00000234
Thay doi: +90.2%

4. Unknown (UNKNOWN)
Contract: 0x1111111111111111111111111111111111111111
Nguoi gui: whale_alert
Thoi gian: 15/12/2024 20:15
Gia luc gui: $0.00000000012
Gia hien tai: $0.00000000045
Thay doi: +275.0%

5. Pump Token (PUMP)
Contract: 0x3333333333333333333333333333333333333333
Nguoi gui: pump_king
Thoi gian: 15/12/2024 22:30
Gia luc gui: $0.0002346
Gia hien tai: $0.0001988
Thay doi: -15.2%"""
    
    print(demo_output)
    print()
    
    print("=" * 60)
    print()
    
    print("SO SANH FORMAT CU VA MOI:")
    print("-" * 30)
    
    print("FORMAT CU (bang monospace):")
    print("-" * 25)
    old_format = """```
Token               Contract                                      Nguoi gui       Thoi gian    Gia gui         Gia hien tai    Thay doi  
----------------------------------------------------------------------------------------------------------------------------------
PEPE (PEPE)        0x6982508145454Ce325dDbE47a25d4ec3d2311933     crypto_trader   15/12 14:30  $0.00000012     $0.00000016     +27.0%    
Shiba Inu (SHIB)   0x95aD61b0a150d79219dCF64E1E6Cc01f0B64C4cE     moon_hunter     15/12 16:45  $0.0005679      $0.0004321      -23.9%    
```"""
    print(old_format)
    print()
    
    print("FORMAT MOI (danh sach):")
    print("-" * 25)
    new_format = """1. PEPE (PEPE)
Contract: 0x6982508145454Ce325dDbE47a25d4ec3d2311933
Nguoi gui: crypto_trader
Thoi gian: 15/12/2024 14:30
Gia luc gui: $0.00000012
Gia hien tai: $0.00000016
Thay doi: +27.0%

2. Shiba Inu (SHIB)
Contract: 0x95aD61b0a150d79219dCF64E1E6Cc01f0B64C4cE
Nguoi gui: moon_hunter
Thoi gian: 15/12/2024 16:45
Gia luc gui: $0.0005679
Gia hien tai: $0.0004321
Thay doi: -23.9%"""
    print(new_format)
    print()
    
    print("=" * 60)
    print()
    
    print("UU DIEM CUA FORMAT MOI:")
    print("-" * 30)
    print("+ De doc tren mobile - khong bi vo format")
    print("+ Contract trong code block - de copy")
    print("+ Emoji ro rang - de nhan biet")
    print("+ So thu tu - de theo doi")
    print("+ Markdown bold - de nhin")
    print("+ Khong bi gioi han chieu rong")
    print()
    
    print("CACH SU DUNG:")
    print("-" * 30)
    print("1. Xem so thu tu va ten token")
    print("2. Click vao contract trong code block")
    print("3. Copy contract address")
    print("4. Paste len DexScreener")
    print("5. Xem chi tiet token")
    print()
    
    print("VI DU THUC TE TREN TELEGRAM:")
    print("-" * 30)
    print("• Ten token duoc in dam")
    print("• Contract trong code block (backtick)")
    print("• Emoji cho moi thong tin")
    print("• So thu tu de theo doi")
    print("• Khong bi vo format tren mobile")
    print()
    
    print("LUU Y:")
    print("-" * 30)
    print("• Format nay toi uu cho Telegram")
    print("• De doc tren ca desktop va mobile")
    print("• Contract de copy paste")
    print("• Khong bi gioi han chieu rong")
    print("• Emoji lam ro rang hon")

if __name__ == "__main__":
    main()
