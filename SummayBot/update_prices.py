#!/usr/bin/env python3
"""
Script cập nhật giá cho các tin nhắn đã import
"""

import sqlite3
import asyncio
import aiohttp
from datetime import datetime

class PriceUpdater:
    def __init__(self, db_path="coin_tracker.db"):
        self.db_path = db_path
        self.price_apis = {
            'dexscreener': 'https://api.dexscreener.com/latest/dex/tokens/',
            'coingecko': 'https://api.coingecko.com/api/v3/simple/token_price/ethereum'
        }
    
    async def get_token_price(self, contract_address: str) -> float:
        """Lấy giá token từ DexScreener hoặc CoinGecko"""
        try:
            # Thử DexScreener API trước
            async with aiohttp.ClientSession() as session:
                url = f"{self.price_apis['dexscreener']}{contract_address}"
                async with session.get(url) as response:
                    if response.status == 200:
                        data = await response.json()
                        if data.get('pairs') and len(data['pairs']) > 0:
                            # Lấy pair có liquidity cao nhất
                            best_pair = max(data['pairs'], key=lambda x: float(x.get('liquidity', {}).get('usd', 0)))
                            price = float(best_pair.get('priceUsd', 0))
                            if price > 0:
                                return price
            
            # Fallback: Thử CoinGecko API
            async with aiohttp.ClientSession() as session:
                url = f"{self.price_apis['coingecko']}?contract_addresses={contract_address}&vs_currencies=usd"
                async with session.get(url) as response:
                    if response.status == 200:
                        data = await response.json()
                        if contract_address.lower() in data:
                            price = float(data[contract_address.lower()]['usd'])
                            if price > 0:
                                return price
        
        except Exception as e:
            print(f"Loi lay gia cho {contract_address}: {e}")
        
        return None
    
    def update_prices(self):
        """Cập nhật giá cho các tin nhắn chưa có giá"""
        
        print("CAP NHAT GIA CHO CAC TIN NHAN DA IMPORT")
        print("=" * 50)
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Lấy các tin nhắn chưa có giá
        cursor.execute('''
            SELECT DISTINCT contract_address 
            FROM coin_signals 
            WHERE price_at_signal IS NULL
        ''')
        
        contracts = cursor.fetchall()
        print(f"Tim thay {len(contracts)} contract addresses chua co gia")
        
        if not contracts:
            print("Tat ca contract addresses da co gia!")
            conn.close()
            return
        
        # Cap nhat gia cho tung contract
        updated_count = 0
        failed_count = 0
        
        for contract_tuple in contracts:
            contract = contract_tuple[0]
            print(f"Dang cap nhat gia cho: {contract[:20]}...")
            
            # Lay gia
            price = asyncio.run(self.get_token_price(contract))
            
            if price:
                # Cap nhat gia trong database
                cursor.execute('''
                    UPDATE coin_signals 
                    SET price_at_signal = ?
                    WHERE contract_address = ? AND price_at_signal IS NULL
                ''', (price, contract))
                
                updated_count += 1
                print(f"  + Cap nhat gia: ${price}")
            else:
                failed_count += 1
                print(f"  - Khong the lay gia")
        
        conn.commit()
        conn.close()
        
        print()
        print(f"HOAN THANH!")
        print(f"+ Cap nhat thanh cong: {updated_count} contract")
        print(f"- Khong the cap nhat: {failed_count} contract")

if __name__ == "__main__":
    updater = PriceUpdater()
    updater.update_prices()
