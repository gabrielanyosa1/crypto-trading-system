import sys
from pathlib import Path
import pandas as pd
from datetime import datetime
import logging
from pprint import pprint

# Add project root to path
project_root = str(Path(__file__).resolve().parent.parent)
if project_root not in sys.path:
    sys.path.append(project_root)

from utils.mongodb_utils import MongoDBManager
from utils.logger import setup_logger

# Setup logging
logger = setup_logger('mongodb_test')

def test_mongodb_connection():
    """Test MongoDB connection and analyze collection data."""
    try:
        # Initialize MongoDB connection
        mongo_uri = "mongodb://localhost:27017/"
        db_name = "crypto_data_db"
        collection_name = "crypto_time_series_with_technical_indicators"
        
        db_manager = MongoDBManager(mongo_uri, db_name)
        
        # Test basic connection
        logger.info("Testing MongoDB connection...")
        
        # Get collection information
        logger.info("\nCollection Information:")
        # Count documents
        doc_count = db_manager.db[collection_name].count_documents({})
        logger.info(f"Total documents: {doc_count}")
        
        # Get collection stats safely
        try:
            stats = db_manager.db.command("collstats", collection_name)
            logger.info("Collection stats:")
            logger.info(f"Raw stats: {stats}")
        except Exception as e:
            logger.warning(f"Could not get detailed stats: {e}")
        
        # Get distinct symbols
        symbols = sorted(db_manager.get_distinct_values(collection_name, "symbol"))
        logger.info(f"\nFound {len(symbols)} distinct symbols:")
        logger.info(f"Symbols: {symbols[:10]}...")
        
        # Get date range
        pipeline = [
            {
                "$group": {
                    "_id": None,
                    "min_date": {"$min": "$date"},
                    "max_date": {"$max": "$date"}
                }
            }
        ]
        
        date_range = list(db_manager.db[collection_name].aggregate(pipeline))
        if date_range:
            date_info = date_range[0]
            logger.info(f"\nDate range: {date_info['min_date']} to {date_info['max_date']}")
        
        # Get sample document structure
        sample_doc = db_manager.db[collection_name].find_one()
        if sample_doc:
            logger.info("\nSample document structure:")
            logger.info("Fields available:")
            for field in sorted(sample_doc.keys()):
                field_value = sample_doc[field]
                logger.info(f"- {field}: {type(field_value).__name__} = {field_value}")
        
        # Test data retrieval for first symbol
        if symbols:
            test_symbol = symbols[0]
            logger.info(f"\nTesting data retrieval for {test_symbol}")
            
            # Get sample data
            sample_data = db_manager.get_dataframe(
                collection_name,
                query={"symbol": test_symbol},
                sort_by=[("date", 1)]
            )
            
            logger.info(f"Retrieved {len(sample_data)} records")
            logger.info(f"Columns: {list(sample_data.columns)}")
            
            if not sample_data.empty:
                logger.info("\nBasic statistics for numeric columns:")
                numeric_cols = sample_data.select_dtypes(include=['float64', 'int64']).columns
                for col in numeric_cols[:5]:  # First 5 numeric columns
                    stats = sample_data[col].describe()
                    logger.info(f"\n{col}:")
                    logger.info(stats)
        
        logger.info("\nMongoDB connection test completed successfully!")
        return True
        
    except Exception as e:
        logger.error(f"Error testing MongoDB connection: {str(e)}")
        logger.error("Error details:", exc_info=True)
        raise

if __name__ == "__main__":
    test_mongodb_connection()
