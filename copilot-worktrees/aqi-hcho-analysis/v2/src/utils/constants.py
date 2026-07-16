# ============================================================
# Project Constants
# ============================================================

"""Project-wide constants."""

# India bounding box
INDIA_BBOX = {
    "lat_min": 8,
    "lat_max": 38,
    "lon_min": 68,
    "lon_max": 98,
}

# Grid resolution
GRID_RESOLUTION = 0.25

# Grid dimensions
GRID_LAT = int((INDIA_BBOX["lat_max"] - INDIA_BBOX["lat_min"]) / GRID_RESOLUTION)  # 120
GRID_LON = int((INDIA_BBOX["lon_max"] - INDIA_BBOX["lon_min"]) / GRID_RESOLUTION)  # 120

# Pollutant columns
POLLUTANT_COLUMNS = ["pm25", "pm10", "no2", "so2", "co", "o3", "hcho"]

# Satellite products
SATELLITE_PRODUCTS = ["NO2", "SO2", "CO", "O3", "HCHO"]

# Meteorological variables
METEOROLOGICAL_VARIABLES = ["temp", "rh", "wind_speed", "wind_u", "wind_v", "blh"]

# AQI breakpoints (CPCB)
AQI_BREAKPOINTS = [
    {"bp_low": 0, "bp_high": 30, "i_low": 0, "i_high": 50, "category": "Good"},
    {"bp_low": 31, "bp_high": 60, "i_low": 51, "i_high": 100, "category": "Satisfactory"},
    {"bp_low": 61, "bp_high": 90, "i_low": 101, "i_high": 200, "category": "Moderate"},
    {"bp_low": 91, "bp_high": 120, "i_low": 201, "i_high": 300, "category": "Poor"},
    {"bp_low": 121, "bp_high": 250, "i_low": 301, "i_high": 400, "category": "Very Poor"},
    {"bp_low": 251, "bp_high": float("inf"), "i_low": 401, "i_high": 500, "category": "Severe"},
]

# DBSCAN parameters
DBSCAN_EPS = 0.5
DBSCAN_MIN_SAMPLES = 4
HCHO_PERCENTILE = 90

# Source regions
SOURCE_REGIONS = {
    "IGP": {"lat_min": 22, "lat_max": 32, "lon_min": 74, "lon_max": 90},
    "Central_India": {"lat_min": 18, "lat_max": 24, "lon_min": 76, "lon_max": 84},
    "Northeast": {"lat_min": 22, "lat_max": 28, "lon_min": 90, "lon_max": 98},
}