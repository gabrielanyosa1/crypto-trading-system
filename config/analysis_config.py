from typing import Dict, List

# Feature Groups Configuration
FEATURE_GROUPS = {
    "trend": [
        "trend_sma_fast", "trend_sma_slow",
        "trend_ema_fast", "trend_ema_slow",
        "trend_adx", "trend_vortex_ind_pos",
        "trend_vortex_ind_neg", "trend_trix"
    ],
    "momentum": [
        "momentum_rsi", "momentum_stoch_rsi",
        "momentum_stoch", "momentum_tsi",
        "momentum_uo", "momentum_stoch_signal",
        "momentum_wr", "momentum_ao"
    ],
    "volatility": [
        "volatility_bbm", "volatility_bbh",
        "volatility_bbl", "volatility_bbw",
        "volatility_kcc", "volatility_kch",
        "volatility_kcl", "volatility_dcl",
        "volatility_dch", "volatility_dcm"
    ],
    "volume": [
        "volume_em", "volume_sma_em",
        "volume_vwap", "volume_nvi",
        "volume_vpt", "volume_fi",
        "volume_mfi", "volume_adi"
    ]
}

# Model Configuration
MODEL_CONFIGS = {
    "lstm": {
        "layers": [64, 32],
        "dropout": 0.2,
        "recurrent_dropout": 0.2,
        "activation": "relu",
        "optimizer": "adam",
        "loss": "mse",
        "epochs": 100,
        "batch_size": 32,
        "validation_split": 0.2
    },
    "random_forest": {
        "n_estimators": 100,
        "max_depth": None,
        "min_samples_split": 2,
        "min_samples_leaf": 1,
        "max_features": "auto",
        "random_state": 42
    },
    "xgboost": {
        "n_estimators": 100,
        "max_depth": 6,
        "learning_rate": 0.1,
        "subsample": 0.8,
        "colsample_bytree": 0.8,
        "random_state": 42
    }
}

# Time Window Configuration
TIME_WINDOWS = {
    "training": 252,  # One trading year
    "validation": 63,  # One quarter
    "test": 21,      # One month
    "prediction": 5   # One trading week
}

# Risk Management Configuration
RISK_PARAMS = {
    "max_position_size": 0.05,  # 5% of portfolio
    "max_correlation": 0.7,     # Maximum correlation between assets
    "stop_loss": 0.02,         # 2% stop loss
    "take_profit": 0.05,       # 5% take profit
    "max_drawdown": 0.15,      # 15% maximum drawdown
    "risk_free_rate": 0.02,    # 2% risk-free rate
    "target_volatility": 0.15  # 15% target volatility
}

# Signal Generation Configuration
SIGNAL_PARAMS = {
    "min_confidence": 0.7,     # Minimum confidence for signals
    "lookback_periods": 20,    # Periods for signal generation
    "momentum_threshold": 0.02, # Momentum signal threshold
    "volatility_threshold": 1.5,# Volatility expansion threshold
    "volume_threshold": 2.0     # Volume surge threshold
}

# Performance Metrics Configuration
PERFORMANCE_METRICS = {
    "return_metrics": [
        "total_return",
        "annual_return",
        "monthly_returns",
        "daily_returns"
    ],
    "risk_metrics": [
        "volatility",
        "sharpe_ratio",
        "sortino_ratio",
        "max_drawdown",
        "var_95",
        "expected_shortfall"
    ],
    "trading_metrics": [
        "win_rate",
        "profit_factor",
        "average_win",
        "average_loss",
        "max_consecutive_wins",
        "max_consecutive_losses"
    ]
}
