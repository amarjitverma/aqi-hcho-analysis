# ============================================================
# Raster Utilities
# ============================================================

"""Raster data reading and writing."""

import numpy as np
import rasterio
from rasterio.transform import from_origin
from loguru import logger


def read_raster(filepath: str, band: int = 1) -> tuple:
    """
    Read raster file.

    Args:
        filepath (str): Path to raster file
        band (int): Band number (1-indexed)

    Returns:
        tuple: (data, metadata)
    """
    logger.info(f"📖 Reading raster: {filepath}")

    with rasterio.open(filepath) as src:
        data = src.read(band)
        metadata = src.meta

    logger.info(f"  Shape: {data.shape}, CRS: {metadata['crs']}")
    return data, metadata


def write_raster(
    data: np.ndarray,
    filepath: str,
    metadata: dict = None,
    crs: str = "EPSG:4326",
    transform: tuple = None,
) -> None:
    """
    Write raster file.

    Args:
        data (np.ndarray): Data array
        filepath (str): Output path
        metadata (dict): Raster metadata
        crs (str): CRS string
        transform (tuple): Affine transform
    """
    logger.info(f"💾 Writing raster: {filepath}")

    if metadata is None:
        metadata = {
            "driver": "GTiff",
            "height": data.shape[0],
            "width": data.shape[1],
            "count": 1,
            "dtype": data.dtype,
            "crs": crs,
            "transform": transform or from_origin(68, 38, 0.25, 0.25),
        }

    with rasterio.open(filepath, "w", **metadata) as dst:
        dst.write(data, 1)

    logger.info(f"  Saved to {filepath}")


def resample_raster(
    data: np.ndarray,
    target_shape: tuple,
    method: str = "bilinear",
) -> np.ndarray:
    """
    Resample raster to target shape.

    Args:
        data (np.ndarray): Input data
        target_shape (tuple): (height, width)
        method (str): Resampling method

    Returns:
        np.ndarray: Resampled data
    """
    from rasterio.enums import Resampling

    if method == "bilinear":
        _resampling = Resampling.bilinear
    elif method == "nearest":
        _resampling = Resampling.nearest  # noqa: F841
    else:
        raise ValueError(f"Unknown method: {method}")

    # Simple resampling using interpolation
    from scipy.ndimage import zoom

    h, w = data.shape
    target_h, target_w = target_shape
    zoom_factors = (target_h / h, target_w / w)

    resampled = zoom(data, zoom_factors, order=1 if method == "bilinear" else 0)

    logger.info(f"✅ Resampled: {data.shape} → {resampled.shape}")
    return resampled


if __name__ == "__main__":
    # Test with sample data
    test_data = np.random.randn(120, 120)
    resampled = resample_raster(test_data, (60, 60))
    print(f"Resampled shape: {resampled.shape}")
