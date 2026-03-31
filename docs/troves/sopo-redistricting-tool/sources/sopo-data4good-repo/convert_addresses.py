"""
Convert geocoded student addresses to Census block GEOID20 student counts.

Input:  CSV with coordinates + current school + grade (addresses already removed)
Output: data/student_blocks.json — per-block student counts by grade and current school
        NO coordinates are written to the output file.

Run locally only. Output is safe to commit (block IDs + counts, no PII).
"""
import json
import os
import pandas as pd
import geopandas as gpd
import numpy as np
from shapely.geometry import Point

CSV_PATH   = "/Users/atishok/Downloads/Copy of Addresses CY NY - K 4 - Encoded - 2020 (1).csv"
BLOCKS_PATH = "Polygons.geojson"
OUT_PATH   = "data/student_blocks.json"

NO_STUDENTS_BLOCKS = {"230050030022012"}  # Retirement community

SCHOOL_NAME_MAP = {
    "Waldo T Skillin Elementary School":  "Skillin",
    "Dora L Small Elementary School":     "Small",
    "Frank I Brown Elementary School":    "Brown",
    "Dyer Elementary School":             "Dyer",
    "James Otis Kaler Elementary School": "Kaler",
}

GRADE_KEYS = ["k", "g1", "g2", "g3", "g4"]

def normalize_grade(g):
    g = str(g).strip().upper()
    return {"K": "k", "1": "g1", "2": "g2", "3": "g3", "4": "g4"}.get(g)


def add_student(block_data, block_id, grade_key, school, count=1.0):
    if block_id in NO_STUDENTS_BLOCKS or grade_key is None:
        return
    if block_id not in block_data:
        block_data[block_id] = {gk: {} for gk in GRADE_KEYS}
    d = block_data[block_id][grade_key]
    d[school] = round(d.get(school, 0.0) + count, 6)


def main():
    os.makedirs("data", exist_ok=True)

    # ── Load data ──────────────────────────────────────────────────────────────
    df = pd.read_csv(CSV_PATH)
    df["school_short"] = df["Current school"].map(SCHOOL_NAME_MAP)
    df["grade_key"]    = df["Grade"].apply(normalize_grade)

    assert df["school_short"].notna().all(), "Unknown school names found"
    assert df["grade_key"].notna().all(),    "Unknown grade values found"

    # ── Load block polygons ────────────────────────────────────────────────────
    blocks = gpd.read_file(BLOCKS_PATH)[["GEOID20", "POP20", "geometry"]]
    blocks = blocks.set_crs("EPSG:4326", allow_override=True)
    blocks["GEOID20"] = blocks["GEOID20"].astype(str)
    blocks["POP20"]   = pd.to_numeric(blocks["POP20"], errors="coerce").fillna(0).astype(int)

    eligible_blocks = blocks[~blocks["GEOID20"].isin(NO_STUDENTS_BLOCKS)].copy()
    total_pop = eligible_blocks["POP20"].sum()

    # ── Split: has coords vs no coords ────────────────────────────────────────
    has_coords  = df["Coordinates"].notna()
    matched_df  = df[has_coords].copy()
    no_coord_df = df[~has_coords].copy()

    print(f"Students with coordinates:    {len(matched_df)}")
    print(f"Students without coordinates: {len(no_coord_df)}  (will distribute proportionally)")

    # ── Parse coordinates ──────────────────────────────────────────────────────
    def parse_coord(s):
        lon, lat = s.strip().split(",")
        return float(lon.strip()), float(lat.strip())

    lons, lats = zip(*matched_df["Coordinates"].apply(parse_coord))
    matched_df = matched_df.copy()
    matched_df["lon"] = lons
    matched_df["lat"] = lats

    # ── Spatial join: point-in-polygon → GEOID20 ──────────────────────────────
    pts = gpd.GeoDataFrame(
        matched_df,
        geometry=[Point(lon, lat) for lon, lat in zip(lons, lats)],
        crs="EPSG:4326",
    )
    joined = gpd.sjoin(pts, blocks[["GEOID20", "geometry"]], how="left", predicate="within")

    inside  = joined[joined["GEOID20"].notna()]
    outside = joined[joined["GEOID20"].isna()]

    print(f"Spatially matched:            {len(inside)}")
    if len(outside) > 0:
        print(f"Outside all block polygons:   {len(outside)}  (distributing proportionally)")

    # ── Build per-block student counts ─────────────────────────────────────────
    block_data = {}

    # Students with a matched block
    for _, row in inside.iterrows():
        add_student(block_data, row["GEOID20"], row["grade_key"], row["school_short"])

    # Students whose point fell outside block boundaries — distribute by pop
    for _, row in outside.iterrows():
        for _, brow in eligible_blocks.iterrows():
            frac = brow["POP20"] / total_pop
            add_student(block_data, brow["GEOID20"], row["grade_key"], row["school_short"], frac)

    # Students with no coordinates at all — distribute by pop
    for _, row in no_coord_df.iterrows():
        for _, brow in eligible_blocks.iterrows():
            frac = brow["POP20"] / total_pop
            add_student(block_data, brow["GEOID20"], row["grade_key"], row["school_short"], frac)

    # ── Verify totals ──────────────────────────────────────────────────────────
    total_check = sum(
        v
        for bd in block_data.values()
        for gd in bd.values()
        for v in gd.values()
    )
    print(f"\nTotal students encoded: {total_check:.1f}  (expected: {len(df)})")

    by_grade = {gk: 0.0 for gk in GRADE_KEYS}
    for bd in block_data.values():
        for gk in GRADE_KEYS:
            by_grade[gk] += sum(bd[gk].values())
    print("By grade:", {gk: round(v, 1) for gk, v in by_grade.items()})

    by_school = {}
    for bd in block_data.values():
        for gk in GRADE_KEYS:
            for sch, cnt in bd[gk].items():
                by_school[sch] = by_school.get(sch, 0.0) + cnt
    print("By school:", {k: round(v, 1) for k, v in sorted(by_school.items())})

    # ── Blocks in polygon file with no students (sanity check) ────────────────
    matched_block_ids = set(block_data.keys())
    all_eligible_ids  = set(eligible_blocks["GEOID20"])
    missing = all_eligible_ids - matched_block_ids
    print(f"\nBlocks with no students: {len(missing)} (of {len(all_eligible_ids)} eligible)")

    # ── Write output (NO coordinates) ─────────────────────────────────────────
    with open(OUT_PATH, "w") as f:
        json.dump(block_data, f, separators=(",", ":"))

    size_kb = os.path.getsize(OUT_PATH) / 1024
    print(f"\nWritten: {OUT_PATH}  ({size_kb:.0f} KB, {len(block_data)} blocks with students)")


if __name__ == "__main__":
    main()
