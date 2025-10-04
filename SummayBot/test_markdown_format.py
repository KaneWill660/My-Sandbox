#!/usr/bin/env python3
"""
Script test Markdown format cho bot
"""

def test_markdown_format():
    """Test Markdown format cho bot"""
    
    print("TEST MARKDOWN FORMAT")
    print("=" * 50)
    
    # Contract address mẫu
    contract = "0x1234567890123456789012345678901234567890"
    
    # Format Markdown
    markdown_text = f"""**TONG HOP KEO 24 GIO QUA**
Group: Test Group

**1. Token Name (SYMBOL)**
Contract: `{contract}`
Nguoi gui: username
Thoi gian: 04/10/2025 10:30
Gia luc gui: $0.001234
Gia hien tai: $0.001456
Thay doi: +18.0%

**2. Another Token (TOKEN)**
Contract: `0xabcdef1234567890abcdef1234567890abcdef12`
Nguoi gui: user2
Thoi gian: 04/10/2025 09:15
Gia luc gui: $0.000567
Gia hien tai: $0.000789
Thay doi: +39.2%

Tin nhan nay se tu dong xoa sau 1 phut"""
    
    print("MARKDOWN FORMAT:")
    print("-" * 30)
    print(markdown_text)
    print()
    
    print("TINH NANG MARKDOWN:")
    print("-" * 30)
    print("+ **Bold text** - Ten token va so thu tu")
    print("+ `Code format` - Contract address co the click va copy")
    print("+ Tu dong xoa sau 1 phut")
    print("+ Phan biet group")
    
    print()
    print("HUONG DAN SU DUNG:")
    print("-" * 30)
    print("1. Trong Telegram, contract address se hien thi trong o vuong")
    print("2. Click vao contract address se copy vao clipboard")
    print("3. Paste vao DexScreener hoac DEX khac de tim token")
    print("4. Bot se tu dong xoa tin nhan sau 1 phut")
    print("5. Moi group chi hien thi keo cua rieng group do")

if __name__ == "__main__":
    test_markdown_format()
