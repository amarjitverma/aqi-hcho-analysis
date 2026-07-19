# ============================================================
# Source Attribution Analysis
# ============================================================

"""Source region attribution for HCHO emissions."""

import pandas as pd
from loguru import logger


class SourceAttribution:
    """Calculate source region contributions."""

    def __init__(self):
        self.attribution_results = None

    def calculate(self, clusters):
        """
        Calculate source region contribution percentages.

        Args:
            clusters (dict): Cluster data from hotspot detection

        Returns:
            pd.DataFrame: Source contributions
        """
        if not clusters:
            logger.warning("No clusters provided")
            return pd.DataFrame()

        total = sum(c["mean_hcho"] * c["num_cells"] for c in clusters.values())

        contributions = []
        for cluster in clusters.values():
            cluster_total = cluster["mean_hcho"] * cluster["num_cells"]
            contributions.append(
                {
                    "source_region": cluster["source_region"],
                    "num_cells": cluster["num_cells"],
                    "mean_hcho": cluster["mean_hcho"],
                    "total_contribution": cluster_total,
                    "percentage": (cluster_total / total) * 100 if total > 0 else 0,
                }
            )

        df = pd.DataFrame(contributions)
        df = df.sort_values("percentage", ascending=False)
        df["cumulative_percentage"] = df["percentage"].cumsum()

        self.attribution_results = df

        logger.info("  Source attribution:")
        for _, row in df.iterrows():
            logger.info(f"    {row['source_region']}: {row['percentage']:.1f}%")

        return df

    def get_regional_comparison(self, clusters_by_season):
        """
        Compare source attribution across seasons.

        Args:
            clusters_by_season (dict): {season: clusters}

        Returns:
            pd.DataFrame: Seasonal comparison
        """
        results = []
        for season, clusters in clusters_by_season.items():
            df = self.calculate(clusters)
            df["season"] = season
            results.append(df)

        return pd.concat(results, ignore_index=True)


if __name__ == "__main__":
    # Test with sample data
    sample_clusters = {
        0: {"source_region": "IGP (Crop Burning)", "mean_hcho": 18.4, "num_cells": 45},
        1: {"source_region": "Central India (Forest Fires)", "mean_hcho": 15.2, "num_cells": 28},
        2: {"source_region": "Northeast India (Forest Fires)", "mean_hcho": 16.8, "num_cells": 17},
    }

    attribution = SourceAttribution()
    df = attribution.calculate(sample_clusters)
    print(df)
