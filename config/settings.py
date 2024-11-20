import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Base directory
BASE_DIR = Path(__file__).resolve().parent.parent

# MongoDB settings
MONGODB_LOCAL_URI = os.getenv('MONGODB_LOCAL_URI', 'mongodb://localhost:27017')
MONGODB_ATLAS_URI = os.getenv('MONGODB_ATLAS_URI')
MONGODB_DATABASE = os.getenv('MONGODB_DATABASE', 'crypto_trading')

# Data settings
DATA_START_DATE = '2023-01-07'
DATA_END_DATE = '2024-11-14'

# Trading settings
RISK_FREE_RATE = 0.02
MAX_POSITION_SIZE = 0.05  # 5% of portfolio
MIN_CASH_POSITION = 0.25  # 25% minimum cash
MAX_DRAWDOWN = 0.02      # 2% maximum daily drawdown

# Model settings
PREDICTION_HORIZON = 1    # days
TRAINING_WINDOW = 252    # one trading year
VALIDATION_WINDOW = 63   # one quarter

# Feature groups
TECHNICAL_FEATURES = [
    'trend_sma_fast', 'trend_sma_slow',
    'momentum_rsi', 'momentum_stoch',
    'volatility_bbm', 'volatility_atr',
    'volume_em', 'volume_vwap'
]