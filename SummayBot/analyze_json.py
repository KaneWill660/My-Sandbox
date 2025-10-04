#!/usr/bin/env python3
"""
Script phân tích file JSON để tìm contract addresses
"""

import json
import re
from datetime import datetime

def analyze_json_file(json_file_path):
    """Phân tích file JSON để tìm contract addresses"""
    
    print(f"Dang doc file: {json_file_path}")
    
    try:
        with open(json_file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # Lấy thông tin cơ bản
        name = data.get('name', 'Unknown')
        chat_type = data.get('type', 'Unknown')
        chat_id = data.get('id', 'Unknown')
        
        print(f"Group: {name}")
        print(f"Type: {chat_type}")
        print(f"Chat ID: {chat_id}")
        print()
        
        messages = data.get('messages', [])
        print(f"Tim thay {len(messages)} tin nhan")
        
        # Tìm contract addresses
        contract_pattern = r'0x[a-fA-F0-9]{40}'
        contract_messages = []
        
        for msg in messages:
            text = msg.get('text', '')
            if isinstance(text, str):
                contracts = re.findall(contract_pattern, text)
                if contracts:
                    contract_messages.append({
                        'text': text,
                        'contracts': contracts,
                        'date': msg.get('date', ''),
                        'from': msg.get('from', 'Unknown')
                    })
        
        print(f"Tim thay {len(contract_messages)} tin nhan co contract address")
        print()
        
        # Hiển thị tất cả contract addresses
        all_contracts = set()
        for msg in contract_messages:
            for contract in msg['contracts']:
                all_contracts.add(contract)
        
        print(f"Tong so contract addresses duy nhat: {len(all_contracts)}")
        print()
        
        # Hiển thị 10 contract đầu tiên
        print("10 contract addresses dau tien:")
        for i, contract in enumerate(list(all_contracts)[:10], 1):
            print(f"{i}. {contract}")
        
        if len(all_contracts) > 10:
            print(f"... va {len(all_contracts) - 10} contract khac")
        
        print()
        
        # Hiển thị 5 tin nhắn đầu tiên có contract
        print("5 tin nhan dau tien co contract address:")
        for i, msg in enumerate(contract_messages[:5], 1):
            print(f"{i}. Tu {msg['from']} ({msg['date']}):")
            print(f"   {msg['text'][:100]}...")
            print(f"   Contract: {msg['contracts']}")
            print()
        
        # Tính chat_id đúng
        if isinstance(chat_id, int) and chat_id > 0:
            correct_chat_id = f"-100{chat_id}"
            print(f"Chat ID dung: {correct_chat_id}")
        else:
            print(f"Chat ID: {chat_id}")
        
        return contract_messages, all_contracts
        
    except Exception as e:
        print(f"Loi doc file: {e}")
        return [], set()

if __name__ == "__main__":
    json_file = r".\data\result.json"
    analyze_json_file(json_file)
