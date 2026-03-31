#!/usr/bin/env python3
"""
McKinney-Vento Exposure Analysis (SPEC-061)

Estimates the transportation cost obligations triggered by school closure
for McKinney-Vento eligible students under each configuration.

Data sources:
- MV eligibility rate: 10% district-wide (from evidence pools)
- Elementary enrollment: school-geography trove
- Transport per-pupil cost: maine-doe-transport-expenditure trove
"""

import json
from pathlib import Path

# === DATA ===

# McKinney-Vento eligibility
MV_DISTRICT_RATE = 0.10  # 10% of student body
TOTAL_DISTRICT_STUDENTS = 2744  # From evidence pools
TOTAL_ELEMENTARY_K4 = 1013
KALER_K4 = 135
KALER_WITH_PREK = 164

# Transport cost data (from maine-doe-transport-expenditure trove)
# Multi-year trend (data/transport-per-pupil-multiyear.csv):
#   FY23: $709.49  |  FY24: $940.16  |  FY25: $1,065.44
#   South Portland: +50.2% over 2 years vs. state average +10.5%
#   This anomalous increase is unexplained (possible contract renegotiation,
#   SPED transport growth, or reporting reclassification). We use FY25 as the
#   baseline because it is the most current data; sensitivity analysis in the
#   configuration comparison tests the FY23 baseline as an alternative.
SOPO_TRANSPORT_PER_PUPIL = 1065.44  # FY25
SOPO_TRANSPORT_PER_PUPIL_FY23 = 709.49  # For sensitivity analysis
STATE_AVG_TRANSPORT_PER_PUPIL = 1092.53

# Cost assumptions for incremental MV transport
# Incremental cost per displaced MV student is HIGHER than average per-pupil
# because these are individual or small-group routes, not marginal additions
# to existing routes. Factor of 1.5-3x is typical for individual transport.
INCREMENTAL_COST_MULTIPLIER_LOW = 1.5
INCREMENTAL_COST_MULTIPLIER_HIGH = 3.0

# Duration of obligation
# MV students have right to stay at school of origin through terminal grade.
# For elementary, that means through grade 4.
# Average remaining years depends on grade distribution of affected students.
AVG_OBLIGATION_YEARS_LOW = 1.5  # If students are mostly upper grades
AVG_OBLIGATION_YEARS_HIGH = 3.0  # If students are evenly distributed


def analyze_configuration(name, description, displaced_students_from_kaler,
                          additional_displacement=0, notes=""):
    """
    Analyze MV exposure for a configuration.

    displaced_students_from_kaler: Kaler students who must change schools
    additional_displacement: Extra displacement from redistricting beyond Kaler
    """
    # Estimate MV-eligible students among displaced population
    # Using district-wide rate as baseline; Kaler may have higher rate
    mv_displaced_low = round(displaced_students_from_kaler * MV_DISTRICT_RATE)
    mv_displaced_high = round(displaced_students_from_kaler * MV_DISTRICT_RATE * 1.5)  # Higher-need school adjustment

    mv_additional = round(additional_displacement * MV_DISTRICT_RATE)

    total_mv_low = mv_displaced_low + mv_additional
    total_mv_high = mv_displaced_high + mv_additional

    # Annual incremental transport cost per MV student
    cost_per_student_low = SOPO_TRANSPORT_PER_PUPIL * INCREMENTAL_COST_MULTIPLIER_LOW
    cost_per_student_high = SOPO_TRANSPORT_PER_PUPIL * INCREMENTAL_COST_MULTIPLIER_HIGH

    # Annual cost range
    annual_cost_low = total_mv_low * cost_per_student_low
    annual_cost_high = total_mv_high * cost_per_student_high

    # Total obligation (over duration)
    total_obligation_low = annual_cost_low * AVG_OBLIGATION_YEARS_LOW
    total_obligation_high = annual_cost_high * AVG_OBLIGATION_YEARS_HIGH

    return {
        "configuration": name,
        "description": description,
        "displaced_students": displaced_students_from_kaler + additional_displacement,
        "kaler_displaced": displaced_students_from_kaler,
        "redistricting_displaced": additional_displacement,
        "mv_eligible_displaced": {"low": total_mv_low, "high": total_mv_high},
        "incremental_annual_cost_per_student": {
            "low": round(cost_per_student_low),
            "high": round(cost_per_student_high),
        },
        "annual_cost_range": {
            "low": round(annual_cost_low),
            "high": round(annual_cost_high),
        },
        "total_obligation_range": {
            "low": round(total_obligation_low),
            "high": round(total_obligation_high),
        },
        "as_pct_of_claimed_savings": {
            "savings_range": "$1.5M-$2.2M",
            "annual_pct_low": round(annual_cost_low / 2_200_000 * 100, 1),
            "annual_pct_high": round(annual_cost_high / 1_500_000 * 100, 1),
        },
        "notes": notes,
    }


# All configurations close Kaler (135 K-4 students displaced)
# Option A also redistricts ALL remaining students into grade bands
# Option B redistricts by proximity (some students change schools)
# Variant C also redistricts into grade bands

OPTION_A = analyze_configuration(
    "Option A",
    "2 primary (PreK-1) + 2 intermediate (2-4), Kaler closed",
    displaced_students_from_kaler=135,
    additional_displacement=200,  # Significant redistricting: ALL students reassigned to grade-band schools
    notes="Every elementary student changes school assignment. All MV-eligible students district-wide are potentially affected.",
)

OPTION_B = analyze_configuration(
    "Option B",
    "4 buildings K-4, Kaler closed, redistrict by proximity",
    displaced_students_from_kaler=135,
    additional_displacement=50,  # Minimal redistricting: only students near Kaler reassigned
    notes="Only Kaler students displaced. Proximity-based reassignment minimizes disruption.",
)

VARIANT_C = analyze_configuration(
    "Variant C",
    "3 buildings PreK-2 + 1 building Grades 3-4, Kaler closed",
    displaced_students_from_kaler=135,
    additional_displacement=150,  # Moderate redistricting: grade 3-4 students consolidated
    notes="Kaler students displaced plus grade 3-4 students consolidated into one building.",
)


def print_results():
    configs = [OPTION_A, OPTION_B, VARIANT_C]

    print("=" * 70)
    print("McKINNEY-VENTO EXPOSURE ANALYSIS — SPEC-061")
    print("=" * 70)
    print()
    print(f"District MV rate: {MV_DISTRICT_RATE*100}%")
    print(f"Kaler K-4 enrollment: {KALER_K4}")
    print(f"Current transport cost/pupil: ${SOPO_TRANSPORT_PER_PUPIL:,.2f}")
    print()

    for cfg in configs:
        print(f"### {cfg['configuration']}: {cfg['description']}")
        print(f"  Displaced students: {cfg['displaced_students']} "
              f"(Kaler: {cfg['kaler_displaced']}, redistricting: {cfg['redistricting_displaced']})")
        mv = cfg["mv_eligible_displaced"]
        print(f"  MV-eligible displaced: {mv['low']}-{mv['high']} students")
        ac = cfg["annual_cost_range"]
        print(f"  Annual cost: ${ac['low']:,}-${ac['high']:,}")
        to = cfg["total_obligation_range"]
        print(f"  Total obligation: ${to['low']:,}-${to['high']:,}")
        pct = cfg["as_pct_of_claimed_savings"]
        print(f"  As % of claimed savings: {pct['annual_pct_low']}-{pct['annual_pct_high']}% annually")
        print()

    return configs


def export_json(configs, path):
    output = {
        "spec": "SPEC-061",
        "title": "McKinney-Vento Exposure Analysis",
        "methodology": {
            "mv_rate": MV_DISTRICT_RATE,
            "transport_per_pupil": SOPO_TRANSPORT_PER_PUPIL,
            "incremental_multiplier_range": f"{INCREMENTAL_COST_MULTIPLIER_LOW}-{INCREMENTAL_COST_MULTIPLIER_HIGH}x",
            "obligation_years_range": f"{AVG_OBLIGATION_YEARS_LOW}-{AVG_OBLIGATION_YEARS_HIGH}",
            "legal_basis": "42 U.S.C. § 11432 (McKinney-Vento Homeless Assistance Act)",
        },
        "configurations": configs,
        "limitations": [
            "10% MV rate is district-wide; Kaler may be higher or lower",
            "Incremental transport costs estimated via multiplier, not route-level modeling",
            "Obligation duration estimated from average grade distribution",
            "Does not include SPED transport obligations (separate analysis needed)",
            "Self-reported MV eligibility likely undercounts actual eligible population",
        ],
    }
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w") as f:
        json.dump(output, f, indent=2)
    print(f"\nExported to {path}")


if __name__ == "__main__":
    configs = print_results()
    export_json(
        [OPTION_A, OPTION_B, VARIANT_C],
        "data/mckinney-vento-exposure.json",
    )
