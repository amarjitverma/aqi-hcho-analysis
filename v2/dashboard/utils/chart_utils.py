"""
Chart Utilities - Helper functions for chart creation
"""

import plotly.graph_objects as go
import plotly.express as px
import pandas as pd

def format_number(value, decimals=2):
    """Format number for display"""
    return f"{value:.{decimals}f}"

def get_aqi_color(aqi_value):
    """Get color based on AQI value"""
    if aqi_value <= 50:
        return "#2ECC71"  # Good
    elif aqi_value <= 100:
        return "#F39C12"  # Satisfactory
    elif aqi_value <= 200:
        return "#E67E22"  # Moderate
    elif aqi_value <= 300:
        return "#E74C3C"  # Poor
    else:
        return "#8E44AD"  # Very Poor/Hazardous

def get_aqi_label(aqi_value):
    """Get AQI category label"""
    if aqi_value <= 50:
        return "Good"
    elif aqi_value <= 100:
        return "Satisfactory"
    elif aqi_value <= 200:
        return "Moderate"
    elif aqi_value <= 300:
        return "Poor"
    else:
        return "Very Poor/Hazardous"

def add_gridlines(fig):
    """Add gridlines to figure"""
    fig.update_xaxes(showgrid=True, gridwidth=1, gridcolor='lightgray')
    fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor='lightgray')
    return fig

def apply_dashboard_theme(fig):
    """Apply dashboard theme to Plotly figure"""
    fig.update_layout(
        plot_bgcolor='white',
        paper_bgcolor='white',
        font=dict(family="Open Sans, sans-serif", size=12),
        margin=dict(l=50, r=50, t=50, b=50)
    )
    return fig
