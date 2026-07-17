"""
Download 5-Year Historical Dataset - Swachh Agam (Updated)
Downloads Sentinel-5P columns from GEE and ERA5 meteorology from Copernicus CDS
for the latest 5 years till date (2021-01-01 to 2026-07-17).
"""

import os
import sys
from pathlib import Path
from loguru import logger
import pandas as pd
from datetime import datetime

# Add root folder to path
root_dir = Path(__file__).parent.parent
sys.path.insert(0, str(root_dir))

from src.acquisition.sentinel5p_downloader import initialize_gee, download_sentinel5p
from src.acquisition.era5_downloader import download_era5

# Logger configuration
logger.add("runtime/logs/download_5years.log", rotation="500 MB")

def download_historical_data():
    logger.info("🚀 Starting 5-year historical download script (2021 to 2026)...")
    
    current_year = datetime.now().year # 2026
    years = [2021, 2022, 2023, 2024, 2025, 2026]
    
    # 1. Download Sentinel-5P Satellite Columns via GEE
    try:
        logger.info("📡 Initializing Google Earth Engine...")
        if initialize_gee():
            for year in years:
                start_date = f"{year}-01-01"
                if year == current_year:
                    # Download up to yesterday
                    yesterday = datetime.now() - pd.Timedelta(days=1)
                    end_date = yesterday.strftime("%Y-%m-%d")
                else:
                    end_date = f"{year}-12-31"
                    
                logger.info(f"Downloading Sentinel-5P products for year {year} ({start_date} to {end_date})...")
                for product in ["HCHO", "NO2", "SO2", "CO", "O3"]:
                    logger.info(f"Downloading {product} for {year}...")
                    download_sentinel5p(start_date=start_date, end_date=end_date, product=product)
        else:
            logger.error("GEE initialization failed.")
    except Exception as e:
        logger.error(f"Error during Sentinel-5P download: {e}")
        
    # 2. Download ERA5 Meteorological NetCDFs via Copernicus CDS
    try:
        logger.info("🌍 Initializing Copernicus CDS Downloads...")
        for year in years:
            start_date = f"{year}-01-01"
            if year == current_year:
                # ERA5 has a latency, so download up to 5 days ago (ERA5T)
                five_days_ago = datetime.now() - pd.Timedelta(days=5)
                end_date = five_days_ago.strftime("%Y-%m-%d")
            else:
                end_date = f"{year}-12-31"
                
            logger.info(f"Submitting request for ERA5 {year} reanalysis layers...")
            download_era5(start_date=start_date, end_date=end_date)
    except Exception as e:
        logger.error(f"Error during ERA5 download: {e}")

    logger.info("🎉 5-year historical download batch submission finished.")

if __name__ == "__main__":
    download_historical_data()
