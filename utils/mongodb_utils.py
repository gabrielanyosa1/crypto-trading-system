from typing import Dict, List, Optional
from datetime import datetime
import pandas as pd
from pymongo import MongoClient, ASCENDING, DESCENDING
from pymongo.errors import BulkWriteError
import logging

logger = logging.getLogger(__name__)

class MongoDBManager:
    """Utility class for MongoDB operations with enhanced functionality."""
    
    def __init__(self, uri: str, database: str):
        self.client = MongoClient(uri)
        self.db = self.client[database]
        
    def bulk_insert(self, collection: str, documents: List[Dict], 
                   ordered: bool = True) -> int:
        """Bulk insert documents with error handling."""
        try:
            result = self.db[collection].insert_many(documents, ordered=ordered)
            return len(result.inserted_ids)
        except BulkWriteError as bwe:
            logger.error(f"Bulk write error: {bwe.details}")
            return len(bwe.details['nInserted'])
            
    def get_dataframe(self, collection: str, query: Dict = None, 
                     projection: Dict = None, sort_by: List = None) -> pd.DataFrame:
        """Retrieve data as pandas DataFrame."""
        cursor = self.db[collection].find(
            filter=query or {},
            projection=projection
        )
        
        if sort_by:
            cursor = cursor.sort(sort_by)
            
        return pd.DataFrame(list(cursor))
        
    def create_index(self, collection: str, keys: List[tuple], unique: bool = False):
        """Create index on collection."""
        self.db[collection].create_index(keys, unique=unique)
        
    def get_distinct_values(self, collection: str, field: str, 
                          query: Dict = None) -> List:
        """Get distinct values for a field."""
        return self.db[collection].distinct(field, query)
        
    def update_documents(self, collection: str, query: Dict, 
                        update: Dict, upsert: bool = False) -> int:
        """Update documents with error handling."""
        try:
            result = self.db[collection].update_many(
                query, {'$set': update}, upsert=upsert
            )
            return result.modified_count
        except Exception as e:
            logger.error(f"Update error: {str(e)}")
            raise
        