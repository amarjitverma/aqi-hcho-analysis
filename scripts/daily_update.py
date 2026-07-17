"""
Daily Update Scheduler - Swachh Agam
Fetches the latest available satellite, fire, and ground data,
updates local caches, and runs hotspot analyses.
"""

import os
import sys
from pathlib import Path
from datetime import datetime, timedelta
from loguru import logger

# Add root folder to path
root_dir = Path(__file__).parent.parent
sys.path.insert(0, str(root_dir))

from src.acquisition.sentinel5p_downloader import initialize_gee, download_sentinel5p
from src.acquisition.firms_downloader import download_firms
from src.acquisition.cpcb_downloader import download_cpcb

# Set up logging
logger.add("runtime/logs/daily_update.log", rotation="500 MB")

def run_daily_update():
    logger.info("⏰ Starting automated daily update pipeline...")
    
    # 1. Define target date range (normally yesterday to handle satellite data latency)
    end_date = datetime.now() - timedelta(days=1)
    start_date = end_date - timedelta(days=2) # 3-day window
    
    start_str = start_date.strftime("%Y-%m-%d")
    end_str = end_date.strftime("%Y-%m-%d")
    
    logger.info(f"Targeting window: {start_str} to {end_str}")
    
    # 2. Download active fires (NASA FIRMS)
    try:
        logger.info("🔥 Fetching active fires...")
        download_firms(start_date=start_str, end_date=end_str)
    except Exception as e:
        logger.error(f"Failed to fetch fires: {e}")
        
    # 3. Download Sentinel-5P columns (GEE)
    try:
        logger.info("📡 Initializing Earth Engine...")
        if initialize_gee():
            for product in ["HCHO", "NO2", "SO2", "CO", "O3"]:
                logger.info(f"Downloading Sentinel-5P {product}...")
                download_sentinel5p(start_date=start_str, end_date=end_str, product=product)
        else:
            logger.error("Failed to initialize Earth Engine.")
    except Exception as e:
        logger.error(f"Failed to fetch satellite columns: {e}")
        
    # 4. Download CPCB ground data (OpenAQ)
    try:
        logger.info("📥 Fetching ground station measurements...")
        download_cpcb(start_date=start_str, end_date=end_str)
    except Exception as e:
        logger.error(f"Failed to fetch CPCB ground data: {e}")

    # 5. Regenerate Hotspots
    try:
        logger.info("🗺️ Regenerating HCHO hotspot clusters...")
        # Resolve path to runner
        runner_path = root_dir / "run_hotspot.py"
        if runner_path.exists():
            import subprocess
            subprocess.run([sys.executable, str(runner_path)], check=True)
            logger.info("✅ Hotspots regenerated and exported to dashboard/cache.")
    except Exception as e:
        logger.error(f"Failed to regenerate hotspots: {e}")

    logger.info("🎉 Daily update pipeline run completed successfully.")

if __name__ == "__main__":
    run_daily_update()
