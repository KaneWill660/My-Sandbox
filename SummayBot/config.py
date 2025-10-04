# Cấu hình bot
BOT_TOKEN = "XXX"  # Thay bằng token từ BotFather

# Cấu hình database
DATABASE_PATH = "coin_tracker.db"

# Cấu hình API
PRICE_APIS = {
    'dexscreener': 'https://api.dexscreener.com/latest/dex/tokens/',
    'coingecko': 'https://api.coingecko.com/api/v3/simple/token_price/ethereum'
}

# Cấu hình regex cho contract addresses
CONTRACT_PATTERN = r'0x[a-fA-F0-9]{40}'

# Giới hạn thời gian tối đa cho summary (ngày)
MAX_SUMMARY_DAYS = 30

# Giới hạn độ dài message
MAX_MESSAGE_LENGTH = 4000
