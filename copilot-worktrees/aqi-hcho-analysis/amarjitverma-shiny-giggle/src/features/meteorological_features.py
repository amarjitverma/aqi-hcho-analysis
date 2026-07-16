# ============================================================
# Meteorological Features
# ============================================================

"""Creates meteorological-derived features."""

import pandas as pd
import numpy as np
from loguru import logger


def create_meteorological_features(df: pd.DataFrame) -> pd.DataFrame:
    """
    Create meteorological-derived features.

    Args:
        df (pd.DataFrame): Input data with temperature, humidity, wind

    Returns:
        pd.DataFrame: Data with meteorological features
    """
    logger.info("🌤️ Creating meteorological features...")

    df = df.copy()
    features_added = 0

    # Heat index
    if "temp" in df.columns and "rh" in df.columns:
        df["heat_index"] = _calculate_heat_index(df["temp"], df["rh"])
        features_added += 1

    # Dew point
    if "temp" in df.columns and "rh" in df.columns:
        df["dew_point"] = _calculate_dew_point(df["temp"], df["rh"])
        features_added += 1

    # Wind chill
    if "temp" in df.columns and "wind_speed" in df.columns:
        df["wind_chill"] = _calculate_wind_chill(df["temp"], df["wind_speed"])
        features_added += 1

    # Boundary layer height categories
    if "blh" in df.columns:
        df["blh_category"] = pd.cut(
            df["blh"],
            bins=[-np.inf, 200, 500, 1000, np.inf],
            labels=["very_low", "low", "medium", "high"],
        )
        features_added += 1

    # Wind direction categories
    if "wind_dir" in df.columns or ("wind_u" in df.columns and "wind_v" in df.columns):
        if "wind_dir" not in df.columns and "wind_u" in df.columns and "wind_v" in df.columns:
            df["wind_dir"] = np.arctan2(df["wind_v"], df["wind_u"])
        df["wind_dir_category"] = pd.cut(
            df["wind_dir"],
            bins=[-np.pi, -np.pi/2, 0, np.pi/2, np.pi],
            labels=["NW", "NE", "SE", "SW"],
        )
        features_added += 1

    logger.info(f"  Added {features_added} meteorological features")
    return df


def _calculate_heat_index(temp: pd.Series, rh: pd.Series) -> pd.Series:
    """Calculate simplified heat index."""
    # Simplified Steadman formula
    return temp + 0.5 * (rh / 100) * temp * 0.01


def _calculate_dew_point(temp: pd.Series, rh: pd.Series) -> pd.Series:
    """Calculate dew point using Magnus formula."""
    a = 17.27
    b = 237.7
    gamma = (a * temp) / (b + temp) + np.log(rh / 100)
    return (b * gamma) / (a - gamma)


def _calculate_wind_chill(temp: pd.Series, wind_speed: pd.Series) -> pd.Series:
    """Calculate wind chill."""
    return 13.12 + 0.6215 * temp - 11.37 * wind_speed**0.16 + 0.3965 * temp * wind_speed**0.16


if __name__ == "__main__":
    # Test with sample data
    test_df = pd.DataFrame(
        {
            "temp": np.random.uniform(10, 40, 100),
            "rh": np.random.uniform(30, 90, 100),
            "wind_speed": np.random.uniform(0, 10, 100),
            "blh": np.random.uniform(100, 2000, 100),
            "wind_u": np.random.uniform(-5, 5, 100),
            "wind_v": np.random.uniform(-5, 5, 100),
        }
    )
    result = create_meteorological_features(test_df)
    print(result.columns.tolist())