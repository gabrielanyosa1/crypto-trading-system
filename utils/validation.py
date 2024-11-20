from typing import Dict, List, Any
import pandas as pd
import numpy as np

def validate_dataframe(df: pd.DataFrame, 
                      required_columns: List[str],
                      numeric_columns: List[str] = None,
                      date_columns: List[str] = None) -> Dict[str, Any]:
    """
    Validate DataFrame structure and content.
    Returns dictionary with validation results and any issues found.
    """
    issues = []
    
    # Check required columns
    missing_cols = [col for col in required_columns if col not in df.columns]
    if missing_cols:
        issues.append(f"Missing required columns: {missing_cols}")
    
    # Check for nulls
    null_counts = df.isnull().sum()
    cols_with_nulls = null_counts[null_counts > 0]
    if not cols_with_nulls.empty:
        issues.append(f"Columns with null values: {dict(cols_with_nulls)}")
    
    # Validate numeric columns
    if numeric_columns:
        for col in numeric_columns:
            if col in df.columns:
                if not np.issubdtype(df[col].dtype, np.number):
                    issues.append(f"Column {col} should be numeric")
    
    # Validate date columns
    if date_columns:
        for col in date_columns:
            if col in df.columns:
                if not pd.api.types.is_datetime64_any_dtype(df[col]):
                    issues.append(f"Column {col} should be datetime")
    
    return {
        "is_valid": len(issues) == 0,
        "issues": issues,
        "shape": df.shape,
        "dtypes": df.dtypes.to_dict()
    }
