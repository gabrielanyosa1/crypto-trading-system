from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
from typing import Dict, List, Tuple
import numpy as np
import pandas as pd

def evaluate_predictions(y_true: np.ndarray, 
                       y_pred: np.ndarray, 
                       sample_weights: np.ndarray = None) -> Dict[str, float]:
    """
    Evaluate predictions using multiple metrics.
    """
    results = {}
    
    # Basic metrics
    results['mse'] = mean_squared_error(y_true, y_pred, 
                                      sample_weight=sample_weights)
    results['rmse'] = np.sqrt(results['mse'])
    results['mae'] = mean_absolute_error(y_true, y_pred, 
                                       sample_weight=sample_weights)
    results['r2'] = r2_score(y_true, y_pred, sample_weight=sample_weights)
    
    # Directional accuracy
    direction_correct = np.sign(y_true) == np.sign(y_pred)
    results['directional_accuracy'] = direction_correct.mean()
    
    # Custom metrics
    results['mape'] = np.mean(np.abs((y_true - y_pred) / y_true)) * 100
    results['hit_rate'] = np.mean((y_true * y_pred) > 0)
    
    return results

def calculate_trading_metrics(predictions: np.ndarray, 
                            actual_returns: np.ndarray,
                            threshold: float = 0.0) -> Dict[str, float]:
    """
    Calculate trading-specific metrics based on predictions.
    """
    # Generate trading signals based on predictions and threshold
    signals = np.where(predictions > threshold, 1, 
                      np.where(predictions < -threshold, -1, 0))
    
    # Calculate strategy returns
    strategy_returns = signals[:-1] * actual_returns[1:]
    
    # Calculate metrics
    total_trades = np.sum(signals != 0)
    winning_trades = np.sum((strategy_returns > 0) & (signals[:-1] != 0))
    
    metrics = {
        'total_return': np.prod(1 + strategy_returns) - 1,
        'annual_return': np.prod(1 + strategy_returns) ** (252/len(strategy_returns)) - 1,
        'sharpe_ratio': np.mean(strategy_returns) / np.std(strategy_returns) * np.sqrt(252),
        'win_rate': winning_trades / total_trades if total_trades > 0 else 0,
        'total_trades': total_trades,
        'avg_return_per_trade': np.mean(strategy_returns[signals[:-1] != 0])
                                if total_trades > 0 else 0
    }
    
    return metrics