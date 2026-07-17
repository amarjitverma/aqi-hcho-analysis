"""Run HCHO hotspot detection on real Sentinel-5P data and save to dashboard cache."""
import rasterio
import numpy as np
import json
import os
import sys

sys.path.insert(0, '.')
from src.analysis.hotspot_detector import HCHOHotspotDetector

# ── Load real HCHO GeoTIFF ────────────────────────────────────────────────
hcho_path = "data/raw/satellite/sentinel5p/hcho/HCHO_2024-10-01_2024-11-05.tif"
with rasterio.open(hcho_path) as src:
    data = src.read(1).astype(np.float32)
    transform = src.transform
    height, width = data.shape

# Build lat/lon grids from transform
cols = np.arange(width)
rows = np.arange(height)
lons = transform.c + cols * transform.a
lats = transform.f + rows * transform.e
lon_grid, lat_grid = np.meshgrid(lons, lats)

# Clean: replace negatives with NaN
data[data < 0] = np.nan

print(f"HCHO grid shape: {data.shape}")
print(f"Valid pixels: {np.sum(~np.isnan(data))}")
print(f"HCHO range: {np.nanmin(data):.6f} – {np.nanmax(data):.6f} mol/m²")

# ── Run hotspot detector ──────────────────────────────────────────────────
detector = HCHOHotspotDetector(eps=1.0, min_samples=5, percentile_threshold=90)
clusters = detector.detect(data, lat_grid, lon_grid)

print(f"\nDetected {len(clusters)} hotspot clusters:")
for cid, info in list(clusters.items())[:10]:
    print(
        "  Cluster {}: center=({:.2f}, {:.2f}), cells={}, mean_HCHO={:.6f} mol/m2".format(
            cid,
            info["centroid_lat"],
            info["centroid_lon"],
            info["num_cells"],
            info["mean_hcho"],
        )
    )

# ── Save GeoJSON for dashboard ────────────────────────────────────────────
os.makedirs("dashboard/cache", exist_ok=True)
out_path = "dashboard/cache/hcho_hotspots.geojson"
detector.export_geojson(out_path)
print("\nSaved hotspots to", out_path)

# Also print stats table
stats_df = detector.get_statistics()
print("\nTop hotspots by HCHO:")
print(stats_df[["cluster_id","source_region","num_cells","mean_hcho","max_hcho"]].head(10).to_string(index=False))

