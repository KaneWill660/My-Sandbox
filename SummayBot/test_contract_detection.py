import re

def test_contract_detection():
    """Test contract detection với tin nhắn thực tế"""
    
    # Regex pattern hiện tại từ bot
    contract_pattern = re.compile(r'0x[a-fA-F0-9]{40}')
    
    # Tin nhắn test của user
    test_message = """kèo " 1234 " 
CA : 0x0fD6Bc232D04D4d0b54772D4F13C72e1e13d4444"""
    
    print("TESTING CONTRACT DETECTION")
    print("=" * 50)
    print(f"Tin nhan test: {repr(test_message)}")
    print()
    
    # Tìm tất cả contract addresses
    contracts = contract_pattern.findall(test_message)
    
    print(f"So luong contracts tim thay: {len(contracts)}")
    for i, contract in enumerate(contracts, 1):
        print(f"Contract {i}: {contract}")
    
    print()
    
    # Test với các format khác
    test_cases = [
        "0x0fD6Bc232D04D4d0b54772D4F13C72e1e13d4444",
        "CA: 0x0fD6Bc232D04D4d0b54772D4F13C72e1e13d4444",
        "Contract: 0x0fD6Bc232D04D4d0b54772D4F13C72e1e13d4444",
        "0x0fD6Bc232D04D4d0b54772D4F13C72e1e13d4444",
        "keo 0x0fD6Bc232D04D4d0b54772D4F13C72e1e13d4444",
        "0x0fD6Bc232D04D4d0b54772D4F13C72e1e13d4444 - token moi",
    ]
    
    print("TEST CAC FORMAT KHAC:")
    print("-" * 30)
    for i, test_case in enumerate(test_cases, 1):
        contracts = contract_pattern.findall(test_case)
        print(f"{i}. {test_case}")
        print(f"   Tim thay: {len(contracts)} contracts")
        for contract in contracts:
            print(f"   -> {contract}")
        print()

if __name__ == "__main__":
    test_contract_detection()
