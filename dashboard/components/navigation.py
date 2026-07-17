"""
Navigation Component - Premium horizontal navigation tabs for multi-page dashboard
"""

import streamlit as st

def render_navigation(active_page: str):
    """
    Render a premium horizontal navigation bar at the top of the dashboard pages.
    
    Args:
        active_page (str): Key of the current active page to apply active styling
    """
    pages = {
        'dashboard': {'label': '🏠 Dashboard', 'url': '/'},
        'map_view': {'label': '🗺️ Map View', 'url': '/Map_View'},
        'model_performance': {'label': '📊 Model Performance', 'url': '/Model_Performance'},
        'biomass_burning': {'label': '🔥 Biomass Burning', 'url': '/Biomass_Burning'},
        'export_share': {'label': '📥 Export & Share', 'url': '/Export_Share'},
        'alerts': {'label': '🔔 Alerts', 'url': '/Alerts'}
    }
    
    nav_html = "<div style='display: flex; gap: 8px; margin-bottom: 25px; overflow-x: auto; padding-bottom: 12px; border-bottom: 1px solid #E2E8F0;'>"
    
    for key, info in pages.items():
        is_active = (key == active_page)
        bg = "#0066CC" if is_active else "#FFFFFF"
        color = "#FFFFFF" if is_active else "#1F2328"
        border = "1px solid #005bb7" if is_active else "1px solid #E2E8F0"
        shadow = "box-shadow: 0 4px 6px -1px rgba(0, 102, 204, 0.12);" if is_active else "box-shadow: 0 1px 2px 0 rgba(0, 0, 0, 0.05);"
        
        # Single-line tag generation to prevent Streamlit's markdown parser from interpreting newlines as text
        nav_html += f"<a href='{info['url']}' target='_self' style='text-decoration: none; padding: 10px 20px; background-color: {bg}; color: {color}; border: {border}; border-radius: 8px; font-weight: 500; font-size: 14px; font-family: \"Inter\", sans-serif; transition: all 0.2s ease-in-out; white-space: nowrap; {shadow}'>{info['label']}</a>"
        
    nav_html += "</div>"
    
    # Strip any newlines to ensure it is parsed purely as HTML
    st.markdown(nav_html.replace('\n', ' '), unsafe_allow_html=True)
