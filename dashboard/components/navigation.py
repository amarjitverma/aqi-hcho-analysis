"""
Navigation Component - Premium horizontal navigation tabs for multi-page dashboard
"""

import streamlit as st
import json
from pathlib import Path

# Compatibility patch for older Streamlit versions
if not hasattr(st, "rerun"):
    st.rerun = st.experimental_rerun

def initialize_cache_files():
    """Write mock fallback JSON and GeoJSON datasets to cache directory if they do not exist."""
    data_dir = Path("dashboard/cache/")
    data_dir.mkdir(parents=True, exist_ok=True)
    
    # 1. AQI Grid Coordinates
    aqi_path = data_dir / "aqi_grid.json"
    if not aqi_path.exists():
        aqi_data = {
            "type": "FeatureCollection",
            "features": [
                {"type": "Feature", "geometry": {"type": "Point", "coordinates": [77.2090, 28.6139]}, "properties": {"aqi": 312, "pm25": 110.5}},
                {"type": "Feature", "geometry": {"type": "Point", "coordinates": [72.8777, 19.0760]}, "properties": {"aqi": 95, "pm25": 32.4}},
                {"type": "Feature", "geometry": {"type": "Point", "coordinates": [88.3639, 22.5726]}, "properties": {"aqi": 145, "pm25": 55.2}},
                {"type": "Feature", "geometry": {"type": "Point", "coordinates": [80.2707, 13.0827]}, "properties": {"aqi": 62, "pm25": 18.1}},
                {"type": "Feature", "geometry": {"type": "Point", "coordinates": [78.4867, 17.3850]}, "properties": {"aqi": 88, "pm25": 28.4}}
            ]
        }
        with open(aqi_path, "w", encoding="utf-8") as f:
            json.dump(aqi_data, f, indent=2)

    # 2. HCHO Hotspots
    hcho_path = data_dir / "hcho_hotspots.geojson"
    if not hcho_path.exists():
        hcho_data = {
            "type": "FeatureCollection",
            "features": [
                {
                    "type": "Feature",
                    "geometry": {"type": "Point", "coordinates": [77.2090, 28.6139]},
                    "properties": {
                        "cluster_id": 0,
                        "num_cells": 45,
                        "mean_hcho": 18.4,
                        "max_hcho": 25.6,
                        "source_region": "IGP (Crop Burning)",
                        "color": "#6D28D9",
                        "radius": 5
                    }
                },
                {
                    "type": "Feature",
                    "geometry": {"type": "Point", "coordinates": [80.0, 22.0]},
                    "properties": {
                        "cluster_id": 1,
                        "num_cells": 28,
                        "mean_hcho": 15.2,
                        "max_hcho": 22.0,
                        "source_region": "Central India (Forest Fires)",
                        "color": "#F59E0B",
                        "radius": 4
                    }
                },
                {
                    "type": "Feature",
                    "geometry": {"type": "Point", "coordinates": [94.0, 26.0]},
                    "properties": {
                        "cluster_id": 2,
                        "num_cells": 17,
                        "mean_hcho": 16.8,
                        "max_hcho": 20.5,
                        "source_region": "Northeast India (Forest Fires)",
                        "color": "#A78BFA",
                        "radius": 3
                    }
                }
            ]
        }
        with open(hcho_path, "w", encoding="utf-8") as f:
            json.dump(hcho_data, f, indent=2)

    # 3. Active Fires
    fires_path = data_dir / "fire_locations.geojson"
    if not fires_path.exists():
        fires_data = {
            "type": "FeatureCollection",
            "features": [
                {"type": "Feature", "geometry": {"type": "Point", "coordinates": [76.5, 30.5]}, "properties": {"frp": 85.2, "confidence": 92}},
                {"type": "Feature", "geometry": {"type": "Point", "coordinates": [82.3, 21.8]}, "properties": {"frp": 45.8, "confidence": 78}},
                {"type": "Feature", "geometry": {"type": "Point", "coordinates": [93.5, 25.2]}, "properties": {"frp": 62.1, "confidence": 85}}
            ]
        }
        with open(fires_path, "w", encoding="utf-8") as f:
            json.dump(fires_data, f, indent=2)

    # 4. Wind Vectors
    wind_path = data_dir / "wind_vectors.json"
    if not wind_path.exists():
        wind_data = {
            "u_wind": -2.5,
            "v_wind": 1.8,
            "direction": "North-East"
        }
        with open(wind_path, "w", encoding="utf-8") as f:
            json.dump(wind_data, f, indent=2)

    # 5. Model Metrics
    metrics_path = data_dir / "model_metrics.json"
    if not metrics_path.exists():
        metrics_data = {
            "rmse": 12.4,
            "mae": 8.7,
            "r2": 0.87,
            "mape": 14.2
        }
        with open(metrics_path, "w", encoding="utf-8") as f:
            json.dump(metrics_data, f, indent=2)

def render_navigation(active_page: str):
    """
    Render a premium horizontal navigation bar at the top of the dashboard pages.
    
    Args:
        active_page (str): Key of the current active page to apply active styling
    """
    # Ensure cache files are initialized
    initialize_cache_files()
    
    pages = {
        'dashboard': {'label': '🏠 Dashboard', 'url': '/'},
        'map_view': {'label': '🗺️ Map View', 'url': '/Map_View'},
        'model_performance': {'label': '📊 Model Performance', 'url': '/Model_Performance'},
        'biomass_burning': {'label': '🔥 Biomass Burning', 'url': '/Biomass_Burning'},
        'export_share': {'label': '📥 Export & Share', 'url': '/Export_Share'},
        'alerts': {'label': '🔔 Alerts', 'url': '/Alerts'}
    }
    
    # Secondary pages appended dynamically when active
    secondary_pages = {
        'reports': {'label': '📄 Reports', 'url': '/Reports'},
        'data_sources': {'label': '🗂️ Data Sources', 'url': '/Data_Sources'},
        'admin_panel': {'label': '⚙️ Admin Panel', 'url': '/Admin_Panel'},
        'help_support': {'label': '❓ Help & Support', 'url': '/Help_Support'}
    }
    
    if active_page in secondary_pages:
        pages[active_page] = secondary_pages[active_page]
    
    nav_html = "<div style='display: flex; gap: 8px; margin-bottom: 25px; overflow-x: auto; padding-bottom: 12px; border-bottom: 1px solid #E2E8F0;'>"
    
    for key, info in pages.items():
        is_active = (key == active_page)
        bg = "#0066CC" if is_active else "#FFFFFF"
        color = "#FFFFFF" if is_active else "#1F2328"
        border = "1px solid #005bb7" if is_active else "1px solid #E2E8F0"
        shadow = "box-shadow: 0 4px 6px -1px rgba(0, 102, 204, 0.12);" if is_active else "box-shadow: 0 1px 2px 0 rgba(0, 0, 0, 0.05);"
        
        nav_html += f"<a href='{info['url']}' target='_self' style='text-decoration: none; padding: 10px 20px; background-color: {bg}; color: {color}; border: {border}; border-radius: 8px; font-weight: 500; font-size: 14px; font-family: \"Inter\", sans-serif; transition: all 0.2s ease-in-out; white-space: nowrap; {shadow}'>{info['label']}</a>"
        
    nav_html += "</div>"
    st.markdown(nav_html.replace('\n', ' '), unsafe_allow_html=True)
