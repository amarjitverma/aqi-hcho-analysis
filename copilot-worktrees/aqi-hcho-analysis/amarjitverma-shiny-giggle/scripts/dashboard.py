#!/usr/bin/env python3
# ============================================================
# Launch Dashboard Script
# ============================================================

"""Launch the Streamlit dashboard."""

import subprocess
import sys
import os
from pathlib import Path


def main():
    """Launch the dashboard."""
    print("🚀 Launching Streamlit Dashboard...")
    
    # Check if Streamlit is installed
    try:
        import streamlit
    except ImportError:
        print("❌ Streamlit is not installed. Run: pip install streamlit")
        sys.exit(1)
    
    # Get the dashboard path
    dashboard_path = Path(__file__).parent.parent / "dashboard" / "app.py"
    
    if not dashboard_path.exists():
        print(f"❌ Dashboard not found at {dashboard_path}")
        sys.exit(1)
    
    # Launch Streamlit
    cmd = [sys.executable, "-m", "streamlit", "run", str(dashboard_path)]
    print(f"Running: {' '.join(cmd)}")
    print("🌍 Dashboard will open in your browser")
    print("Press Ctrl+C to stop")
    
    subprocess.run(cmd)


if __name__ == "__main__":
    main()