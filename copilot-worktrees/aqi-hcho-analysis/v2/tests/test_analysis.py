# ============================================================
# Analysis Tests
# ============================================================

"""Tests for analysis modules."""

import pytest
import numpy as np
import pandas as pd
import sys
import os

# Add project root to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.analysis.hotspot_detector import HCHOHotspotDetector
from src.analysis.correlation import lagged_correlation
from src.analysis.transport import calculate_wind_speed, calculate_wind_direction, plume_decay


class TestHotspotDetection:
    """Tests for HCHO hotspot detection."""
    
    def test_detect_hotspots(self):
        """Test hotspot detection."""
        # Create sample grid
        lat = np.linspace(8, 38, 120)
        lon = np.linspace(68, 98, 120)
        lat_grid, lon_grid = np.meshgrid(lat, lon)
        
        hcho_grid = np.random.randn(120, 120) * 0.001 + 0.005
        hcho_grid[50:60, 70:80] = 0.05  # Add a hotspot
        
        detector = HCHOHotspotDetector()
        clusters = detector.detect(hcho_grid, lat_grid, lon_grid)
        
        assert len(clusters) > 0
        for cluster in clusters.values():
            assert "num_cells" in cluster
            assert "mean_hcho" in cluster
            assert "source_region" in cluster
    
    def test_get_statistics(self):
        """Test cluster statistics."""
        lat = np.linspace(8, 38, 120)
        lon = np.linspace(68, 98, 120)
        lat_grid, lon_grid = np.meshgrid(lat, lon)
        
        hcho_grid = np.random.randn(120, 120) * 0.001 + 0.005
        hcho_grid[50:60, 70:80] = 0.05
        
        detector = HCHOHotspotDetector()
        detector.detect(hcho_grid, lat_grid, lon_grid)
        stats = detector.get_statistics()
        
        assert stats is not None
        assert not stats.empty


class TestCorrelation:
    """Tests for correlation analysis."""
    
    def test_lagged_correlation(self):
        """Test lagged correlation."""
        np.random.seed(42)
        fire_counts = np.random.poisson(10, 100)
        hcho_values = fire_counts * 0.5 + np.random.randn(100) * 0.1
        
        results = lagged_correlation(fire_counts, hcho_values, max_lag=3)
        
        assert len(results) == 4
        assert "lag_days" in results.columns
        assert "pearson_r" in results.columns
        assert "pearson_p" in results.columns


class TestTransport:
    """Tests for transport analysis."""
    
    def test_calculate_wind_speed(self):
        """Test wind speed calculation."""
        u = np.array([2.0, 3.0, 4.0])
        v = np.array([1.0, 2.0, 3.0])
        speed = calculate_wind_speed(u, v)
        expected = np.sqrt(u**2 + v**2)
        np.testing.assert_array_almost_equal(speed, expected)
    
    def test_calculate_wind_direction(self):
        """Test wind direction calculation."""
        u = np.array([1.0, 0.0, -1.0])
        v = np.array([0.0, 1.0, 0.0])
        direction = calculate_wind_direction(u, v)
        expected = np.array([0.0, 90.0, 180.0])
        np.testing.assert_array_almost_equal(direction, expected)
    
    def test_plume_decay(self):
        """Test plume decay model."""
        c_source = 10.0
        distance = 100.0
        wind_speed = 5.0
        decay_constant = 0.02
        result = plume_decay(c_source, distance, wind_speed, decay_constant)
        expected = c_source * np.exp(-decay_constant * distance / wind_speed)
        np.testing.assert_almost_equal(result, expected)