"""
Swachh Agam - Air Quality Dashboard
Main Streamlit Application Entry Point

Team: Swachh Agam (ISRO Hackathon 2026)
Built for: Satellite-based AQI Prediction & HCHO Hotspot Analysis
"""

import streamlit as st
import yaml
import os
from pathlib import Path
from datetime import datetime

# ============================================================
# Page Configuration
# ============================================================

st.set_page_config(
    page_title="Swachh Agam - Air Quality Dashboard",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        "Get Help": "https://github.com/amarjitverma/aqi-hcho-analysis",
        "Report a bug": "https://github.com/amarjitverma/aqi-hcho-analysis/issues",
        "About": "Team Swachh Agam - ISRO Hackathon 2026"
    }
)

# ============================================================
# Load Configuration
# ============================================================

@st.cache_resource
def load_config():
    """Load configuration from YAML file"""
    config_path = Path(__file__).parent / "config.yaml"
    try:
        with open(config_path, 'r') as f:
            return yaml.safe_load(f)
    except FileNotFoundError:
        st.error(f"Configuration file not found: {config_path}")
        return {}

config = load_config()

# ============================================================
# Theme & Styling
# ============================================================

st.markdown("""
<style>
    /* Header styling */
    .header-container {
        display: flex;
        align-items: center;
        justify-content: space-between;
        padding: 1.5rem 2rem;
        background: linear-gradient(135deg, #0066CC 0%, #0052A3 100%);
        color: white;
        border-radius: 10px;
        margin-bottom: 2rem;
    }
    
    .header-title {
        font-size: 2rem;
        font-weight: bold;
        margin: 0;
    }
    
    .header-subtitle {
        font-size: 0.9rem;
        opacity: 0.9;
        margin: 0;
    }
    
    /* Sidebar styling */
    .css-1d391kg {
        padding-top: 2rem;
    }
    
    /* Main content area */
    .main {
        padding: 2rem;
    }
    
    /* Metric card styling */
    .metric-card {
        background: white;
        padding: 1.5rem;
        border-radius: 10px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        border-left: 4px solid #0066CC;
    }
    
    /* Tab styling */
    .stTabs [data-baseweb="tab-list"] button {
        font-size: 1rem;
        padding: 0.5rem 1.5rem;
    }
    
    /* Button styling */
    .stButton > button {
        width: 100%;
        border-radius: 8px;
        border: 1px solid #ddd;
        padding: 0.75rem 1rem;
        background-color: white;
        color: #333;
        font-weight: 500;
        transition: all 0.3s ease;
    }
    
    .stButton > button:hover {
        background-color: #f0f0f0;
        border-color: #0066CC;
        color: #0066CC;
    }
</style>
""", unsafe_allow_html=True)

# ============================================================
# Initialize Session State
# ============================================================

if 'page' not in st.session_state:
    st.session_state.page = "dashboard"

if 'theme' not in st.session_state:
    st.session_state.theme = config.get('ui', {}).get('theme', 'light')

# ============================================================
# Header Component
# ============================================================

def render_header():
    """Render dashboard header with branding"""
    col1, col2, col3 = st.columns([2, 1, 1])
    
    with col1:
        st.markdown("""
        <div style='display: flex; align-items: center; gap: 1rem;'>
            <h1 style='margin: 0; color: #0066CC; font-size: 2rem;'>🌍 Swachh Agam</h1>
            <span style='color: #666; font-size: 1.1rem;'>Air Quality Dashboard</span>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.write("")
    
    with col3:
        # Right-aligned controls
        col_notif, col_settings = st.columns(2, gap="small")
        with col_notif:
            st.button("🔔", key="btn_notifications", help="Notifications", use_container_width=True)
        with col_settings:
            st.button("⚙️", key="btn_settings", help="Settings", use_container_width=True)
    
    st.divider()

# ============================================================
# Sidebar Navigation
# ============================================================

def render_sidebar():
    """Render sidebar navigation menu"""
    with st.sidebar:
        st.markdown("### 📍 Navigation")
        st.write("")
        
        pages = {
            "🏠 Dashboard": "dashboard",
            "🗺️ Map View": "map_view",
            "📊 Model Performance": "model_performance",
            "🔥 Biomass Burning": "biomass_burning",
            "📥 Export & Share": "export_share",
            "🔔 Alerts": "alerts",
            "📄 Reports": "reports",
            "🗂️ Data Sources": "data_sources",
            "⚙️ Admin Panel": "admin_panel",
            "❓ Help & Support": "help_support",
        }
        
        for page_name, page_key in pages.items():
            if st.button(
                page_name,
                key=f"nav_{page_key}",
                use_container_width=True,
            ):
                st.session_state.page = page_key
                st.rerun()
        
        st.divider()
        
        # Dashboard Info
        st.markdown("### 📊 Dashboard Info")
        st.markdown(f"""
        **Version**: {config.get('app', {}).get('version', 'N/A')}  
        **Team**: {config.get('app', {}).get('team', 'N/A')}  
        **Last Updated**: {datetime.now().strftime('%Y-%m-%d %H:%M')} IST
        """)
        
        st.markdown("### 📡 Data Sources")
        st.markdown("""
        - 🛰️ Sentinel-5P (TROPOMI)
        - 🌤️ ERA5
        - 🔥 FIRMS/VIIRS
        - 📊 CPCB
        - 🌐 OpenAQ
        """)

# ============================================================
# Page Loader
# ============================================================

def load_page(page_key):
    """Load page from pages/ directory"""
    pages_dir = Path(__file__).parent / "pages"
    
    # Map page keys to file names
    page_mapping = {
        "dashboard": "01_🏠_Dashboard.py",
        "map_view": "02_🗺️_Map_View.py",
        "model_performance": "03_📊_Model_Performance.py",
        "biomass_burning": "04_🔥_Biomass_Burning.py",
        "export_share": "05_📥_Export_Share.py",
        "alerts": "06_🔔_Alerts.py",
        "reports": "07_📄_Reports.py",
        "data_sources": "08_🗂️_Data_Sources.py",
        "admin_panel": "09_⚙️_Admin_Panel.py",
        "help_support": "10_❓_Help_Support.py",
    }
    
    page_file = page_mapping.get(page_key)
    
    if page_file:
        page_path = pages_dir / page_file
        if page_path.exists():
            with open(page_path, 'r', encoding='utf-8') as f:
                page_code = f.read()
                exec(page_code, {"__name__": "__main__", "st": st, "config": config})
        else:
            st.warning(f"📄 Page file not found: {page_file}")
            st.info("⏳ This page is under development. Please check back soon!")
    else:
        st.error("❌ Unknown page")

# ============================================================
# Main Application
# ============================================================

def main():
    """Main application entry point"""
    
    # Render header
    render_header()
    
    # Render sidebar
    render_sidebar()
    
    # Load and render selected page
    page_key = st.session_state.get('page', 'dashboard')
    
    try:
        load_page(page_key)
    except Exception as e:
        st.error(f"Error loading page: {str(e)}")
        st.info("Please try reloading the page or report this issue on GitHub.")

if __name__ == "__main__":
    main()
