import pandas as pd
import numpy as np
from typing import Dict, List, Tuple
from sklearn.feature_selection import mutual_info_regression
from scipy.stats import spearmanr
import sys
from pathlib import Path

# Add the project root directory to Python path
project_root = str(Path(__file__).resolve().parent.parent)
if project_root not in sys.path:
    sys.path.append(project_root)

# Import configurations
from config.analysis_config import (
    FEATURE_GROUPS,
    TIME_WINDOWS,
    RISK_PARAMS,
    SIGNAL_PARAMS,
    PERFORMANCE_METRICS
)

class IndicatorAnalyzer:
    """Analyze and evaluate technical indicators for predictive power."""
    
    def __init__(self, df: pd.DataFrame, target_col: str = 'close',
                 feature_groups: Dict[str, List[str]] = None):
        self.df = df
        self.target_col = target_col
        self.feature_groups = feature_groups or FEATURE_GROUPS
        self.results = {}

    def calculate_feature_importance(self) -> Dict[str, float]:
        """Calculate feature importance using mutual information."""
        feature_importance = {}
        
        for group, features in self.feature_groups.items():
            valid_features = [f for f in features if f in self.df.columns]
            if not valid_features:
                continue
                
            X = self.df[valid_features].fillna(0)
            y = self.df[self.target_col]
            
            # Calculate mutual information
            mi_scores = mutual_info_regression(X, y)
            
            # Store results
            for feature, score in zip(valid_features, mi_scores):
                feature_importance[feature] = score
                
        return dict(sorted(feature_importance.items(), 
                         key=lambda x: x[1], reverse=True))

    def analyze_predictive_power(self, 
                               forward_returns: int = 1) -> Dict[str, Dict[str, float]]:
        """Analyze predictive power of indicators for future returns."""
        results = {}
        
        # Calculate forward returns
        self.df['forward_returns'] = self.df[self.target_col].pct_change(
            forward_returns).shift(-forward_returns)
        
        for group, features in self.feature_groups.items():
            valid_features = [f for f in features if f in self.df.columns]
            if not valid_features:
                continue
                
            group_results = {}
            for feature in valid_features:
                # Calculate Spearman correlation
                correlation, p_value = spearmanr(
                    self.df[feature].fillna(0),
                    self.df['forward_returns'].fillna(0),
                    nan_policy='omit'
                )
                
                group_results[feature] = {
                    'correlation': correlation,
                    'p_value': p_value
                }
                
            results[group] = group_results
            
        return results

    def get_top_indicators(self, 
                          n_top: int = 10, 
                          min_significance: float = 0.05) -> List[str]:
        """Get top predictive indicators based on analysis."""
        all_indicators = []
        
        # Analyze predictive power
        analysis_results = self.analyze_predictive_power()
        
        # Flatten and filter results
        for group_results in analysis_results.values():
            for feature, metrics in group_results.items():
                if metrics['p_value'] < min_significance:
                    all_indicators.append((
                        feature,
                        abs(metrics['correlation']),
                        metrics['p_value']
                    ))
        
        # Sort by absolute correlation and return top n
        all_indicators.sort(key=lambda x: x[1], reverse=True)
        return [ind[0] for ind in all_indicators[:n_top]]

    def generate_analysis_report(self) -> Dict:
        """Generate comprehensive analysis report."""
        report = {
            'feature_importance': self.calculate_feature_importance(),
            'predictive_power': self.analyze_predictive_power(),
            'top_indicators': self.get_top_indicators(),
            'correlation_matrix': self.df[list(self.calculate_feature_importance().keys())]
                                .corr().to_dict()
        }
        
        return report

# Example usage
if __name__ == "__main__":
    # Example of how to use the analyzer
    # This is just for demonstration, you would typically import your actual data
    example_data = pd.DataFrame({
        'close': np.random.randn(100),
        'trend_sma_fast': np.random.randn(100),
        'momentum_rsi': np.random.randn(100),
        'volatility_bbm': np.random.randn(100),
        'volume_em': np.random.randn(100)
    })
    
    analyzer = IndicatorAnalyzer(example_data)
    report = analyzer.generate_analysis_report()
    print("Top indicators:", analyzer.get_top_indicators(n_top=3))
    