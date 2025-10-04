#!/usr/bin/env python3
"""
Demo script hien thi ket qua moi voi ten token va contract day du
"""

def main():
    print("DEMO BANG MOI VOI TEN TOKEN VA CONTRACT DAY DU")
    print("=" * 80)
    print()
    
    print("THAY DOI CHINH:")
    print("-" * 40)
    print("+ Them cot 'Token' hien thi ten va symbol")
    print("+ Contract address hien thi day du (khong rut gon)")
    print("+ Lay thong tin token tu DexScreener API")
    print("+ Co the copy contract de paste len DexScreener")
    print()
    
    print("DEMO BANG MOI:")
    print("-" * 40)
    
    demo_output = """TONG HOP KEO 6 GIO QUA

```
Token               Contract                                      Nguoi gui       Thoi gian    Gia gui         Gia hien tai    Thay doi  
----------------------------------------------------------------------------------------------------------------------------------
PEPE (PEPE)        0x6982508145454Ce325dDbE47a25d4ec3d2311933     crypto_trader   15/12 14:30  $0.00000012     $0.00000016     +27.0%    
Shiba Inu (SHIB)   0x95aD61b0a150d79219dCF64E1E6Cc01f0B64C4cE     moon_hunter     15/12 16:45  $0.0005679      $0.0004321      -23.9%    
DogeCoin (DOGE)    0x4206931337dc273a630d328dA6441786BfaD668f     diamond_hands   15/12 18:20  $0.00000123     $0.00000234     +90.2%    
Unknown (UNKNOWN)  0x1111111111111111111111111111111111111111     whale_alert     15/12 20:15  $0.00000000012  $0.00000000045  +275.0%   
Pump Token (PUMP)  0x3333333333333333333333333333333333333333     pump_king       15/12 22:30  $0.0002346      $0.0001988      -15.2%    
```"""
    
    print(demo_output)
    print()
    
    print("=" * 80)
    print()
    
    print("SO SANH FORMAT CU VA MOI:")
    print("-" * 40)
    
    print("FORMAT CU:")
    print("-" * 20)
    old_format = """```
Contract     Nguoi gui       Thoi gian    Gia gui         Gia hien tai    Thay doi  
-------------------------------------------------------------------------------------
0x1234...7890 crypto_trader   15/12 14:30  $0.00000012     $0.00000016     +27.0%    
0xabcd...1234 moon_hunter     15/12 16:45  $0.0005679      $0.0004321      -23.9%    
```"""
    print(old_format)
    print()
    
    print("FORMAT MOI:")
    print("-" * 20)
    new_format = """```
Token               Contract                                      Nguoi gui       Thoi gian    Gia gui         Gia hien tai    Thay doi  
----------------------------------------------------------------------------------------------------------------------------------
PEPE (PEPE)        0x6982508145454Ce325dDbE47a25d4ec3d2311933     crypto_trader   15/12 14:30  $0.00000012     $0.00000016     +27.0%    
Shiba Inu (SHIB)   0x95aD61b0a150d79219dCF64E1E6Cc01f0B64C4cE     moon_hunter     15/12 16:45  $0.0005679      $0.0004321      -23.9%    
```"""
    print(new_format)
    print()
    
    print("=" * 80)
    print()
    
    print("UU DIEM CUA FORMAT MOI:")
    print("-" * 40)
    print("+ Hien thi ten token - de nhan biet hon")
    print("+ Contract day du - co the copy paste len DexScreener")
    print("+ Symbol token - de tim kiem nhanh")
    print("+ Thong tin day du - khong can tra cuu them")
    print("+ Chuyen nghiep hon - giong cac bang thong ke thuc te")
    print()
    
    print("CACH SU DUNG:")
    print("-" * 40)
    print("1. Xem ten token trong cot 'Token'")
    print("2. Copy contract address tu cot 'Contract'")
    print("3. Paste len DexScreener de xem chi tiet")
    print("4. So sanh gia va % thay doi")
    print("5. Tim kiem token bang ten hoac symbol")
    print()
    
    print("VI DU THUC TE:")
    print("-" * 40)
    print("• PEPE (PEPE) - 0x6982508145454Ce325dDbE47a25d4ec3d2311933")
    print("• Shiba Inu (SHIB) - 0x95aD61b0a150d79219dCF64E1E6Cc01f0B64C4cE")
    print("• DogeCoin (DOGE) - 0x4206931337dc273a630d328dA6441786BfaD668f")
    print("• Unknown (UNKNOWN) - 0x1111111111111111111111111111111111111111")
    print()
    
    print("LUU Y:")
    print("-" * 40)
    print("• Ten token duoc lay tu DexScreener API")
    print("• Neu khong tim thay se hien thi 'Unknown'")
    print("• Contract address hien thi day du 42 ky tu")
    print("• Co the copy truc tiep de su dung")
    print("• Bang rong hon nhung thong tin day du hon")

if __name__ == "__main__":
    main()
