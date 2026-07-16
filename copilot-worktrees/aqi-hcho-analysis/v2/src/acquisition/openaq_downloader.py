# ============================================================
# OpenAQ API Data Downloader
# ============================================================

"""
Direct OpenAQ API wrapper for air quality data.
"""

import os
import pandas as pd
import requests
from dotenv import load_dotenv
from loguru import logger

load_dotenv()


class OpenAQClient:
    """OpenAQ API v3 client."""

    BASE_URL = "https://api.openaq.org/v3/"

    def __init__(self, api_key: str = None):
        """Initialize OpenAQ client."""
        self.api_key = api_key or os.getenv("OPENAQ_API_KEY")
        self.headers = {"X-API-Key": self.api_key} if self.api_key else {}

    def get_locations(self, coordinates: str = None, radius: int = 50000, limit: int = 100):
        """Get monitoring locations."""
        url = f"{self.BASE_URL}locations"
        params = {"limit": limit}

        if coordinates:
            params["coordinates"] = coordinates
            params["radius"] = radius

        response = requests.get(url, headers=self.headers, params=params)
        return response.json().get("results", [])

    def get_measurements(
        self,
        parameter: str = "pm25",
        city: str = None,
        start_date: str = None,
        end_date: str = None,
        limit: int = 1000,
    ) -> pd.DataFrame:
        """Get measurements for a parameter."""
        url = f"{self.BASE_URL}measurements"
        params = {"parameter": parameter, "limit": limit}

        if city:
            params["city"] = city
        if start_date:
            params["date_from"] = start_date
        if end_date:
            params["date_to"] = end_date

        try:
            response = requests.get(url, headers=self.headers, params=params)
            response.raise_for_status()
            data = response.json()

            records = []
            for result in data.get("results", []):
                records.append(
                    {
                        "city": result.get("city", "unknown"),
                        "parameter": parameter,
                        "value": result.get("value"),
                        "unit": result.get("unit"),
                        "date": result.get("date", {}).get("utc"),
                        "latitude": result.get("coordinates", {}).get("latitude"),
                        "longitude": result.get("coordinates", {}).get("longitude"),
                    }
                )

            return pd.DataFrame(records)

        except Exception as e:
            logger.error(f"❌ OpenAQ request failed: {e}")
            return pd.DataFrame()


def download_openaq(
    start_date: str,
    end_date: str,
    output_dir: str = "data/raw/ground/openaq/",
    api_key: str = None,
) -> pd.DataFrame:
    """
    Download data from OpenAQ API.

    Args:
        start_date (str): 'YYYY-MM-DD'
        end_date (str): 'YYYY-MM-DD'
        output_dir (str): Output directory
        api_key (str): OpenAQ API key

    Returns:
        pd.DataFrame: Air quality data
    """
    logger.info(f"📥 Downloading OpenAQ data from {start_date} to {end_date}")

    client = OpenAQClient(api_key)
    if not client.api_key:
        logger.warning("No OpenAQ API key provided. Using mock data.")
        return _generate_mock_openaq_data()

    # Fetch data for each parameter
    parameters = ["pm25", "pm10", "no2", "so2", "co", "o3"]
    all_data = []

    for param in parameters:
        df = client.get_measurements(param, start_date=start_date, end_date=end_date)
        if not df.empty:
            all_data.append(df)

    if not all_data:
        logger.warning("No OpenAQ data fetched. Using mock data.")
        return _generate_mock_openaq_data()

    combined_df = pd.concat(all_data, ignore_index=True)

    # Save to file
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, f"openaq_{start_date}_{end_date}.csv")
    combined_df.to_csv(output_path, index=False)

    logger.info(f"✅ Downloaded OpenAQ data to {output_path}")
    return combined_df


def _generate_mock_openaq_data(n_points: int = 1000) -> pd.DataFrame:
    """Generate mock OpenAQ data for testing."""
    import numpy as np

    np.random.seed(42)
    parameters = ["pm25", "pm10", "no2", "so2", "co", "o3"]

    data = {
        "city": np.random.choice(["Delhi", "Mumbai", "Kolkata", "Bengaluru", "Chennai"], n_points),
        "parameter": np.random.choice(parameters, n_points),
        "value": np.random.uniform(10, 200, n_points),
        "date": pd.date_range("2024-01-01", periods=n_points),
        "latitude": np.random.uniform(8, 38, n_points),
        "longitude": np.random.uniform(68, 98, n_points),
    }
    return pd.DataFrame(data)


if __name__ == "__main__":
    df = download_openaq("2024-01-01", "2024-01-31")
    print(df.head())