# ============================================================
# Wind Transport Analysis
# ============================================================

"""Wind transport and plume decay modeling."""

import numpy as np
from loguru import logger


def calculate_wind_speed(u_wind, v_wind):
    """Calculate wind speed from U and V components."""
    return np.sqrt(u_wind**2 + v_wind**2)


def calculate_wind_direction(u_wind, v_wind):
    """Calculate wind direction in degrees (0° = North)."""
    return np.degrees(np.arctan2(v_wind, u_wind))


def plume_decay(c_source, distance, wind_speed, decay_constant=0.02):
    """
    Calculate plume concentration downwind.

    Args:
        c_source (float): Source concentration
        distance (float or np.ndarray): Distance downwind (km)
        wind_speed (float): Wind speed (m/s)
        decay_constant (float): Decay rate (1/km)

    Returns:
        float or np.ndarray: Downwind concentration
    """
    return c_source * np.exp(-decay_constant * distance / wind_speed)


def model_plume_transport(
    source_lon, source_lat, wind_u, wind_v, hcho_source, max_distance=300, decay_constant=0.02
):
    """
    Model HCHO plume transport downwind.

    Args:
        source_lon, source_lat: Source coordinates
        wind_u, wind_v: Wind components (m/s)
        hcho_source: HCHO concentration at source (mol/m²)
        max_distance (km): Maximum transport distance
        decay_constant (float): Decay rate (1/km)

    Returns:
        dict: Plume model results
    """
    logger.info("💨 Modeling plume transport...")

    wind_speed = calculate_wind_speed(wind_u, wind_v)
    wind_dir = calculate_wind_direction(wind_u, wind_v)

    distances = np.linspace(0, max_distance, 100)
    concentrations = plume_decay(hcho_source, distances, wind_speed, decay_constant)

    wind_angle_rad = np.radians(wind_dir)
    lon_plume = source_lon + distances * np.sin(wind_angle_rad) * 0.01
    lat_plume = source_lat + distances * np.cos(wind_angle_rad) * 0.01

    plume = {
        "distances": distances.tolist(),
        "hcho_concentrations": concentrations.tolist(),
        "longitudes": lon_plume.tolist(),
        "latitudes": lat_plume.tolist(),
        "wind_speed": float(wind_speed),
        "wind_direction": float(wind_dir),
        "source_hcho": float(hcho_source),
    }

    logger.info(f"  Wind: {wind_speed:.2f} m/s, {wind_dir:.1f}°")
    logger.info(
        f"  At 100 km: HCHO = {plume_decay(hcho_source, 100, wind_speed, decay_constant):.4f} mol/m²"
    )

    return plume


def export_plume_geojson(plume_data, output_path="outputs/maps/plume_transport.geojson"):
    """Export plume transport data as GeoJSON."""
    features = []
    for i in range(len(plume_data["distances"])):
        features.append(
            {
                "type": "Feature",
                "geometry": {
                    "type": "Point",
                    "coordinates": [plume_data["longitudes"][i], plume_data["latitudes"][i]],
                },
                "properties": {
                    "distance": plume_data["distances"][i],
                    "hcho": plume_data["hcho_concentrations"][i],
                },
            }
        )

    geojson = {"type": "FeatureCollection", "features": features}

    from pathlib import Path

    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    import json

    with open(output_path, "w") as f:
        json.dump(geojson, f, indent=2)

    logger.info(f"💾 Plume data exported to {output_path}")


if __name__ == "__main__":
    # Test with sample data
    plume = model_plume_transport(
        source_lon=76.0,
        source_lat=30.0,
        wind_u=2.0,
        wind_v=-2.0,
        hcho_source=0.01,
        max_distance=300,
    )
    print(f"Plume length: {len(plume['distances'])} points")
