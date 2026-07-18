# ============================================================
# Lag Features
# ============================================================

"""Creates lagged features for time-series data."""

import pandas as pd
import numpy as np
from loguru import logger


def create_lag_features(
    df: pd.DataFrame, columns: list, lag_days: list = [1, 2, 3, 7]
) -> pd.DataFrame:
    """
    Create lag features for specified columns.

    Args:
        df (pd.DataFrame): Input data
        columns (list): Column names to lag
        lag_days (list): Lag values

    Returns:
        pd.DataFrame: Data with lag features
    """
    logger.info(f"⏳ Creating lag features for: {columns}")

    df = df.copy()
    df = df.sort_values("date")

    for col in columns:
        if col not in df.columns:
            logger.warning(f"  Column '{col}' not found, skipping")
            continue
        for lag in lag_days:
            df[f"{col}_lag{lag}"] = df[col].shift(lag)

    logger.info(f"  Added {len(columns) * len(lag_days)} lag features")
    return df


def create_lag_features_grouped(
    df: pd.DataFrame,
    columns: list,
    group_col: str = "station_id",
    lag_days: list = [1, 2, 3, 7],
) -> pd.DataFrame:
    """
    Create lag features grouped by a column (e.g., station ID).

    Args:
        df (pd.DataFrame): Input data
        columns (list): Column names to lag
        group_col (str): Column to group by
        lag_days (list): Lag values

    Returns:
        pd.DataFrame: Data with lag features
    """
    logger.info(f"⏳ Creating grouped lag features for: {columns}")

    df = df.copy()
    df = df.sort_values(["date", group_col])

    for col in columns:
        if col not in df.columns:
            continue
        for lag in lag_days:
            df[f"{col}_lag{lag}"] = df.groupby(group_col)[col].shift(lag)

    return df


if __name__ == "__main__":
    # Test with sample data
    test_df = pd.DataFrame(
        {
            "date": pd.date_range("2024-01-01", periods=100),
            "pm25": np.random.randn(100),
            "aod": np.random.randn(100),
        }
    )
    result = create_lag_features(test_df, ["pm25", "aod"])
    print(result.columns.tolist())
