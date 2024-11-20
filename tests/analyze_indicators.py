import sys
from pathlib import Path
import pandas as pd
import numpy as np
from datetime import datetime
import logging
from scipy.stats import pearsonr
import matplotlib.pyplot as plt
import seaborn as sns

# Add project root to path
project_root = str(Path(__file__).resolve().parent.parent)
if project_root not in sys.path:
    sys.path.append(project_root)

from utils.mongodb_utils import MongoDBManager
from utils.logger import setup_logger

# Setup logging
logger = setup_logger('enhanced_indicator_analysis')

def analyze_predictive_power_enhanced(data: pd.DataFrame, 
                                    forward_periods: list = [1, 3, 5, 10],
                                    correlation_threshold: float = 0.1,
                                    pvalue_threshold: float = 0.05):
    """
    Enhanced analysis of indicators' predictive power over different time horizons.
    """
    results = {}
    price_changes = {}
    
    # Calculate price changes for different periods
    for period in forward_periods:
        price_changes[period] = data['close'].astype(float).pct_change(period).shift(-period)
    
    # Get numeric columns only
    numeric_columns = data.select_dtypes(include=[np.number]).columns
    
    # Analyze indicators
    for column in numeric_columns:
        if column in ['date', 'symbol', 'close', 'open', 'high', 'low', 'volume']:
            continue
            
        # Ensure data is clean and numeric
        indicator_data = pd.to_numeric(data[column], errors='coerce')
        indicator_results = {}
        
        for period, changes in price_changes.items():
            # Remove any NaN values
            mask = ~(indicator_data.isna() | changes.isna())
            if mask.sum() < 2:  # Need at least 2 points for correlation
                continue
                
            try:
                # Calculate correlation
                correlation, p_value = pearsonr(
                    indicator_data[mask].values,
                    changes[mask].values
                )
                
                # Store if significant
                if abs(correlation) > correlation_threshold and p_value < pvalue_threshold:
                    indicator_results[period] = {
                        'correlation': correlation,
                        'p_value': p_value
                    }
            except Exception as e:
                logger.warning(f"Error calculating correlation for {column} at period {period}: {str(e)}")
                continue
        
        if indicator_results:
            results[column] = indicator_results
    
    return results

def analyze_technical_indicators_enhanced(symbol: str = "BTC-USD"):
    """Enhanced analysis of technical indicators for a specific symbol."""
    try:
        # Initialize MongoDB connection
        mongo_uri = "mongodb://localhost:27017/"
        db_name = "crypto_data_db"
        collection_name = "crypto_time_series_with_technical_indicators"
        
        db_manager = MongoDBManager(mongo_uri, db_name)
        
        # Fetch data for the symbol
        data = db_manager.get_dataframe(
            collection_name,
            query={"symbol": symbol},
            sort_by=[("date", 1)]
        )
        
        # Convert price columns to float
        price_columns = ['close', 'open', 'high', 'low']
        for col in price_columns:
            if col in data.columns:
                data[col] = pd.to_numeric(data[col], errors='coerce')
        
        logger.info(f"\nEnhanced Analysis for {symbol}")
        logger.info(f"Data points: {len(data)}")
        
        # Print column types
        logger.info("\nColumn Types:")
        for col in data.columns:
            logger.info(f"{col}: {data[col].dtype}")
        
        # Calculate returns
        data['daily_returns'] = data['close'].pct_change()
        
        # Basic price statistics
        logger.info("\nPrice Statistics:")
        price_stats = data['close'].describe()
        logger.info(price_stats)
        
        # Volatility analysis
        daily_volatility = data['daily_returns'].std()
        annualized_volatility = daily_volatility * np.sqrt(252)
        logger.info(f"\nVolatility Analysis:")
        logger.info(f"Daily Volatility: {daily_volatility:.4f}")
        logger.info(f"Annualized Volatility: {annualized_volatility:.4f}")
        
        # Enhanced predictive power analysis
        logger.info("\nPredictive Power Analysis:")
        predictive_results = analyze_predictive_power_enhanced(data)
        
        # Sort indicators by their predictive power
        indicator_scores = {}
        for indicator, periods in predictive_results.items():
            # Calculate average absolute correlation across periods
            avg_correlation = np.mean([abs(p['correlation']) for p in periods.values()])
            indicator_scores[indicator] = avg_correlation
        
        # Sort and display top indicators
        top_indicators = dict(sorted(indicator_scores.items(), 
                                   key=lambda x: abs(x[1]), reverse=True)[:15])
        
        logger.info("\nTop 15 Most Predictive Indicators:")
        for indicator, score in top_indicators.items():
            logger.info(f"{indicator}: {score:.4f}")
            # Show detailed period analysis
            if indicator in predictive_results:
                for period, metrics in predictive_results[indicator].items():
                    logger.info(f"  {period} day forecast: correlation={metrics['correlation']:.4f}, "
                              f"p-value={metrics['p_value']:.4f}")
        
        # Calculate correlation matrix for top indicators
        top_indicator_names = list(top_indicators.keys())
        if top_indicator_names:
            correlation_matrix = data[top_indicator_names].corr()
            
            # Create output directory if it doesn't exist
            output_dir = Path("analysis_output")
            output_dir.mkdir(exist_ok=True)
            
            # Save correlation matrix plot
            plt.figure(figsize=(12, 8))
            sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', center=0)
            plt.title(f"Indicator Correlation Matrix - {symbol}")
            plt.tight_layout()
            plt.savefig(output_dir / f"{symbol}_correlation_matrix.png")
            plt.close()
            
            # Identify highly correlated pairs
            logger.info("\nHighly Correlated Indicator Pairs:")
            for i in range(len(top_indicator_names)):
                for j in range(i+1, len(top_indicator_names)):
                    correlation = correlation_matrix.iloc[i, j]
                    if abs(correlation) > 0.7:  # Threshold for high correlation
                        logger.info(f"{top_indicator_names[i]} & {top_indicator_names[j]}: "
                                  f"{correlation:.4f}")
            
            # Save indicator importance report
            report = pd.DataFrame(list(top_indicators.items()), 
                                columns=['Indicator', 'Predictive Score'])
            report.to_csv(output_dir / f"{symbol}_indicator_importance.csv", index=False)
            
            logger.info(f"\nAnalysis artifacts saved to {output_dir}")
        
        return {
            'top_indicators': top_indicators,
            'predictive_results': predictive_results,
            'correlation_matrix': correlation_matrix if top_indicator_names else None
        }
        
    except Exception as e:
        logger.error(f"Error in enhanced analysis: {str(e)}")
        logger.error("Error details:", exc_info=True)
        raise

if __name__ == "__main__":
    # Create output directory
    Path("analysis_output").mkdir(exist_ok=True)
    
    # Analyze BTC-USD
    results = analyze_technical_indicators_enhanced("BTC-USD")