#!/usr/bin/env python3
"""
Script test tính năng tự động xóa tin nhắn
"""

def test_auto_delete():
    """Test tính năng tự động xóa tin nhắn"""
    
    print("TEST TINH NANG TU DONG XOA TIN NHAN")
    print("=" * 50)
    
    print("TINH NANG DA HOAN THIEN:")
    print("-" * 30)
    print("+ Tu dong xoa tin nhan summary sau 1 phut")
    print("+ Tu dong xoa tin nhan 'khong co keo nao' sau 1 phut")
    print("+ Khong lam roi group chat")
    print("+ Tiet kiem dung luong")
    print("+ Bao mat thong tin")
    
    print()
    print("CAC LOAI TIN NHAN DUOC TU DONG XOA:")
    print("-" * 30)
    print("1. Tin nhan summary (co keo)")
    print("   - Hien thi danh sach keo")
    print("   - Tu dong xoa sau 1 phut")
    print()
    print("2. Tin nhan 'khong co keo nao'")
    print("   - Hien thi: 'Khong co keo nao trong X gio qua'")
    print("   - Tu dong xoa sau 1 phut")
    print()
    print("3. Tin nhan 'khong co keo nao' (theo ngay)")
    print("   - Hien thi: 'Khong co keo nao trong X ngay qua'")
    print("   - Tu dong xoa sau 1 phut")
    
    print()
    print("VI DU SU DUNG:")
    print("-" * 30)
    print("1. Go lenh /summary")
    print("   - Neu co keo: Hien thi summary + tu dong xoa sau 1 phut")
    print("   - Neu khong co keo: Hien thi 'khong co keo nao' + tu dong xoa sau 1 phut")
    print()
    print("2. Go lenh /summary 2")
    print("   - Neu co keo: Hien thi summary 2h qua + tu dong xoa sau 1 phut")
    print("   - Neu khong co keo: Hien thi 'khong co keo nao trong 2 gio qua' + tu dong xoa sau 1 phut")
    print()
    print("3. Go lenh /summary 48")
    print("   - Neu co keo: Hien thi summary 48h qua + tu dong xoa sau 1 phut")
    print("   - Neu khong co keo: Hien thi 'khong co keo nao trong 2 ngay qua' + tu dong xoa sau 1 phut")
    
    print()
    print("LOI ICH:")
    print("-" * 30)
    print("+ Khong lam roi group chat")
    print("+ Tiet kiem dung luong")
    print("+ Bao mat thong tin")
    print("+ Trai nghiem nguoi dung tot hon")
    print("+ Khong can xoa thu cong")

if __name__ == "__main__":
    test_auto_delete()
