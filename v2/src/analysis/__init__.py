# ============================================================
# Analysis Module
# ============================================================

"""Scientific analysis modules."""

from src.analysis.hotspot_detector import detect_hotspots
from src.analysis.correlation import lagged_correlation, calculate_source_contribution
from src.analysis.transport import model_plume_transport
from src.analysis.source_attribution import calculate_attribution
from src.analysis.trend_analysis import analyze_trend

__all__ = [
    "detect_hotspots",
    "lagged_correlation",
    "calculate_source_contribution",
    "model_plume_transport",
    "calculate_attribution",
    "analyze_trend",
]