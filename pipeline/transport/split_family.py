#!/usr/bin/env python3
"""
Split-Family Count Model (SPEC-060)

Estimates the number of families with children in two different buildings
under each reconfiguration option.

Data sources:
- Enrollment by grade: school-geography trove (schools.json)
- Sibling co-enrollment rate: Census Bureau SIPP / education research
"""

import json
import math
from pathlib import Path

# === ENROLLMENT DATA (2025-26) ===
# Source: docs/troves/school-geography/schools.json

ENROLLMENT_BY_GRADE = {
    "PreK": 58,  # Dyer 29 + Kaler 29
    "K": 191,    # Brown 29 + Dyer 35 + Kaler 26 + Small 33 + Skillin 68
    "1": 200,    # Brown 44 + Dyer 28 + Kaler 33 + Small 39 + Skillin 56
    "2": 218,    # Brown 46 + Dyer 39 + Kaler 30 + Small 39 + Skillin 64
    "3": 189,    # Brown 38 + Dyer 25 + Kaler 26 + Small 42 + Skillin 58
    "4": 215,    # Brown 37 + Dyer 39 + Kaler 20 + Small 46 + Skillin 73
}

TOTAL_K4 = 1013  # From schools.json
TOTAL_WITH_PREK = 1071


# === SIBLING CO-ENROLLMENT ASSUMPTIONS ===
# Source: Census Bureau SIPP data, NCES family composition research
#
# Key parameters:
# - ~35% of elementary families have 2+ children in the system (range: 30-40%)
#   Ref: Census Bureau, "School Enrollment of Young Children" (SIPP surveys)
#   Ref: NCES Condition of Education, household composition tables
# - Average family size for multi-child families: ~2.3 children in system
# - Sibling grade gaps are roughly uniformly distributed across 0-5 years

# Estimated total elementary families (students / avg children per family)
# Single-child families: ~65% of families have 1 child
# Multi-child families: ~35% have 2+ children, avg 2.3 children
# Total students = (0.65 * F * 1) + (0.35 * F * 2.3) = F * (0.65 + 0.805) = F * 1.455
# F = 1013 / 1.455 ≈ 696 families
# With PreK: 1071 / 1.455 ≈ 736 families

MULTI_CHILD_RATE_LOW = 0.30
MULTI_CHILD_RATE_MID = 0.35
MULTI_CHILD_RATE_HIGH = 0.40
AVG_CHILDREN_MULTI = 2.3


def estimate_families(total_students, multi_child_rate=0.35, avg_multi=2.3):
    """Estimate total families from student count and sibling rates."""
    # total_students = single_families * 1 + multi_families * avg_multi
    # single_families = (1 - multi_child_rate) * total_families
    # multi_families = multi_child_rate * total_families
    # total_students = total_families * ((1 - multi_child_rate) + multi_child_rate * avg_multi)
    family_multiplier = (1 - multi_child_rate) + multi_child_rate * avg_multi
    return total_students / family_multiplier


def grade_boundary_split_probability(boundary_grade, grades_below, grades_above):
    """
    Estimate the probability that a multi-child family spans a grade boundary.

    For a family with 2 children in grades drawn from PreK-4 (6 grades),
    the probability that one child is in grades_below and the other in grades_above
    depends on the sibling grade gap distribution.

    Simplification: assume sibling pairs have grade gaps of 1-5 years with
    roughly equal probability (uniform distribution). Then compute what fraction
    of possible grade pairs span the boundary.
    """
    total_grade_slots = len(grades_below) + len(grades_above)
    # For 2 children: number of ordered pairs that span the boundary
    spanning_pairs = 0
    total_pairs = 0

    for g1 in range(total_grade_slots):
        for g2 in range(total_grade_slots):
            if g1 == g2:
                continue
            total_pairs += 1
            g1_below = g1 < len(grades_below)
            g2_below = g2 < len(grades_below)
            if g1_below != g2_below:
                spanning_pairs += 1

    return spanning_pairs / total_pairs if total_pairs > 0 else 0


def model_configuration(name, description, grade_bands, include_prek=True):
    """
    Model split-family count for a configuration.

    grade_bands: list of (band_name, grade_list) tuples
    If there's only one band, split families = 0.
    If there are two bands, calculate boundary-spanning probability.
    """
    result = {
        "configuration": name,
        "description": description,
        "grade_bands": {band: grades for band, grades in grade_bands},
        "num_buildings_per_band": {},
    }

    if len(grade_bands) <= 1:
        # No grade-band split — all K-4 in every building
        result["split_families"] = {"low": 0, "mid": 0, "high": 0}
        result["split_families_pct"] = {"low": 0.0, "mid": 0.0, "high": 0.0}
        result["explanation"] = "No grade-band split. All grades in every building. Siblings always attend the same school (assuming proximity-based assignment)."
        return result

    # For two-band configurations, compute the split probability
    band1_name, band1_grades = grade_bands[0]
    band2_name, band2_grades = grade_bands[1]

    # Count students on each side
    band1_students = sum(ENROLLMENT_BY_GRADE.get(g, 0) for g in band1_grades)
    band2_students = sum(ENROLLMENT_BY_GRADE.get(g, 0) for g in band2_grades)
    total = band1_students + band2_students

    result["students_per_band"] = {
        band1_name: band1_students,
        band2_name: band2_students,
    }

    # Probability a multi-child family spans the boundary
    split_prob = grade_boundary_split_probability(
        None, band1_grades, band2_grades
    )

    result["boundary_split_probability"] = round(split_prob, 3)

    # Calculate split families for low/mid/high sibling rates
    estimates = {}
    pct_estimates = {}
    for label, rate in [("low", MULTI_CHILD_RATE_LOW),
                        ("mid", MULTI_CHILD_RATE_MID),
                        ("high", MULTI_CHILD_RATE_HIGH)]:
        total_families = estimate_families(total, rate)
        multi_families = total_families * rate
        split_families = multi_families * split_prob
        estimates[label] = round(split_families)
        pct_estimates[label] = round(split_families / total_families * 100, 1)

    result["total_families_est"] = {
        "low": round(estimate_families(total, MULTI_CHILD_RATE_LOW)),
        "mid": round(estimate_families(total, MULTI_CHILD_RATE_MID)),
        "high": round(estimate_families(total, MULTI_CHILD_RATE_HIGH)),
    }
    result["multi_child_families_est"] = {
        "low": round(estimate_families(total, MULTI_CHILD_RATE_LOW) * MULTI_CHILD_RATE_LOW),
        "mid": round(estimate_families(total, MULTI_CHILD_RATE_MID) * MULTI_CHILD_RATE_MID),
        "high": round(estimate_families(total, MULTI_CHILD_RATE_HIGH) * MULTI_CHILD_RATE_HIGH),
    }
    result["split_families"] = estimates
    result["split_families_pct"] = pct_estimates

    return result


# === CONFIGURATIONS ===

OPTION_A = model_configuration(
    "Option A",
    "2 primary (PreK-1) + 2 intermediate (2-4), Kaler closed",
    [
        ("Primary (PreK-1)", ["PreK", "K", "1"]),
        ("Intermediate (2-4)", ["2", "3", "4"]),
    ],
)

OPTION_B = model_configuration(
    "Option B",
    "4 buildings K-4, Kaler closed, redistrict by proximity",
    [
        ("K-4 (all buildings)", ["PreK", "K", "1", "2", "3", "4"]),
    ],
)

VARIANT_C = model_configuration(
    "Variant C",
    "3 buildings PreK-2 + 1 building Grades 3-4, Kaler closed",
    [
        ("PreK-2", ["PreK", "K", "1", "2"]),
        ("Grades 3-4", ["3", "4"]),
    ],
)


def print_results():
    """Print formatted results for all configurations."""
    configs = [OPTION_A, OPTION_B, VARIANT_C]

    print("=" * 70)
    print("SPLIT-FAMILY COUNT MODEL — SPEC-060")
    print("=" * 70)
    print()

    for cfg in configs:
        print(f"### {cfg['configuration']}: {cfg['description']}")
        print(f"  Grade bands: {cfg['grade_bands']}")
        if "students_per_band" in cfg:
            for band, count in cfg["students_per_band"].items():
                print(f"  {band}: {count} students")
            print(f"  Boundary split probability: {cfg['boundary_split_probability']}")
        print(f"  Estimated split families (low/mid/high): "
              f"{cfg['split_families']['low']} / {cfg['split_families']['mid']} / {cfg['split_families']['high']}")
        print(f"  As % of families: "
              f"{cfg['split_families_pct']['low']}% / {cfg['split_families_pct']['mid']}% / {cfg['split_families_pct']['high']}%")
        if "explanation" in cfg:
            print(f"  Note: {cfg['explanation']}")
        print()

    # Comparison table
    print("### COMPARISON TABLE")
    print(f"{'Config':<12} {'Split Families (range)':<25} {'% of Families':<20}")
    print("-" * 57)
    for cfg in configs:
        sf = cfg["split_families"]
        pct = cfg["split_families_pct"]
        print(f"{cfg['configuration']:<12} {sf['low']}-{sf['high']:<23} {pct['low']}-{pct['high']}%")

    return configs


def export_json(configs, path):
    """Export results as JSON for downstream consumption."""
    output = {
        "spec": "SPEC-060",
        "title": "Split-Family Count Model",
        "methodology": {
            "approach": "Grade boundary probability model with sibling co-enrollment rates",
            "sibling_rate_range": f"{MULTI_CHILD_RATE_LOW}-{MULTI_CHILD_RATE_HIGH}",
            "sibling_rate_source": "Census Bureau SIPP; NCES household composition",
            "avg_children_multi_child": AVG_CHILDREN_MULTI,
            "enrollment_source": "school-geography trove (2025-26 data)",
            "total_k4_students": TOTAL_K4,
        },
        "configurations": configs,
        "limitations": [
            "Estimate, not precise count — no family-level enrollment data available",
            "Sibling rate assumptions from national data; South Portland may differ",
            "Uniform grade-gap distribution assumed; actual may skew toward 1-2 year gaps",
            "Does not account for families who might choose to opt out of the system",
            "PreK families included where applicable but PreK is not mandatory",
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
        "data/split-family-model.json",
    )
