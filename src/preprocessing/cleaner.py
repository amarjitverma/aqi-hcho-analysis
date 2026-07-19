# ============================================================
# Data Cleaner
# ============================================================

"""
Removes outliers and handles missing values.
"""

import numpy as np
import pandas as pd
from loguru import logger


def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Clean the input dataframe.

    Args:
        df (pd.DataFrame): Input data

    Returns:
        pd.DataFrame: Cleaned data
    """
    logger.info("🧹 Cleaning data...")
    df = df.copy()

    # Remove rows with missing target
    if "pm25" in df.columns:
        df = df.dropna(subset=["pm25"])
        logger.info("  Removed rows with missing PM2.5")

    # Remove outliers using IQR
    for col in ["pm25", "aod", "no2", "so2", "co", "o3", "hcho"]:
        if col in df.columns:
            df = _remove_outliers_iqr(df, col)

    # Fill remaining missing values with mean
    numeric_cols = df.select_dtypes(include=[np.number]).columns
    df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].mean())

    logger.info(f"  Final shape: {df.shape}")
    return df


def _remove_outliers_iqr(df: pd.DataFrame, column: str) -> pd.DataFrame:
    """Remove outliers using IQR method."""
    Q1 = df[column].quantile(0.25)
    Q3 = df[column].quantile(0.75)
    IQR = Q3 - Q1

    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR

    before = len(df)
    df = df[(df[column] >= lower_bound) & (df[column] <= upper_bound)]
    after = len(df)

    if after < before:
        logger.info(f"  Removed {before - after} outliers from {column}")

    return df


if __name__ == "__main__":
    # Test with sample data
    test_df = pd.DataFrame(
        {"pm25": np.random.normal(50, 20, 1000), "aod": np.random.normal(0.5, 0.2, 1000)}
    )
    cleaned = clean_data(test_df)
    print(f"Cleaned shape: {cleaned.shape}")
