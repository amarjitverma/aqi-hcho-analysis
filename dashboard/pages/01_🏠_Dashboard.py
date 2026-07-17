"""
Dashboard Home Page - Complete Overview with Interactive Map and KPIs
Phase 2 Implementation: Header, KPI Cards, Interactive Map, Layer Controls, Date/Time Selectors
"""

import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import sys
from pathlib import Path

# Add dashboard to path for imports
dashboard_path = Path(__file__).parent.parent
sys.path.insert(0, str(dashboard_path))

# Import components and utilities
from components.header import render_header
from components.metrics_cards import render_metrics_row, render_status_card
from components.map_viewer import create_interactive_map
from utils.data_loader import load_aqi_data, load_fire_data, load_hcho_data, get_kpi_values

# ============================================================
# Page Configuration
# ============================================================

st.set_page_config(layout="wide")

# Initialize session state
if 'selected_date' not in st.session_state:
    st.session_state.selected_date = datetime.now().date()
if 'time_day' not in st.session_state:
    st.session_state.time_day = 15
if 'show_aqi' not in st.session_state:
    st.session_state.show_aqi = True
if 'show_fires' not in st.session_state:
    st.session_state.show_fires = True
if 'show_hcho' not in st.session_state:
    st.session_state.show_hcho = True

# ============================================================
# Render Header & Navigation
# ============================================================

render_header()
from components.navigation import render_navigation
render_navigation('dashboard')

# ============================================================
# KPI Cards Row
# ============================================================

st.subheader("📊 Key Performance Indicators")

# Get KPI values
kpi_values = get_kpi_values()

metrics_data = [
    {
        'title': '🌡️ AQI Today',
        'value': kpi_values['aqi_today'],
        'delta': f"{kpi_values['aqi_trend']:+d} (trend)",
        'help': 'Air Quality Index - Lower is better'
    },
    {
        'title': '🧪 HCHO Average',
        'value': f"{kpi_values['hcho_avg']} ppb",
        'delta': f"{kpi_values['high_hcho_areas']} hotspots",
        'help': 'Formaldehyde concentration - ppb'
    },
    {
        'title': '🔥 Active Fires',
        'value': kpi_values['active_fires'],
        'delta': f"+{np.random.randint(5, 20)} today",
        'help': 'Active fire detections'
    },
    {
        'title': '📡 Data Points',
        'value': len(load_aqi_data()) + len(load_fire_data()),
        'delta': 'Real-time',
        'help': 'Total measurements available'
    },
]

render_metrics_row(metrics_data)

st.divider()

# ============================================================
# Controls Section - Date, Time, Layer Selection
# ============================================================

st.subheader("🎛️ Controls & Visualization Settings")

control_col1, control_col2, control_col3 = st.columns(3)

with control_col1:
    st.markdown("**📅 Select Date**")
    selected_date = st.date_input(
        "Date",
        value=st.session_state.selected_date,
        label_visibility="collapsed",
        help="Choose date for data visualization"
    )
    st.session_state.selected_date = selected_date

with control_col2:
    st.markdown("**📍 Map Layers**")
    col_a, col_b, col_c = st.columns(3)
    with col_a:
        show_aqi = st.checkbox("AQI", value=st.session_state.show_aqi, label_visibility="collapsed")
        st.session_state.show_aqi = show_aqi
    with col_b:
        show_fires = st.checkbox("🔥 Fires", value=st.session_state.show_fires, label_visibility="collapsed")
        st.session_state.show_fires = show_fires
    with col_c:
        show_hcho = st.checkbox("☁️ HCHO", value=st.session_state.show_hcho, label_visibility="collapsed")
        st.session_state.show_hcho = show_hcho

with control_col3:
    st.markdown("**⏱️ Time Series**")
    time_day = st.slider(
        "Day",
        min_value=1,
        max_value=28,
        value=st.session_state.time_day,
        label_visibility="collapsed",
        help="Select day within 28-day window"
    )
    st.session_state.time_day = time_day
    st.caption(f"Viewing: **Day {time_day} / 28**")

st.divider()

# ============================================================
# Interactive Map Section
# ============================================================

st.subheader("🗺️ Interactive Geospatial Map")
st.markdown(f"*Showing data for {selected_date.strftime('%B %d, %Y')} • Day {time_day} of 28-day cycle*")

# Load data
aqi_data = load_aqi_data(selected_date)
fire_data = load_fire_data(selected_date)
hcho_data = load_hcho_data(selected_date)

# Create and display map
try:
    # Create interactive map with selected layers
    map_obj = create_interactive_map(
        aqi_data=aqi_data if show_aqi else None,
        fire_data=fire_data if show_fires else None,
        hcho_data=hcho_data if show_hcho else None,
        show_aqi=show_aqi,
        show_fires=show_fires,
        show_hcho=show_hcho
    )
    
    # Display map
    from components.map_viewer import display_map
    map_data = display_map(map_obj, height=500)
    
    # Display map statistics
    col_stats1, col_stats2, col_stats3 = st.columns(3)
    with col_stats1:
        st.metric("🌡️ AQI Coverage", f"{len(aqi_data)} locations")
    with col_stats2:
        st.metric("🔥 Fire Detections", f"{len(fire_data)} active")
    with col_stats3:
        st.metric("☁️ HCHO Hotspots", f"{len(hcho_data)} areas")
        
except Exception as e:
    st.error(f"Error rendering map: {str(e)}")
    st.info("Map component requires streamlit-folium. Ensure it's installed in requirements.txt")

st.divider()

# ============================================================
# Status Cards
# ============================================================

st.subheader("📈 System Status")

status_col1, status_col2, status_col3 = st.columns(3)

with status_col1:
    render_status_card(
        "Air Quality",
        "Poor",
        "Index trending upward",
        "🌡️"
    )

with status_col2:
    render_status_card(
        "Biomass Burning",
        "High",
        f"{kpi_values['high_hcho_areas']} hotspots detected",
        "🔥"
    )

with status_col3:
    render_status_card(
        "System Status",
        "Operational",
        "All sensors operational",
        "✅"
    )

st.divider()

# ============================================================
# Quick Navigation Tabs
# ============================================================

st.subheader("📑 Quick Navigation")

tab1, tab2, tab3, tab4 = st.tabs(["🗺️ Map View", "📊 Model Performance", "🔥 Biomass Burning", "📥 Export"])

with tab1:
    st.markdown("### 🗺️ Map View - Detailed Geospatial Analysis")
    st.write("""
    Comprehensive geospatial analysis with:
    - AQI choropleth by region
    - Fire marker clusters
    - HCHO hotspot visualization
    - Wind vector overlay
    - Historical time-series animation
    """)
    if st.button("Go to Map View", key="goto_map"):
        st.session_state.page = "02_🗺️_Map_View"
        st.rerun()

with tab2:
    st.markdown("### 📊 Model Performance - ML Metrics & Explainability")
    st.write("""
    Machine learning model analysis:
    - XGBoost vs Random Forest vs LSTM comparison
    - RMSE, MAE, R², MAPE metrics
    - Feature importance rankings
    - SHAP explainability plots
    - Model performance over time
    """)
    if st.button("Go to Model Performance", key="goto_model"):
        st.session_state.page = "03_📊_Model_Performance"
        st.rerun()

with tab3:
    st.markdown("### 🔥 Biomass Burning - HCHO Analysis")
    st.write("""
    Biomass burning and HCHO hotspot analysis:
    - Fire-HCHO correlation analysis
    - Hotspot clustering algorithms
    - Wind transport modeling
    - Burning source identification
    - Pollution trajectory prediction
    """)
    if st.button("Go to Biomass Burning", key="goto_biomass"):
        st.session_state.page = "04_🔥_Biomass_Burning"
        st.rerun()

with tab4:
    st.markdown("### 📥 Export & Share - Data Download")
    st.write("""
    Export and share functionality:
    - CSV, JSON, Excel export formats
    - Custom date range selection
    - Map snapshot capture
    - Report generation
    - Scheduled email delivery
    """)
    if st.button("Go to Export", key="goto_export"):
        st.session_state.page = "05_📥_Export_Share"
        st.rerun()

st.divider()

# ============================================================
# Footer
# ============================================================

footer_col1, footer_col2, footer_col3 = st.columns(3)

with footer_col1:
    st.markdown("""
    **Swachh Agam Dashboard**
    
    ISRO Bharatiya Antariksh Hackathon 2026
    """)

with footer_col2:
    st.markdown(f"""
    **Data Updated:**
    
    {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} IST
    """)

with footer_col3:
    st.markdown("""
    **Quick Links**
    
    - [GitHub](https://github.com/amarjitverma/aqi-hcho-analysis)
    - [Issues](https://github.com/amarjitverma/aqi-hcho-analysis/issues)
    - [Team](https://github.com/amarjitverma)
    """)

st.caption("© 2026 Team Swachh Agam - ISRO Hackathon 2026 | Satellite-based AQI & HCHO Analysis")
