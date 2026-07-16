#!/usr/bin/env python3
# ============================================================
# Download Data Script
# ============================================================

"""Download all required data for the project."""

import argparse
from pathlib import Path
from loguru import logger
import sys
import os

# Add project root to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.acquisition.sentinel5p_downloader import download_all_sentinel5p, initialize_gee
from src.acquisition.era5_downloader import download_era5
from src.acquisition.firms_downloader import download_firms
from src.acquisition.cpcb_downloader import download_cpcb


def main():
    parser = argparse.ArgumentParser(description="Download all data for the project")
    parser.add_argument("--years", type=int, default=5, help="Number of years of data to download")
    parser.add_argument("--start-date", type=str, default=None, help="Start date (YYYY-MM-DD)")
    parser.add_argument("--end-date", type=str, default="2023-12-31", help="End date (YYYY-MM-DD)")
    parser.add_argument("--sentinel5p", action="store_true", help="Download Sentinel-5P data")
    parser.add_argument("--era5", action="store_true", help="Download ERA5 data")
    parser.add_argument("--firms", action="store_true", help="Download FIRMS fire data")
    parser.add_argument("--cpcb", action="store_true", help="Download CPCB data")
    parser.add_argument("--all", action="store_true", default=True, help="Download all data")
    
    args = parser.parse_args()
    
    logger.info("🚀 Starting data download...")
    
    # Determine what to download
    download_sentinel5p = args.sentinel5p or args.all
    download_era5_flag = args.era5 or args.all
    download_firms_flag = args.firms or args.all
    download_cpcb_flag = args.cpcb or args.all
    
    if download_sentinel5p:
        logger.info("📡 Downloading Sentinel-5P data...")
        if initialize_gee():
            download_all_sentinel5p(
                years=args.years,
                start_date=args.start_date,
                end_date=args.end_date
            )
        else:
            logger.error("GEE initialization failed. Skipping Sentinel-5P download.")
    
    if download_era5_flag:
        logger.info("🌤️ Downloading ERA5 data...")
        download_era5(
            start_date=args.start_date or f"{2023 - args.years + 1}-01-01",
            end_date=args.end_date
        )
    
    if download_firms_flag:
        logger.info("🔥 Downloading FIRMS fire data...")
        download_firms(
            start_date=args.start_date or f"{2023 - args.years + 1}-01-01",
            end_date=args.end_date
        )
    
    if download_cpcb_flag:
        logger.info("🏭 Downloading CPCB data...")
        download_cpcb(
            start_date=args.start_date or f"{2023 - args.years + 1}-01-01",
            end_date=args.end_date
        )
    
    logger.info("✅ Data download complete!")


if __name__ == "__main__":
    main()