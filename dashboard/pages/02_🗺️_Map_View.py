# ============================================================
# Dashboard Page: Map View
# ============================================================

"""Interactive map view page for the dashboard."""

import streamlit as st
import folium
from streamlit_folium import st_folium
import json
from pathlib import Path


def render():
    """Render the Map View page."""
    st.header("🗺️ Interactive Map View")
    st.caption("Explore air quality data across India")
    
    # Layer controls
    col1, col2 = st.columns([1, 3])
    
    with col1:
        st.subheader("Layer Controls")
        show_hcho = st.checkbox("HCHO Hotspots", value=True)
        show_fire = st.checkbox("Active Fires", value=False)
        show_boundary = st.checkbox("India Boundary", value=True)
    
    with col2:
        # Create map
        m = folium.Map(
            location=[20.5937, 78.9629],
            zoom_start=5,
            tiles="CartoDB dark_matter",
            control_scale=True
        )
        
        # Add India boundary
        if show_boundary:
            try:
                import geopandas as gpd
                gdf = gpd.read_file('data/external/boundaries/india_boundary.geojson')
                folium.GeoJson(
                    gdf,
                    style_function=lambda x: {
                        'fillColor': 'none',
                        'color': '#58A6FF',
                        'weight': 2,
                        'opacity': 0.5
                    }
                ).add_to(m)
            except:
                pass
        
        # Load and add HCHO hotspots
        if show_hcho:
            try:
                with open('dashboard/cache/hcho_hotspots.geojson', 'r') as f:
                    hcho_data = json.load(f)
                for feature in hcho_data.get('features', []):
                    coords = feature['geometry']['coordinates']
                    props = feature['properties']
                    folium.CircleMarker(
                        location=[coords[1], coords[0]],
                        radius=props.get('radius', 5),
                        popup=f"""
                        <b>Cluster {props.get('cluster_id', 'Unknown')}</b><br>
                        Cells: {props.get('num_cells', 0)}<br>
                        HCHO: {props.get('mean_hcho', 0):.4f} mol/m²
                        """,
                        color=props.get('color', '#FF6B35'),
                        fill=True,
                        fill_color=props.get('color', '#FF6B35'),
                        fill_opacity=0.7
                    ).add_to(m)
            except:
                pass
        
        # Display map
        st_folium(m, width=700, height=550)
        
        # Map info
        st.caption("🟢 Click on markers for more information")


if __name__ == "__main__":
    render()
