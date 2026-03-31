#!/usr/bin/env python3
"""
Transport Configuration Comparison (SPEC-065)

Assembles all EPIC-031 metric outputs into a structured comparison.
Capstone deliverable for INITIATIVE-006 V1.

Inputs: SPEC-060 through SPEC-064 outputs
Outputs: comparison doc + JSON for site consumption

Data sources added in V2 refresh:
- Multi-year DOE transport data (FY23–FY25): data/transport-per-pupil-multiyear.csv
- 20 bus drivers confirmed: Dir. of Operations Mike Natalie, 3/30/2026
- Diesel cost risk: flagged as "considerable" at 3/30 meeting, unquantified
"""

import json
from pathlib import Path

# Load all spec outputs
DATA_DIR = Path("data")

with open(DATA_DIR / "split-family-model.json") as f:
    split_data = json.load(f)

with open(DATA_DIR / "mckinney-vento-exposure.json") as f:
    mv_data = json.load(f)

with open(DATA_DIR / "sea-staffing-assessment.json") as f:
    sea_data = json.load(f)

with open(DATA_DIR / "bell-schedule-analysis.json") as f:
    bell_data = json.load(f)

with open(DATA_DIR / "before-after-care-gap.json") as f:
    care_data = json.load(f)

# District claimed savings for reference
CLAIMED_SAVINGS_LOW = 1_500_000
CLAIMED_SAVINGS_HIGH = 2_200_000

# === TRANSPORT COST BASELINES ===
# FY25 (most current): $1,065.44/pupil × 2,810 pupils = ~$2.99M
# FY23 (pre-anomaly): $709.49/pupil × 3,074 pupils = ~$2.18M
# South Portland's per-pupil transport costs rose 50.2% FY23→FY25 while
# the state average rose 10.5%. The cause is unknown.
TRANSPORT_PER_PUPIL_FY25 = 1065.44
TRANSPORT_PER_PUPIL_FY23 = 709.49
PUPILS_FY25 = 2810
PUPILS_FY23 = 3074
TOTAL_TRANSPORT_BUDGET_FY25 = round(TRANSPORT_PER_PUPIL_FY25 * PUPILS_FY25)
TOTAL_TRANSPORT_BUDGET_FY23 = round(TRANSPORT_PER_PUPIL_FY23 * PUPILS_FY23)


def extract_config(configs_list, name):
    """Extract a configuration from a list by name."""
    for cfg in configs_list:
        if cfg.get("configuration", cfg.get("name", "")) == name:
            return cfg
    return None


def build_comparison_row(config_name, transport_budget, budget_label):
    """Build a comparison row from all spec outputs."""
    # Split families (SPEC-060)
    split_cfg = extract_config(split_data["configurations"], config_name)
    split_low = split_cfg["split_families"]["low"]
    split_high = split_cfg["split_families"]["high"]

    # McKinney-Vento (SPEC-061)
    mv_cfg = extract_config(mv_data["configurations"], config_name)
    mv_annual_low = mv_cfg["annual_cost_range"]["low"]
    mv_annual_high = mv_cfg["annual_cost_range"]["high"]
    mv_total_low = mv_cfg["total_obligation_range"]["low"]
    mv_total_high = mv_cfg["total_obligation_range"]["high"]

    # SEA staffing (SPEC-062)
    sea_gap = extract_config(sea_data["gap_analysis"], config_name)
    sea_routes = sea_gap["estimated_routes"]
    sea_gap_best = sea_gap["gap"]["best_case"]
    sea_gap_worst = sea_gap["gap"]["worst_case"]
    drivers_needed = sea_gap["drivers_needed"]

    # Bell schedule (SPEC-063)
    bell_cfg = extract_config(bell_data["configurations"], config_name)
    if "scenarios" in bell_cfg:
        tiers_min = min(s["tiers_total"] for s in bell_cfg["scenarios"])
        tiers_max = max(s["tiers_total"] for s in bell_cfg["scenarios"])
    else:
        tiers_min = tiers_max = bell_cfg["tiers"]

    # Care gap (SPEC-064)
    care_cfg = extract_config(care_data["configurations"], config_name)
    care_scenarios = care_cfg["scenarios"]
    care_families_low = min(s["new_care_families"]["low"] for s in care_scenarios)
    care_families_high = max(s["new_care_families"]["high"] for s in care_scenarios)
    care_cost_low = min(s["total_annual_cost_burden"]["low"] for s in care_scenarios)
    care_cost_high = max(s["total_annual_cost_burden"]["high"] for s in care_scenarios)

    # Route expansion cost — Option B as baseline (fewest routes)
    option_b_routes = extract_config(sea_data["gap_analysis"], "Option B")["estimated_routes"]
    route_increase_pct = (sea_routes - option_b_routes) / option_b_routes
    route_cost_increase = round(transport_budget * max(0, route_increase_pct))

    # Total fiscal exposure
    # District costs: MV + route expansion
    # Family costs: care gap
    district_cost_low = mv_annual_low + route_cost_increase
    district_cost_high = mv_annual_high + route_cost_increase
    family_cost_low = care_cost_low
    family_cost_high = care_cost_high
    total_fiscal_low = district_cost_low + family_cost_low
    total_fiscal_high = district_cost_high + family_cost_high

    return {
        "configuration": config_name,
        "budget_baseline": budget_label,
        "split_families": f"{split_low}-{split_high}",
        "split_families_raw": {"low": split_low, "high": split_high},
        "mv_exposure_annual": f"${mv_annual_low:,}-${mv_annual_high:,}",
        "mv_exposure_annual_raw": {"low": mv_annual_low, "high": mv_annual_high},
        "mv_exposure_total": f"${mv_total_low:,}-${mv_total_high:,}",
        "sea_staffing_gap": f"{sea_gap_worst:+d} to {sea_gap_best:+d} drivers",
        "drivers_needed": drivers_needed,
        "sea_routes": sea_routes,
        "bus_tiers": f"{tiers_min}" if tiers_min == tiers_max else f"{tiers_min}-{tiers_max}",
        "bus_tiers_raw": {"min": tiers_min, "max": tiers_max},
        "care_gap_families": f"{care_families_low}-{care_families_high}",
        "care_gap_families_raw": {"low": care_families_low, "high": care_families_high},
        "care_gap_annual_cost": f"${care_cost_low:,}-${care_cost_high:,}",
        "care_gap_annual_cost_raw": {"low": care_cost_low, "high": care_cost_high},
        "route_expansion_cost": f"${route_cost_increase:,}",
        "route_expansion_cost_raw": route_cost_increase,
        "district_annual_cost": f"${district_cost_low:,}-${district_cost_high:,}",
        "district_annual_cost_raw": {"low": district_cost_low, "high": district_cost_high},
        "family_annual_cost": f"${family_cost_low:,}-${family_cost_high:,}",
        "family_annual_cost_raw": {"low": family_cost_low, "high": family_cost_high},
        "total_annual_fiscal_exposure": f"${total_fiscal_low:,}-${total_fiscal_high:,}",
        "total_annual_fiscal_exposure_raw": {"low": total_fiscal_low, "high": total_fiscal_high},
        "as_pct_of_claimed_savings": {
            "low": round(total_fiscal_low / CLAIMED_SAVINGS_HIGH * 100, 1),
            "high": round(total_fiscal_high / CLAIMED_SAVINGS_LOW * 100, 1),
        },
    }


# Primary analysis: FY25 baseline
OPTION_A = build_comparison_row("Option A", TOTAL_TRANSPORT_BUDGET_FY25, "FY25")
OPTION_B = build_comparison_row("Option B", TOTAL_TRANSPORT_BUDGET_FY25, "FY25")
VARIANT_C = build_comparison_row("Variant C", TOTAL_TRANSPORT_BUDGET_FY25, "FY25")

# Sensitivity: FY23 baseline (pre-anomaly)
OPTION_A_FY23 = build_comparison_row("Option A", TOTAL_TRANSPORT_BUDGET_FY23, "FY23")
OPTION_B_FY23 = build_comparison_row("Option B", TOTAL_TRANSPORT_BUDGET_FY23, "FY23")
VARIANT_C_FY23 = build_comparison_row("Variant C", TOTAL_TRANSPORT_BUDGET_FY23, "FY23")


def print_results():
    configs = [OPTION_A, OPTION_B, VARIANT_C]

    print("=" * 70)
    print("TRANSPORT CONFIGURATION COMPARISON — SPEC-065")
    print("=" * 70)
    print()
    print(f"Reference: Claimed savings from school closure: ${CLAIMED_SAVINGS_LOW:,}-${CLAIMED_SAVINGS_HIGH:,}")
    print(f"Current transport budget (FY25): ~${TOTAL_TRANSPORT_BUDGET_FY25:,}/year")
    print(f"Pre-anomaly transport budget (FY23): ~${TOTAL_TRANSPORT_BUDGET_FY23:,}/year")
    print()

    metrics = [
        ("Split families", "split_families"),
        ("MV exposure (annual)", "mv_exposure_annual"),
        ("SEA staffing gap", "sea_staffing_gap"),
        ("Drivers needed", "drivers_needed"),
        ("Bus tiers required", "bus_tiers"),
        ("Care gap (families)", "care_gap_families"),
        ("Care gap cost (annual)", "care_gap_annual_cost"),
        ("Route expansion cost", "route_expansion_cost"),
        ("District cost (annual)", "district_annual_cost"),
        ("Family cost (annual)", "family_annual_cost"),
        ("TOTAL fiscal exposure", "total_annual_fiscal_exposure"),
    ]

    print("PRIMARY ANALYSIS (FY25 baseline)")
    print(f"{'Metric':<28} {'Option A':<24} {'Option B':<24} {'Variant C':<24}")
    print("-" * 100)
    for label, key in metrics:
        vals = [str(cfg[key]) for cfg in configs]
        print(f"{label:<28} {vals[0]:<24} {vals[1]:<24} {vals[2]:<24}")

    print()
    for cfg in configs:
        pct = cfg["as_pct_of_claimed_savings"]
        print(f"{cfg['configuration']}: Total fiscal exposure = "
              f"{pct['low']}-{pct['high']}% of claimed savings")

    # Sensitivity
    sensitivity = [OPTION_A_FY23, OPTION_B_FY23, VARIANT_C_FY23]
    print(f"\nSENSITIVITY (FY23 baseline — pre-anomaly)")
    for cfg in sensitivity:
        pct = cfg["as_pct_of_claimed_savings"]
        print(f"  {cfg['configuration']}: ${cfg['total_annual_fiscal_exposure_raw']['low']:,}"
              f"-${cfg['total_annual_fiscal_exposure_raw']['high']:,} "
              f"({pct['low']}-{pct['high']}% of claimed savings)")

    return configs


def export_json(configs, path):
    sensitivity = [OPTION_A_FY23, OPTION_B_FY23, VARIANT_C_FY23]

    output = {
        "spec": "SPEC-065",
        "title": "Transport Configuration Comparison",
        "initiative": "INITIATIVE-006",
        "date": "2026-03-31",
        "version": "V2 — updated with 3/30 meeting data + multi-year DOE trends",
        "reference": {
            "claimed_savings": f"${CLAIMED_SAVINGS_LOW:,}-${CLAIMED_SAVINGS_HIGH:,}",
            "current_transport_budget_fy25": TOTAL_TRANSPORT_BUDGET_FY25,
            "transport_per_pupil_fy25": TRANSPORT_PER_PUPIL_FY25,
            "pre_anomaly_transport_budget_fy23": TOTAL_TRANSPORT_BUDGET_FY23,
            "transport_per_pupil_fy23": TRANSPORT_PER_PUPIL_FY23,
            "transport_trend_note": "South Portland per-pupil transport costs rose 50.2% FY23→FY25 "
                                   "(vs. state average +10.5%). Cause unknown.",
        },
        "configurations": configs,
        "sensitivity_fy23_baseline": sensitivity,
        "new_data_sources": {
            "driver_count": "Director of Operations Mike Natalie, 3/30/2026 BoE meeting: 20 drivers",
            "driver_schedule": "7 AM–4 PM, idle 9:30–1:30 (same meeting)",
            "multi_year_doe": "Maine DOE Resident Expenditure Per Pupil, FY23–FY25",
            "diesel_risk": "Board member Feller flagged 25-50% diesel cost increase; "
                          "Dir. of Operations called impact 'considerable' but could not quantify on the spot",
            "transport_logistics": "Superintendent confirmed transport logistics 'underway with a partner' "
                                   "but operationalized AFTER board vote, not before",
        },
        "source_specs": {
            "SPEC-060": "Split-Family Count Model",
            "SPEC-061": "McKinney-Vento Exposure Analysis",
            "SPEC-062": "SEA Staffing Adequacy Assessment",
            "SPEC-063": "Bell Schedule Tier Analysis",
            "SPEC-064": "Before/After Care Gap Analysis",
        },
        "key_finding": (
            "Option B (4 buildings K-4) has the lowest transportation impact across every metric. "
            "Option A (administration recommendation) has the highest impact on split families, "
            "McKinney-Vento obligations, route expansion, and before/after care gaps. "
            "The total unaccounted fiscal exposure under Option A ranges from "
            f"${configs[0]['total_annual_fiscal_exposure_raw']['low']:,} to "
            f"${configs[0]['total_annual_fiscal_exposure_raw']['high']:,} annually — "
            f"representing {configs[0]['as_pct_of_claimed_savings']['low']}-"
            f"{configs[0]['as_pct_of_claimed_savings']['high']}% of the claimed savings. "
            f"District-borne costs alone (excluding family care burden) are "
            f"${configs[0]['district_annual_cost_raw']['low']:,}-"
            f"${configs[0]['district_annual_cost_raw']['high']:,}."
        ),
        "cost_separation_note": (
            "This analysis separates district-budget costs (MV transport obligations + route expansion) "
            "from family-borne costs (before/after care gap). Both are real economic impacts of "
            "reconfiguration, but only district costs affect the claimed savings calculation directly."
        ),
        "sources_of_error": [
            "All figures are order-of-magnitude estimates, not precise calculations",
            "Route expansion cost is the largest and softest number — derived from aggregate model with "
            "adjustment heuristics (+10%/building, +15%/grade-band), not route-level analysis",
            "The FY25 transport baseline ($2.99M) may be anomalously high — sensitivity analysis with "
            "FY23 baseline ($2.18M) shows range under both assumptions",
            "Care gap costs are borne by families, not the district budget — separated in this analysis",
            "MV and SPED obligations are federal mandates regardless of district budgeting",
            "Diesel cost escalation (flagged 3/30 meeting) is unquantified and not included in estimates",
            "20-driver count is confirmed but post-cut allocation is unknown — cuts could spare or target drivers",
        ],
        "what_would_improve": [
            "Route-level modeling with actual fleet data and student addresses",
            "District confirmation of which SEA positions are cut",
            "Diesel cost projections from the district's fuel contract",
            "Walk-zone policy data for GIS-derived walkability",
            "The transport consultant's analysis (confirmed 'underway' at 3/30 meeting)",
        ],
        "invitation": (
            "The district has family-level enrollment data, route cost data, fleet size, "
            "SEA staffing breakdown, and care waitlist numbers that would replace every "
            "estimate in this comparison with facts. A transport consultant has been engaged "
            "(confirmed 3/30/2026). All methodology is documented and transparent. "
            "Corrections and data contributions are welcome."
        ),
    }
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w") as f:
        json.dump(output, f, indent=2)
    print(f"\nExported to {path}")


if __name__ == "__main__":
    configs = print_results()
    export_json(
        [OPTION_A, OPTION_B, VARIANT_C],
        "data/transport-comparison.json",
    )
