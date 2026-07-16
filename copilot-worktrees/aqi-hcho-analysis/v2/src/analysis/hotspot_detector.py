# ============================================================
# HCHO Hotspot Detector
# ============================================================

"""HCHO hotspot detection using DBSCAN clustering."""

import numpy as np
import pandas as pd
from sklearn.cluster import DBSCAN
from sklearn.preprocessing import StandardScaler
import json
from pathlib import Path
from loguru import logger


class HCHOHotspotDetector:
    """
    Detect HCHO hotspots using DBSCAN clustering.

    Attributes:
        eps (float): DBSCAN epsilon (radius in degrees)
        min_samples (int): Minimum points to form a cluster
        percentile_threshold (float): Percentile threshold for high HCHO
        clusters (dict): Detected clusters
    """

    def __init__(self, eps=0.5, min_samples=4, percentile_threshold=90):
        self.eps = eps
        self.min_samples = min_samples
        self.percentile_threshold = percentile_threshold
        self.clusters = None
        self.high_cells = None

    def detect(self, hcho_grid, lat_grid, lon_grid):
        """
        Detect HCHO hotspots.

        Args:
            hcho_grid (np.ndarray): 2D HCHO concentration grid
            lat_grid (np.ndarray): 2D latitude grid
            lon_grid (np.ndarray): 2D longitude grid

        Returns:
            dict: Cluster information
        """
        logger.info("🔍 Detecting HCHO hotspots...")

        # Flatten arrays
        hcho_flat = hcho_grid.flatten()
        lat_flat = lat_grid.flatten()
        lon_flat = lon_grid.flatten()

        # Apply threshold
        positive_mask = hcho_flat > 0
        if not np.any(positive_mask):
            logger.warning("No positive HCHO values found")
            return {}

        threshold = np.percentile(hcho_flat[positive_mask], self.percentile_threshold)
        high_idx = hcho_flat > threshold

        if not np.any(high_idx):
            logger.warning("No high HCHO cells found")
            return {}

        # Extract coordinates
        coords = np.column_stack([lon_flat[high_idx], lat_flat[high_idx]])
        hcho_values = hcho_flat[high_idx]
        self.high_cells = coords

        # Scale coordinates
        scaler = StandardScaler()
        coords_scaled = scaler.fit_transform(coords)

        # Apply DBSCAN
        dbscan = DBSCAN(eps=self.eps, min_samples=self.min_samples)
        labels = dbscan.fit_predict(coords_scaled)

        # Process clusters
        self.clusters = self._process_clusters(coords, hcho_values, labels)

        logger.info(f"  Found {len(self.clusters)} clusters")
        return self.clusters

    def _process_clusters(self, coords, values, labels):
        """Process DBSCAN results into cluster dictionaries."""
        clusters = {}
        unique_labels = set(labels) - {-1}
        colors = ["#FF6B35", "#FF1744", "#FF9800", "#F44336", "#E91E63", "#9C27B0"]

        for idx, label in enumerate(unique_labels):
            mask = labels == label
            cluster_cells = coords[mask]
            cluster_values = values[mask]

            centroid_lon = np.mean(cluster_cells[:, 0])
            centroid_lat = np.mean(cluster_cells[:, 1])

            source_region = self._assign_source_region(centroid_lat, centroid_lon)

            clusters[label] = {
                "id": int(label),
                "num_cells": len(cluster_cells),
                "centroid_lon": float(centroid_lon),
                "centroid_lat": float(centroid_lat),
                "mean_hcho": float(np.mean(cluster_values)),
                "max_hcho": float(np.max(cluster_values)),
                "source_region": source_region,
                "color": colors[idx % len(colors)],
                "cells": cluster_cells.tolist()
            }

        return clusters

    def _assign_source_region(self, lat, lon):
        """Assign source region based on coordinates."""
        if 22 <= lat <= 32 and 74 <= lon <= 90:
            return "IGP (Crop Burning)"
        elif 18 <= lat <= 24 and 76 <= lon <= 84:
            return "Central India (Forest Fires)"
        elif 22 <= lat <= 28 and 90 <= lon <= 98:
            return "Northeast India (Forest Fires)"
        else:
            return "Other Region"

    def get_statistics(self):
        """Get cluster statistics as DataFrame."""
        if not self.clusters:
            logger.warning("No clusters found")
            return pd.DataFrame()

        stats = []
        for cluster in self.clusters.values():
            stats.append({
                "cluster_id": cluster["id"],
                "num_cells": cluster["num_cells"],
                "centroid_lat": cluster["centroid_lat"],
                "centroid_lon": cluster["centroid_lon"],
                "mean_hcho": cluster["mean_hcho"],
                "max_hcho": cluster["max_hcho"],
                "source_region": cluster["source_region"],
            })

        return pd.DataFrame(stats).sort_values("mean_hcho", ascending=False)

    def export_geojson(self, output_path="outputs/maps/hcho_hotspots.geojson"):
        """Export clusters as GeoJSON."""
        if not self.clusters:
            logger.warning("No clusters to export")
            return

        features = []
        for cluster in self.clusters.values():
            features.append({
                "type": "Feature",
                "geometry": {
                    "type": "Point",
                    "coordinates": [cluster["centroid_lon"], cluster["centroid_lat"]]
                },
                "properties": {
                    "cluster_id": cluster["id"],
                    "num_cells": cluster["num_cells"],
                    "mean_hcho": cluster["mean_hcho"],
                    "max_hcho": cluster["max_hcho"],
                    "source_region": cluster["source_region"],
                    "color": cluster["color"],
                    "radius": np.sqrt(cluster["num_cells"]) * 0.3
                }
            })

        geojson = {"type": "FeatureCollection", "features": features}

        Path(output_path).parent.mkdir(parents=True, exist_ok=True)
        with open(output_path, "w") as f:
            json.dump(geojson, f, indent=2)

        logger.info(f"💾 Hotspots exported to {output_path}")


if __name__ == "__main__":
    # Test with sample data
    np.random.seed(42)
    lat = np.linspace(8, 38, 120)
    lon = np.linspace(68, 98, 120)
    lat_grid, lon_grid = np.meshgrid(lat, lon)

    hcho_grid = np.random.randn(120, 120) * 0.001 + 0.005
    hcho_grid[50:60, 70:80] = 0.05  # IGP hotspot

    detector = HCHOHotspotDetector()
    clusters = detector.detect(hcho_grid, lat_grid, lon_grid)
    stats = detector.get_statistics()
    print(stats)