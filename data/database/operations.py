from typing import List, Dict, Optional
from pymongo import MongoClient
from datetime import datetime
from config.settings import MONGODB_LOCAL_URI, MONGODB_DATABASE

class DatabaseManager:
    """Handle database operations for the trading system."""
    
    def __init__(self, uri: str = MONGODB_LOCAL_URI, db_name: str = MONGODB_DATABASE):
        self.client = MongoClient(uri)
        self.db = self.client[db_name]
        
    def insert_market_data(self, collection: str, data: Dict) -> str:
        """Insert market data into specified collection."""
        result = self.db[collection].insert_one(data)
        return str(result.inserted_id)
        
    def get_market_data(self, 
                       collection: str,
                       symbol: Optional[str] = None,
                       start_date: Optional[datetime] = None,
                       end_date: Optional[datetime] = None,
                       limit: Optional[int] = None) -> List[Dict]:
        """Retrieve market data with optional filters."""
        query = {}
        if symbol:
            query['symbol'] = symbol
        if start_date or end_date:
            query['date'] = {}
            if start_date:
                query['date']['$gte'] = start_date
            if end_date:
                query['date']['$lte'] = end_date
                
        cursor = self.db[collection].find(query)
        if limit:
            cursor = cursor.limit(limit)
            
        return list(cursor)
        
    def update_market_data(self, collection: str, query: Dict, update: Dict) -> int:
        """Update market data documents matching query."""
        result = self.db[collection].update_many(query, {'$set': update})
        return result.modified_count
        
    def delete_market_data(self, collection: str, query: Dict) -> int:
        """Delete market data documents matching query."""
        result = self.db[collection].delete_many(query)
        return result.deleted_count