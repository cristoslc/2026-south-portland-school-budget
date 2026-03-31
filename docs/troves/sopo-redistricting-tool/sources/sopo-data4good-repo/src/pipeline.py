"""
Main pipeline orchestrator.

Runs five assignment modes per closure scenario:
  community_current  — community schools, current PreK pilot (Dyer + Kaler)
  community_full     — community schools, full PreK (29 per open school)
  prek1_current      — grade-center PreK-1 band, 29 PreK per center
  prek1_full         — grade-center PreK-1 band, 58 PreK per center
  g24                — grade-center Grades 2-4 band (no PreK impact)
"""
import os, json, pickle
import numpy as np
import pandas as pd
import geopandas as gpd

from src.config import (
    SCENARIOS, RECONFIG_SCENARIOS, PREK_COMMUNITY_CURRENT,
    PREK_PER_SCHOOL, PREK_PER_CENTER,
    OUTPUT_DIR, CACHE_DIR, SCHOOL_COLORS, WALK_THRESHOLD_METERS,
)
from src.data_loader import load_blocks, load_schools
from src.network import build_distance_matrices
from src.contiguity import build_adjacency_graph
from src.assignment import initial_assignment, balance_capacity, smooth_bussed_communities, consolidate_fragments, recover_walkable_assignments, equalize_loads
from src.metrics import compute_scenario_metrics, build_summary_table
from src.visualization import make_scenario_map, save_map


# ── helpers ──────────────────────────────────────────────────────────────────

def _load_adjacency(blocks_gdf):
    path = os.path.join(CACHE_DIR, "adjacency.pkl")
    if os.path.exists(path):
        print("  Loading cached adjacency graph...")
        with open(path, "rb") as f:
            return pickle.load(f)
    print("  Building block adjacency graph...")
    G = build_adjacency_graph(blocks_gdf)
    with open(path, "wb") as f:
        pickle.dump(G, f)
    return G


def _prek_schools(open_schools, prek_alloc):
    """Return copy of open_schools with capacities reduced by PreK overhead."""
    s = open_schools.copy()
    for sid, count in prek_alloc.items():
        if sid in s.index:
            s.loc[sid, "capacity"] = max(0, int(s.loc[sid, "capacity"]) - count)
    return s


def _with_student_col(blocks_gdf, col):
    """Return blocks_gdf with 'students' replaced by the named column."""
    b = blocks_gdf.copy()
    b["students"] = b[col]
    return b


def _run_3stage(blocks_gdf, open_schools, walk_df, drive_df, adjacency, label):
    print(f"    [{label}] Stage 1...")
    asgn = initial_assignment(blocks_gdf, open_schools, walk_df, drive_df, adjacency)
    print(f"    [{label}] Stage 2...")
    asgn = balance_capacity(asgn, blocks_gdf, open_schools, drive_df, adjacency)
    print(f"    [{label}] Stage 3...")
    asgn = smooth_bussed_communities(asgn, blocks_gdf, open_schools, walk_df, drive_df, adjacency)
    print(f"    [{label}] Stage 2b (re-balance after smoothing)...")
    asgn = balance_capacity(asgn, blocks_gdf, open_schools, drive_df, adjacency)
    print(f"    [{label}] Stage 4 (fragment consolidation)...")
    asgn = consolidate_fragments(asgn, blocks_gdf, open_schools, drive_df, adjacency, walk_df=walk_df)
    print(f"    [{label}] Stage 2c (re-balance after consolidation)...")
    asgn = balance_capacity(asgn, blocks_gdf, open_schools, drive_df, adjacency)
    print(f"    [{label}] Stage 4.5 (walkability recovery)...")
    asgn = recover_walkable_assignments(asgn, blocks_gdf, open_schools, walk_df, adjacency)
    print(f"    [{label}] Stage 2e (re-balance after walkability recovery)...")
    asgn = balance_capacity(asgn, blocks_gdf, open_schools, drive_df, adjacency)
    print(f"    [{label}] Stage 5 (load equalization)...")
    asgn = equalize_loads(asgn, blocks_gdf, open_schools, drive_df, walk_df, adjacency)
    print(f"    [{label}] Stage 2d (re-balance after equalization)...")
    asgn = balance_capacity(asgn, blocks_gdf, open_schools, drive_df, adjacency)
    for sid in open_schools["school_id"]:
        load = sum(blocks_gdf.loc[b, "students"] for b, s in asgn.items() if s == sid)
        cap  = open_schools.loc[sid, "capacity"]
        print(f"      {sid}: {load:.0f}/{cap} {'✓' if load <= cap else f'OVER by {load-cap:.0f}'}")
    return asgn


def _save_csv(assignments, blocks_gdf, walk_df, drive_df, path):
    rows = []
    for bid, sid in assignments.items():
        wd = walk_df.loc[bid, sid] if sid in walk_df.columns else None
        dd = drive_df.loc[bid, sid] if sid in drive_df.columns else None
        if wd is not None and not np.isfinite(wd): wd = None
        if dd is not None and not np.isfinite(dd): dd = None
        rows.append({
            "block_id":        bid,
            "assigned_school": sid,
            "population":      int(blocks_gdf.loc[bid, "population"]),
            "students":        round(float(blocks_gdf.loc[bid, "students"]), 2),
            "walk_dist_m":     round(wd, 1)         if wd is not None else None,
            "drive_dist_m":    round(dd, 1)         if dd is not None else None,
            "walk_dist_mi":    round(wd/1609.34, 3) if wd is not None else None,
            "drive_dist_mi":   round(dd/1609.34, 3) if dd is not None else None,
            "walkable":        bool(wd is not None and wd <= WALK_THRESHOLD_METERS),
        })
    pd.DataFrame(rows).to_csv(path, index=False)


# ── main pipeline ─────────────────────────────────────────────────────────────

def run():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    os.makedirs(CACHE_DIR,  exist_ok=True)

    print("=" * 60)
    print("Step 1: Loading data")
    print("=" * 60)
    blocks_gdf  = load_blocks()
    schools_gdf = load_schools()
    print(f"  {len(blocks_gdf)} census blocks, pop = {blocks_gdf['population'].sum():,}")
    print(f"  {len(schools_gdf)} schools  |  K-4 students to assign: "
          f"{blocks_gdf['students'].sum():.0f}")

    print("\n" + "=" * 60)
    print("Step 2: Block adjacency graph")
    print("=" * 60)
    adjacency = _load_adjacency(blocks_gdf)
    print(f"  Graph: {adjacency.number_of_nodes()} nodes, "
          f"{adjacency.number_of_edges()} edges")

    print("\n" + "=" * 60)
    print("Step 3: Travel distance matrices")
    print("=" * 60)
    dist     = build_distance_matrices(blocks_gdf, schools_gdf)
    walk_df  = dist["walk"]
    drive_df = dist["drive"]
    print(f"  Walk matrix:  {walk_df.shape}")
    print(f"  Drive matrix: {drive_df.shape}")

    print("\n" + "=" * 60)
    print("Step 4: Running scenarios (5 modes each)")
    print("=" * 60)

    all_metrics = []

    for scenario in SCENARIOS:
        sname  = scenario["name"]
        closed = scenario["closed"]
        print(f"\n{'─'*55}")
        print(f"Scenario: {sname}")
        print(f"{'─'*55}")

        open_schools = schools_gdf[schools_gdf["school_id"] != closed].copy()
        open_ids     = list(open_schools["school_id"])
        reconfig     = RECONFIG_SCENARIOS[sname]
        prek1_ids    = reconfig["prek1_schools"]
        g24_ids      = reconfig["g24_schools"]

        prek1_schools = open_schools[open_schools["school_id"].isin(prek1_ids)]
        g24_schools   = open_schools[open_schools["school_id"].isin(g24_ids)]

        blocks_k4  = _with_student_col(blocks_gdf, "students")      # K-4
        blocks_k1  = _with_student_col(blocks_gdf, "students_k1")   # K-1
        blocks_g24 = _with_student_col(blocks_gdf, "students_g24")  # 2-4

        # --- community current ---
        prek_cc = PREK_COMMUNITY_CURRENT[sname]
        asgn_cc = _run_3stage(blocks_k4, _prek_schools(open_schools, prek_cc),
                              walk_df, drive_df, adjacency, "community_current")
        _save_csv(asgn_cc, blocks_k4, walk_df, drive_df,
                  os.path.join(OUTPUT_DIR, f"{sname}_community_current.csv"))

        # --- community full (29 per open school) ---
        prek_cf = {sid: PREK_PER_SCHOOL for sid in open_ids}
        asgn_cf = _run_3stage(blocks_k4, _prek_schools(open_schools, prek_cf),
                              walk_df, drive_df, adjacency, "community_full")
        _save_csv(asgn_cf, blocks_k4, walk_df, drive_df,
                  os.path.join(OUTPUT_DIR, f"{sname}_community_full.csv"))

        # --- reconfig prek1 current (29 per prek1 school) ---
        prek_p1c = {sid: PREK_PER_SCHOOL for sid in prek1_ids}
        asgn_p1c = _run_3stage(blocks_k1, _prek_schools(prek1_schools, prek_p1c),
                               walk_df, drive_df, adjacency, "prek1_current")
        _save_csv(asgn_p1c, blocks_k1, walk_df, drive_df,
                  os.path.join(OUTPUT_DIR, f"{sname}_prek1_current.csv"))

        # --- reconfig prek1 full (58 per prek1 school) ---
        prek_p1f = {sid: PREK_PER_CENTER for sid in prek1_ids}
        asgn_p1f = _run_3stage(blocks_k1, _prek_schools(prek1_schools, prek_p1f),
                               walk_df, drive_df, adjacency, "prek1_full")
        _save_csv(asgn_p1f, blocks_k1, walk_df, drive_df,
                  os.path.join(OUTPUT_DIR, f"{sname}_prek1_full.csv"))

        # --- reconfig g24 (no PreK impact, full capacity) ---
        asgn_g24 = _run_3stage(blocks_g24, g24_schools,
                               walk_df, drive_df, adjacency, "g24")
        _save_csv(asgn_g24, blocks_g24, walk_df, drive_df,
                  os.path.join(OUTPUT_DIR, f"{sname}_g24.csv"))

        # -- community_current metrics + map (backward compat) --
        scene_metrics = compute_scenario_metrics(
            sname, asgn_cc, blocks_gdf, open_schools, walk_df, drive_df, adjacency
        )
        all_metrics.append(scene_metrics)

        with open(os.path.join(OUTPUT_DIR, f"{sname}_metrics.json"), "w") as f:
            json.dump(scene_metrics, f, indent=2, default=str)

        # boundary GeoJSON
        zone_polys = []
        for sid in open_ids:
            zone_bids = [b for b, s in asgn_cc.items() if s == sid]
            if not zone_bids: continue
            zg = blocks_gdf.loc[zone_bids].copy()
            zg["geometry"] = zg["geometry_4326"]
            zg = zg.set_geometry("geometry").set_crs("EPSG:4326", allow_override=True)
            dissolved = zg.dissolve()
            zone_polys.append({"school_id": sid, "geometry": dissolved.geometry.iloc[0],
                                "color": SCHOOL_COLORS.get(sid, "#999")})
        if zone_polys:
            gpd.GeoDataFrame(zone_polys, crs="EPSG:4326").to_file(
                os.path.join(OUTPUT_DIR, f"{sname}_boundaries.geojson"), driver="GeoJSON")

        # HTML map
        fmap = make_scenario_map(
            sname, asgn_cc, blocks_gdf, open_schools,
            scene_metrics["school_metrics"], walk_df, drive_df)
        save_map(fmap, sname)
        print(f"  → all outputs saved for {sname}")

    # ── summary ──
    print("\n" + "=" * 60)
    print("Step 5: Summary")
    print("=" * 60)
    summary_df = build_summary_table(all_metrics)
    summary_df.to_csv(os.path.join(OUTPUT_DIR, "scenario_summary.csv"))
    pd.set_option("display.max_columns", 20)
    pd.set_option("display.width", 120)
    print(summary_df[["scenario","capacity_feasible","total_walkable_students",
                       "avg_drive_distance_mi","max_drive_distance_mi",
                       "capacity_overflow","composite_rank"]].to_string())

    print("\n" + "=" * 60)
    print("Pipeline complete. All outputs in:", OUTPUT_DIR)
    print("=" * 60)
    return all_metrics, summary_df
