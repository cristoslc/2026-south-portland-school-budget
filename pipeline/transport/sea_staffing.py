#!/usr/bin/env python3
"""
SEA Staffing Adequacy Assessment (SPEC-062)

Assesses whether the post-cut SEA workforce (86 FTE, down from 100)
can cover expanded transportation routes under each configuration.

Data sources:
- SEA staffing: TC-016 (100 FTE → 86 FTE, 14% reduction)
- Transport per-pupil: maine-doe-transport-expenditure trove
- Peer district ratios: derived from DOE data
"""

import json
from pathlib import Path

# === SEA STAFFING DATA ===
# Source: TC-016, FY27 budget documents

SEA_FTE_CURRENT = 100
SEA_FTE_POST_CUT = 86
SEA_CUT_PERCENT = 14

# SEA covers three functions: facilities, food, transport
# Budget documents don't break out transport-specific FTE
# Estimate: based on typical district allocation patterns
#
# National benchmarks (NCES School District Finance Survey):
# - Transport staff typically 30-40% of operations support staff
# - For a district of ~2,800 students with 5 elementary + 1 middle + 1 high:
#   ~25-35 bus drivers/aides is typical
#
# We estimate transport share at 30-35% of SEA

TRANSPORT_SHARE_LOW = 0.30
TRANSPORT_SHARE_HIGH = 0.35

# Current transport FTE estimate
TRANSPORT_FTE_CURRENT_LOW = round(SEA_FTE_CURRENT * TRANSPORT_SHARE_LOW)
TRANSPORT_FTE_CURRENT_HIGH = round(SEA_FTE_CURRENT * TRANSPORT_SHARE_HIGH)

# Post-cut transport FTE (assuming proportional cut across functions)
TRANSPORT_FTE_POST_CUT_LOW = round(SEA_FTE_POST_CUT * TRANSPORT_SHARE_LOW)
TRANSPORT_FTE_POST_CUT_HIGH = round(SEA_FTE_POST_CUT * TRANSPORT_SHARE_HIGH)

# === ROUTE ESTIMATION ===
# Current: 5 elementary schools, tiered bus service
# South Portland transport spend: $1,065/pupil × 2,810 = ~$2.99M
# Average driver cost (salary + benefits): ~$45-55K (Maine bus driver wages)
# This implies roughly 54-66 total route-equivalents (all levels)
# Elementary share: ~50-60% of routes (5 of 7 schools)

CURRENT_ELEMENTARY_ROUTES_LOW = 27
CURRENT_ELEMENTARY_ROUTES_HIGH = 40

# Students per route: 1,013 students / 27-40 routes = 25-38 students/route
# This aligns with typical Maine school bus capacity utilization


def estimate_routes(config_name, num_schools, grade_bands,
                    walkable_pct, total_students, notes=""):
    """Estimate route requirements for a configuration."""
    bused_students = round(total_students * (1 - walkable_pct))

    # More buildings with wider geographic catchments need more routes
    # Fewer buildings = wider catchments = longer routes = need more routes
    # Grade-band splits add routes because students in same area go to different schools

    # Base: students per route efficiency
    students_per_route = 33  # midpoint estimate for South Portland

    base_routes = round(bused_students / students_per_route)

    # Adjustment factors
    # Fewer buildings = wider catchments = ~10% more routes per building lost
    building_reduction_factor = 1.0 + (5 - num_schools) * 0.10

    # Grade-band split = same-area students going to different buildings
    # adds deadhead routes
    grade_band_factor = 1.0 + (len(grade_bands) - 1) * 0.15

    adjusted_routes = round(base_routes * building_reduction_factor * grade_band_factor)

    # Driver FTE needed (1 route ≈ 1 driver, but some drivers do 2 tiers)
    # With tiered service, driver FTE = routes / tiers_per_driver
    # Typically 1.5-2 tiers per driver
    driver_fte_low = round(adjusted_routes / 2.0)
    driver_fte_high = round(adjusted_routes / 1.5)

    return {
        "configuration": config_name,
        "num_schools": num_schools,
        "grade_bands": grade_bands,
        "total_students": total_students,
        "walkable_pct": walkable_pct,
        "bused_students": bused_students,
        "students_per_route": students_per_route,
        "base_routes": base_routes,
        "building_reduction_factor": building_reduction_factor,
        "grade_band_factor": grade_band_factor,
        "estimated_routes": adjusted_routes,
        "driver_fte_needed": {"low": driver_fte_low, "high": driver_fte_high},
        "notes": notes,
    }


# Walkability drops from ~44% (5 schools) as catchments widen
# Redistricting tool data: ~44% walkable under 5-school config
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


def staffing_gap_analysis(route_estimate, transport_fte_low, transport_fte_high):
    """Assess staffing gap."""
    driver_low = route_estimate["driver_fte_needed"]["low"]
    driver_high = route_estimate["driver_fte_needed"]["high"]

    return {
        "configuration": route_estimate["configuration"],
        "estimated_routes": route_estimate["estimated_routes"],
        "driver_fte_needed": route_estimate["driver_fte_needed"],
        "transport_fte_available": {"low": transport_fte_low, "high": transport_fte_high},
        "gap": {
            "best_case": transport_fte_high - driver_low,  # Most FTE, fewest drivers needed
            "worst_case": transport_fte_low - driver_high,  # Fewest FTE, most drivers needed
        },
        "adequate": transport_fte_high >= driver_low,  # Is there ANY scenario where it works?
    }


GAPS = []
for route_est in [OPTION_A_ROUTES, OPTION_B_ROUTES, VARIANT_C_ROUTES]:
    gap = staffing_gap_analysis(
        route_est,
        TRANSPORT_FTE_POST_CUT_LOW,
        TRANSPORT_FTE_POST_CUT_HIGH,
    )
    GAPS.append(gap)


def print_results():
    print("=" * 70)
    print("SEA STAFFING ADEQUACY ASSESSMENT — SPEC-062")
    print("=" * 70)
    print()
    print(f"SEA FTE: {SEA_FTE_CURRENT} → {SEA_FTE_POST_CUT} ({SEA_CUT_PERCENT}% cut)")
    print(f"Estimated transport share: {TRANSPORT_SHARE_LOW*100:.0f}-{TRANSPORT_SHARE_HIGH*100:.0f}%")
    print(f"Transport FTE pre-cut: {TRANSPORT_FTE_CURRENT_LOW}-{TRANSPORT_FTE_CURRENT_HIGH}")
    print(f"Transport FTE post-cut: {TRANSPORT_FTE_POST_CUT_LOW}-{TRANSPORT_FTE_POST_CUT_HIGH}")
    print()

    print("### Route Estimates")
    for r in [OPTION_A_ROUTES, OPTION_B_ROUTES, VARIANT_C_ROUTES]:
        print(f"\n{r['configuration']}:")
        print(f"  Schools: {r['num_schools']}, Bands: {r['grade_bands']}")
        print(f"  Bused students: {r['bused_students']}")
        print(f"  Estimated routes: {r['estimated_routes']}")
        print(f"  Driver FTE needed: {r['driver_fte_needed']['low']}-{r['driver_fte_needed']['high']}")

    print("\n### Staffing Gap Analysis (Post-Cut)")
    print(f"{'Config':<12} {'Routes':<8} {'Drivers Needed':<16} {'FTE Available':<16} {'Gap':<20} {'Adequate?'}")
    print("-" * 80)
    for g in GAPS:
        gap_str = f"{g['gap']['worst_case']:+d} to {g['gap']['best_case']:+d}"
        print(f"{g['configuration']:<12} {g['estimated_routes']:<8} "
              f"{g['driver_fte_needed']['low']}-{g['driver_fte_needed']['high']:<12} "
              f"{g['transport_fte_available']['low']}-{g['transport_fte_available']['high']:<12} "
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
            "transport_share_range": f"{TRANSPORT_SHARE_LOW}-{TRANSPORT_SHARE_HIGH}",
            "transport_fte_pre_cut": f"{TRANSPORT_FTE_CURRENT_LOW}-{TRANSPORT_FTE_CURRENT_HIGH}",
            "transport_fte_post_cut": f"{TRANSPORT_FTE_POST_CUT_LOW}-{TRANSPORT_FTE_POST_CUT_HIGH}",
        },
        "route_estimates": routes,
        "gap_analysis": gaps,
        "limitations": [
            "SEA transport share estimated — actual breakdown not in budget documents",
            "Route estimation uses aggregate model, not route-level analysis",
            "Driver FTE assumes typical tier utilization (1.5-2 tiers per driver)",
            "Does not account for specialized routes (SPED, MV, field trips)",
            "Walkability reduction from reconfiguration is estimated, not modeled",
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
