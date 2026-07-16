# ============================================================
# Rolling Features
# ============================================================

"""Creates rolling window features."""

import pandas as pd
import numpy as np
from loguru import logger


def create_rolling_features(
    df: pd.DataFrame,
    columns: list,
    windows: list = [3, 7, 14],
    stats: list = ["mean", "std"],
) -> pd.DataFrame:
    """
    Create rolling window features.

    Args:
        df (pd.DataFrame): Input data
        columns (list): Column names
        windows (list): Window sizes
        stats (list): Statistics to compute

    Returns:
        pd.DataFrame: Data with rolling features
    """
    logger.info(f"📊 Creating rolling features for: {columns}")

    df = df.copy()
    df = df.sort_values("date")

    for col in columns:
        if col not in df.columns:
            continue

        rolling = df[col].rolling
        for window in windows:
            for stat in stats:
                if stat == "mean":
                    df[f"{col}_roll{window}_mean"] = rolling(window).mean()
                elif stat == "std":
                    df[f"{col}_roll{window}_std"] = rolling(window).std()
                elif stat == "min":
                    df[f"{col}_roll{window}_min"] = rolling(window).min()
                elif stat == "max":
                    df[f"{col}_roll{window}_max"] = rolling(window).max()

    return df


def create_rolling_features_grouped(
    df: pd.DataFrame,
    columns: list,
    group_col: str = "station_id",
    windows: list = [3, 7, 14],
) -> pd.DataFrame:
    """
    Create rolling features grouped by a column.

    Args:
        df (pd.DataFrame): Input data
        columns (list): Column names
        group_col (str): Column to group by
        windows (list): Window sizes

    Returns:
        pd.DataFrame: Data with rolling features
    """
    logger.info(f"📊 Creating grouped rolling features for: {columns}")

    df = df.copy()
    df = df.sort_values(["date", group_col])

    for col in columns:
        if col not in df.columns:
            continue
        for window in windows:
            df[f"{col}_roll{window}"] = df.groupby(group_col)[col].transform(
                lambda x: x.rolling(window, min_periods=1).mean()
            )

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
    result = create_rolling_features(test_df, ["pm25", "aod"])
    print(result.columns.tolist())