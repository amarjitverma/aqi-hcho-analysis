# ============================================================
# Vector Utilities
# ============================================================

"""Vector data (shapefile, GeoJSON) reading and writing."""

import json
import geopandas as gpd
import numpy as np
from shapely.geometry import Point, Polygon
from loguru import logger


def read_geojson(filepath: str) -> gpd.GeoDataFrame:
    """
    Read GeoJSON file.

    Args:
        filepath (str): Path to GeoJSON file

    Returns:
        gpd.GeoDataFrame: GeoDataFrame
    """
    logger.info(f"📖 Reading GeoJSON: {filepath}")
    gdf = gpd.read_file(filepath)
    logger.info(f"  {len(gdf)} features found")
    return gdf


def write_geojson(gdf: gpd.GeoDataFrame, filepath: str) -> None:
    """
    Write GeoJSON file.

    Args:
        gdf (gpd.GeoDataFrame): GeoDataFrame
        filepath (str): Output path
    """
    logger.info(f"💾 Writing GeoJSON: {filepath}")
    gdf.to_file(filepath, driver="GeoJSON")
    logger.info(f"  Saved {len(gdf)} features")


def points_to_geojson(points: list, properties: list = None) -> dict:
    """
    Convert points to GeoJSON.

    Args:
        points (list): List of (lon, lat) tuples
        properties (list): List of property dicts

    Returns:
        dict: GeoJSON feature collection
    """
    features = []
    for i, (lon, lat) in enumerate(points):
        props = properties[i] if properties and i < len(properties) else {}
        features.append(
            {
                "type": "Feature",
                "geometry": {"type": "Point", "coordinates": [lon, lat]},
                "properties": props,
            }
        )

    return {"type": "FeatureCollection", "features": features}


def create_grid_polygons(lat_grid: np.ndarray, lon_grid: np.ndarray) -> gpd.GeoDataFrame:
    """
    Create polygons for grid cells.

    Args:
        lat_grid (np.ndarray): Latitude grid
        lon_grid (np.ndarray): Longitude grid

    Returns:
        gpd.GeoDataFrame: Grid polygons
    """
    from shapely.geometry import box

    polygons = []
    for i in range(lat_grid.shape[0] - 1):
        for j in range(lon_grid.shape[1] - 1):
            lat_min = lat_grid[i, j]
            lat_max = lat_grid[i + 1, j + 1]
            lon_min = lon_grid[i, j]
            lon_max = lon_grid[i + 1, j + 1]
            polygons.append(box(lon_min, lat_min, lon_max, lat_max))

    gdf = gpd.GeoDataFrame({"geometry": polygons}, crs="EPSG:4326")
    logger.info(f"✅ Created {len(gdf)} grid polygons")
    return gdf


if __name__ == "__main__":
    # Test points to GeoJSON
    points = [(77.2090, 28.6139), (72.8777, 19.0760)]
    geojson = points_to_geojson(points)
    print(f"Created GeoJSON with {len(geojson['features'])} features")
