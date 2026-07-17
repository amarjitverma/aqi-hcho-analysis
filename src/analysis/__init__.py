# ============================================================
# Analysis Module
# ============================================================

"""Scientific analysis modules."""

from src.analysis.hotspot_detector import HCHOHotspotDetector
from src.analysis.correlation import lagged_correlation, calculate_source_contribution
from src.analysis.transport import model_plume_transport
from src.analysis.source_attribution import SourceAttribution
from src.analysis.trend_analysis import TrendAnalyzer

__all__ = [
    "HCHOHotspotDetector",
    "lagged_correlation",
    "calculate_source_contribution",
    "model_plume_transport",
    "SourceAttribution",
    "TrendAnalyzer",
]