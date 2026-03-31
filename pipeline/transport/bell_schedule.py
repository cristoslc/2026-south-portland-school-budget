#!/usr/bin/env python3
"""
Bell Schedule Tier Analysis (SPEC-063)

Analyzes bus tier requirements under each configuration using
current bell schedule data from SPSD website.

Data sources:
- Current bell schedules: spsd.org (researched 2026-03-31)
- School geography trove
"""

import json
from pathlib import Path

# === CURRENT BELL SCHEDULE ===
# Source: https://www.spsd.org/families/school-start-dismissal-times

CURRENT_TIERS = {
    "Tier 1 (High School)": {"start": "8:10", "end": "2:25", "schools": ["SPHS"]},
    "Tier 2 (Middle School)": {"start": "8:30", "end": "2:45", "schools": ["SPMS"]},
    "Tier 3 (Elementary)": {"start": "9:05", "end": "3:05", "schools": ["Brown", "Dyer", "Kaler", "Small", "Skillin"]},
}

# Bus turnaround time between tiers
TURNAROUND_MINUTES = 25  # Time for bus to complete a route and start the next tier

# Current: 3 tiers, buses run HS → MS → Elementary
# Gap: HS ends 2:25, MS ends 2:45 (20 min gap), Elementary ends 3:05 (20 min gap)
# Morning: HS starts 8:10, MS starts 8:30 (20 min gap), Elementary starts 9:05 (35 min gap)


def analyze_current():
    """Document current tier structure."""
    return {
        "name": "Current (5 schools)",
        "tiers": 3,
        "schedule": CURRENT_TIERS,
        "notes": "All 5 elementary schools on single tier (Tier 3). "
                 "Buses run 3 tiers: HS → MS → Elementary. "
                 "35-minute gap between MS and elementary start allows full route coverage.",
        "feasible": True,
    }


def analyze_option_a():
    """
    Option A: 2 primary (PreK-1) + 2 intermediate (2-4)

    With 4 buildings but 2 grade bands, the question is: do primary and
    intermediate schools need different start times?

    If all 4 schools stay on the same tier (9:05 start): 3 tiers total, same as current.
    But: grade-band routing means some buses serve BOTH primary and intermediate
    buildings in the same tier, which may not be feasible if buildings are
    geographically dispersed.

    If primary and intermediate need different start times: 4 tiers required.
    This is challenging — typical maximum is 3 tiers for one bus fleet.
    """
    return {
        "name": "Option A",
        "description": "2 primary (PreK-1) + 2 intermediate (2-4), Kaler closed",
        "scenarios": [
            {
                "scenario": "All 4 elementary on same tier",
                "tiers_total": 3,
                "elementary_tiers": 1,
                "schedule": {
                    "HS": "8:10",
                    "MS": "8:30",
                    "All Elementary": "9:05",
                },
                "feasible": True,
                "risk": "Buses must serve both primary and intermediate buildings in one pass. "
                        "Grade-band routing (same neighborhood, different buildings) reduces efficiency. "
                        "Longer routes due to wider catchments may not fit in the tier window.",
                "family_impact": "Same start time for both bands — no scheduling conflict for split families.",
            },
            {
                "scenario": "Primary and intermediate on different tiers",
                "tiers_total": 4,
                "elementary_tiers": 2,
                "schedule": {
                    "HS": "8:10",
                    "MS": "8:30",
                    "Primary (PreK-1)": "8:50",
                    "Intermediate (2-4)": "9:20",
                },
                "feasible": "Marginal",
                "risk": "4 tiers strains fleet capacity. Either the earliest start (8:10) must move "
                        "earlier or the latest end moves later. Both affect families and drivers. "
                        "Most comparable districts max out at 3 tiers.",
                "family_impact": "Split families face 30-minute gap between drop-offs. "
                                 "A parent with a K student (8:50) and a 3rd grader (9:20) "
                                 "has a 30-minute wait between schools, or two separate trips.",
            },
        ],
        "likely_outcome": "The district would likely attempt same-tier (3 tiers) but may need "
                          "to split to 4 tiers if route times don't fit. The 4-tier scenario "
                          "has been attempted in similar districts and often forces compromises "
                          "on start times or route efficiency.",
    }


def analyze_option_b():
    """
    Option B: 4 buildings K-4, redistrict by proximity

    Same structure as current minus one school.
    All buildings serve same grades — single tier.
    """
    return {
        "name": "Option B",
        "description": "4 buildings K-4, Kaler closed, redistrict by proximity",
        "scenarios": [
            {
                "scenario": "All 4 elementary on same tier (same as current)",
                "tiers_total": 3,
                "elementary_tiers": 1,
                "schedule": {
                    "HS": "8:10",
                    "MS": "8:30",
                    "All Elementary": "9:05",
                },
                "feasible": True,
                "risk": "Wider catchments for 4 schools vs. 5 may stretch route times, "
                        "but single-tier simplicity is the same as current operation. "
                        "Routes are longer but conceptually identical.",
                "family_impact": "No change from current. All grades in every building, "
                                 "same start time.",
            },
        ],
        "likely_outcome": "Straightforward. Same 3-tier structure as current. "
                          "Wider catchments add route time but don't change tier count.",
    }


def analyze_variant_c():
    """
    Variant C: 3 buildings PreK-2 + 1 building Grades 3-4

    Similar to Option A but with uneven building distribution.
    The single grades 3-4 building serves ~404 students from across the city.
    """
    return {
        "name": "Variant C",
        "description": "3 buildings PreK-2 + 1 building Grades 3-4, Kaler closed",
        "scenarios": [
            {
                "scenario": "All 4 elementary on same tier",
                "tiers_total": 3,
                "elementary_tiers": 1,
                "schedule": {
                    "HS": "8:10",
                    "MS": "8:30",
                    "All Elementary": "9:05",
                },
                "feasible": "Marginal",
                "risk": "The single grades 3-4 building draws from the entire city — every "
                        "neighborhood must be served. This creates very long routes. "
                        "Combining these with PreK-2 routes in one tier may not fit "
                        "the time window, forcing a tier split.",
                "family_impact": "Same start time means no scheduling conflict, but the "
                                 "grades 3-4 building may need an earlier or later start "
                                 "to accommodate route length.",
            },
            {
                "scenario": "PreK-2 and 3-4 on different tiers",
                "tiers_total": 4,
                "elementary_tiers": 2,
                "schedule": {
                    "HS": "8:10",
                    "MS": "8:30",
                    "PreK-2": "8:50",
                    "Grades 3-4": "9:20",
                },
                "feasible": "Marginal",
                "risk": "Same 4-tier strain as Option A. Additionally, the single 3-4 "
                        "building's city-wide catchment means very long routes even "
                        "within its own tier.",
                "family_impact": "Split families face 30-minute gap between drop-offs. "
                                 "Worse than Option A because ALL grade 3-4 students go "
                                 "to one building — families are guaranteed a different "
                                 "building for their younger children.",
            },
        ],
        "likely_outcome": "Higher pressure toward 4 tiers than Option A because the single "
                          "grades 3-4 building creates city-wide routes that don't fit "
                          "neatly into a shared tier with neighborhood-based PreK-2 routes.",
    }


def print_results():
    configs = [analyze_current(), analyze_option_a(), analyze_option_b(), analyze_variant_c()]

    print("=" * 70)
    print("BELL SCHEDULE TIER ANALYSIS — SPEC-063")
    print("=" * 70)
    print()

    for cfg in configs:
        print(f"### {cfg['name']}")
        if "scenarios" in cfg:
            for s in cfg["scenarios"]:
                print(f"  Scenario: {s['scenario']}")
                print(f"    Tiers: {s['tiers_total']} | Feasible: {s['feasible']}")
                print(f"    Family impact: {s['family_impact']}")
            print(f"  Likely outcome: {cfg['likely_outcome']}")
        else:
            print(f"  Tiers: {cfg['tiers']} | Feasible: {cfg['feasible']}")
        print()

    return configs


def export_json(configs, path):
    output = {
        "spec": "SPEC-063",
        "title": "Bell Schedule Tier Analysis",
        "current_schedule": CURRENT_TIERS,
        "source": "https://www.spsd.org/families/school-start-dismissal-times",
        "turnaround_assumption_minutes": TURNAROUND_MINUTES,
        "configurations": configs,
        "limitations": [
            "Tier feasibility assessment is qualitative, not route-modeled",
            "Turnaround time assumption (25 min) is an estimate for South Portland geography",
            "Does not model specific route times — would require routing software",
            "Middle school bell time consolidation (deferred to fall 2027) could free a tier",
            "Fleet size unknown — tier analysis assumes current fleet is adequate for 3 tiers",
        ],
    }
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w") as f:
        json.dump(output, f, indent=2, default=str)
    print(f"\nExported to {path}")


if __name__ == "__main__":
    configs = print_results()
    export_json(
        [analyze_current(), analyze_option_a(), analyze_option_b(), analyze_variant_c()],
        "data/bell-schedule-analysis.json",
    )
