# ============================================================
# Data Acquisition Module
# ============================================================

"""Data acquisition from satellite, meteorology, and ground sources."""

from src.acquisition.sentinel5p_downloader import download_sentinel5p
from src.acquisition.era5_downloader import download_era5
from src.acquisition.firms_downloader import download_firms
from src.acquisition.cpcb_downloader import download_cpcb
from src.acquisition.openaq_downloader import download_openaq

__all__ = [
    "download_sentinel5p",
    "download_era5",
    "download_firms",
    "download_cpcb",
    "download_openaq",
]
