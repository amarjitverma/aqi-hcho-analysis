# ============================================================
# NASA FIRMS Fire Data Downloader
# ============================================================

"""
Downloads active fire data from NASA FIRMS API.
"""

import os
import requests
import pandas as pd
from dotenv import load_dotenv
from loguru import logger

load_dotenv()


def download_firms(
    start_date: str,
    end_date: str,
    output_dir: str = "data/raw/satellite/viirs/fires/",
    api_key: str = None,
) -> pd.DataFrame:
    """
    Download FIRMS fire data for India.

    Args:
        start_date (str): 'YYYY-MM-DD'
        end_date (str): 'YYYY-MM-DD'
        output_dir (str): Output directory
        api_key (str): FIRMS API key

    Returns:
        pd.DataFrame: Fire data
    """
    logger.info(f"📥 Downloading FIRMS data from {start_date} to {end_date}")

    if api_key is None:
        api_key = os.getenv("FIRMS_API_KEY")
        if not api_key:
            logger.warning("FIRMS_API_KEY not set. Using mock data.")
            return _generate_mock_fire_data()

    # India bounding box
    bbox = "68.0,8.0,98.0,38.0"

    # FIRMS API URL
    url = f"https://firms.modaps.eosdis.nasa.gov/api/area/csv/{api_key}/VIIRS_SP/70.0,8.0,100.0,40.0/1/{start_date}"

    try:
        response = requests.get(url, timeout=30)
        response.raise_for_status()

        # Parse CSV
        from io import StringIO

        df = pd.read_csv(StringIO(response.text))

        # Save to file
        os.makedirs(output_dir, exist_ok=True)
        output_path = os.path.join(output_dir, f"fires_{start_date}_{end_date}.csv")
        df.to_csv(output_path, index=False)

        logger.info(f"✅ Downloaded {len(df)} fire points to {output_path}")
        return df

    except Exception as e:
        logger.error(f"❌ FIRMS download failed: {e}")
        return _generate_mock_fire_data()


def _generate_mock_fire_data(n_points: int = 100) -> pd.DataFrame:
    """Generate mock fire data for testing."""
    import numpy as np

    np.random.seed(42)
    data = {
        "latitude": np.random.uniform(8, 38, n_points),
        "longitude": np.random.uniform(68, 98, n_points),
        "frp": np.random.uniform(0, 100, n_points),
        "confidence": np.random.uniform(0, 100, n_points),
    }
    return pd.DataFrame(data)


if __name__ == "__main__":
    df = download_firms("2024-01-01", "2024-01-31")
    print(df.head())