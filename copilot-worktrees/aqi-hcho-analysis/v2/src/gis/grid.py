# ============================================================
# Grid Utilities
# ============================================================

"""Grid creation and management."""

import numpy as np
import pandas as pd
from loguru import logger


def create_grid(
    lat_min: float = 8,
    lat_max: float = 38,
    lon_min: float = 68,
    lon_max: float = 98,
    resolution: float = 0.25,
) -> tuple:
    """
    Create a regular grid.

    Args:
        lat_min (float): Minimum latitude
        lat_max (float): Maximum latitude
        lon_min (float): Minimum longitude
        lon_max (float): Maximum longitude
        resolution (float): Grid resolution

    Returns:
        tuple: (lat_grid, lon_grid, cell_centers)
    """
    lat_edges = np.arange(lat_min, lat_max + resolution, resolution)
    lon_edges = np.arange(lon_min, lon_max + resolution, resolution)

    lat_centers = lat_edges[:-1] + resolution / 2
    lon_centers = lon_edges[:-1] + resolution / 2

    lon_grid, lat_grid = np.meshgrid(lon_centers, lat_centers)

    logger.info(f"✅ Created grid: {lat_grid.shape[0]} × {lat_grid.shape[1]} cells")
    return lat_grid, lon_grid, (lat_centers, lon_centers)


def get_grid_cell(lat: float, lon: float, lat_centers: np.ndarray, lon_centers: np.ndarray) -> tuple:
    """
    Find grid cell index for a given latitude/longitude.

    Args:
        lat (float): Latitude
        lon (float): Longitude
        lat_centers (np.ndarray): Latitude centers
        lon_centers (np.ndarray): Longitude centers

    Returns:
        tuple: (lat_idx, lon_idx)
    """
    lat_idx = np.argmin(np.abs(lat_centers - lat))
    lon_idx = np.argmin(np.abs(lon_centers - lon))
    return lat_idx, lon_idx


def grid_to_dataframe(lat_grid: np.ndarray, lon_grid: np.ndarray, data: np.ndarray = None) -> pd.DataFrame:
    """
    Convert grid to DataFrame.

    Args:
        lat_grid (np.ndarray): Latitude grid
        lon_grid (np.ndarray): Longitude grid
        data (np.ndarray): Optional data grid

    Returns:
        pd.DataFrame: Grid as DataFrame
    """
    df = pd.DataFrame({
        "latitude": lat_grid.flatten(),
        "longitude": lon_grid.flatten(),
    })

    if data is not None:
        df["value"] = data.flatten()

    return df


if __name__ == "__main__":
    lat_grid, lon_grid, centers = create_grid()
    print(f"Grid shape: {lat_grid.shape}")
    print(f"Cell centers: {centers[0].shape[0]} × {centers[1].shape[0]}")