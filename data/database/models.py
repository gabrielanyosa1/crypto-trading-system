from datetime import datetime
from typing import Dict, List, Optional

class MarketData:
    """Market data schema definition."""
    
    def __init__(self, 
                 symbol: str,
                 date: datetime,
                 close: float,
                 volume: float,
                 technical_indicators: Dict[str, float],
                 metadata: Optional[Dict] = None):
        self.symbol = symbol
        self.date = date
        self.close = close
        self.volume = volume
        self.technical_indicators = technical_indicators
        self.metadata = metadata or {}

    def to_dict(self) -> Dict:
        """Convert to dictionary for MongoDB storage."""
        return {
            'symbol': self.symbol,
            'date': self.date,
            'close': self.close,
            'volume': self.volume,
            'technical_indicators': self.technical_indicators,
            'metadata': self.metadata
        }

    @classmethod
    def from_dict(cls, data: Dict) -> 'MarketData':
        """Create instance from dictionary."""
        return cls(
            symbol=data['symbol'],
            date=data['date'],
            close=data['close'],
            volume=data['volume'],
            technical_indicators=data.get('technical_indicators', {}),
            metadata=data.get('metadata', {})
        )