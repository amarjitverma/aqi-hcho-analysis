# ============================================================
# Chronological Splitter
# ============================================================

"""
Splits data chronologically to prevent data leakage.
"""

import numpy as np
import pandas as pd
from loguru import logger


def chronological_split(
    df: pd.DataFrame,
    date_col: str = "date",
    train_ratio: float = 0.70,
    val_ratio: float = 0.15,
) -> tuple:
    """
    Split data chronologically by date.

    Args:
        df (pd.DataFrame): Input DataFrame
        date_col (str): Date column name
        train_ratio (float): Training set proportion
        val_ratio (float): Validation set proportion

    Returns:
        tuple: (train_df, val_df, test_df)
    """
    logger.info("🔄 Splitting data chronologically...")

    # Ensure date column is datetime
    df[date_col] = pd.to_datetime(df[date_col])
    df = df.sort_values(date_col)

    n = len(df)
    train_idx = int(n * train_ratio)
    val_idx = int(n * (train_ratio + val_ratio))

    train_df = df.iloc[:train_idx]
    val_df = df.iloc[train_idx:val_idx]
    test_df = df.iloc[val_idx:]

    logger.info(f"  Training set: {len(train_df)} samples ({train_ratio * 100:.0f}%)")
    logger.info(f"  Validation set: {len(val_df)} samples ({val_ratio * 100:.0f}%)")
    logger.info(f"  Test set: {len(test_df)} samples ({(1 - train_ratio - val_ratio) * 100:.0f}%)")

    return train_df, val_df, test_df


def split_sequences(
    X: np.ndarray, y: np.ndarray, train_ratio: float = 0.70, val_ratio: float = 0.15
) -> tuple:
    """
    Split sequences chronologically.

    Args:
        X (np.ndarray): Feature sequences
        y (np.ndarray): Targets
        train_ratio (float): Training set proportion
        val_ratio (float): Validation set proportion

    Returns:
        tuple: (X_train, X_val, X_test, y_train, y_val, y_test)
    """
    n = len(X)
    train_idx = int(n * train_ratio)
    val_idx = int(n * (train_ratio + val_ratio))

    X_train = X[:train_idx]
    X_val = X[train_idx:val_idx]
    X_test = X[val_idx:]

    y_train = y[:train_idx]
    y_val = y[train_idx:val_idx]
    y_test = y[val_idx:]

    return X_train, X_val, X_test, y_train, y_val, y_test


if __name__ == "__main__":
    # Test with sample data
    test_df = pd.DataFrame(
        {
            "date": pd.date_range("2024-01-01", periods=1000),
            "value": np.random.randn(1000),
        }
    )
    train, val, test = chronological_split(test_df)
    print(f"Train: {len(train)}, Val: {len(val)}, Test: {len(test)}")
