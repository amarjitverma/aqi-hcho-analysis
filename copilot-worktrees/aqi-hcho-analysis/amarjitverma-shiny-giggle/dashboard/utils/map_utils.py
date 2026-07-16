"""
Map Utilities - Helper functions for map operations
"""

import folium
import streamlit as st
import pandas as pd

def create_choropleth_layer(geojson_data, data, key_on, fill_color="YlOrRd", name="Choropleth"):
    """Create a choropleth layer for Folium map"""
    # Placeholder implementation
    pass

def add_markers(map_obj, data, lat_col, lon_col, popup_col=None, color="red"):
    """Add markers to map"""
    for idx, row in data.iterrows():
        folium.CircleMarker(
            location=[row[lat_col], row[lon_col]],
            radius=5,
            popup=popup_col and row[popup_col],
            color=color,
            fill=True,
            fillColor=color,
            fillOpacity=0.7
        ).add_to(map_obj)
    return map_obj

def add_heatmap_layer(map_obj, data, lat_col, lon_col, weight_col):
    """Add heatmap layer to map"""
    from folium.plugins import HeatMap
    heat_data = [[row[lat_col], row[lon_col], row[weight_col]] 
                 for idx, row in data.iterrows()]
    HeatMap(heat_data).add_to(map_obj)
    return map_obj

def create_aqi_legend():
    """Create AQI legend HTML"""
    legend_html = '''
    <div style="position: fixed; 
                bottom: 50px; right: 50px; width: 200px; height: 300px; 
                background-color: white; border:2px solid grey; z-index:9999; 
                font-size:14px; padding: 10px">
    <b>AQI Categories</b><br>
    <i style="background:#2ECC71"></i> Good (0-50)<br>
    <i style="background:#F39C12"></i> Satisfactory (51-100)<br>
    <i style="background:#E67E22"></i> Moderate (101-200)<br>
    <i style="background:#E74C3C"></i> Poor (201-300)<br>
    <i style="background:#8E44AD"></i> Very Poor (301+)<br>
    </div>
    '''
    return legend_html
