#!/usr/bin/env python3
# ============================================================
# Preprocess Data Script
# ============================================================

"""Run the preprocessing pipeline."""

import argparse
from pathlib import Path
from loguru import logger
import sys
import os
import pandas as pd
import numpy as np

# Add project root to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.preprocessing.cleaner import clean_data
from src.preprocessing.aligner import create_standard_grid
from src.preprocessing.splitter import chronological_split
from src.preprocessing.validator import validate_data
from src.features.lag_features import create_lag_features
from src.features.rolling_features import create_rolling_features


def main():
    parser = argparse.ArgumentParser(description="Run preprocessing pipeline")
    parser.add_argument("--input-dir", type=str, default="data/raw", help="Input directory")
    parser.add_argument("--output-dir", type=str, default="data/processed", help="Output directory")
    parser.add_argument("--validate", action="store_true", help="Run validation after preprocessing")
    
    args = parser.parse_args()
    
    logger.info("🔧 Starting preprocessing pipeline...")
    
    # Create output directory
    Path(args.output_dir).mkdir(parents=True, exist_ok=True)
    
    # Placeholder: In real implementation, load and process data
    logger.info("Loading raw data...")
    
    # Example: Generate sample data
    np.random.seed(42)
    n_samples = 10000
    
    # Create sample dataframe
    df = pd.DataFrame({
        "date": pd.date_range("2019-01-01", periods=n_samples),
        "pm25": np.random.normal(50, 20, n_samples),
        "aod": np.random.normal(0.5, 0.2, n_samples),
        "no2": np.random.normal(30, 10, n_samples),
        "so2": np.random.normal(10, 5, n_samples),
        "co": np.random.normal(1, 0.5, n_samples),
        "o3": np.random.normal(40, 15, n_samples),
        "hcho": np.random.normal(0.005, 0.002, n_samples),
        "temp": np.random.normal(25, 5, n_samples),
        "rh": np.random.normal(60, 15, n_samples),
        "wind_speed": np.random.normal(3, 1.5, n_samples),
        "blh": np.random.normal(500, 200, n_samples),
        "latitude": np.random.uniform(8, 38, n_samples),
        "longitude": np.random.uniform(68, 98, n_samples),
    })
    
    logger.info(f"Loaded {len(df)} samples")
    
    # Clean data
    logger.info("Cleaning data...")
    df_cleaned = clean_data(df)
    
    # Create features
    logger.info("Creating features...")
    df_features = create_lag_features(df_cleaned, ["pm25", "aod", "hcho"])
    df_features = create_rolling_features(df_features, ["pm25", "aod"])
    
    # Split data
    logger.info("Splitting data chronologically...")
    train_df, val_df, test_df = chronological_split(df_features)
    
    # Save processed data
    logger.info(f"Saving processed data to {args.output_dir}...")
    train_df.to_parquet(f"{args.output_dir}/train.parquet")
    val_df.to_parquet(f"{args.output_dir}/validation.parquet")
    test_df.to_parquet(f"{args.output_dir}/test.parquet")
    
    # Create grid
    logger.info("Creating standard grid...")
    lat_grid, lon_grid = create_standard_grid()
    np.save(f"{args.output_dir}/lat_grid.npy", lat_grid)
    np.save(f"{args.output_dir}/lon_grid.npy", lon_grid)
    
    # Validate
    if args.validate:
        logger.info("Validating data...")
        validate_data(train_df)
        validate_data(val_df)
        validate_data(test_df)
    
    logger.info("✅ Preprocessing complete!")
    logger.info(f"  Training: {len(train_df)} samples")
    logger.info(f"  Validation: {len(val_df)} samples")
    logger.info(f"  Test: {len(test_df)} samples")


if __name__ == "__main__":
    main()