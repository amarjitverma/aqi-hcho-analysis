# ============================================================
# GIS Tests
# ============================================================

"""Tests for GIS utilities."""

import pytest
import numpy as np
import sys
import os

# Add project root to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.gis.grid import create_grid, get_grid_cell
from src.gis.masking import create_igp_mask, apply_mask


class TestGrid:
    """Tests for grid utilities."""
    
    def test_create_grid(self):
        """Test grid creation."""
        lat_grid, lon_grid, centers = create_grid()
        assert lat_grid.shape == (120, 120)
        assert lon_grid.shape == (120, 120)
        assert len(centers[0]) == 120
        assert len(centers[1]) == 120
    
    def test_create_grid_custom_resolution(self):
        """Test grid creation with custom resolution."""
        lat_grid, lon_grid, centers = create_grid(resolution=0.5)
        assert lat_grid.shape == (60, 60)
    
    def test_get_grid_cell(self):
        """Test grid cell lookup."""
        _, _, centers = create_grid()
        lat_centers, lon_centers = centers
        
        lat_idx, lon_idx = get_grid_cell(25.0, 80.0, lat_centers, lon_centers)
        assert 0 <= lat_idx < len(lat_centers)
        assert 0 <= lon_idx < len(lon_centers)


class TestMasking:
    """Tests for masking utilities."""
    
    def test_create_igp_mask(self):
        """Test IGP mask creation."""
        lat = np.linspace(8, 38, 120)
        lon = np.linspace(68, 98, 120)
        lat_grid, lon_grid = np.meshgrid(lat, lon)
        
        mask = create_igp_mask(lat_grid, lon_grid)
        assert mask.shape == (120, 120)
        assert mask.dtype == bool
        assert mask.sum() > 0
    
    def test_apply_mask(self):
        """Test mask application."""
        data = np.random.randn(120, 120)
        mask = np.ones((120, 120), dtype=bool)
        mask[30:40, 40:50] = False
        
        masked = apply_mask(data, mask, fill_value=np.nan)
        assert np.isnan(masked[30:40, 40:50]).all()
        assert not np.isnan(masked[0:10, 0:10]).any()