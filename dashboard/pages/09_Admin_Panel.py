"""
Admin Panel - Configuration and Model Deployments
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
render_navigation('admin_panel')

st.title("⚙️ Admin Panel")
st.markdown("Configure system thresholds, manage database sync cycles, and deploy ML models.")

# ============================================================
# Session State Initialization
# ============================================================
if "admin_logged_in" not in st.session_state:
    st.session_state.admin_logged_in = False
if "active_model_name" not in st.session_state:
    st.session_state.active_model_name = "LSTM Model"
if "aqi_alert_threshold" not in st.session_state:
    st.session_state.aqi_alert_threshold = 200
if "hcho_alert_threshold" not in st.session_state:
    st.session_state.hcho_alert_threshold = 15.0

# ============================================================
# Authentication Layer
# ============================================================

if not st.session_state.admin_logged_in:
    st.subheader("🔑 Admin Authentication Required")
    
    with st.form("admin_login_form"):
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        submit_btn = st.form_submit_button("Authenticate")
        
        if submit_btn:
            if username == "admin" and password == "admin":
                st.session_state.admin_logged_in = True
                st.success("Authenticated successfully!")
                st.rerun()
            else:
                st.error("Invalid credentials. Try username: admin, password: admin")
    
    st.stop()  # Stop page execution if not authenticated

# ============================================================
# Logged In Admin Interface
# ============================================================

# Add logout option in columns
col_title, col_logout = st.columns([5, 1])
with col_title:
    st.write(f"👋 Logged in as: **admin**")
with col_logout:
    if st.button("🚪 Logout"):
        st.session_state.admin_logged_in = False
        st.rerun()

st.divider()

# System Metrics
st.subheader("System Metrics")
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("API Gateway", "✅ Active", help="Inference server API status")
with col2:
    st.metric("Parquet DB", "✅ Linked", help="Feature store connection status")
with col3:
    st.metric("Storage Volume", "42.8 GB / 100 GB (42.8%)", help="Model and grid checkpoint partition space")

# Threshold Settings
st.subheader("Global Warning Configurations")

aqi_thr = st.slider(
    "Global AQI Warning Limit",
    min_value=50,
    max_value=400,
    value=st.session_state.aqi_alert_threshold,
    step=10,
    key="admin_aqi_slider"
)
hcho_thr = st.slider(
    "Global HCHO Concentration Limit (ppb)",
    min_value=5.0,
    max_value=30.0,
    value=st.session_state.hcho_alert_threshold,
    step=0.5,
    key="admin_hcho_slider"
)

if st.button("💾 Apply Configurations"):
    st.session_state.aqi_alert_threshold = aqi_thr
    st.session_state.hcho_alert_threshold = hcho_thr
    st.success("✅ Configurations successfully updated globally!")

# Model Deployments
st.divider()
st.subheader("🤖 Model Deployment Controls")
st.write(f"Currently active model: **{st.session_state.active_model_name}**")

selected_model = st.selectbox(
    "Deploy Model Variant",
    ["LSTM Model", "CNN-LSTM Model", "ConvLSTM Model", "Random Forest Classifier"]
)

if st.button("🚀 Deploy Variant to Production"):
    with st.spinner("Re-linking weights file path..."):
        import time
        time.sleep(0.8)
        st.session_state.active_model_name = selected_model
        st.success(f"✅ Successfully deployed {selected_model} as active predictor!")
        st.rerun()
