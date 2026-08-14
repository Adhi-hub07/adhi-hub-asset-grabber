@echo off
title ADHI-HUB Asset Grabber
cd /d "%~dp0"
pip install rich >nul 2>nul
python asset_grabber.py
pause