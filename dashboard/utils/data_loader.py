"""
Data Loader - Load and cache data for dashboard
Provides synthetic data for AQI, Fire, HCHO, and model metrics
"""

import streamlit as st
import pandas as pd
import numpy as np
from pathlib import Path
from datetime import datetime, timedelta
from loguru import logger

@st.cache_data(ttl=3600)
def load_aqi_data(date=None):
    """Load AQI data with geospatial distribution across India
    
    Args:
        date: Specific date to load (optional)
    
    Returns:
        DataFrame with columns: lat, lon, aqi, state, date
    """
    # Major Indian cities with latitude/longitude
    cities = {
        'Delhi': {'lat': 28.7041, 'lon': 77.1025},
        'Mumbai': {'lat': 19.0760, 'lon': 72.8777},
        'Bangalore': {'lat': 12.9716, 'lon': 77.5946},
        'Kolkata': {'lat': 22.5726, 'lon': 88.3639},
        'Chennai': {'lat': 13.0827, 'lon': 80.2707},
        'Hyderabad': {'lat': 17.3850, 'lon': 78.4867},
        'Pune': {'lat': 18.5204, 'lon': 73.8567},
        'Ahmedabad': {'lat': 23.0225, 'lon': 72.5714},
        'Jaipur': {'lat': 26.9124, 'lon': 75.7873},
        'Lucknow': {'lat': 26.8467, 'lon': 80.9462},
        'Kochi': {'lat': 9.9312, 'lon': 76.2673},
        'Surat': {'lat': 21.1458, 'lon': 72.1944},
    }
    
    data = []
    for city, coords in cities.items():
        # Generate synthetic AQI with some variation
        base_aqi = np.random.randint(50, 300)
        data.append({
            'lat': coords['lat'] + np.random.normal(0, 0.1),
            'lon': coords['lon'] + np.random.normal(0, 0.1),
            'aqi': base_aqi,
            'state': city,
            'date': datetime.now().date()
        })
    
    # Add random points across India
    num_random = 50
    for _ in range(num_random):
        data.append({
            'lat': np.random.uniform(8, 35),
            'lon': np.random.uniform(68, 97),
            'aqi': np.random.randint(50, 350),
            'state': 'Region',
            'date': datetime.now().date()
        })
    
    df = pd.DataFrame(data)
    return df

@st.cache_data(ttl=3600)
def load_fire_data(date=None):
    """Load active fire data from satellite sensors
    
    Args:
        date: Specific date to load (optional)
        
    Returns:
        DataFrame with columns: lat, lon, intensity, detected_time
    """
    # Try loading all downloaded real data files in the fires directory
    fire_dir = Path("data/raw/satellite/viirs/fires/")
    df_list = []
    covered_ranges = []
    if fire_dir.exists():
        for csv_path in fire_dir.glob("fires_*.csv"):
            try:
                # Parse range from filename: fires_YYYY-MM-DD_YYYY-MM-DD.csv
                parts = csv_path.stem.split('_')
                if len(parts) == 3:
                    start_t = pd.to_datetime(parts[1]).date()
                    end_t = pd.to_datetime(parts[2]).date()
                    covered_ranges.append((start_t, end_t))
                
                df_real = pd.read_csv(csv_path)
                df_list.append(df_real)
            except Exception:
                pass
                
    if df_list:
        try:
            df_real = pd.concat(df_list, ignore_index=True)
            
            # Filter by date if specified
            if date is not None:
                # Convert date to date object and string
                if isinstance(date, str):
                    date_str = date.split(' ')[0]
                    date_obj = pd.to_datetime(date_str).date()
                else:
                    date_str = date.strftime('%Y-%m-%d')
                    date_obj = date
                    if isinstance(date_obj, datetime):
                        date_obj = date_obj.date()
                
                # Check if the requested date is covered by any downloaded file range
                is_date_covered = False
                for start_t, end_t in covered_ranges:
                    if start_t <= date_obj <= end_t:
                        is_date_covered = True
                        break
                
                if is_date_covered:
                    df_filtered = df_real[df_real['acq_date'] == date_str]
                    df_out = pd.DataFrame({
                        'lat': df_filtered['latitude'] if not df_filtered.empty else pd.Series(dtype=float),
                        'lon': df_filtered['longitude'] if not df_filtered.empty else pd.Series(dtype=float),
                        'intensity': df_filtered['frp'] if not df_filtered.empty else pd.Series(dtype=float),
                        'detected_time': (df_filtered['acq_time'].astype(str) + " UTC") if not df_filtered.empty else pd.Series(dtype=str)
                    })
                    logger.info(f"Loaded {len(df_out)} real fire hotspots (covered date range) for date {date}")
                    return df_out
            else:
                # Map all real data
                df_out = pd.DataFrame({
                    'lat': df_real['latitude'],
                    'lon': df_real['longitude'],
                    'intensity': df_real['frp'],
                    'detected_time': df_real['acq_time'].astype(str) + " UTC",
                    'date': df_real['acq_date']
                })
                logger.info(f"Loaded all {len(df_out)} real fire hotspots from downloaded CSVs")
                return df_out
        except Exception as e:
            logger.warning(f"Failed to read real fire data CSVs: {e}. Falling back to mock data.")

    # Fire hotspot regions in India
    fire_regions = [
        {'lat': 23.5, 'lon': 77.0},   # Madhya Pradesh
        {'lat': 21.0, 'lon': 78.5},   # Maharashtra
        {'lat': 25.5, 'lon': 73.0},   # Rajasthan
        {'lat': 26.0, 'lon': 81.0},   # Uttar Pradesh
        {'lat': 19.0, 'lon': 72.5},   # Gujarat coast
    ]
    
    data = []
    np.random.seed(42)
    
    for region in fire_regions:
        # Generate multiple fires around each region
        num_fires = np.random.randint(80, 200)
        for _ in range(num_fires):
            data.append({
                'lat': region['lat'] + np.random.normal(0, 2.5),
                'lon': region['lon'] + np.random.normal(0, 2.5),
                'intensity': np.random.uniform(30, 100),
                'detected_time': (datetime.now() - timedelta(hours=np.random.randint(0, 24))).strftime('%H:%M UTC')
            })
    
    df = pd.DataFrame(data)
    return df

@st.cache_data(ttl=3600)
def load_hcho_data(date=None):
    """Load HCHO concentration data with hotspot markers
    
    Args:
        date: Specific date to load (optional)
    
    Returns:
        DataFrame with columns: lat, lon, concentration, status
    """
    # Try loading real downloaded HCHO tif files
    hcho_dir = Path("data/raw/satellite/sentinel5p/hcho/")
    if hcho_dir.exists():
        try:
            import rasterio
            for tif_path in hcho_dir.glob("HCHO_*.tif"):
                # Parse date range from filename: HCHO_YYYY-MM-DD_YYYY-MM-DD.tif
                parts = tif_path.stem.split('_')
                if len(parts) == 3:
                    start_t = pd.to_datetime(parts[1]).date()
                    end_t = pd.to_datetime(parts[2]).date()
                    
                    # Convert query date to date object
                    query_date = None
                    if date is not None:
                        if isinstance(date, str):
                            query_date = pd.to_datetime(date.split(' ')[0]).date()
                        else:
                            query_date = date
                            if isinstance(query_date, datetime):
                                query_date = query_date.date()
                                
                    # If date matches range or date is None (load latest)
                    if date is None or (query_date is not None and start_t <= query_date <= end_t):
                        with rasterio.open(tif_path) as src:
                            band1 = src.read(1)
                            # Replace nodata with NaN
                            if src.nodata is not None:
                                band1[band1 == src.nodata] = np.nan
                            
                            # Find valid coordinates and values
                            valid_mask = ~np.isnan(band1) & (band1 > 0)
                            rows, cols = np.where(valid_mask)
                            
                            if len(rows) > 0:
                                values = band1[valid_mask]
                                
                                # Subsample to prevent dashboard map from lagging/crashing (max 500 points)
                                if len(rows) > 500:
                                    # Take top 500 highest values (hotspots!)
                                    idx = np.argsort(values)[-500:]
                                    rows = rows[idx]
                                    cols = cols[idx]
                                    values = values[idx]
                                    
                                lons, lats = src.xy(rows, cols)
                                
                                # Scale values to match mock scale (e.g. 5 to 25 ppb for HCHO)
                                max_val = values.max() if values.max() > 0 else 1
                                concentrations = 5 + (values / max_val) * 20
                                
                                statuses = []
                                for conc in concentrations:
                                    status = 'High' if conc > 15 else ('Medium' if conc > 10 else 'Low')
                                    statuses.append(status)
                                    
                                df_out = pd.DataFrame({
                                    'lat': lats,
                                    'lon': lons,
                                    'concentration': concentrations,
                                    'status': statuses
                                })
                                logger.info(f"Loaded {len(df_out)} real HCHO hotspots from {tif_path.name} for date {date}")
                                return df_out
        except Exception as e:
            logger.warning(f"Failed to read real HCHO TIF file: {e}. Falling back to mock data.")

    # HCHO hotspot regions (typically near industrial areas and biomass burning)
    hcho_regions = [
        {'lat': 28.7, 'lon': 77.1},   # Delhi-NCR
        {'lat': 19.0, 'lon': 72.8},   # Mumbai region
        {'lat': 23.2, 'lon': 79.8},   # Central India
        {'lat': 26.0, 'lon': 85.0},   # Eastern India
    ]
    
    data = []
    np.random.seed(43)
    
    for region in hcho_regions:
        # Generate HCHO hotspots
        num_hotspots = np.random.randint(5, 15)
        for _ in range(num_hotspots):
            conc = np.random.uniform(5, 25)
            status = 'High' if conc > 15 else ('Medium' if conc > 10 else 'Low')
            
            data.append({
                'lat': region['lat'] + np.random.normal(0, 1),
                'lon': region['lon'] + np.random.normal(0, 1),
                'concentration': conc,
                'status': status
            })
    
    df = pd.DataFrame(data)
    return df

@st.cache_data(ttl=3600)
def load_model_metrics():
    """Load model performance metrics
    
    Returns:
        Dict with metrics for different ML models
    """
    return {
        'xgboost': {
            'rmse': 12.4,
            'mae': 8.7,
            'r2': 0.87,
            'mape': 14.2,
            'name': 'XGBoost'
        },
        'random_forest': {
            'rmse': 15.8,
            'mae': 11.2,
            'r2': 0.79,
            'mape': 18.5,
            'name': 'Random Forest'
        },
        'lstm': {
            'rmse': 14.2,
            'mae': 9.5,
            'r2': 0.83,
            'mape': 16.1,
            'name': 'LSTM'
        },
    }

@st.cache_data(ttl=3600)
def get_kpi_values():
    """Get current KPI values
    
    Returns:
        Dict with key metrics
    """
    aqi_data = load_aqi_data()
    fire_data = load_fire_data()
    hcho_data = load_hcho_data()
    
    return {
        'aqi_today': int(aqi_data['aqi'].mean()),
        'aqi_trend': np.random.randint(-20, 20),
        'hcho_avg': round(hcho_data['concentration'].mean(), 1),
        'active_fires': len(fire_data),
        'high_hcho_areas': len(hcho_data[hcho_data['concentration'] > 15]),
    }

def clear_cache():
    """Clear all cached data"""
    st.cache_data.clear()
