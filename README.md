# Crypto Trading System

A comprehensive cryptocurrency trading system focused on risk-managed portfolio optimization and automated trading strategies. The system employs machine learning models, technical analysis, and risk management techniques to generate trading signals while maintaining strict risk controls.

## Features

### Data Management
- Historical price and volume data collection
- Technical indicator computation and analysis
- Market sentiment analysis
- Portfolio performance tracking

### Analysis
- Machine learning-based price prediction
- Technical analysis signal generation
- Risk metrics calculation
- Portfolio optimization

### Risk Management
- Position size optimization
- Stop-loss management
- Portfolio diversification
- Drawdown controls

### Monitoring
- Real-time portfolio tracking
- Performance analytics
- Risk metrics visualization
- Trading signals dashboard

## Prerequisites

- Python 3.9+
- MongoDB 4.4+
- Git

## Installation

1. Clone the repository:
```bash
git clone https://github.com/gabrielanyosa1/crypto-trading-system.git
cd crypto-trading-system
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: .\venv\Scripts\activate
```

3. Install required packages:
```bash
pip install -r requirements/dev.txt  # For development
# or
pip install -r requirements/base.txt  # For production
```

## Configuration

1. Copy the example environment file:
```bash
cp .env.example .env
```

2. Configure your environment variables in `.env`:

### MongoDB Configuration
```
MONGODB_LOCAL_URI=mongodb://localhost:27017
MONGODB_ATLAS_URI=your_atlas_uri
MONGODB_DATABASE=crypto_trading
```
- `MONGODB_LOCAL_URI`: Local MongoDB connection string
- `MONGODB_ATLAS_URI`: MongoDB Atlas connection string (for production)
- `MONGODB_DATABASE`: Database name for the trading system

### API Keys
```
BINANCE_API_KEY=your_binance_api_key
BINANCE_SECRET_KEY=your_binance_secret_key
```
- Generate API keys from your Binance account
- Ensure appropriate permissions are set for the API keys

### Trading Configuration
```
MAX_POSITION_SIZE=0.05
MIN_CASH_POSITION=0.25
MAX_DRAWDOWN=0.02
```
- `MAX_POSITION_SIZE`: Maximum size for any single position (5% of portfolio)
- `MIN_CASH_POSITION`: Minimum cash position to maintain (25% of portfolio)
- `MAX_DRAWDOWN`: Maximum allowed daily drawdown (2%)

## Usage

### Data Collection
```python
from data.collectors.market_data import MarketDataCollector

# Initialize collector
collector = MarketDataCollector()

# Fetch historical data
collector.fetch_historical_data(
    symbols=['BTC-USD', 'ETH-USD'],
    start_date='2023-01-01',
    end_date='2024-11-14'
)
```

### Trading Signal Generation
```python
from strategy.signals.generator import SignalGenerator
from data.database.operations import DatabaseManager

# Initialize components
db = DatabaseManager()
signal_gen = SignalGenerator(db)

# Generate trading signals
signals = signal_gen.generate_signals(
    symbol='BTC-USD',
    lookback_period=30
)
```

### Portfolio Management
```python
from strategy.portfolio.allocation import PortfolioManager

# Initialize portfolio manager
portfolio_manager = PortfolioManager()

# Update portfolio allocation
portfolio_manager.rebalance_portfolio(
    signals=signals,
    current_positions=current_positions
)
```

### Monitoring
```python
from monitoring.performance import PerformanceMonitor

# Initialize monitor
monitor = PerformanceMonitor()

# Update performance metrics
monitor.update_metrics(
    portfolio_value=current_value,
    positions=current_positions
)
```

## Development

### Running Tests
```bash
# Run all tests
pytest

# Run specific test file
pytest tests/unit/test_signal_generator.py

# Run with coverage report
pytest --cov=.
```

### Code Quality
```bash
# Format code
black .

# Lint code
flake8 .
```

## Contributing

1. Fork the repository
2. Create your feature branch:
```bash
git checkout -b feature/AmazingFeature
```

3. Commit your changes:
```bash
git commit -m 'Add some AmazingFeature'
```

4. Push to the branch:
```bash
git push origin feature/AmazingFeature
```

5. Open a Pull Request

### Contribution Guidelines
- Follow PEP 8 style guide
- Write tests for new features
- Update documentation as needed
- Use type hints for function arguments
- Include docstrings for classes and functions

## Project Structure
```
crypto-trading-system/
├── .github/
│   └── workflows/              # CI/CD pipelines
│
├── config/
│   ├── settings.py            # Global configuration
│   └── logging_config.yaml    # Logging configuration
│
├── data/
│   ├── collectors/            # Data collection scripts
│   │   ├── market_data.py
│   │   ├── sentiment_data.py
│   │   └── macro_data.py
│   │
│   ├── processors/            # Data processing scripts
│   │   ├── feature_engineering.py
│   │   ├── signal_generator.py
│   │   └── data_validator.py
│   │
│   └── database/             # Database operations
│       ├── models.py        # MongoDB models/schemas
│       └── operations.py    # Database CRUD operations
│
├── analysis/
│   ├── models/               # ML models
│   │   ├── lstm.py
│   │   ├── random_forest.py
│   │   └── ensemble.py
│   │
│   ├── indicators/           # Technical analysis
│   │   ├── trend.py
│   │   ├── momentum.py
│   │   └── volatility.py
│   │
│   └── risk/                # Risk analysis
│       ├── metrics.py
│       └── portfolio.py
│
├── strategy/
│   ├── portfolio/            # Portfolio management
│   │   ├── allocation.py
│   │   └── rebalancer.py
│   │
│   ├── signals/             # Trading signals
│   │   ├── generator.py
│   │   └── validator.py
│   │
│   └── risk_management/     # Risk management
│       ├── position_sizer.py
│       └── stop_loss.py
│
├── backtesting/
│   ├── engine.py            # Backtesting core
│   ├── metrics.py           # Performance metrics
│   └── optimizer.py         # Strategy optimization
│
├── monitoring/
│   ├── dashboards/          # Grafana dashboards
│   │   ├── performance.json
│   │   ├── risk.json
│   │   └── signals.json
│   │
│   └── alerts/             # Alert configurations
│       └── rules.yaml
│
├── utils/
│   ├── metrics.py          # Common metrics
│   ├── validators.py       # Data validation
│   └── helpers.py         # Helper functions
│
├── tests/
│   ├── unit/
│   ├── integration/
│   └── system/
│
├── notebooks/              # Research notebooks
│   ├── analysis/
│   ├── backtesting/
│   └── strategy/
│
├── requirements/
│   ├── base.txt
│   ├── dev.txt
│   └── prod.txt
│
├── .env.example           # Environment variables template
├── README.md             # Project documentation
├── setup.py             # Package setup
└── main.py             # Application entry point
```

## License

This project is licensed under the APACHE 2.0 License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Technical analysis indicators from [ta](https://technical-analysis-library-in-python.readthedocs.io/en/latest/)
- Machine learning models built with [scikit-learn](https://scikit-learn.org/)
- Data visualization using [Grafana](https://grafana.com/)