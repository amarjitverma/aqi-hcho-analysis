"""
Help & Support Page - Documentation and User Guide
"""

import streamlit as st
import sys
from pathlib import Path

dashboard_path = Path(__file__).parent.parent
if str(dashboard_path) not in sys.path:
    sys.path.insert(0, str(dashboard_path))

from components.header import render_header
from components.navigation import render_navigation
render_header()
render_navigation('help_support')

st.title("❓ Help & Support")
st.markdown("User documentation, tutorials, and team support contacts.")

# Tabs for different help sections
tab1, tab2, tab3, tab4 = st.tabs(["📖 User Guide", "❓ FAQ", "🔧 Troubleshooting", "📞 Contact"])

with tab1:
    st.markdown("""
    ## User Guide
    
    ### Getting Started
    
    1. **Dashboard Home**: View key metrics (AQI, HCHO, Active Fires)
    2. **Map View**: Interactive map with layers and controls
    3. **Model Performance**: ML metrics and comparisons
    4. **Biomass Burning**: HCHO hotspot analysis
    5. **Export & Share**: Download and share data
    
    ### Understanding the Data
    
    **AQI (Air Quality Index)**
    - 0-50: Good (Green)
    - 51-100: Satisfactory (Yellow)
    - 101-200: Moderate (Orange)
    - 201-300: Poor (Red)
    - 301+: Very Poor/Hazardous (Purple/Dark Red)
    
    **HCHO (Formaldehyde)**
    - Measured in ppb (parts per billion)
    - Indicates biomass burning activity
    - Tracked through Sentinel-5P TROPOMI
    
    **Active Fires**
    - Detected by FIRMS/VIIRS satellites
    - Real-time monitoring
    - Correlation with HCHO concentration
    
    ### Tips & Tricks
    - 💡 Use the date selector to look at historical data
    - 💡 Toggle layers to focus on specific data
    - 💡 Click on the map for detailed location info
    - 💡 Export data for offline analysis
    """)

with tab2:
    st.markdown("""
    ## Frequently Asked Questions
    
    ### Data & Updates
    
    **Q: How often is the data updated?**
    A: Data is updated every 6 hours. Sentinel-5P data is refreshed daily, while FIRMS fire data updates every 4 hours.
    
    **Q: Is this real-time data?**
    A: Most data has a 6-24 hour latency due to satellite processing. FIRMS fire data is near real-time (4-6 hours).
    
    **Q: What is the geographic coverage?**
    A: Full global coverage for satellite data. Ground-truth CPCB data is limited to India.
    
    ### Models & Predictions
    
    **Q: Which model should I trust the most?**
    A: XGBoost shows the best performance (RMSE: 12.4 µg/m³, R²: 0.87).
    
    **Q: What does the lag in correlation mean?**
    A: A 2-day lag means HCHO concentration peaks 2 days after fire activity.
    
    **Q: Can I download the model predictions?**
    A: Yes, visit Export & Share page to download predictions in CSV format.
    
    ### Technical
    
    **Q: What browsers are supported?**
    A: Chrome, Firefox, Safari, Edge (latest versions recommended).
    
    **Q: Can I access this on mobile?**
    A: Yes, the dashboard is responsive. Some features may be simplified on small screens.
    """)

with tab3:
    st.markdown("""
    ## Troubleshooting
    
    ### Map Not Loading
    
    1. Clear browser cache (Ctrl+Shift+Delete)
    2. Disable browser extensions
    3. Try a different browser
    4. Check internet connection
    
    ### Data Not Updating
    
    1. Refresh page (F5)
    2. Clear session cache (browser cookies)
    3. Wait for next scheduled update (6-hour cycle)
    4. Contact support if issue persists
    
    ### Slow Performance
    
    1. Reduce date range selection
    2. Disable unnecessary layers
    3. Close other browser tabs
    4. Try different device with better specs
    
    ### Export Errors
    
    1. Check available disk space
    2. Try different export format
    3. Use Chrome if using other browsers
    4. Contact support for persistent issues
    """)

with tab4:
    st.markdown("""
    ## Get in Touch
    
    ### Support Channels
    
    **🐙 GitHub Issues**
    - Report bugs: https://github.com/amarjitverma/aqi-hcho-analysis/issues
    
    **📚 Project Resources**
    - Repository: https://github.com/amarjitverma/aqi-hcho-analysis
    - Documentation: https://github.com/amarjitverma/aqi-hcho-analysis/wiki
    
    ### Report an Issue
    """)
    
    if st.button("Report Issue on GitHub"):
        st.markdown("[Open Issue Form](https://github.com/amarjitverma/aqi-hcho-analysis/issues/new)")

# Footer
st.markdown("---")
st.caption("© 2026 AQI & HCHO Analysis")
