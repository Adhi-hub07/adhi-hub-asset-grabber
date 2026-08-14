#!/bin/bash
# ADHI-HUB Asset Grabber — Linux/macOS launcher
cd "$(dirname "$0")"
command -v python3 >/dev/null || { echo "Python 3 required"; exit 1; }
python3 -m pip install rich --quiet 2>/dev/null
python3 asset_grabber.py