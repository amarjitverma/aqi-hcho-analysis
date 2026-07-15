# ============================================================
# Data Tests
# ============================================================

"""Tests for data acquisition and preprocessing modules."""

import pytest
import numpy as np
import pandas as pd
from pathlib import Path
import sys
import os

# Add project root to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.preprocessing.cleaner import clean_data
from src.preprocessing.aligner import create_standard_grid, align_to_grid
from src.preprocessing.interpolator import fill_gaps
from src.preprocessing.splitter import chronological_split
from src.preprocessing.validator import validate_data


class TestDataCleaning:
    """Tests for data cleaning."""
    
    def test_clean_data_removes_outliers(self):
        """Test that clean_data removes outliers."""
        df = pd.DataFrame({
            "pm25": [10, 20, 30, 40, 50, 1000],
            "aod": [0.1, 0.2, 0.3, 0.4, 0.5, 0.6]
        })
        cleaned = clean_data(df)
        assert len(cleaned) < len(df)
        assert cleaned["pm25"].max() < 100
    
    def test_clean_data_handles_missing_values(self):
        """Test that clean_data handles missing values."""
        df = pd.DataFrame({
            "pm25": [10, 20, np.nan, 40, 50],
            "aod": [0.1, 0.2, 0.3, 0.4, 0.5]
        })
        cleaned = clean_data(df)
        assert cleaned.isnull().sum().sum() == 0


class TestGridAlignment:
    """Tests for grid alignment."""
    
    def test_create_standard_grid(self):
        """Test grid creation."""
        lat_grid, lon_grid = create_standard_grid()
        assert lat_grid.shape == (120, 120)
        assert lon_grid.shape == (120, 120)
        assert lat_grid.min() >= 8
        assert lat_grid.max() <= 38
        assert lon_grid.min() >= 68
        assert lon_grid.max() <= 98
    
    def test_align_to_grid(self):
        """Test data alignment."""
        lat_grid, lon_grid = create_standard_grid()
        test_data = np.random.randn(lat_grid.shape[0], lat_grid.shape[1])
        target_lat, target_lon = create_standard_grid(0.5)
        aligned = align_to_grid(test_data, lat_grid, lon_grid, target_lat, target_lon)
        assert aligned.shape == target_lat.shape


class TestGapFilling:
    """Tests for gap-filling."""
    
    def test_fill_gaps_2d(self):
        """Test 2D gap-filling."""
        data = np.random.randn(120, 120)
        data[30:40, 40:50] = np.nan
        filled = fill_gaps(data)
        assert not np.isnan(filled).any()
    
    def test_fill_gaps_3d(self):
        """Test 3D gap-filling."""
        data = np.random.randn(10, 120, 120)
        data[0, 30:40, 40:50] = np.nan
        filled = fill_gaps(data)
        assert not np.isnan(filled).any()


class TestDataSplitting:
    """Tests for data splitting."""
    
    def test_chronological_split(self):
        """Test chronological splitting."""
        df = pd.DataFrame({
            "date": pd.date_range("2024-01-01", periods=1000),
            "value": np.random.randn(1000)
        })
        train, val, test = chronological_split(df)
        assert len(train) + len(val) + len(test) == len(df)
        assert train["date"].max() < val["date"].min()
        assert val["date"].max() < test["date"].min()


class TestDataValidation:
    """Tests for data validation."""
    
    def test_validate_data_passes(self):
        """Test that validate_data passes for valid data."""
        df = pd.DataFrame({
            "pm25": np.random.normal(50, 20, 100),
            "aod": np.random.normal(0.5, 0.2, 100),
            "date": pd.date_range("2024-01-01", periods=100),
            "latitude": np.random.uniform(8, 38, 100),
            "longitude": np.random.uniform(68, 98, 100)
        })
        results = validate_data(df)
        assert results["passed"] == True
    
    def test_validate_data_fails_for_empty(self):
        """Test that validate_data fails for empty DataFrame."""
        df = pd.DataFrame()
        results = validate_data(df)
        assert results["passed"] == False