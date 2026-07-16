"""
Alerts Page - Real-time Notifications
"""

import streamlit as st
from datetime import datetime, timedelta

st.title("🔔 Alerts")
st.markdown("---")

st.markdown("""
## Real-time Alert System

Monitor critical AQI, fire activity, and model notifications.

**Alert Types:**
- 🔴 **Critical**: AQI > 300 (Very Poor/Hazardous)
- 🟡 **Warning**: AQI 200-300, Fire spike, Model degradation
- 🟢 **Info**: Regular updates, model deployments
- ✅ **Success**: Data download complete

**Status**: 🔨 Under Development (Phase 6)
""")

st.info("📋 Full implementation coming in Phase 6 (Days 14-15)")

# Sample alerts
st.subheader("Recent Alerts")

# Create sample alert data
alerts_data = [
    {"type": "🔴 Critical", "message": "AQI crossed 300 in Delhi", "time": "2 mins ago", "status": "Active"},
    {"type": "🟡 Warning", "message": "847 active fires detected in IGP region", "time": "15 mins ago", "status": "Active"},
    {"type": "🟢 Info", "message": "Model updated successfully", "time": "1 hour ago", "status": "Resolved"},
    {"type": "✅ Success", "message": "Daily report generated", "time": "2 hours ago", "status": "Completed"},
]

for alert in alerts_data:
    col1, col2, col3, col4 = st.columns([1, 3, 1, 1])
    with col1:
        st.write(alert["type"])
    with col2:
        st.write(alert["message"])
    with col3:
        st.write(f"__{alert['time']}__")
    with col4:
        st.write(f"_{alert['status']}_")
    st.divider()

# Alert settings placeholder
st.subheader("Alert Settings")
st.markdown("""
- ✅ AQI Alerts
- ✅ Fire Alerts
- ✅ Model Alerts
- ⬜ Email Notifications (Coming Soon)
- ⬜ SMS Notifications (Coming Soon)
""")

st.warning("Full alert customization will be available soon!")
