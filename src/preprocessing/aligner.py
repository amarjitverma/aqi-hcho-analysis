# ============================================================
# Spatial Aligner
# ============================================================

"""
Aligns data to a common 0.25° grid using bilinear interpolation.
"""

import numpy as np
import pandas as pd
from scipy.interpolate import RectBivariateSpline
from loguru import logger


def align_to_grid(
    data: np.ndarray,
    lat_grid: np.ndarray,
    lon_grid: np.ndarray,
    target_lat: np.ndarray,
    target_lon: np.ndarray,
) -> np.ndarray:
    """
    Align data to target grid using bilinear interpolation.

    Args:
        data (np.ndarray): Input data (lat, lon)
        lat_grid (np.ndarray): Input latitude grid
        lon_grid (np.ndarray): Input longitude grid
        target_lat (np.ndarray): Target latitude grid
        target_lon (np.ndarray): Target longitude grid

    Returns:
        np.ndarray: Aligned data
    """
    logger.info("📐 Aligning data to 0.25° grid...")

    # Handle 1D grids
    if lat_grid.ndim == 2:
        lat_vals = lat_grid[:, 0]
        lon_vals = lon_grid[0, :]
    else:
        lat_vals = lat_grid
        lon_vals = lon_grid

    # Create interpolator
    interpolator = RectBivariateSpline(lat_vals, lon_vals, data, kx=1, ky=1)

    # Interpolate to target grid
    if target_lat.ndim == 2:
        target_lat_vals = target_lat[:, 0]
        target_lon_vals = target_lon[0, :]
    else:
        target_lat_vals = target_lat
        target_lon_vals = target_lon

    aligned = interpolator(target_lat_vals, target_lon_vals)

    logger.info(f"  Aligned shape: {aligned.shape}")
    return aligned


def create_standard_grid(resolution: float = 0.25) -> tuple:
    """
    Create standard 0.25° grid for India.

    Args:
        resolution (float): Grid resolution in degrees

    Returns:
        tuple: (lat_grid, lon_grid)
    """
    lat = np.arange(8, 38, resolution)
    lon = np.arange(68, 98, resolution)
    lon_grid, lat_grid = np.meshgrid(lon, lat)

    logger.info(f"  Created grid: {lat_grid.shape[0]} × {lat_grid.shape[1]} cells")
    return lat_grid, lon_grid


def align_dataframe_to_grid(
    df: pd.DataFrame,
    lat_col: str = "latitude",
    lon_col: str = "longitude",
    value_col: str = "pm25",
    resolution: float = 0.25,
) -> pd.DataFrame:
    """
    Align DataFrame values to a regular grid.

    Args:
        df (pd.DataFrame): Input DataFrame with lat/lon and value
        lat_col (str): Latitude column name
        lon_col (str): Longitude column name
        value_col (str): Value column name
        resolution (float): Grid resolution

    Returns:
        pd.DataFrame: Gridded data
    """
    logger.info(f"📐 Aligning DataFrame to {resolution}° grid...")

    # Create grid
    lat_grid, lon_grid = create_standard_grid(resolution)

    # Create empty grid
    grid_data = np.full_like(lat_grid, np.nan, dtype=float)

    # For each point, find nearest grid cell
    for _, row in df.iterrows():
        lat = row[lat_col]
        lon = row[lon_col]
        value = row[value_col]

        # Find nearest grid indices
        lat_idx = np.argmin(np.abs(lat_grid[:, 0] - lat))
        lon_idx = np.argmin(np.abs(lon_grid[0, :] - lon))

        grid_data[lat_idx, lon_idx] = value

    # Create DataFrame
    grid_df = pd.DataFrame(
        {
            "latitude": lat_grid.flatten(),
            "longitude": lon_grid.flatten(),
            value_col: grid_data.flatten(),
        }
    )

    logger.info(f"  Gridded data shape: {grid_df.shape}")
    return grid_df


if __name__ == "__main__":
    # Test with sample data
    lat_grid, lon_grid = create_standard_grid()
    print(f"Grid shape: {lat_grid.shape}")

    # Test alignment
    test_data = np.random.randn(lat_grid.shape[0], lat_grid.shape[1])
    target_lat, target_lon = create_standard_grid(0.5)
    aligned = align_to_grid(test_data, lat_grid, lon_grid, target_lat, target_lon)
    print(f"Aligned shape: {aligned.shape}")
