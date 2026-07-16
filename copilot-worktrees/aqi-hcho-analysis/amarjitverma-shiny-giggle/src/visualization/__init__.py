# ============================================================
# Visualization Module
# ============================================================

"""Visualization utilities for maps, charts, and dashboard."""

from src.visualization.maps import create_india_map, add_hcho_hotspots, add_fire_locations
from src.visualization.charts import create_scatter_plot, create_feature_importance, create_correlation_chart
from src.visualization.dashboard_utils import generate_dashboard_data

__all__ = [
    "create_india_map",
    "add_hcho_hotspots",
    "add_fire_locations",
    "create_scatter_plot",
    "create_feature_importance",
    "create_correlation_chart",
    "generate_dashboard_data",
]