# ============================================================
# CPCB Ground Data Downloader
# ============================================================

"""
Downloads CPCB ground monitoring data via OpenAQ API.
"""

import os
import pandas as pd
import requests
import time
from dotenv import load_dotenv
from loguru import logger
from concurrent.futures import ThreadPoolExecutor, as_completed

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

    headers = {"X-API-Key": api_key}
    
    # 1. Fetch all locations in India
    logger.info("📡 Fetching locations index from OpenAQ v3...")
    try:
        loc_url = "https://api.openaq.org/v3/locations"
        loc_params = {"countries_id": 9, "limit": 1000}
        loc_res = requests.get(loc_url, headers=headers, params=loc_params, timeout=30)
        loc_res.raise_for_status()
        locations = loc_res.json().get("results", [])
    except Exception as e:
        logger.error(f"❌ Failed to fetch locations index: {e}. Using mock data.")
        return _generate_mock_cpcb_data()

    # Map locations to target cities
    city_sensors = {c: [] for c in cities}
    for loc in locations:
        name = loc.get("name", "")
        if name is None:
            name = ""
        name = name.lower()
        
        matched_city = None
        for city in cities:
            if city.lower() in name or (city == "Bengaluru" and "bangalore" in name):
                matched_city = city
                break
        if not matched_city:
            continue
            
        coords = loc.get("coordinates", {})
        for s in loc.get("sensors", []):
            if s.get("parameter", {}).get("name") == "pm25":
                city_sensors[matched_city].append({
                    "sensor_id": s["id"],
                    "lat": coords.get("latitude"),
                    "lon": coords.get("longitude")
                })

    # Sort sensors descending by sensor_id (prioritizing newer active sensors)
    for city in cities:
        city_sensors[city].sort(key=lambda x: x["sensor_id"], reverse=True)

    def fetch_sensor_data(s_info, city):
        sensor_id = s_info["sensor_id"]
        m_url = f"https://api.openaq.org/v3/sensors/{sensor_id}/measurements/daily"
        m_params = {
            "datetime_from": f"{start_date}T00:00:00Z",
            "datetime_to": f"{end_date}T23:59:59Z",
            "limit": 100
        }
        # Add slight spacing to prevent rate limits
        time.sleep(0.1)
        try:
            res = requests.get(m_url, headers=headers, params=m_params, timeout=10)
            if res.status_code == 200:
                results = res.json().get("results", [])
                if results:
                    records = []
                    for item in results:
                        val = item.get("value")
                        if val is not None and val > 0:
                            records.append({
                                "city": city,
                                "pm25": val,
                                "date": item.get("period", {}).get("datetimeFrom", {}).get("utc"),
                                "latitude": s_info["lat"],
                                "longitude": s_info["lon"]
                            })
                    return sensor_id, records
        except Exception:
            pass
        return sensor_id, []

    all_data = []

    # 2. Fetch daily measurements for each city
    for city in cities:
        sensors = city_sensors[city]
        logger.info(f"📥 Querying {city} ground data (found {len(sensors)} candidate PM2.5 sensors)...")
        
        city_records = []
        # Query up to 30 sensors per city concurrently
        with ThreadPoolExecutor(max_workers=8) as executor:
            futures = {executor.submit(fetch_sensor_data, s_info, city): s_info for s_info in sensors[:30]}
            for future in as_completed(futures):
                sensor_id, records = future.result()
                if records:
                    logger.info(f"  Sensor {sensor_id} -> Fetched {len(records)} daily records")
                    city_records.extend(records)
                    if len(city_records) >= 150:
                        break
                        
        if city_records:
            df = pd.DataFrame(city_records)
            all_data.append(df)

    if not all_data:
        logger.warning("⚠️ No CPCB ground data could be fetched. Using mock data.")
        return _generate_mock_cpcb_data()

    combined_df = pd.concat(all_data, ignore_index=True)

    # Save to file
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, f"cpcb_{start_date}_{end_date}.csv")
    combined_df.to_csv(output_path, index=False)

    logger.info(f"✅ Ground CPCB data successfully downloaded to {output_path}")
    return combined_df


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