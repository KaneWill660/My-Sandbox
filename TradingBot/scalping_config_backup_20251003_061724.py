import os

def read_env_file():
    """Read .env file directly"""
    env_vars = {}
    try:
        with open('.env', 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#') and '=' in line:
                    key, value = line.split('=', 1)
                    env_vars[key.strip()] = value.strip()
    except Exception as e:
        print(f"Warning: Could not read .env file: {e}")
    return env_vars

# Load environment variables from .env file
env_vars = read_env_file()

class ScalpingConfig:
    # Binance API Configuration
    BINANCE_API_KEY = env_vars.get('BINANCE_API_KEY', '')
    BINANCE_SECRET_KEY = env_vars.get('BINANCE_SECRET_KEY', '')
    
    # Telegram Configuration
    TELEGRAM_BOT_TOKEN = env_vars.get('TELEGRAM_BOT_TOKEN', '')
    TELEGRAM_CHAT_ID = '@tradingbotbykane'  # Your Telegram channel
    
    # Scalping Trading Configuration
    SYMBOL = 'BTCUSDT'
    TIMEFRAME = '5m'  # 5 minute timeframe for scalping
    LIMIT = 100  # Number of candles to fetch
    
    # Scalping Indicator Settings (optimized for 5m)
    RSI_PERIOD = 9  # Shorter RSI for scalping
    RSI_OVERSOLD = 25  # More aggressive oversold
    RSI_OVERBOUGHT = 75  # More aggressive overbought
    
    MACD_FAST = 5   # Faster MACD
    MACD_SLOW = 13  # Faster MACD
    MACD_SIGNAL = 4 # Faster signal
    
    EMA_SHORT = 5   # Very short EMA
    EMA_LONG = 15   # Short EMA
    
    BOLLINGER_PERIOD = 20
    BOLLINGER_STD = 2
    
    STOCHASTIC_K = 9
    STOCHASTIC_D = 3
    
    WILLIAMS_PERIOD = 9
    
    ATR_PERIOD = 14
    
    # Ichimoku Cloud Settings
    ICHIMOKU_CONVERSION = 9
    ICHIMOKU_BASE = 26
    ICHIMOKU_SPAN_B = 52
    
    # Scalping Signal Strength Thresholds
    MIN_SIGNAL_STRENGTH = 0.2  # Adjusted threshold
    
    # Scalping Risk Management
    LEVERAGE = 5  # 5x leverage
    TAKE_PROFIT_PERCENT = 20.0      # 20% take profit (4% spot) - single target
    MAX_STOP_LOSS_PERCENT = 10.0    # Maximum 10% stop loss (2% spot)
    
    # Position Sizing
    MAX_POSITION_SIZE_PERCENT = 5.0  # Max 5% of portfolio per trade
    
    # Notification Settings
    ENABLE_NOTIFICATIONS = True
    NOTIFICATION_COOLDOWN = 300  # 5 minutes between notifications
    
    # Scalping Specific Settings
    SCALPING_ENABLED = True
    SCALPING_TIMEFRAME = '5m'
    SCALPING_LEVERAGE = 5
    
    # Logging
    LOG_LEVEL = 'INFO'