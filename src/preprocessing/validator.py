# ============================================================
# Data Validator
# ============================================================

"""
Validates data quality and integrity.
"""

import numpy as np
import pandas as pd
from loguru import logger


def validate_data(df: pd.DataFrame, schema: dict = None) -> dict:
    """
    Validate data quality.

    Args:
        df (pd.DataFrame): Input data
        schema (dict): Optional schema validation

    Returns:
        dict: Validation results
    """
    logger.info("🔍 Validating data quality...")

    results = {
        "shape": df.shape,
        "columns": list(df.columns),
        "missing_values": df.isnull().sum().to_dict(),
        "dtypes": df.dtypes.to_dict(),
        "unique_counts": {col: df[col].nunique() for col in df.select_dtypes(include=["object"]).columns},
        "passed": True,
    }

    # Check for empty DataFrame
    if df.empty:
        results["passed"] = False
        results["error"] = "DataFrame is empty"
        logger.error("❌ DataFrame is empty")
        return results

    # Check for missing values in critical columns
    critical_cols = ["pm25", "date", "latitude", "longitude"]
    for col in critical_cols:
        if col in df.columns:
            missing = df[col].isnull().sum()
            if missing > 0:
                logger.warning(f"  {col}: {missing} missing values")

    # Check for negative values in concentration columns
    concentration_cols = ["pm25", "aod", "no2", "so2", "co", "o3", "hcho"]
    for col in concentration_cols:
        if col in df.columns:
            negative = (df[col] < 0).sum()
            if negative > 0:
                logger.warning(f"  {col}: {negative} negative values found")

    # Check for outliers
    for col in df.select_dtypes(include=[np.number]).columns:
        Q1 = df[col].quantile(0.25)
        Q3 = df[col].quantile(0.75)
        IQR = Q3 - Q1
        outliers = ((df[col] < Q1 - 3 * IQR) | (df[col] > Q3 + 3 * IQR)).sum()
        if outliers > 0:
            logger.info(f"  {col}: {outliers} outliers detected")

    # Check for duplicate rows
    if "date" in df.columns and "grid_id" in df.columns:
        duplicates = df.duplicated(subset=["date", "grid_id"]).sum()
        if duplicates > 0:
            logger.warning(f"  Found {duplicates} duplicate date-grid records")
            results["duplicates"] = duplicates

    # Schema validation
    if schema:
        for col, dtype in schema.items():
            if col not in df.columns:
                results["passed"] = False
                results["error"] = f"Missing column: {col}"
                logger.error(f"❌ Missing column: {col}")
                return results
            if str(df[col].dtype) != dtype:
                logger.warning(f"  {col} dtype: {df[col].dtype}, expected: {dtype}")

    # Date range check
    if "date" in df.columns:
        results["date_range"] = {
            "start": df["date"].min(),
            "end": df["date"].max(),
            "days": (df["date"].max() - df["date"].min()).days,
        }
        logger.info(f"  Date range: {results['date_range']['start']} to {results['date_range']['end']}")

    logger.info(f"✅ Data validation complete. Passed: {results['passed']}")
    return results


def validate_split(train: pd.DataFrame, val: pd.DataFrame, test: pd.DataFrame, date_col: str = "date"):
    """
    Validate that splits are chronological and have no overlap.

    Args:
        train (pd.DataFrame): Training set
        val (pd.DataFrame): Validation set
        test (pd.DataFrame): Test set
        date_col (str): Date column name

    Raises:
        AssertionError: If splits overlap
    """
    train_end = train[date_col].max()
    val_start = val[date_col].min()
    val_end = val[date_col].max()
    test_start = test[date_col].min()

    assert val_start > train_end, f"Validation set overlaps with training set: {val_start} <= {train_end}"
    assert test_start > val_end, f"Test set overlaps with validation set: {test_start} <= {val_end}"

    logger.info("✅ Chronological split validated successfully")


def validate_spatial_coverage(df: pd.DataFrame, bounds: tuple = (8, 38, 68, 98)):
    """
    Validate spatial coverage of data.

    Args:
        df (pd.DataFrame): Input data
        bounds (tuple): (lat_min, lat_max, lon_min, lon_max)

    Returns:
        dict: Coverage statistics
    """
    lat_min, lat_max, lon_min, lon_max = bounds

    results = {
        "lat_min": df["latitude"].min(),
        "lat_max": df["latitude"].max(),
        "lon_min": df["longitude"].min(),
        "lon_max": df["longitude"].max(),
        "coverage_pct": 0,
    }

    # Check coverage
    lat_coverage = (df["latitude"].min() >= lat_min) and (df["latitude"].max() <= lat_max)
    lon_coverage = (df["longitude"].min() >= lon_min) and (df["longitude"].max() <= lon_max)
    results["full_coverage"] = lat_coverage and lon_coverage

    if not results["full_coverage"]:
        logger.warning(f"  Spatial coverage incomplete: lat {results['lat_min']}-{results['lat_max']}, lon {results['lon_min']}-{results['lon_max']}")

    return results


if __name__ == "__main__":
    # Test with sample data
    test_df = pd.DataFrame(
        {
            "pm25": np.random.normal(50, 20, 1000),
            "aod": np.random.normal(0.5, 0.2, 1000),
            "date": pd.date_range("2024-01-01", periods=1000),
            "latitude": np.random.uniform(8, 38, 1000),
            "longitude": np.random.uniform(68, 98, 1000),
        }
    )
    results = validate_data(test_df)
    print(f"Validation passed: {results['passed']}")