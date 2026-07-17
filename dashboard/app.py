# ============================================================
# Streamlit Dashboard - Main Application
# ============================================================

"""
Swachh Agam - Air Quality Dashboard
Interactive dashboard for AQI and HCHO hotspot visualization.
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import folium
from streamlit_folium import st_folium
import json
from datetime import datetime, timedelta
from pathlib import Path
import sys
dashboard_path = Path(__file__).parent
if str(dashboard_path) not in sys.path:
    sys.path.insert(0, str(dashboard_path))

from components.header import render_header
from components.navigation import render_navigation

# ============================================================
# Page Configuration
# ============================================================

st.set_page_config(
    page_title="Swachh Agam - Air Quality Dashboard",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ============================================================
# Custom CSS
# ============================================================

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    html, body, [data-testid="stAppViewContainer"] {
        font-family: 'Inter', -apple-system, sans-serif;
    }
    .main { background-color: #F8F9FA; color: #1F2328; }
    .stMetric { 
        background-color: #FFFFFF; 
        border-radius: 12px; 
        padding: 20px; 
        border: 1px solid #E2E8F0;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05), 0 2px 4px -1px rgba(0, 0, 0, 0.03);
        transition: all 0.25s cubic-bezier(0.4, 0, 0.2, 1);
    }
    .stMetric:hover { 
        border-color: #0066CC; 
        box-shadow: 0 10px 15px -3px rgba(0, 102, 204, 0.08), 0 4px 6px -2px rgba(0, 102, 204, 0.04);
        transform: translateY(-2px);
    }
    h1, h2, h3 { 
        color: #1F2328; 
        font-family: 'Inter', sans-serif;
        font-weight: 600;
    }
    h1 { color: #0066CC; font-weight: 700; letter-spacing: -0.025em; }
    .st-emotion-cache-1v0mbdj { color: #475569; }
    section[data-testid="stSidebar"] { background-color: #FFFFFF; border-right: 1px solid #E2E8F0; }
    .st-emotion-cache-16idsys { background-color: #F8F9FA; }
    .stTabs [data-baseweb="tab"] {
        background-color: #F1F5F9;
        border-radius: 8px 8px 0 0;
        padding: 10px 20px;
        color: #475569;
        font-weight: 500;
        border: 1px solid #E2E8F0;
        border-bottom: none;
        transition: all 0.2s ease;
    }
    .stTabs [data-baseweb="tab"]:hover {
        color: #0066CC;
        background-color: #E2E8F0;
    }
    .stTabs [data-baseweb="tab"][aria-selected="true"] {
        background-color: #FFFFFF;
        color: #0066CC;
        border-color: #E2E8F0;
        border-bottom: 2px solid #FFFFFF;
        font-weight: 600;
    }
    .stButton > button {
        background-color: #0066CC;
        color: #FFFFFF;
        border: 1px solid #005bb7;
        border-radius: 8px;
        padding: 10px 20px;
        font-weight: 500;
        transition: all 0.2s ease;
    }
    .stButton > button:hover { 
        background-color: #005bb7; 
        border-color: #004b99; 
        color: #FFFFFF; 
        box-shadow: 0 4px 6px -1px rgba(0, 102, 204, 0.12);
        transform: translateY(-1px);
    }
    .reportview-container .main .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
    }
</style>
""", unsafe_allow_html=True)

# ============================================================
# Session State
# ============================================================

if "data" not in st.session_state:
    st.session_state.data = {}

# ============================================================
# Data Loading Functions
# ============================================================

def load_data():
    """Load dashboard data files."""
    data_dir = Path("dashboard/cache/")
    
    files = {
        "aqi": "aqi_grid.json",
        "hotspots": "hcho_hotspots.geojson",
        "fires": "fire_locations.geojson",
        "wind": "wind_vectors.json",
        "metrics": "model_metrics.json",
    }
    
    data = {}
    for key, filename in files.items():
        filepath = data_dir / filename
        if filepath.exists():
            try:
                with open(filepath, "r") as f:
                    data[key] = json.load(f)
            except:
                data[key] = None
        else:
            data[key] = None
    
    return data

def generate_demo_data():
    """Generate demo data for testing when real data isn't available."""
    np.random.seed(42)
    
    # Demo metrics
    metrics = {
        "rmse": 12.4,
        "mae": 8.7,
        "r2": 0.87,
        "mape": 14.2
    }
    
    # Demo hotspots
    hotspots = {
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
    
    return {"metrics": metrics, "hotspots": hotspots}

# ============================================================
# Sidebar
# ============================================================

with st.sidebar:
    st.title("🌍 Swachh Agam")
    st.caption("Air Quality Dashboard")
    st.markdown("---")
    
    date = st.date_input(
        "Select Date",
        value=datetime.now().date() - timedelta(days=1),
        max_value=datetime.now().date(),
    )
    
    st.subheader("Map Layers")
    layers = {
        "AQI": st.checkbox("AQI", value=True),
        "HCHO": st.checkbox("HCHO Hotspots", value=True),
        "Fire": st.checkbox("Active Fires", value=False),
        "Wind": st.checkbox("Wind Vectors", value=False),
    }
    
    st.markdown("---")
    st.caption("Team Swachh Agam | ISRO Hackathon 2026")

# ============================================================
# Load Data
# ============================================================

data = load_data()
if not any(data.values()):
    data = generate_demo_data()

# ============================================================
# Main Content
# ============================================================

render_header()
render_navigation('dashboard')

st.title("🌍 Air Quality Dashboard - India")
st.markdown("*Satellite-based Surface AQI & HCHO Hotspot Analysis Platform*")

# ============================================================
# Metrics Row
# ============================================================

metrics = data.get("metrics", {})
if metrics:
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("RMSE", f"{metrics.get('rmse', 0):.2f} µg/m³", help="Root Mean Square Error")
    with col2:
        st.metric("MAE", f"{metrics.get('mae', 0):.2f} µg/m³", help="Mean Absolute Error")
    with col3:
        st.metric("R²", f"{metrics.get('r2', 0):.3f}", help="Coefficient of Determination")
    with col4:
        st.metric("MAPE", f"{metrics.get('mape', 0):.1f}%", help="Mean Absolute Percentage Error")

# ============================================================
# Tabs
# ============================================================

# --------------------------------------------------------------
# The interactive tabs (Map View, Model Performance, Biomass Burning) have been
# moved to their own page files under `dashboard/pages/`. The code block below
# is no longer needed and has been removed to avoid NameError for `tab1`, `tab2`,
# `tab3`.


# ============================================================
# Footer
# ============================================================

st.markdown("---")
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    st.caption("🌍 Built with ❤️ by Team Swachh Agam | ISRO Hackathon 2026")
    st.caption("📡 Data sources: Sentinel-5P · ERA5 · FIRMS · CPCB")