"""
Load and prepare census block geometries and school point data.
"""
import json
import os
import geopandas as gpd
import pandas as pd
from shapely.geometry import Point
from src.config import SCHOOLS, BLOCKS_GEOJSON

STUDENT_BLOCKS_PATH = "data/student_blocks.json"


def _load_student_counts():
    """Load real per-block student counts from geocoded address data."""
    with open(STUDENT_BLOCKS_PATH) as f:
        raw = json.load(f)
    # raw: {block_id: {grade_key: {school: count}}}
    result = {}
    for bid, grades in raw.items():
        k4  = sum(sum(d.values()) for d in grades.values())
        k1  = sum(sum(grades.get(g, {}).values()) for g in ("k", "g1"))
        g24 = sum(sum(grades.get(g, {}).values()) for g in ("g2", "g3", "g4"))
        result[bid] = {"k4": round(k4, 4), "k1": round(k1, 4), "g24": round(g24, 4)}
    return result


def load_blocks() -> gpd.GeoDataFrame:
    """
    Load census block polygons from GeoJSON.

    Returns a GeoDataFrame with columns:
        block_id, geometry, population, centroid_lat, centroid_lon,
        students     -- K-4 actual student count  (community zone assignment)
        students_k1  -- K-1 actual student count  (grade-center PreK-1 band)
        students_g24 -- 2-4 actual student count  (grade-center 2-4 band)
        geometry_4326, centroid, centroid_proj
    CRS: EPSG:32619 (UTM 19N, Maine)
    """
    gdf = gpd.read_file(BLOCKS_GEOJSON)

    gdf = gdf.rename(columns={
        "GEOID20":    "block_id",
        "POP20":      "population",
        "INTPTLAT20": "centroid_lat",
        "INTPTLON20": "centroid_lon",
    })

    gdf["population"]   = pd.to_numeric(gdf["population"],   errors="coerce").fillna(0).astype(int)
    gdf["centroid_lat"] = pd.to_numeric(gdf["centroid_lat"], errors="coerce")
    gdf["centroid_lon"] = pd.to_numeric(gdf["centroid_lon"], errors="coerce")

    gdf["centroid"] = gdf.apply(
        lambda r: Point(r["centroid_lon"], r["centroid_lat"]), axis=1
    )

    NO_STUDENTS_BLOCKS = {"230050030022012"}  # Retirement community

    # Load real per-block student counts from geocoded address data
    student_counts = _load_student_counts()
    gdf["students"]     = gdf["block_id"].map(lambda b: student_counts.get(b, {}).get("k4",  0.0))
    gdf["students_k1"]  = gdf["block_id"].map(lambda b: student_counts.get(b, {}).get("k1",  0.0))
    gdf["students_g24"] = gdf["block_id"].map(lambda b: student_counts.get(b, {}).get("g24", 0.0))

    # Ensure retirement community block has no students
    gdf.loc[gdf["block_id"].isin(NO_STUDENTS_BLOCKS),
            ["students", "students_k1", "students_g24"]] = 0.0

    gdf = gdf.set_crs("EPSG:4326", allow_override=True)
    gdf["geometry_4326"] = gdf["geometry"]
    gdf = gdf.to_crs("EPSG:32619")
    gdf["centroid_proj"] = gdf.geometry.centroid

    gdf = gdf.set_index("block_id", drop=False)
    gdf.index.name = "idx"

    return gdf[["block_id", "geometry", "geometry_4326", "centroid",
                "centroid_proj", "population",
                "students", "students_k1", "students_g24",
                "centroid_lat", "centroid_lon"]]


def load_schools() -> gpd.GeoDataFrame:
    """
    Build a GeoDataFrame of school point locations from config.
    """
    records = []
    for name, info in SCHOOLS.items():
        records.append({
            "school_id": name,
            "lat":       info["lat"],
            "lng":       info["lng"],
            "capacity":  info["capacity"],
            "geometry":  Point(info["lng"], info["lat"]),
        })

    gdf = gpd.GeoDataFrame(records, crs="EPSG:4326")
    gdf = gdf.to_crs("EPSG:32619")
    gdf = gdf.set_index("school_id", drop=False)
    gdf.index.name = "idx"
    return gdf
