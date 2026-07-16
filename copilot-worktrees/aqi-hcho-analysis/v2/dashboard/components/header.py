"""
Header Component - Dashboard header with branding and status indicators
Swachh Agam - Satellite-based Air Quality Monitoring
"""

import streamlit as st
from datetime import datetime

def render_header():
    """Render dashboard header with branding and status"""
    col1, col2, col3, col4 = st.columns([2, 1.5, 0.5, 1], gap="medium")
    
    with col1:
        st.markdown("""
        <div style='display: flex; align-items: center; gap: 0.8rem;'>
            <h1 style='margin: 0; color: #0066CC; font-size: 2rem;'>🌍 Swachh Agam</h1>
            <div>
                <p style='margin: 0; color: #333; font-weight: 600;'>Air Quality Dashboard</p>
                <p style='margin: 0; color: #999; font-size: 0.85rem;'>ISRO Hackathon 2026</p>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        # Status indicator
        st.markdown("""
        <div style='background: #E8F5E9; border-left: 4px solid #4CAF50; padding: 0.5rem; border-radius: 4px;'>
            <p style='margin: 0; font-size: 0.85rem;'><b>System Status</b></p>
            <p style='margin: 0; color: #4CAF50; font-size: 0.8rem;'>● Operational</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        # Notification badge
        st.markdown("""
        <div style='text-align: center; font-size: 1.2rem;'>
            <span style='background: #FF5252; color: white; border-radius: 50%; width: 24px; height: 24px; display: inline-flex; align-items: center; justify-content: center; font-size: 0.7rem; font-weight: bold;'>2</span>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        col_a, col_b, col_c = st.columns(3, gap="small")
        with col_a:
            st.button("🔔", key="header_notifications", help="Notifications (2)", use_container_width=True)
        with col_b:
            st.button("📊", key="header_export", help="Export", use_container_width=True)
        with col_c:
            st.button("⚙️", key="header_settings", help="Settings", use_container_width=True)
    
    # Last updated timestamp
    st.markdown(f"""
    <div style='color: #999; font-size: 0.8rem; text-align: right; margin-top: 0.5rem;'>
        Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} IST
    </div>
    """, unsafe_allow_html=True)
    
    st.divider()
