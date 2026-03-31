"""
Compute per-school and per-scenario metrics after assignment.
"""
import numpy as np
import pandas as pd
from src.config import WALK_THRESHOLD_METERS, TOTAL_ENROLLMENT
from src.contiguity import validate_all_zones


def compute_school_metrics(assignments, blocks_gdf, open_schools, walk_df, drive_df):
    """
    Per-school metrics for a single scenario.

    Returns: dict {school_id: metrics_dict}
    """
    metrics = {}

    for sid in open_schools["school_id"]:
        zone_blocks = [b for b, s in assignments.items() if s == sid]

        if not zone_blocks:
            metrics[sid] = {
                "school_id": sid,
                "assigned_population": 0,
                "assigned_students": 0.0,
                "capacity": int(open_schools.loc[sid, "capacity"]),
                "utilization_rate": 0.0,
                "pct_walkable": 0.0,
                "walkable_population": 0,
                "walkable_students": 0.0,
                "non_walkable_students": 0.0,
                "avg_walk_distance_m": None,
                "avg_drive_distance_m": None,
                "avg_drive_distance_non_walkable_m": None,
                "max_drive_distance_m": None,
                "capacity_overflow": 0.0,
                "avg_drive_distance_mi": None,
                "max_drive_distance_mi": None,
                "avg_drive_non_walkable_mi": None,
            }
            continue

        pop  = blocks_gdf.loc[zone_blocks, "population"].sum()
        stud = blocks_gdf.loc[zone_blocks, "students"].sum()
        cap  = int(open_schools.loc[sid, "capacity"])

        walk_dists  = walk_df.loc[zone_blocks, sid]
        drive_dists = drive_df.loc[zone_blocks, sid]

        walkable_mask    = walk_dists <= WALK_THRESHOLD_METERS
        non_walkable_mask = ~walkable_mask

        walkable_blocks     = [b for b, w in zip(zone_blocks, walkable_mask.values) if w]
        non_walkable_blocks = [b for b, w in zip(zone_blocks, non_walkable_mask.values) if w]

        walkable_pop   = blocks_gdf.loc[walkable_blocks, "population"].sum() if walkable_blocks else 0
        walkable_stud  = blocks_gdf.loc[walkable_blocks, "students"].sum() if walkable_blocks else 0.0
        non_walk_stud  = blocks_gdf.loc[non_walkable_blocks, "students"].sum() if non_walkable_blocks else 0.0

        pct_walkable = round(float(walkable_stud) / float(stud) * 100, 1) if stud > 0 else 0.0

        # Population-weighted average distances (all blocks)
        pops = blocks_gdf.loc[zone_blocks, "population"].values
        finite_walk  = walk_dists.replace([np.inf], np.nan).values
        finite_drive = drive_dists.replace([np.inf], np.nan).values

        with np.errstate(invalid="ignore"):
            avg_walk  = np.nansum(finite_walk  * pops) / pops.sum() if pops.sum() > 0 else np.nan
            avg_drive = np.nansum(finite_drive * pops) / pops.sum() if pops.sum() > 0 else np.nan

        max_drive = np.nanmax(finite_drive) if np.any(np.isfinite(finite_drive)) else np.nan

        # Population-weighted average drive distance for NON-WALKABLE blocks only
        if non_walkable_blocks:
            nw_pops  = blocks_gdf.loc[non_walkable_blocks, "population"].values
            nw_drive = drive_df.loc[non_walkable_blocks, sid].replace([np.inf], np.nan).values
            with np.errstate(invalid="ignore"):
                avg_drive_nw = (np.nansum(nw_drive * nw_pops) / nw_pops.sum()
                                if nw_pops.sum() > 0 else np.nan)
        else:
            avg_drive_nw = np.nan

        metrics[sid] = {
            "school_id":                        sid,
            "assigned_population":              int(pop),
            "assigned_students":                round(float(stud), 1),
            "capacity":                         cap,
            "utilization_rate":                 round(float(stud) / cap, 3) if cap > 0 else None,
            "capacity_overflow":                max(0.0, round(float(stud) - cap, 1)),
            "pct_walkable":                     pct_walkable,
            "walkable_population":              int(walkable_pop),
            "walkable_students":                round(float(walkable_stud), 1),
            "non_walkable_students":            round(float(non_walk_stud), 1),
            "avg_walk_distance_m":              round(avg_walk, 1) if np.isfinite(avg_walk) else None,
            "avg_drive_distance_m":             round(avg_drive, 1) if np.isfinite(avg_drive) else None,
            "avg_drive_distance_non_walkable_m": round(avg_drive_nw, 1) if np.isfinite(avg_drive_nw) else None,
            "max_drive_distance_m":             round(max_drive, 1) if np.isfinite(max_drive) else None,
            "avg_drive_distance_mi":            round(avg_drive / 1609.34, 3) if np.isfinite(avg_drive) else None,
            "max_drive_distance_mi":            round(max_drive / 1609.34, 3) if np.isfinite(max_drive) else None,
            "avg_drive_non_walkable_mi":        round(avg_drive_nw / 1609.34, 3) if np.isfinite(avg_drive_nw) else None,
        }

    return metrics


def compute_scenario_metrics(scenario_name, assignments, blocks_gdf, open_schools,
                              walk_df, drive_df, adjacency):
    """Aggregate scenario-level metrics."""
    school_metrics = compute_school_metrics(
        assignments, blocks_gdf, open_schools, walk_df, drive_df
    )

    total_walkable_pop   = sum(m["walkable_population"]  for m in school_metrics.values())
    total_walkable_stud  = sum(m["walkable_students"]     for m in school_metrics.values())
    total_non_walk_stud  = sum(m["non_walkable_students"] for m in school_metrics.values())
    total_overflow       = sum(m["capacity_overflow"]     for m in school_metrics.values())
    total_stud           = sum(m["assigned_students"]     for m in school_metrics.values())

    all_drive    = [m["avg_drive_distance_m"] for m in school_metrics.values()
                    if m["avg_drive_distance_m"] is not None]
    all_max      = [m["max_drive_distance_m"] for m in school_metrics.values()
                    if m["max_drive_distance_m"] is not None]
    all_nw_drive = [m["avg_drive_distance_non_walkable_m"] for m in school_metrics.values()
                    if m["avg_drive_distance_non_walkable_m"] is not None]

    contiguity = validate_all_zones(assignments, adjacency)

    return {
        "scenario":                         scenario_name,
        "open_schools":                     list(open_schools["school_id"]),
        "total_walkable_population":        total_walkable_pop,
        "total_walkable_students":          round(total_walkable_stud, 1),
        "total_non_walkable_students":      round(total_non_walk_stud, 1),
        "pct_walkable":                     round(total_walkable_stud / total_stud * 100, 1) if total_stud > 0 else 0.0,
        "avg_drive_distance_m":             round(np.mean(all_drive), 1) if all_drive else None,
        "avg_drive_distance_mi":            round(np.mean(all_drive) / 1609.34, 3) if all_drive else None,
        "avg_drive_non_walkable_m":         round(np.mean(all_nw_drive), 1) if all_nw_drive else None,
        "avg_drive_non_walkable_mi":        round(np.mean(all_nw_drive) / 1609.34, 3) if all_nw_drive else None,
        "max_drive_distance_m":             round(max(all_max), 1) if all_max else None,
        "max_drive_distance_mi":            round(max(all_max) / 1609.34, 3) if all_max else None,
        "capacity_overflow":                round(total_overflow, 1),
        "capacity_feasible":                total_overflow == 0.0,
        "zone_contiguity":                  contiguity,
        "all_zones_contiguous":             all(contiguity.values()),
        "school_metrics":                   school_metrics,
    }


def build_summary_table(all_scenario_metrics: list) -> pd.DataFrame:
    """Build a ranked summary DataFrame comparing all scenarios."""
    rows = []
    for m in all_scenario_metrics:
        rows.append({
            "scenario":                    m["scenario"],
            "capacity_feasible":           m["capacity_feasible"],
            "pct_walkable":                m["pct_walkable"],
            "total_walkable_students":     m["total_walkable_students"],
            "total_non_walkable_students": m["total_non_walkable_students"],
            "avg_drive_distance_mi":       m["avg_drive_distance_mi"],
            "avg_drive_non_walkable_mi":   m["avg_drive_non_walkable_mi"],
            "max_drive_distance_mi":       m["max_drive_distance_mi"],
            "capacity_overflow":           m["capacity_overflow"],
            "all_zones_contiguous":        m["all_zones_contiguous"],
        })

    df = pd.DataFrame(rows)
    df["rank_drive"]    = df["avg_drive_distance_mi"].rank(ascending=True, na_option="bottom")
    df["rank_walkable"] = df["total_walkable_students"].rank(ascending=False, na_option="bottom")
    df["rank_overflow"] = df["capacity_overflow"].rank(ascending=True, na_option="bottom")
    df["composite_rank"] = (df["rank_drive"] + df["rank_walkable"] + df["rank_overflow"]) / 3
    df = df.sort_values("composite_rank").reset_index(drop=True)
    df.index += 1
    return df
