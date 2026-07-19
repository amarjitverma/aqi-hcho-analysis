# ============================================================
# Map Visualization
# ============================================================

"""Interactive map generation using Folium."""

import folium
import json
import numpy as np
from pathlib import Path
from loguru import logger


def create_india_map(location=[20.5937, 78.9629], zoom_start=5, tiles="CartoDB dark_matter"):
    """
    Create a base map of India.

    Args:
        location (list): Map center [lat, lon]
        zoom_start (int): Initial zoom level
        tiles (str): Map tileset

    Returns:
        folium.Map: Base map
    """
    m = folium.Map(location=location, zoom_start=zoom_start, tiles=tiles, control_scale=True)
    return m


def add_india_boundary(m, shapefile_path="data/external/boundaries/india_boundary.geojson"):
    """
    Add India boundary to map.

    Args:
        m (folium.Map): Map object
        shapefile_path (str): Path to shapefile

    Returns:
        folium.Map: Map with boundary
    """
    try:
        if Path(shapefile_path).exists():
            with open(shapefile_path, "r") as f:
                india_geojson = json.load(f)
            folium.GeoJson(
                india_geojson,
                style_function=lambda x: {
                    "fillColor": "none",
                    "color": "#58A6FF",
                    "weight": 2,
                    "opacity": 0.5,
                },
            ).add_to(m)
            logger.info("✅ Added India boundary")
        else:
            logger.warning(f"Boundary file not found: {shapefile_path}")
    except Exception as e:
        logger.warning(f"Could not add India boundary: {e}")

    return m


def add_hcho_hotspots(m, hcho_geojson):
    """
    Add HCHO hotspot clusters to map.

    Args:
        m (folium.Map): Map object
        hcho_geojson (dict): GeoJSON data

    Returns:
        folium.Map: Map with hotspots
    """
    if not hcho_geojson or "features" not in hcho_geojson:
        logger.warning("No HCHO hotspots to add")
        return m

    for feature in hcho_geojson["features"]:
        props = feature["properties"]
        coords = feature["geometry"]["coordinates"]

        popup_html = f"""
        <div style="font-family: Arial; min-width: 150px;">
            <b>Cluster {props.get('cluster_id', 'Unknown')}</b><br>
            <hr>
            <b>Cells:</b> {props.get('num_cells', 0)}<br>
            <b>Mean HCHO:</b> {props.get('mean_hcho', 0):.4f} mol/m²<br>
            <b>Max HCHO:</b> {props.get('max_hcho', 0):.4f} mol/m²<br>
            <b>Source:</b> {props.get('source_region', 'Unknown')}
        </div>
        """

        folium.CircleMarker(
            location=[coords[1], coords[0]],
            radius=props.get("radius", 5),
            popup=folium.Popup(popup_html, max_width=300),
            color=props.get("color", "#FF6B35"),
            fill=True,
            fill_color=props.get("color", "#FF6B35"),
            fill_opacity=0.7,
        ).add_to(m)

    logger.info(f"✅ Added {len(hcho_geojson['features'])} HCHO hotspots")
    return m


def add_fire_locations(m, fire_geojson):
    """
    Add active fire locations to map.

    Args:
        m (folium.Map): Map object
        fire_geojson (dict): GeoJSON data

    Returns:
        folium.Map: Map with fire locations
    """
    if not fire_geojson or "features" not in fire_geojson:
        logger.warning("No fire locations to add")
        return m

    for feature in fire_geojson["features"]:
        coords = feature["geometry"]["coordinates"]
        props = feature.get("properties", {})

        popup_html = f"""
        <div style="font-family: Arial;">
            <b>Fire Location</b><br>
            <hr>
            <b>FRP:</b> {props.get('frp', 'N/A')} MW<br>
            <b>Confidence:</b> {props.get('confidence', 'N/A')}%
        </div>
        """

        folium.CircleMarker(
            location=[coords[1], coords[0]],
            radius=3,
            popup=folium.Popup(popup_html, max_width=200),
            color="#FF1744",
            fill=True,
            fill_color="#FF1744",
            fill_opacity=0.8,
        ).add_to(m)

    logger.info(f"✅ Added {len(fire_geojson['features'])} fire locations")
    return m


def add_wind_vectors(m, wind_data):
    """
    Add wind vector arrows to map.

    Args:
        m (folium.Map): Map object
        wind_data (list): Wind vector data

    Returns:
        folium.Map: Map with wind vectors
    """
    for vector in wind_data:
        lat = vector.get("lat", 0)
        lon = vector.get("lon", 0)
        u = vector.get("u", 0)
        v = vector.get("v", 0)
        speed = np.sqrt(u**2 + v**2)

        if speed > 0.1:
            angle = np.degrees(np.arctan2(v, u))
            folium.Marker(
                location=[lat, lon],
                icon=folium.DivIcon(
                    html=f"""
                    <div style="
                        font-size: 14px;
                        color: #00BCD4;
                        transform: rotate({angle}deg);
                        text-align: center;
                    ">
                        ➜ {speed:.1f} m/s
                    </div>
                    """
                ),
            ).add_to(m)

    logger.info(f"✅ Added {len(wind_data)} wind vectors")
    return m


def create_full_map(
    aqi_geojson=None,
    hcho_geojson=None,
    fire_geojson=None,
    wind_data=None,
    show_boundary=True,
    shapefile_path="data/external/boundaries/india_boundary.geojson",
):
    """
    Create a complete map with all layers.

    Args:
        aqi_geojson (dict): AQI grid data
        hcho_geojson (dict): HCHO hotspots
        fire_geojson (dict): Fire locations
        wind_data (list): Wind vectors
        show_boundary (bool): Add India boundary
        shapefile_path (str): Path to shapefile

    Returns:
        folium.Map: Complete map
    """
    m = create_india_map()

    if show_boundary:
        add_india_boundary(m, shapefile_path)

    if hcho_geojson:
        add_hcho_hotspots(m, hcho_geojson)

    if fire_geojson:
        add_fire_locations(m, fire_geojson)

    if wind_data:
        add_wind_vectors(m, wind_data)

    return m
