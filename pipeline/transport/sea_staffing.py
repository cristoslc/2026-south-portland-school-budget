#!/usr/bin/env python3
"""
SEA Staffing Adequacy Assessment (SPEC-062)

Assesses whether the post-cut SEA workforce (86 FTE, down from 100)
can cover expanded transportation routes under each configuration.

Data sources:
- SEA staffing: TC-016 (100 FTE → 86 FTE, 14% reduction)
- Driver count: Director of Operations Mike Natalie, 3/30/2026 BoE meeting
- Driver schedule: 7 AM–4 PM, idle 9:30–1:00/1:30 (same meeting)
- Transport per-pupil: Maine DOE FY23–FY25 resident expenditure reports
- Multi-year DOE trend: data/transport-per-pupil-multiyear.csv
"""

import json
from pathlib import Path

# === SEA STAFFING DATA ===
# Source: TC-016, FY27 budget documents

SEA_FTE_CURRENT = 100
SEA_FTE_POST_CUT = 86
SEA_CUT_PERCENT = 14

# === ACTUAL DRIVER COUNT ===
# Source: Director of Operations Mike Natalie, 3/30/2026 BoE meeting
# Quote: "Thereabouts there's 20 drivers."
# Context: Natalie described drivers on the clock 7 AM–4 PM, idle 9:30 to
# ~1:00/1:30. He proposed 4 drivers rotating into lunchtime support at
# elementary schools, capped at 2 hours/day.
#
# Important: "20 drivers" refers to bus DRIVERS specifically, not the full
# transport operation. The SEA unit also includes aides, mechanics, and
# dispatchers who support transportation. We estimate total transport FTE
# (including non-driver roles) at 25–28, based on 20 drivers + 5–8 support.

ACTUAL_DRIVERS = 20
TRANSPORT_SUPPORT_FTE_LOW = 5   # Aides, mechanics, dispatch (conservative)
TRANSPORT_SUPPORT_FTE_HIGH = 8  # Upper estimate
TRANSPORT_FTE_CURRENT_LOW = ACTUAL_DRIVERS + TRANSPORT_SUPPORT_FTE_LOW   # 25
TRANSPORT_FTE_CURRENT_HIGH = ACTUAL_DRIVERS + TRANSPORT_SUPPORT_FTE_HIGH  # 28

# Transport share of SEA: 25–28 out of 100 = 25–28%
# (Previously estimated at 30–35% from national benchmarks;
#  actual is lower, consistent with South Portland's mixed-function SEA unit)
TRANSPORT_SHARE_LOW = TRANSPORT_FTE_CURRENT_LOW / SEA_FTE_CURRENT  # 0.25
TRANSPORT_SHARE_HIGH = TRANSPORT_FTE_CURRENT_HIGH / SEA_FTE_CURRENT  # 0.28

# Post-cut transport FTE assuming proportional cut across all SEA functions
TRANSPORT_FTE_POST_CUT_LOW = round(SEA_FTE_POST_CUT * TRANSPORT_SHARE_LOW)  # 22
TRANSPORT_FTE_POST_CUT_HIGH = round(SEA_FTE_POST_CUT * TRANSPORT_SHARE_HIGH)  # 24

# Post-cut driver count specifically (proportional to 14% cut)
DRIVERS_POST_CUT_LOW = round(ACTUAL_DRIVERS * (1 - SEA_CUT_PERCENT / 100))  # 17
DRIVERS_POST_CUT_HIGH = ACTUAL_DRIVERS  # 20 (if cuts fall entirely on non-driver roles)

# === DRIVER SCHEDULE (confirmed 3/30/2026 meeting) ===
# Drivers on clock: 7:00 AM – 4:00 PM (9-hour shift)
# AM runs: ~7:00 – 9:30
# Idle window: 9:30 – 1:00/1:30 (~3.5 hours)
# PM runs: ~1:00/1:30 – 4:00
# This confirms a 3-tier bell schedule:
#   Tier 1 (HS): 8:10 start → AM run complete ~8:00
#   Tier 2 (MS): 8:30 start → AM run complete ~8:20
#   Tier 3 (Elem): 9:05 start → AM run complete ~9:30
# Each driver runs all 3 tiers sequentially in the AM, then reverse in PM.

DRIVER_SHIFT_START = "7:00"
DRIVER_SHIFT_END = "16:00"
AM_RUNS_COMPLETE = "9:30"
PM_RUNS_START = "13:00"  # ~1:00 PM (conservative; Natalie said 1:00-1:30)
IDLE_WINDOW_HOURS = 3.5

# === ROUTE ESTIMATION ===
# With 20 drivers confirmed, we can now ground route estimates:
# 20 drivers × 3 tiers (AM) = 60 route-runs per morning
# But drivers serve all tiers sequentially, so:
#   20 drivers × 1 route per tier × 3 tiers = 60 route-runs
#   = ~20 routes per tier level
# Elementary is 1 tier (5 schools) → 20 routes for elementary currently
# This aligns with: 1,013 students / 20 routes = ~51 students/route at capacity
# Accounting for walkers (~44% walkable with 5 schools):
#   ~570 bused students / 20 routes = ~29 students/route ← realistic bus load

CURRENT_ELEMENTARY_ROUTES = 20  # Grounded in 20 drivers, 1 elementary tier
STUDENTS_PER_ROUTE = 29  # Derived: ~570 bused / 20 routes


def estimate_routes(config_name, num_schools, grade_bands,
                    walkable_pct, total_students, notes=""):
    """Estimate route requirements for a configuration."""
    bused_students = round(total_students * (1 - walkable_pct))

    # Base: students per route from current operations
    base_routes = round(bused_students / STUDENTS_PER_ROUTE)

    # Adjustment factors
    # Fewer buildings = wider catchments → ~10% more routes per building lost
    building_reduction_factor = 1.0 + (5 - num_schools) * 0.10

    # Grade-band split = same-area students going to different buildings
    # Adds deadhead routes (bus passes through same neighborhood twice)
    grade_band_factor = 1.0 + (len(grade_bands) - 1) * 0.15

    adjusted_routes = round(base_routes * building_reduction_factor * grade_band_factor)

    # Driver count needed
    # With confirmed 3-tier sequential service, each driver covers 1 route per tier
    # Elementary routes need 1 driver each (driver also covers HS + MS tiers)
    drivers_needed = adjusted_routes  # 1:1 driver-to-elementary-route

    return {
        "configuration": config_name,
        "num_schools": num_schools,
        "grade_bands": grade_bands,
        "total_students": total_students,
        "walkable_pct": walkable_pct,
        "bused_students": bused_students,
        "students_per_route": STUDENTS_PER_ROUTE,
        "base_routes": base_routes,
        "building_reduction_factor": building_reduction_factor,
        "grade_band_factor": grade_band_factor,
        "estimated_routes": adjusted_routes,
        "drivers_needed": drivers_needed,
        "notes": notes,
    }


# Walkability drops from ~44% (5 schools) as catchments widen
OPTION_A_ROUTES = estimate_routes(
    "Option A", 4, ["PreK-1", "2-4"],
    walkable_pct=0.35,  # Wider catchments + grade-band routing reduces walkability
    total_students=1071,
    notes="Grade-band split means children from same neighborhood go to different buildings. "
          "Walkability decreases because assignment is by grade, not proximity.",
)

OPTION_B_ROUTES = estimate_routes(
    "Option B", 4, ["K-4"],
    walkable_pct=0.40,  # Slightly lower than current 5-school (44%) due to wider catchments
    total_students=1071,
    notes="Proximity-based assignment preserves neighborhood routing. "
          "Walkability only slightly reduced from losing one building.",
)

VARIANT_C_ROUTES = estimate_routes(
    "Variant C", 4, ["PreK-2", "3-4"],
    walkable_pct=0.37,  # Grade-band split reduces walkability, but less than Option A
    total_students=1071,
    notes="Grade 3-4 consolidated to one building means all grade 3-4 students bused there. "
          "PreK-2 still somewhat proximity-based across 3 buildings.",
)


def staffing_gap_analysis(route_estimate):
    """Assess staffing gap using actual driver count."""
    drivers_needed = route_estimate["drivers_needed"]

    return {
        "configuration": route_estimate["configuration"],
        "estimated_routes": route_estimate["estimated_routes"],
        "drivers_needed": drivers_needed,
        "current_drivers": ACTUAL_DRIVERS,
        "drivers_post_cut": {
            "low": DRIVERS_POST_CUT_LOW,
            "high": DRIVERS_POST_CUT_HIGH,
        },
        "transport_fte_post_cut": {
            "low": TRANSPORT_FTE_POST_CUT_LOW,
            "high": TRANSPORT_FTE_POST_CUT_HIGH,
        },
        "gap": {
            "best_case": DRIVERS_POST_CUT_HIGH - drivers_needed,  # No driver cuts
            "worst_case": DRIVERS_POST_CUT_LOW - drivers_needed,  # Proportional cuts
        },
        "adequate": DRIVERS_POST_CUT_HIGH >= drivers_needed,
    }


GAPS = []
for route_est in [OPTION_A_ROUTES, OPTION_B_ROUTES, VARIANT_C_ROUTES]:
    gap = staffing_gap_analysis(route_est)
    GAPS.append(gap)


def print_results():
    print("=" * 70)
    print("SEA STAFFING ADEQUACY ASSESSMENT — SPEC-062")
    print("=" * 70)
    print()
    print(f"SEA FTE: {SEA_FTE_CURRENT} → {SEA_FTE_POST_CUT} ({SEA_CUT_PERCENT}% cut)")
    print(f"Actual drivers (confirmed 3/30 meeting): {ACTUAL_DRIVERS}")
    print(f"Driver schedule: {DRIVER_SHIFT_START}–{DRIVER_SHIFT_END}, idle {AM_RUNS_COMPLETE}–{PM_RUNS_START}")
    print(f"Transport FTE (drivers + support): {TRANSPORT_FTE_CURRENT_LOW}–{TRANSPORT_FTE_CURRENT_HIGH}")
    print(f"Transport FTE post-cut: {TRANSPORT_FTE_POST_CUT_LOW}–{TRANSPORT_FTE_POST_CUT_HIGH}")
    print(f"Drivers post-cut: {DRIVERS_POST_CUT_LOW}–{DRIVERS_POST_CUT_HIGH}")
    print()

    print("### Route Estimates")
    for r in [OPTION_A_ROUTES, OPTION_B_ROUTES, VARIANT_C_ROUTES]:
        print(f"\n{r['configuration']}:")
        print(f"  Schools: {r['num_schools']}, Bands: {r['grade_bands']}")
        print(f"  Bused students: {r['bused_students']}")
        print(f"  Estimated routes: {r['estimated_routes']}")
        print(f"  Drivers needed: {r['drivers_needed']}")

    print("\n### Staffing Gap Analysis (Post-Cut)")
    print(f"{'Config':<12} {'Routes':<8} {'Drivers Needed':<16} {'Drivers Avail':<16} {'Gap':<20} {'Adequate?'}")
    print("-" * 80)
    for g in GAPS:
        gap_str = f"{g['gap']['worst_case']:+d} to {g['gap']['best_case']:+d}"
        print(f"{g['configuration']:<12} {g['estimated_routes']:<8} "
              f"{g['drivers_needed']:<16} "
              f"{g['drivers_post_cut']['low']}-{g['drivers_post_cut']['high']:<12} "
              f"{gap_str:<20} {'Possibly' if g['adequate'] else 'NO'}")

    return GAPS


def export_json(gaps, routes, path):
    output = {
        "spec": "SPEC-062",
        "title": "SEA Staffing Adequacy Assessment",
        "staffing": {
            "sea_fte_current": SEA_FTE_CURRENT,
            "sea_fte_post_cut": SEA_FTE_POST_CUT,
            "cut_percent": SEA_CUT_PERCENT,
            "actual_drivers": ACTUAL_DRIVERS,
            "driver_source": "Director of Operations Mike Natalie, 3/30/2026 BoE meeting",
            "driver_schedule": {
                "shift": f"{DRIVER_SHIFT_START}–{DRIVER_SHIFT_END}",
                "idle_window": f"{AM_RUNS_COMPLETE}–{PM_RUNS_START}",
                "idle_hours": IDLE_WINDOW_HOURS,
            },
            "transport_support_fte_range": f"{TRANSPORT_SUPPORT_FTE_LOW}–{TRANSPORT_SUPPORT_FTE_HIGH}",
            "transport_fte_current": f"{TRANSPORT_FTE_CURRENT_LOW}–{TRANSPORT_FTE_CURRENT_HIGH}",
            "transport_fte_post_cut": f"{TRANSPORT_FTE_POST_CUT_LOW}–{TRANSPORT_FTE_POST_CUT_HIGH}",
            "drivers_post_cut": f"{DRIVERS_POST_CUT_LOW}–{DRIVERS_POST_CUT_HIGH}",
        },
        "route_estimates": routes,
        "gap_analysis": gaps,
        "sources_of_error": [
            "20 drivers is bus drivers only — total transport FTE includes aides, mechanics, dispatch (estimated 5–8 additional)",
            "Post-cut driver count assumes proportional reduction across SEA functions; actual cuts could spare or target drivers specifically",
            "Route estimation uses aggregate model with adjustment factors (+10%/building, +15%/grade-band), not route-level analysis",
            "Students-per-route (29) derived from current fleet utilization; actual capacity may vary by route",
            "Walkability reduction from reconfiguration is estimated (35–40%), not modeled from walk-zone policy or GIS",
            "Does not account for specialized routes (SPED, MV, field trips) which require dedicated driver time",
            "SEA union meet-and-consult process (started 3/30) could change driver role assignments",
        ],
        "what_would_improve": [
            "District confirmation of which SEA positions are cut (driver vs. non-driver)",
            "Actual route manifests with student counts per route",
            "Walk-zone policy and GIS-derived walkability by configuration",
            "SPED and MV route requirements (separate from regular routes)",
            "Fleet vehicle count and capacity (distinct from driver count)",
        ],
    }
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w") as f:
        json.dump(output, f, indent=2)
    print(f"\nExported to {path}")


if __name__ == "__main__":
    gaps = print_results()
    export_json(
        GAPS,
        [OPTION_A_ROUTES, OPTION_B_ROUTES, VARIANT_C_ROUTES],
        "data/sea-staffing-assessment.json",
    )
