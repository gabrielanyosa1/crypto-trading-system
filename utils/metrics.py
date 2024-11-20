import numpy as np
import pandas as pd
from typing import Tuple, Dict

def calculate_trading_metrics(returns: np.ndarray, 
                            risk_free_rate: float = 0.0) -> Dict[str, float]:
    """
    Calculate comprehensive trading metrics.
    
    Args:
        returns: Array of returns
        risk_free_rate: Annual risk-free rate
        
    Returns:
        Dictionary of calculated metrics
    """
    returns = np.array(returns)
    
    # Convert annual risk-free rate to daily
    daily_rf = (1 + risk_free_rate) ** (1/252) - 1
    
    # Basic metrics
    total_return = (1 + returns).prod() - 1
    daily_mean = returns.mean()
    daily_std = returns.std()
    
    # Annualized metrics
    annual_return = (1 + daily_mean) ** 252 - 1
    annual_std = daily_std * np.sqrt(252)
    
    # Risk metrics
    excess_returns = returns - daily_rf
    sharpe_ratio = np.sqrt(252) * excess_returns.mean() / returns.std()
    
    downside_returns = returns[returns < 0]
    sortino_ratio = np.sqrt(252) * excess_returns.mean() / downside_returns.std()
    
    max_drawdown = calculate_max_drawdown(returns)
    
    # Risk-adjusted metrics
    calmar_ratio = annual_return / abs(max_drawdown)
    
    return {
        "total_return": total_return,
        "annual_return": annual_return,
        "annual_volatility": annual_std,
        "sharpe_ratio": sharpe_ratio,
        "sortino_ratio": sortino_ratio,
        "max_drawdown": max_drawdown,
        "calmar_ratio": calmar_ratio,
        "win_rate": (returns > 0).mean(),
        "profit_factor": abs(returns[returns > 0].sum() / returns[returns < 0].sum())
    }

def calculate_max_drawdown(returns: np.ndarray) -> float:
    """Calculate maximum drawdown from returns."""
    cum_returns = (1 + returns).cumprod()
    running_max = np.maximum.accumulate(cum_returns)
    drawdowns = cum_returns / running_max - 1
    return drawdowns.min()
