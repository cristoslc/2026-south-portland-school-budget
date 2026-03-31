#!/usr/bin/env python3
"""
Before/After Care Gap Analysis (SPEC-064)

Estimates the number of families facing care gaps from reconfiguration
and the cost implications.

Data sources:
- Split-family counts: SPEC-060 output
- Bell schedule tiers: SPEC-063 output
- Care rates: SoPo Kids Club (city-run program), researched 2026-03-31
"""

import json
from pathlib import Path

# === CARE RATE DATA ===
# Source: South Portland Recreation Department "SoPo Kids Club"
# https://southportlandme.myrec.com/info/activities/program_details.aspx?ProgramID=31539
# Operates in all 5 elementary school gyms, grades K-4

CARE_RATES_WEEKLY = {
    "before_only_5day": 75,
    "after_only_5day": 95,
    "before_and_after_5day": 155,
    "before_only_3day": 54,
    "after_only_3day": 66,
    "before_and_after_3day": 105,
}

SCHOOL_WEEKS_PER_YEAR = 36  # Approximate

# Care capacity finding: After care is FULL at 4 of 5 schools (Brown, Dyer, Skillin, Small)
# Only Kaler has openings — the school proposed for closure
CARE_WAITLIST_SCHOOLS = ["Brown", "Dyer", "Skillin", "Small"]
CARE_AVAILABLE_SCHOOLS = ["Kaler"]  # The one being closed

# === SPLIT FAMILY DATA (from SPEC-060) ===
SPLIT_FAMILIES = {
    "Option A": {"low": 139, "mid": 155, "high": 169},
    "Option B": {"low": 0, "mid": 0, "high": 0},
    "Variant C": {"low": 123, "mid": 137, "high": 150},
}

# === SCHEDULING MISMATCH ASSUMPTIONS ===
# Under 3-tier scenario: all elementary on same schedule (9:05-3:05)
# → No scheduling mismatch, but split families still face logistics burden
# Under 4-tier scenario: 30-minute gap between grade bands
# → Split families need care coverage for the gap

# Percentage of split families that would need additional care due to mismatch
# Under 3-tier: families may need care because of drop-off logistics (two buildings)
#   but times are the same, so pure care gap is minimal
# Under 4-tier: 30-minute gap means ALL split families have a scheduling mismatch
CARE_GAP_RATE_3TIER = 0.30  # Some families need extra care due to logistics
CARE_GAP_RATE_4TIER = 0.85  # Nearly all split families face a scheduling gap

# Current care users among all elementary families (baseline)
# 57% expressed concern about care disruption (TC-011)
# After care FULL at 4/5 schools indicates strong existing demand
# Estimate: ~40% of elementary families currently use some form of care
CURRENT_CARE_USAGE_RATE = 0.40


def analyze_care_gap(config_name, split_families, tier_scenarios):
    """Analyze care gap for a configuration."""
    results = []

    for scenario in tier_scenarios:
        tier_count = scenario["tiers"]
        gap_rate = CARE_GAP_RATE_4TIER if tier_count >= 4 else CARE_GAP_RATE_3TIER

        # Families with NEW care needs due to reconfiguration
        new_care_families = {
            level: round(count * gap_rate)
            for level, count in split_families.items()
        }

        # Annual cost per affected family (after-care only as minimum)
        annual_cost_after_only = CARE_RATES_WEEKLY["after_only_5day"] * SCHOOL_WEEKS_PER_YEAR
        annual_cost_full = CARE_RATES_WEEKLY["before_and_after_5day"] * SCHOOL_WEEKS_PER_YEAR

        # Total annual cost burden
        total_cost_low = new_care_families["low"] * annual_cost_after_only
        total_cost_high = new_care_families["high"] * annual_cost_full

        results.append({
            "scenario": scenario["name"],
            "tiers": tier_count,
            "split_families": split_families,
            "care_gap_rate": gap_rate,
            "new_care_families": new_care_families,
            "per_family_annual_cost": {
                "after_only": annual_cost_after_only,
                "before_and_after": annual_cost_full,
            },
            "total_annual_cost_burden": {
                "low": total_cost_low,
                "high": total_cost_high,
            },
        })

    return {
        "configuration": config_name,
        "scenarios": results,
    }


OPTION_A = analyze_care_gap("Option A", SPLIT_FAMILIES["Option A"], [
    {"name": "3 tiers (same elementary start)", "tiers": 3},
    {"name": "4 tiers (split elementary start)", "tiers": 4},
])

OPTION_B = analyze_care_gap("Option B", SPLIT_FAMILIES["Option B"], [
    {"name": "3 tiers (same as current)", "tiers": 3},
])

VARIANT_C = analyze_care_gap("Variant C", SPLIT_FAMILIES["Variant C"], [
    {"name": "3 tiers (same elementary start)", "tiers": 3},
    {"name": "4 tiers (split elementary start)", "tiers": 4},
])


def print_results():
    print("=" * 70)
    print("BEFORE/AFTER CARE GAP ANALYSIS — SPEC-064")
    print("=" * 70)
    print()
    print(f"SoPo Kids Club rates: ${CARE_RATES_WEEKLY['after_only_5day']}/week (after only), "
          f"${CARE_RATES_WEEKLY['before_and_after_5day']}/week (before+after)")
    print(f"Annual cost (36 weeks): ${CARE_RATES_WEEKLY['after_only_5day'] * 36} - "
          f"${CARE_RATES_WEEKLY['before_and_after_5day'] * 36}")
    print()
    print("CRITICAL FINDING: After care is FULL at 4 of 5 schools.")
    print(f"  Schools at capacity: {', '.join(CARE_WAITLIST_SCHOOLS)}")
    print(f"  Schools with openings: {', '.join(CARE_AVAILABLE_SCHOOLS)} (proposed for closure)")
    print()

    for cfg in [OPTION_A, OPTION_B, VARIANT_C]:
        print(f"### {cfg['configuration']}")
        for s in cfg["scenarios"]:
            ncf = s["new_care_families"]
            tc = s["total_annual_cost_burden"]
            print(f"  {s['scenario']}:")
            print(f"    New families needing care: {ncf['low']}-{ncf['high']}")
            print(f"    Total annual cost burden: ${tc['low']:,}-${tc['high']:,}")
        print()

    return [OPTION_A, OPTION_B, VARIANT_C]


def export_json(configs, path):
    output = {
        "spec": "SPEC-064",
        "title": "Before/After Care Gap Analysis",
        "care_rates": {
            "provider": "SoPo Kids Club (South Portland Recreation Department)",
            "source": "https://southportlandme.myrec.com/info/activities/program_details.aspx?ProgramID=31539",
            "rates_weekly": CARE_RATES_WEEKLY,
            "school_weeks": SCHOOL_WEEKS_PER_YEAR,
        },
        "capacity_finding": {
            "full_schools": CARE_WAITLIST_SCHOOLS,
            "available_schools": CARE_AVAILABLE_SCHOOLS,
            "note": "The only school with care openings is the one proposed for closure",
        },
        "configurations": configs,
        "limitations": [
            "Care gap rate (30% for 3-tier, 85% for 4-tier) is estimated",
            "Not all affected families would choose to use paid care",
            "Some families have informal care networks (family, neighbors)",
            "Cost estimate uses city program rates; private care may cost more",
            "Waitlist depth at full schools is unknown — actual unmet demand may be higher",
            "Does not include summer care transition costs",
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
        "data/before-after-care-gap.json",
    )
