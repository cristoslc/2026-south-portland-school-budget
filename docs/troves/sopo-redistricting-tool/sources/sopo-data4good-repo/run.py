#!/usr/bin/env python3
"""
Entry point for the South Portland redistricting pipeline.

Usage:
    python3 run.py

Outputs (in ./outputs/):
    <scenario>_map.html              — interactive block-level choropleth map
    <scenario>_boundaries.geojson   — dissolved school zone polygons
    <scenario>_block_assignments.csv — per-block assignment + distances
    <scenario>_metrics.json         — per-school and scenario metrics
    scenario_summary.csv            — ranked cross-scenario comparison table
"""
import sys
import os

# Ensure src/ is importable
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src.pipeline import run

if __name__ == "__main__":
    run()
