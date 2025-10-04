#!/usr/bin/env python3
"""
Script test format contract address
"""

def test_contract_format():
    """Test format contract address để có thể click và copy"""
    
    print("TEST FORMAT CONTRACT ADDRESS")
    print("=" * 50)
    
    # Contract address mẫu
    contract = "0x1234567890123456789012345678901234567890"
    
    # Format cũ (không thể click)
    old_format = f"Contract: {contract}"
    
    # Format mới (có thể click và copy)
    new_format = f"Contract: `{contract}`"
    
    print("FORMAT CU (khong the click):")
    print(old_format)
    print()
    
    print("FORMAT MOI (co the click va copy):")
    print(new_format)
    print()
    
    print("HUONG DAN SU DUNG:")
    print("-" * 30)
    print("1. Trong Telegram, contract address se hien thi trong o vuong")
    print("2. Click vao contract address se copy vao clipboard")
    print("3. Paste vao DexScreener hoac DEX khac de tim token")
    print()
    
    print("VI DU HOAN CHINH:")
    print("-" * 30)
    example = f"""1. **Token Name** (SYMBOL)
Contract: `{contract}`
Nguoi gui: username
Thoi gian: 04/10/2025 10:30
Gia luc gui: $0.001234
Gia hien tai: $0.001456
Thay doi: +18.0%"""
    
    print(example)

if __name__ == "__main__":
    test_contract_format()
