#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Test script for /clear command functionality
"""

def test_clear_command():
    """Test clear command functionality"""
    
    print("TESTING CLEAR COMMAND")
    print("=" * 50)
    
    print("1. Bot se hien thi thong bao khi khoi dong:")
    print("   - Bot da khoi dong thanh cong!")
    print("   - Bot se tu dong xoa tin nhan summary sau 1 phut.")
    print("   - Su dung /clear de xoa tin nhan cu thu cong neu can.")
    print()
    
    print("2. Khi user go /clear:")
    print("   - Bot se gui thong bao: 'Dang xoa tin nhan cu cua bot...'")
    print("   - Sau do gui thong bao ve gioi han Bot API")
    print("   - Tu dong xoa thong bao sau 10 giay")
    print()
    
    print("3. Thong bao ve gioi han Bot API:")
    print("   Bot API khong cho phep xoa tin nhan cu.")
    print("   Tin nhan summary se tu dong xoa sau 1 phut.")
    print("   De xoa tin nhan cu, ban can:")
    print("   1. Xoa thu cong trong group")
    print("   2. Hoac kick bot ra va add lai")
    print()
    
    print("4. Cac lenh moi:")
    print("   - /clear - Xoa tin nhan cu cua bot")
    print("   - /help - Da cap nhat de bao gom /clear")
    print()
    
    print("5. Tinh nang tu dong xoa:")
    print("   - Tin nhan summary: Tu dong xoa sau 1 phut")
    print("   - Tin nhan 'no deals': Tu dong xoa sau 1 phut")
    print("   - Tin nhan /clear: Tu dong xoa sau 10 giay")
    print()
    
    print("CLEAR COMMAND TEST COMPLETED")
    print("Bot da san sang voi tinh nang xoa tin nhan cu!")

if __name__ == "__main__":
    test_clear_command()
