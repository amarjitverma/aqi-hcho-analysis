# ============================================================
# ERA5 Meteorological Data Downloader
# ============================================================

"""
Downloads ERA5 reanalysis data from Copernicus CDS API.
"""

import os
import cdsapi
import pandas as pd
from dotenv import load_dotenv
from loguru import logger

load_dotenv()


def download_era5(
    start_date: str,
    end_date: str,
    output_dir: str = "data/raw/meteorology/era5/",
    variables: list = None,
) -> str:
    """
    Download ERA5 data from Copernicus CDS API.

    Args:
        start_date (str): 'YYYY-MM-DD'
        end_date (str): 'YYYY-MM-DD'
        output_dir (str): Output directory
        variables (list): List of variable names

    Returns:
        str: Path to downloaded file
    """
    logger.info(f"📥 Downloading ERA5 data from {start_date} to {end_date}")

    if variables is None:
        variables = [
            "10m_u_component_of_wind",
            "10m_v_component_of_wind",
            "2m_temperature",
            "2m_dewpoint_temperature",
            "boundary_layer_height",
        ]

    # India bounding box
    area = [38.0, 68.0, 8.0, 98.0]  # North, West, South, East

    # Create output directory
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, f"era5_{start_date}_{end_date}.nc")

    # Parse start and end date to determine specific years, months, and days
    try:
        start_dt = pd.to_datetime(start_date)
        end_dt = pd.to_datetime(end_date)
        date_range = pd.date_range(start_dt, end_dt)
        years_list = sorted(list(set(date_range.strftime("%Y"))))
        months_list = sorted(list(set(date_range.strftime("%m"))))
        days_list = sorted(list(set(date_range.strftime("%d"))))
    except Exception as e:
        logger.warning(f"Failed to parse dates {start_date} - {end_date}: {e}. Defaulting to range.")
        years_list = [str(y) for y in range(2019, 2024)]
        months_list = [str(m).zfill(2) for m in range(1, 13)]
        days_list = [str(d).zfill(2) for d in range(1, 32)]

    # Download via CDS API
    try:
        # Initialize CDS client with environment variables if available
        url = os.getenv("CDS_URL")
        key = os.getenv("CDS_API_KEY")
        if url and key:
            client = cdsapi.Client(url=url, key=key)
        else:
            client = cdsapi.Client()
        client.retrieve(
            "reanalysis-era5-single-levels",
            {
                "product_type": "reanalysis",
                "format": "netcdf",
                "variable": variables,
                "year": years_list,
                "month": months_list,
                "day": days_list,
                "time": ["00:00", "06:00", "12:00", "18:00"],
                "area": area,
            },
            output_path,
        )
        logger.info(f"✅ Downloaded ERA5 to {output_path}")
        return output_path
    except Exception as e:
        logger.error(f"❌ ERA5 download failed: {e}")
        return None


if __name__ == "__main__":
    download_era5("2019-01-01", "2023-12-31")