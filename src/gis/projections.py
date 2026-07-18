# ============================================================
# Projections Module
# ============================================================

"""Coordinate Reference System (CRS) transformations."""

import numpy as np
import pyproj
from loguru import logger


def transform_coordinates(
    lon: np.ndarray,
    lat: np.ndarray,
    from_crs: str = "EPSG:4326",
    to_crs: str = "EPSG:3857",
) -> tuple:
    """
    Transform coordinates from one CRS to another.

    Args:
        lon (np.ndarray): Longitude array
        lat (np.ndarray): Latitude array
        from_crs (str): Source CRS (EPSG code)
        to_crs (str): Target CRS (EPSG code)

    Returns:
        tuple: (x, y) in target CRS
    """
    logger.info(f"🔄 Transforming coordinates: {from_crs} → {to_crs}")

    transformer = pyproj.Transformer.from_crs(from_crs, to_crs)
    x, y = transformer.transform(lat, lon)

    return x, y


def get_utm_zone(lon: float) -> int:
    """
    Get UTM zone for a given longitude.

    Args:
        lon (float): Longitude in degrees

    Returns:
        int: UTM zone number
    """
    return int((lon + 180) / 6) + 1


def get_crs_for_region(lat: float, lon: float) -> str:
    """
    Get appropriate CRS for a location.

    Args:
        lat (float): Latitude
        lon (float): Longitude

    Returns:
        str: EPSG code
    """
    # India: UTM zones 43-45
    zone = get_utm_zone(lon)
    if zone in [43, 44, 45]:
        return f"EPSG:326{zone}"
    return "EPSG:4326"


def reproject_raster(
    data: np.ndarray,
    src_crs: str,
    dst_crs: str,
    src_transform: tuple,
    dst_shape: tuple,
) -> np.ndarray:
    """
    Reproject raster data to a new CRS.

    Args:
        data (np.ndarray): Input raster data
        src_crs (str): Source CRS
        dst_crs (str): Target CRS
        src_transform (tuple): Source affine transform
        dst_shape (tuple): Target shape

    Returns:
        np.ndarray: Reprojected raster data
    """
    from rasterio.warp import reproject, Resampling

    dst_data = np.zeros(dst_shape, dtype=np.float32)

    reproject(
        source=data,
        destination=dst_data,
        src_transform=src_transform,
        src_crs=src_crs,
        dst_crs=dst_crs,
        resampling=Resampling.bilinear,
    )

    logger.info(f"✅ Reprojected raster: {data.shape} → {dst_shape}")
    return dst_data


if __name__ == "__main__":
    # Test coordinate transformation
    lon = np.array([77.2090, 72.8777, 88.3639])
    lat = np.array([28.6139, 19.0760, 22.5726])

    x, y = transform_coordinates(lon, lat)
    print(f"Transformed: lon/lat → {x[0]:.2f}, {y[0]:.2f}")
