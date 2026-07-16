# ============================================================
# Sentinel-5P (TROPOMI) Data Downloader
# ============================================================

"""
Downloads TROPOMI data from Google Earth Engine.
Products: NO2, SO2, CO, O3, HCHO
"""

import ee
import geemap
import os
import numpy as np
from dotenv import load_dotenv
from loguru import logger

load_dotenv()

# India bounding box
INDIA_BBOX = ee.Geometry.Rectangle([68.0, 8.0, 98.0, 38.0])

# Product configurations
PRODUCTS = {
    "NO2": {
        "collection": "COPERNICUS/S5P/OFFL/L3_NO2",
        "band": "nitrogen_dioxide_column_number_density",
        "scale": 0.00001,
        "unit": "mol/m²",
    },
    "SO2": {
        "collection": "COPERNICUS/S5P/OFFL/L3_SO2",
        "band": "sulfur_dioxide_column_number_density",
        "scale": 0.00001,
        "unit": "mol/m²",
    },
    "CO": {
        "collection": "COPERNICUS/S5P/OFFL/L3_CO",
        "band": "carbon_monoxide_column_number_density",
        "scale": 0.00001,
        "unit": "mol/m²",
    },
    "O3": {
        "collection": "COPERNICUS/S5P/OFFL/L3_O3",
        "band": "ozone_column_number_density",
        "scale": 0.00001,
        "unit": "mol/m²",
    },
    "HCHO": {
        "collection": "COPERNICUS/S5P/OFFL/L3_HCHO",
        "band": "tropospheric_HCHO_column_number_density",
        "scale": 0.00001,
        "unit": "mol/m²",
    },
}


def initialize_gee():
    """Initialize Google Earth Engine."""
    try:
        project = os.getenv("GEE_PROJECT")
        if project:
            ee.Initialize(project=project)
        else:
            ee.Initialize()
        logger.info("✅ GEE initialized successfully")
        return True
    except Exception as e:
        logger.error(f"❌ GEE initialization failed: {e}")
        return False


def download_sentinel5p(
    start_date: str,
    end_date: str,
    product: str = "HCHO",
    output_dir: str = "data/raw/satellite/sentinel5p/",
) -> str:
    """
    Download TROPOMI data from Google Earth Engine.

    Args:
        start_date (str): 'YYYY-MM-DD'
        end_date (str): 'YYYY-MM-DD'
        product (str): 'NO2', 'SO2', 'CO', 'O3', 'HCHO'
        output_dir (str): Output directory

    Returns:
        str: Path to downloaded file
    """
    logger.info(f"📥 Downloading {product} data from {start_date} to {end_date}")

    if product not in PRODUCTS:
        raise ValueError(f"Unknown product: {product}. Choose from {list(PRODUCTS.keys())}")

    config = PRODUCTS[product]

    # Load collection
    collection = ee.ImageCollection(config["collection"]).filterDate(start_date, end_date).filterBounds(INDIA_BBOX)

    # Quality filter (qa_value > 0.5 for cloud-free)
    collection = collection.map(lambda img: img.updateMask(img.select("qa_value").gt(0.5)))

    # Mean composite
    image = collection.select(config["band"]).mean().clip(INDIA_BBOX)

    # Create output directory
    output_dir = os.path.join(output_dir, product.lower())
    os.makedirs(output_dir, exist_ok=True)

    # Export
    output_path = os.path.join(output_dir, f"{product}_{start_date}_{end_date}.tif")

    try:
        geemap.ee_export_image(
            image, filename=output_path, scale=2500, region=INDIA_BBOX
        )
        logger.info(f"✅ Downloaded {product} to {output_path}")
        return output_path
    except Exception as e:
        logger.error(f"❌ Export failed: {e}")
        return None


def download_all_sentinel5p(
    years: int = 5, start_date: str = None, end_date: str = "2023-12-31"
):
    """
    Download all Sentinel-5P products for multiple years.

    Args:
        years (int): Number of years of data
        start_date (str): Start date (overrides years)
        end_date (str): End date
    """
    if start_date is None:
        start_year = 2023 - years + 1
        start_date = f"{start_year}-01-01"

    products = ["NO2", "SO2", "CO", "O3", "HCHO"]

    for product in products:
        download_sentinel5p(start_date, end_date, product)


if __name__ == "__main__":
    if initialize_gee():
        download_all_sentinel5p(years=5)
    else:
        print("Please authenticate GEE first: ee.Authenticate()")