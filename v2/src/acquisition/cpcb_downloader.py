# ============================================================
# CPCB Ground Data Downloader
# ============================================================

"""
Downloads CPCB ground monitoring data via OpenAQ API.
"""

import os
import pandas as pd
import requests
from dotenv import load_dotenv
from loguru import logger

load_dotenv()


def download_cpcb(
    start_date: str,
    end_date: str,
    output_dir: str = "data/raw/ground/cpcb/",
    api_key: str = None,
    cities: list = None,
) -> pd.DataFrame:
    """
    Download CPCB data for Indian cities.

    Args:
        start_date (str): 'YYYY-MM-DD'
        end_date (str): 'YYYY-MM-DD'
        output_dir (str): Output directory
        api_key (str): OpenAQ API key
        cities (list): List of city names

    Returns:
        pd.DataFrame: CPCB data
    """
    logger.info(f"📥 Downloading CPCB data from {start_date} to {end_date}")

    if api_key is None:
        api_key = os.getenv("OPENAQ_API_KEY")
        if not api_key:
            logger.warning("OPENAQ_API_KEY not set. Using mock data.")
            return _generate_mock_cpcb_data()

    if cities is None:
        cities = ["Delhi", "Mumbai", "Kolkata", "Bengaluru", "Chennai"]

    all_data = []

    for city in cities:
        try:
            df = _fetch_city_data(city, start_date, end_date, api_key)
            if df is not None and not df.empty:
                all_data.append(df)
        except Exception as e:
            logger.error(f"❌ Failed to fetch {city}: {e}")

    if not all_data:
        logger.warning("No CPCB data fetched. Using mock data.")
        return _generate_mock_cpcb_data()

    combined_df = pd.concat(all_data, ignore_index=True)

    # Save to file
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, f"cpcb_{start_date}_{end_date}.csv")
    combined_df.to_csv(output_path, index=False)

    logger.info(f"✅ Downloaded CPCB data to {output_path}")
    return combined_df


def _fetch_city_data(city: str, start_date: str, end_date: str, api_key: str) -> pd.DataFrame:
    """Fetch data for a single city from OpenAQ."""
    url = "https://api.openaq.org/v3/measurements"

    headers = {"X-API-Key": api_key}
    params = {
        "parameter": "pm25",
        "city": city,
        "date_from": start_date,
        "date_to": end_date,
        "limit": 1000,
    }

    try:
        response = requests.get(url, headers=headers, params=params, timeout=30)
        response.raise_for_status()
        data = response.json()

        if "results" not in data or not data["results"]:
            return pd.DataFrame()

        # Parse results
        records = []
        for result in data["results"]:
            records.append(
                {
                    "city": result.get("city", city),
                    "pm25": result.get("value"),
                    "date": result.get("date", {}).get("utc"),
                    "latitude": result.get("coordinates", {}).get("latitude"),
                    "longitude": result.get("coordinates", {}).get("longitude"),
                }
            )

        return pd.DataFrame(records)

    except Exception as e:
        logger.error(f"❌ Error fetching {city}: {e}")
        return pd.DataFrame()


def _generate_mock_cpcb_data(n_points: int = 1000) -> pd.DataFrame:
    """Generate mock CPCB data for testing."""
    import numpy as np

    np.random.seed(42)
    cities = ["Delhi", "Mumbai", "Kolkata", "Bengaluru", "Chennai"]

    data = {
        "city": np.random.choice(cities, n_points),
        "pm25": np.random.uniform(20, 200, n_points),
        "date": pd.date_range("2024-01-01", periods=n_points),
        "latitude": np.random.uniform(8, 38, n_points),
        "longitude": np.random.uniform(68, 98, n_points),
    }
    return pd.DataFrame(data)


if __name__ == "__main__":
    df = download_cpcb("2024-01-01", "2024-01-31")
    print(df.head())