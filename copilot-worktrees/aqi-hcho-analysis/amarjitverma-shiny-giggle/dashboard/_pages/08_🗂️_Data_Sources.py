"""
Data Sources Page - Data Source Management
"""

import streamlit as st
from datetime import datetime, timedelta

st.title("🗂️ Data Sources")
st.markdown("---")

st.markdown("""
## Data Source Management and Status

Monitor and manage all data sources feeding the dashboard.

**Data Sources:**
- 🛰️ **Sentinel-5P (TROPOMI)**: NO₂, SO₂, CO, O₃, HCHO
- 🌤️ **ERA5**: Temperature, wind, humidity
- 🔥 **FIRMS/VIIRS**: Active fires
- 📊 **CPCB**: Ground PM2.5 measurements
- 🌐 **OpenAQ**: Air quality data

**Status**: 🔨 Under Development (Phase 6)
""")

st.info("📋 Full implementation coming in Phase 6 (Days 14-15)")

# Data source status table
st.subheader("Data Source Status")

data_sources = [
    {"source": "🛰️ Sentinel-5P", "status": "✅ Active", "last_sync": "2 hrs ago", "coverage": "Global", "update_freq": "1 day"},
    {"source": "🌤️ ERA5", "status": "✅ Active", "last_sync": "1 hr ago", "coverage": "Global", "update_freq": "6 hours"},
    {"source": "🔥 FIRMS", "status": "✅ Active", "last_sync": "30 mins ago", "coverage": "Global", "update_freq": "4 hours"},
    {"source": "📊 CPCB", "status": "✅ Active", "last_sync": "4 hrs ago", "coverage": "India", "update_freq": "3 hours"},
    {"source": "🌐 OpenAQ", "status": "✅ Active", "last_sync": "1 hr ago", "coverage": "Global", "update_freq": "1 hour"},
]

for source in data_sources:
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.write(source["source"])
    with col2:
        st.write(source["status"])
    with col3:
        st.write(f"_{source['last_sync']}_")
    with col4:
        st.write(source["coverage"])
    with col5:
        st.write(source["update_freq"])
    st.divider()

# Coverage map
st.subheader("Data Coverage Map")
st.info("🗺️ Data coverage visualization will appear here")

# Download raw data
st.subheader("Download Raw Data")
st.markdown("""
Download raw data from any source for further analysis.
""")

col1, col2 = st.columns(2)

with col1:
    source = st.selectbox("Select Data Source", ["Sentinel-5P", "ERA5", "FIRMS", "CPCB", "OpenAQ"])

with col2:
    date_range = st.date_input("Date Range", [datetime.now() - timedelta(days=7), datetime.now()])

if st.button("Download Data"):
    st.success(f"Downloading {source} data...")
