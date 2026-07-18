# ============================================================
# Masking Utilities
# ============================================================

"""Region masking and filtering utilities."""

import numpy as np
import geopandas as gpd
from shapely.geometry import Point, Polygon
from loguru import logger


def apply_mask(data: np.ndarray, mask: np.ndarray, fill_value: float = np.nan) -> np.ndarray:
    """
    Apply a boolean mask to data.

    Args:
        data (np.ndarray): Input data array
        mask (np.ndarray): Boolean mask (True = keep, False = mask out)
        fill_value (float): Value to fill masked pixels

    Returns:
        np.ndarray: Masked data
    """
    logger.info(f"🔲 Applying mask to data of shape {data.shape}")
    logger.info(f"  Mask has {mask.sum()} cells ({(mask.sum() / mask.size * 100):.1f}%)")

    masked = data.copy()
    masked[~mask] = fill_value

    return masked


def create_igp_mask(lat_grid: np.ndarray, lon_grid: np.ndarray) -> np.ndarray:
    """
    Create mask for Indo-Gangetic Plain (IGP).

    Args:
        lat_grid (np.ndarray): Latitude grid
        lon_grid (np.ndarray): Longitude grid

    Returns:
        np.ndarray: Boolean mask for IGP (True = inside IGP)
    """
    # IGP bounds: 22°N-32°N, 74°E-90°E
    mask = (lat_grid >= 22) & (lat_grid <= 32) & (lon_grid >= 74) & (lon_grid <= 90)

    logger.info(f"✅ Created IGP mask with {mask.sum()} cells ({mask.sum() / mask.size * 100:.1f}%)")
    return mask


def create_forest_mask(lat_grid: np.ndarray, lon_grid: np.ndarray) -> np.ndarray:
    """
    Create mask for forest regions (Central and Northeast India).

    Args:
        lat_grid (np.ndarray): Latitude grid
        lon_grid (np.ndarray): Longitude grid

    Returns:
        np.ndarray: Boolean mask for forest regions
    """
    # Central India forest region
    central_forest = (lat_grid >= 18) & (lat_grid <= 24) & (lon_grid >= 76) & (lon_grid <= 84)

    # Northeast India forest region
    northeast_forest = (lat_grid >= 22) & (lat_grid <= 28) & (lon_grid >= 90) & (lon_grid <= 98)

    mask = central_forest | northeast_forest

    logger.info(
        f"✅ Created forest mask with {mask.sum()} cells ({mask.sum() / mask.size * 100:.1f}%)"
    )
    return mask


def create_urban_mask(
    lat_grid: np.ndarray,
    lon_grid: np.ndarray,
    cities: list = None,
    radius_deg: float = 0.3,
) -> np.ndarray:
    """
    Create mask for urban regions (city buffers).

    Args:
        lat_grid (np.ndarray): Latitude grid
        lon_grid (np.ndarray): Longitude grid
        cities (list): List of (city_name, lat, lon) tuples
        radius_deg (float): Buffer radius in degrees

    Returns:
        np.ndarray: Boolean mask for urban regions
    """
    if cities is None:
        cities = [
            ("Delhi", 28.6139, 77.2090),
            ("Mumbai", 19.0760, 72.8777),
            ("Kolkata", 22.5726, 88.3639),
            ("Bengaluru", 12.9716, 77.5946),
            ("Chennai", 13.0827, 80.2707),
            ("Hyderabad", 17.3850, 78.4867),
            ("Ahmedabad", 23.0225, 72.5714),
            ("Pune", 18.5204, 73.8567),
        ]

    mask = np.zeros_like(lat_grid, dtype=bool)

    for city_name, lat, lon in cities:
        distance = np.sqrt((lat_grid - lat) ** 2 + (lon_grid - lon) ** 2)
        city_mask = distance <= radius_deg
        mask = mask | city_mask
        logger.info(f"  Added {city_name}: {city_mask.sum()} cells")

    logger.info(
        f"✅ Created urban mask with {mask.sum()} cells ({mask.sum() / mask.size * 100:.1f}%)"
    )
    return mask


def load_shapefile_mask(
    shapefile_path: str, lat_grid: np.ndarray, lon_grid: np.ndarray
) -> np.ndarray:
    """
    Load mask from shapefile/GeoJSON.

    Args:
        shapefile_path (str): Path to shapefile or GeoJSON
        lat_grid (np.ndarray): Latitude grid
        lon_grid (np.ndarray): Longitude grid

    Returns:
        np.ndarray: Boolean mask
    """
    logger.info(f"📖 Loading mask from: {shapefile_path}")

    try:
        gdf = gpd.read_file(shapefile_path)
        mask = np.zeros_like(lat_grid, dtype=bool)

        # Create points for each grid cell
        lon_flat = lon_grid.flatten()
        lat_flat = lat_grid.flatten()

        # Check each point
        for i in range(len(lon_flat)):
            point = Point(lon_flat[i], lat_flat[i])
            for geometry in gdf.geometry:
                if geometry.contains(point):
                    mask.flat[i] = True
                    break

        logger.info(f"✅ Loaded mask with {mask.sum()} cells ({mask.sum() / mask.size * 100:.1f}%)")
        return mask

    except Exception as e:
        logger.error(f"❌ Failed to load shapefile: {e}")
        # Return full mask as fallback
        return np.ones_like(lat_grid, dtype=bool)


def create_region_mask(
    region_bounds: tuple, lat_grid: np.ndarray, lon_grid: np.ndarray
) -> np.ndarray:
    """
    Create mask from region bounds.

    Args:
        region_bounds (tuple): (lat_min, lat_max, lon_min, lon_max)
        lat_grid (np.ndarray): Latitude grid
        lon_grid (np.ndarray): Longitude grid

    Returns:
        np.ndarray: Boolean mask
    """
    lat_min, lat_max, lon_min, lon_max = region_bounds
    mask = (
        (lat_grid >= lat_min)
        & (lat_grid <= lat_max)
        & (lon_grid >= lon_min)
        & (lon_grid <= lon_max)
    )

    logger.info(f"✅ Created region mask with {mask.sum()} cells")
    return mask


def combine_masks(masks: list, operation: str = "union") -> np.ndarray:
    """
    Combine multiple masks.

    Args:
        masks (list): List of boolean masks
        operation (str): 'union' (OR), 'intersection' (AND), 'difference' (first - others)

    Returns:
        np.ndarray: Combined mask
    """
    if not masks:
        raise ValueError("No masks provided")

    if operation == "union":
        result = masks[0].copy()
        for mask in masks[1:]:
            result = result | mask

    elif operation == "intersection":
        result = masks[0].copy()
        for mask in masks[1:]:
            result = result & mask

    elif operation == "difference":
        result = masks[0].copy()
        for mask in masks[1:]:
            result = result & ~mask

    else:
        raise ValueError(f"Unknown operation: {operation}")

    logger.info(f"✅ Combined mask with {result.sum()} cells")
    return result


def invert_mask(mask: np.ndarray) -> np.ndarray:
    """Invert a boolean mask."""
    return ~mask


def dilate_mask(mask: np.ndarray, radius: int = 1) -> np.ndarray:
    """
    Dilate a mask (expand by radius).

    Args:
        mask (np.ndarray): Boolean mask
        radius (int): Dilation radius in pixels

    Returns:
        np.ndarray: Dilated mask
    """
    from scipy.ndimage import binary_dilation

    structure = np.ones((2 * radius + 1, 2 * radius + 1))
    dilated = binary_dilation(mask, structure=structure)

    logger.info(f"✅ Dilated mask: {mask.sum()} → {dilated.sum()} cells")
    return dilated


def erode_mask(mask: np.ndarray, radius: int = 1) -> np.ndarray:
    """
    Erode a mask (shrink by radius).

    Args:
        mask (np.ndarray): Boolean mask
        radius (int): Erosion radius in pixels

    Returns:
        np.ndarray: Eroded mask
    """
    from scipy.ndimage import binary_erosion

    structure = np.ones((2 * radius + 1, 2 * radius + 1))
    eroded = binary_erosion(mask, structure=structure)

    logger.info(f"✅ Eroded mask: {mask.sum()} → {eroded.sum()} cells")
    return eroded


if __name__ == "__main__":
    # Test masking functions
    lat = np.linspace(8, 38, 120)
    lon = np.linspace(68, 98, 120)
    lat_grid, lon_grid = np.meshgrid(lat, lon)

    # Create and apply masks
    igp_mask = create_igp_mask(lat_grid, lon_grid)
    urban_mask = create_urban_mask(lat_grid, lon_grid)

    combined = combine_masks([igp_mask, urban_mask], operation="union")

    # Test with sample data
    test_data = np.random.randn(120, 120)
    masked_data = apply_mask(test_data, combined)

    print(f"Original data mean: {test_data.mean():.4f}")
    print(f"Masked data mean: {masked_data.mean():.4f}")
    print(f"Masked data has {np.isnan(masked_data).sum()} NaN values")
