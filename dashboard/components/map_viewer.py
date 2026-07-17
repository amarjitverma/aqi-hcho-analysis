"""
Map Viewer Component - Interactive Folium map with layers for AQI, HCHO, and fires
"""

import streamlit as st
import folium
from streamlit_folium import st_folium
import pandas as pd
import numpy as np
from datetime import datetime

def create_base_map(center_lat=23.1815, center_lon=79.9864, zoom=5):
    """Create base Folium map centered on India
    
    Args:
        center_lat: Center latitude (default: India center ~23.1815°N)
        center_lon: Center longitude (default: India center ~79.9864°E)
        zoom: Initial zoom level (5 shows full India)
    
    Returns:
        folium.Map object
    """
    map_obj = folium.Map(
        location=[center_lat, center_lon],
        zoom_start=zoom,
        tiles="OpenStreetMap",
        prefer_canvas=True
    )
    
    return map_obj

def add_aqi_heatmap(map_obj, aqi_data):
    """Add AQI choropleth layer to map
    
    Args:
        map_obj: Folium map object
        aqi_data: DataFrame with columns ['lat', 'lon', 'aqi', 'state']
    """
    from folium.plugins import HeatMap
    
    if aqi_data is not None and len(aqi_data) > 0:
        # Prepare heat data
        heat_data = aqi_data[['lat', 'lon', 'aqi']].values.tolist()
        
        # Add heatmap layer
        HeatMap(
            heat_data,
            name="AQI Heatmap",
            min_opacity=0.2,
            radius=15,
            blur=15,
            max_zoom=1
        ).add_to(map_obj)
    
    return map_obj

def add_fire_markers(map_obj, fire_data):
    """Add fire markers to map
    
    Args:
        map_obj: Folium map object
        fire_data: DataFrame with columns ['lat', 'lon', 'intensity', 'detected_time']
    """
    if fire_data is not None and len(fire_data) > 0:
        # Create feature group for fires
        fire_group = folium.FeatureGroup(name="🔥 Active Fires", show=True)
        
        for idx, row in fire_data.iterrows():
            intensity = row['intensity']
            if intensity > 80:
                color = '#B91C1C'  # Dark Red
            elif intensity > 50:
                color = '#EF4444'  # Crimson Red
            else:
                color = '#F97316'  # Orange
            
            # Add circle marker
            folium.CircleMarker(
                location=[row['lat'], row['lon']],
                radius=5,
                popup=f"<b>Fire Detected</b><br>Intensity: {intensity}%<br>Time: {row['detected_time']}",
                color=color,
                fill=True,
                fillColor=color,
                fillOpacity=0.7,
                weight=2
            ).add_to(fire_group)
        
        fire_group.add_to(map_obj)
    
    return map_obj

def add_hcho_markers(map_obj, hcho_data):
    """Add HCHO hotspot markers to map
    
    Args:
        map_obj: Folium map object
        hcho_data: DataFrame with columns ['lat', 'lon', 'concentration', 'status']
    """
    if hcho_data is not None and len(hcho_data) > 0:
        # Create feature group for HCHO
        hcho_group = folium.FeatureGroup(name="☁️ HCHO Hotspots", show=True)
        
        for idx, row in hcho_data.iterrows():
            conc = row['concentration']
            if conc > 15:
                color = '#6D28D9'  # Deep Purple - High
                status = 'High'
            elif conc > 10:
                color = '#F59E0B'  # Amber Yellow - Medium
                status = 'Medium'
            else:
                color = '#A78BFA'  # Light Purple - Low
                status = 'Low'
            
            # Add marker
            folium.CircleMarker(
                location=[row['lat'], row['lon']],
                radius=4,
                popup=f"<b>HCHO Hotspot</b><br>Concentration: {conc:.1f} ppb<br>Status: {status}",
                color=color,
                fill=True,
                fillColor=color,
                fillOpacity=0.6,
                weight=1
            ).add_to(hcho_group)
        
        hcho_group.add_to(map_obj)
    
    return map_obj

def add_layer_control(map_obj):
    """Add layer control to map"""
    folium.LayerControl(
        position='topright',
        collapsed=False,
        draggable=True
    ).add_to(map_obj)
    
    return map_obj

def display_map(map_obj, height=500):
    """Display Folium map in Streamlit
    
    Args:
        map_obj: Folium map object
        height: Map height in pixels
    
    Returns:
        Click data from st_folium
    """
    map_data = st_folium(map_obj, use_container_width=True, height=height)
    return map_data

def create_interactive_map(aqi_data=None, fire_data=None, hcho_data=None, 
                          show_aqi=True, show_fires=True, show_hcho=True):
    """Create complete interactive map with all layers
    
    Args:
        aqi_data: AQI data (DataFrame)
        fire_data: Fire data (DataFrame)
        hcho_data: HCHO data (DataFrame)
        show_aqi: Show AQI layer
        show_fires: Show fire markers
        show_hcho: Show HCHO hotspots
    
    Returns:
        Folium map object
    """
    # Create base map
    map_obj = create_base_map()
    
    # Add layers based on flags
    if show_aqi and aqi_data is not None:
        map_obj = add_aqi_heatmap(map_obj, aqi_data)
    
    if show_fires and fire_data is not None:
        map_obj = add_fire_markers(map_obj, fire_data)
    
    if show_hcho and hcho_data is not None:
        map_obj = add_hcho_markers(map_obj, hcho_data)
    
    # Add layer control
    map_obj = add_layer_control(map_obj)
    
    return map_obj
