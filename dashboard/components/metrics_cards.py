"""
Metrics Cards Component - KPI card displays with data visualization
"""

import streamlit as st
from utils.chart_utils import get_aqi_color, get_aqi_label

def render_metric_card(title, value, delta=None, icon="", help_text="", delta_color="off"):
    """Render a single metric card with enhanced styling
    
    Args:
        title: Card title
        value: Main value to display
        delta: Change indicator (optional)
        icon: Emoji icon (optional)
        help_text: Help tooltip text (optional)
        delta_color: Color for delta ("off", "normal", "inverse", "off")
    """
    col1, col2 = st.columns([1, 4])
    
    with col1:
        st.markdown(f"<h2 style='text-align: center;'>{icon}</h2>", unsafe_allow_html=True)
    
    with col2:
        st.metric(label=title, value=value, delta=delta, help=help_text)

def render_metrics_row(metrics):
    """Render a row of metric cards
    
    Args:
        metrics: List of dicts with keys 'title', 'value', 'delta', 'icon', 'help'
    
    Example:
        metrics = [
            {'title': 'AQI Today', 'value': '156', 'delta': 'Poor', 'icon': '🌡️', 'help': 'Air Quality Index'},
            {'title': 'HCHO Avg', 'value': '12.4 ppb', 'delta': '+1.2', 'icon': '🧪', 'help': 'Formaldehyde'},
            {'title': 'Active Fires', 'value': '847', 'delta': '+12 today', 'icon': '🔥', 'help': 'Fire detections'}
        ]
        render_metrics_row(metrics)
    """
    cols = st.columns(len(metrics))
    
    for col, metric in zip(cols, metrics):
        with col:
            st.metric(
                label=metric.get('title', ''),
                value=metric.get('value', ''),
                delta=metric.get('delta', None),
                help=metric.get('help', '')
            )

def render_status_card(title, status, description, icon=""):
    """Render a status card with color-coded indicator and matching pastel background
    
    Args:
        title: Card title
        status: Status text (Good, Poor, Hazardous, etc.)
        description: Description text
        icon: Emoji icon
    """
    status_themes = {
        'Good': {'color': '#2E7D32', 'bg': '#EEF9F0'},
        'Satisfactory': {'color': '#B78103', 'bg': '#FFF8E1'},
        'Moderate': {'color': '#A04E00', 'bg': '#FFF3E0'},
        'Poor': {'color': '#A82216', 'bg': '#FADBD8'},
        'Very Poor': {'color': '#5E2D87', 'bg': '#F3E5F5'},
        'Hazardous': {'color': '#801D13', 'bg': '#FFEBEE'},
        'Operational': {'color': '#2E7D32', 'bg': '#E8F5E9'},
        'Warning': {'color': '#A04E00', 'bg': '#FFF3E0'},
        'Critical': {'color': '#B71C1C', 'bg': '#FFEBEE'}
    }
    
    theme = status_themes.get(status, {'color': '#57606A', 'bg': '#F6F8FA'})
    color = theme['color']
    bg_color = theme['bg']
    
    st.markdown(f"""
    <div style='
        background: {bg_color};
        border-left: 4px solid {color};
        padding: 1rem;
        border-radius: 6px;
        box-shadow: 0 1px 3px rgba(0,0,0,0.05);
    '>
        <h4 style='margin: 0; color: #1F2328;'>{icon} {title}</h4>
        <p style='margin: 0.5rem 0 0 0; color: {color}; font-weight: bold; font-size: 1.1rem;'>{status}</p>
        <p style='margin: 0.3rem 0 0 0; color: #57606A; font-size: 0.85rem;'>{description}</p>
    </div>
    """, unsafe_allow_html=True)
