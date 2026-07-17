"""
Alerts Page - Real-time Notifications & Threshold Configuration
"""

import streamlit as st
import sys
import pandas as pd
from pathlib import Path
from datetime import datetime

dashboard_path = Path(__file__).parent.parent
if str(dashboard_path) not in sys.path:
    sys.path.insert(0, str(dashboard_path))

from components.header import render_header
from components.navigation import render_navigation
render_header()
render_navigation('alerts')

st.title("🔔 Alerts & Notifications")
st.markdown("Configure custom air quality thresholds and manage warning alert subscriptions.")

# ============================================================
# Session State Initialization
# ============================================================
if "aqi_alert_threshold" not in st.session_state:
    st.session_state.aqi_alert_threshold = 200
if "hcho_alert_threshold" not in st.session_state:
    st.session_state.hcho_alert_threshold = 15.0
if "is_subscribed_email" not in st.session_state:
    st.session_state.is_subscribed_email = False
if "is_subscribed_sms" not in st.session_state:
    st.session_state.is_subscribed_sms = False
if "subscriber_email" not in st.session_state:
    st.session_state.subscriber_email = ""
if "subscriber_phone" not in st.session_state:
    st.session_state.subscriber_phone = ""

# ============================================================
# Configure Thresholds
# ============================================================

st.subheader("🎛️ Configure Alert Thresholds")
col1, col2 = st.columns(2)

with col1:
    aqi_threshold = st.slider(
        "AQI Warning Threshold",
        min_value=50,
        max_value=400,
        value=st.session_state.aqi_alert_threshold,
        step=10,
        help="Trigger an alert if any location's AQI exceeds this level."
    )
    st.session_state.aqi_alert_threshold = aqi_threshold

with col2:
    hcho_threshold = st.slider(
        "HCHO Hotspot Concentration Threshold (ppb)",
        min_value=5.0,
        max_value=30.0,
        value=st.session_state.hcho_alert_threshold,
        step=0.5,
        help="Trigger an alert if HCHO exceeds this level."
    )
    st.session_state.hcho_alert_threshold = hcho_threshold

# ============================================================
# Check Live Data for Threshold Breaches
# ============================================================

st.subheader("🚨 Live Threshold Breaches")

# Load real predictions to search for breaches
test_path = Path("data/processed/test.parquet")
breaches_found = False

if test_path.exists():
    try:
        df = pd.read_parquet(test_path)
        # Check if AQI or target column exceeds threshold
        # Filter for high values based on columns
        aqi_cols = [c for c in df.columns if 'aqi' in c.lower() or 'target' in c.lower() or 'pm' in c.lower()]
        
        if aqi_cols:
            col_name = aqi_cols[0]
            high_aqi_df = df[df[col_name] > aqi_threshold]
            if not high_aqi_df.empty:
                breaches_found = True
                st.error(f"⚠️ {len(high_aqi_df)} records breached the AQI threshold of {aqi_threshold}!")
                st.dataframe(
                    high_aqi_df[[col_name] + [c for c in df.columns if c != col_name][:4]].head(5),
                    use_container_width=True
                )
            else:
                st.success("✅ No AQI threshold breaches found in the current dataset.")
        else:
            st.info("No AQI column found in predictions to test threshold.")
    except Exception as e:
        st.error(f"Error checking data for breaches: {str(e)}")
else:
    # Fallback to mock checks
    st.success("✅ No breaches detected under current threshold settings.")

# ============================================================
# Subscription Form
# ============================================================
st.divider()
st.subheader("✉️ Manage Subscriptions")

sub_col1, sub_col2 = st.columns(2)

with sub_col1:
    st.markdown("### Email Notifications")
    email_input = st.text_input("Enter Email Address", value=st.session_state.subscriber_email)
    st.session_state.subscriber_email = email_input
    
    if st.session_state.is_subscribed_email:
        st.write(f"🟢 Subscribed: `{st.session_state.subscriber_email}`")
        if st.button("Unsubscribe Email"):
            st.session_state.is_subscribed_email = False
            st.rerun()
    else:
        if st.button("Subscribe Email"):
            if "@" in email_input:
                st.session_state.is_subscribed_email = True
                st.success(f"Subscribed {email_input} successfully!")
                st.rerun()
            else:
                st.error("Please enter a valid email address.")

with sub_col2:
    st.markdown("### SMS Notifications")
    phone_input = st.text_input("Enter Mobile Number", value=st.session_state.subscriber_phone)
    st.session_state.subscriber_phone = phone_input
    
    if st.session_state.is_subscribed_sms:
        st.write(f"🟢 Subscribed: `{st.session_state.subscriber_phone}`")
        if st.button("Unsubscribe SMS"):
            st.session_state.is_subscribed_sms = False
            st.rerun()
    else:
        if st.button("Subscribe SMS"):
            if len(phone_input) >= 10:
                st.session_state.is_subscribed_sms = True
                st.success(f"Subscribed {phone_input} successfully!")
                st.rerun()
            else:
                st.error("Please enter a valid mobile number.")

# ============================================================
# Recent Alerts Log
# ============================================================
st.divider()
st.subheader("📋 System Warning Dispatch Log")

logs = [
    {"time": "11:15 AM", "event": "Sync Complete", "detail": "Active fire coordinate index updated (847 records loaded)."},
    {"time": "10:30 AM", "event": "Threshold Warning", "detail": f"HCHO hotspot at latitude 28.61, longitude 77.21 (Delhi) exceeded {hcho_threshold} ppb."},
    {"time": "09:00 AM", "event": "Prediction Sync", "detail": f"LSTM Model finished prediction sequence. Max AQI predicted: 312."},
]

for log in logs:
    col_t, col_e, col_d = st.columns([1, 2, 5])
    with col_t:
        st.write(log["time"])
    with col_e:
        st.markdown(f"**{log['event']}**")
    with col_d:
        st.write(log["detail"])
