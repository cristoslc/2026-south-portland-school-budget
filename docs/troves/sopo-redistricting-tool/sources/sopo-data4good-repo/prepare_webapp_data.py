"""
Generate per-scenario JSON data files for the web app.
Includes all 5 assignment modes + per-block real student counts + current school
distribution (for % change calculation in the webapp).
"""
import json, os, pickle
import pandas as pd
import geopandas as gpd
import numpy as np

from src.config import (
    SCENARIOS, RECONFIG_SCENARIOS, SCHOOLS,
    PREK_COMMUNITY_CURRENT, PREK_PER_SCHOOL, PREK_PER_CENTER,
    SCHOOL_COLORS, WALK_THRESHOLD_METERS,
)

os.makedirs("webapp/public/data", exist_ok=True)

with open("cache/distance_matrices.pkl", "rb") as f:
    dm = pickle.load(f)
walk_df  = dm["walk"]
drive_df = dm["drive"]
walk_df.index  = walk_df.index.astype(str)
drive_df.index = drive_df.index.astype(str)

NO_STUDENTS_BLOCKS = {"230050030022012"}  # Retirement community

blocks_gdf = gpd.read_file("Polygons.geojson")
blocks_gdf = blocks_gdf.rename(columns={"GEOID20": "block_id", "POP20": "population"})
blocks_gdf["block_id"]   = blocks_gdf["block_id"].astype(str)
blocks_gdf["population"] = pd.to_numeric(blocks_gdf["population"], errors="coerce").fillna(0).astype(int)
blocks_gdf = blocks_gdf.set_index("block_id", drop=False)

# Load real per-block student counts from geocoded address data
with open("data/student_blocks.json") as f:
    student_blocks = json.load(f)
# student_blocks: {block_id: {grade_key: {school: count}}}

def block_students(bid):
    """Return (k4, k1, g24, currentSchoolsK4, currentSchoolsK1, currentSchoolsG24, perGrade)."""
    grades = student_blocks.get(bid, {})
    def merge(keys):
        out = {}
        for g in keys:
            for sch, cnt in grades.get(g, {}).items():
                out[sch] = round(out.get(sch, 0.0) + cnt, 4)
        return out
    cs_k4  = merge(["k", "g1", "g2", "g3", "g4"])
    cs_k1  = merge(["k", "g1"])
    cs_g24 = merge(["g2", "g3", "g4"])
    k4  = round(sum(cs_k4.values()),  2)
    k1  = round(sum(cs_k1.values()),  2)
    g24 = round(sum(cs_g24.values()), 2)
    per_grade = {g: round(sum(grades.get(g, {}).values()), 2) for g in ["k", "g1", "g2", "g3", "g4"]}
    return k4, k1, g24, cs_k4, cs_k1, cs_g24, per_grade

CLOSED_MAP = {s["name"]: s["closed"] for s in SCENARIOS}

SCHOOLS_OUT = {
    k: {"lat": v["lat"], "lng": v["lng"], "capacity": v["capacity"],
        "color": SCHOOL_COLORS[k]}
    for k, v in SCHOOLS.items()
}

def safe_dist(df, bid, sid):
    try:
        v = df.loc[bid, sid]
        return round(float(v), 1) if np.isfinite(v) else None
    except Exception:
        return None

def load_asgn(path):
    df = pd.read_csv(path)
    df["block_id"] = df["block_id"].astype(str)
    return dict(zip(df["block_id"], df["assigned_school"]))

for scenario in SCENARIOS:
    sname  = scenario["name"]
    closed = CLOSED_MAP[sname]
    open_school_ids = [s for s in SCHOOLS if s != closed]
    reconfig  = RECONFIG_SCENARIOS[sname]
    prek1_ids = reconfig["prek1_schools"]
    g24_ids   = reconfig["g24_schools"]

    modes = {
        "community_current": load_asgn(f"outputs/{sname}_community_current.csv"),
        "community_full":    load_asgn(f"outputs/{sname}_community_full.csv"),
        "prek1_current":     load_asgn(f"outputs/{sname}_prek1_current.csv"),
        "prek1_full":        load_asgn(f"outputs/{sname}_prek1_full.csv"),
        "g24":               load_asgn(f"outputs/{sname}_g24.csv"),
    }

    prek_alloc = {
        "community_current": PREK_COMMUNITY_CURRENT[sname],
        "community_full":    {sid: PREK_PER_SCHOOL for sid in open_school_ids},
        "prek1_current":     {sid: PREK_PER_SCHOOL for sid in prek1_ids},
        "prek1_full":        {sid: PREK_PER_CENTER for sid in prek1_ids},
        "g24":               {},
    }

    blocks_out = []
    for bid, row in blocks_gdf.iterrows():
        if bid in NO_STUDENTS_BLOCKS:
            continue

        k4, k1, g24, cs_k4, cs_k1, cs_g24, per_grade = block_students(bid)
        walk_dists  = {sid: safe_dist(walk_df,  bid, sid) for sid in open_school_ids}
        drive_dists = {sid: safe_dist(drive_df, bid, sid) for sid in open_school_ids}
        base_assignments = {mode: asgn.get(bid) for mode, asgn in modes.items()}

        blocks_out.append({
            "id":               bid,
            "geometry":         row["geometry"].__geo_interface__,
            "population":       int(row["population"]),
            "studentsK4":       k4,
            "studentsK1":       k1,
            "studentsG24":      g24,
            "studentsPerGrade": per_grade,
            # Current school distribution — used by webapp to compute % change
            "currentSchoolsK4":  cs_k4,
            "currentSchoolsK1":  cs_k1,
            "currentSchoolsG24": cs_g24,
            "baseAssignments":  base_assignments,
            "walkDists":        walk_dists,
            "driveDists":       drive_dists,
        })

    out = {
        "scenario":        sname,
        "closedSchool":    closed,
        "openSchools":     open_school_ids,
        "schools":         {s: SCHOOLS_OUT[s] for s in open_school_ids},
        "reconfig":        {"prek1Schools": prek1_ids, "g24Schools": g24_ids},
        "prekAllocations": prek_alloc,
        "blocks":          blocks_out,
    }

    path = f"webapp/public/data/{sname}.json"
    with open(path, "w") as f:
        json.dump(out, f, separators=(",", ":"))
    print(f"{sname}: {len(blocks_out)} blocks, {os.path.getsize(path)/1024:.0f} KB")

print("Done.")
