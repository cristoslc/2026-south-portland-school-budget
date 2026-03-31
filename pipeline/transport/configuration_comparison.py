#!/usr/bin/env python3
"""
Transport Configuration Comparison (SPEC-065)

Assembles all EPIC-031 metric outputs into a structured comparison.
Capstone deliverable for INITIATIVE-006 V1.

Inputs: SPEC-060 through SPEC-064 outputs
Outputs: comparison doc + JSON for site consumption
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
TRANSPORT_PER_PUPIL = 1065.44
TOTAL_TRANSPORT_BUDGET = round(TRANSPORT_PER_PUPIL * 2810)


def extract_config(configs_list, name):
    """Extract a configuration from a list by name."""
    for cfg in configs_list:
        if cfg.get("configuration", cfg.get("name", "")) == name:
            return cfg
    return None


def build_comparison_row(config_name):
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

    # Total fiscal exposure (MV + care costs borne by families + implied route expansion)
    # Route expansion cost estimate from DOE data
    route_increase_pct = (sea_routes - 21) / 21  # vs Option B baseline
    route_cost_increase = round(TOTAL_TRANSPORT_BUDGET * max(0, route_increase_pct))

    total_fiscal_low = mv_annual_low + care_cost_low + route_cost_increase
    total_fiscal_high = mv_annual_high + care_cost_high + route_cost_increase

    return {
        "configuration": config_name,
        "split_families": f"{split_low}-{split_high}",
        "split_families_raw": {"low": split_low, "high": split_high},
        "mv_exposure_annual": f"${mv_annual_low:,}-${mv_annual_high:,}",
        "mv_exposure_annual_raw": {"low": mv_annual_low, "high": mv_annual_high},
        "mv_exposure_total": f"${mv_total_low:,}-${mv_total_high:,}",
        "sea_staffing_gap": f"{sea_gap_worst:+d} to {sea_gap_best:+d} FTE",
        "sea_routes": sea_routes,
        "bus_tiers": f"{tiers_min}" if tiers_min == tiers_max else f"{tiers_min}-{tiers_max}",
        "bus_tiers_raw": {"min": tiers_min, "max": tiers_max},
        "care_gap_families": f"{care_families_low}-{care_families_high}",
        "care_gap_families_raw": {"low": care_families_low, "high": care_families_high},
        "care_gap_annual_cost": f"${care_cost_low:,}-${care_cost_high:,}",
        "care_gap_annual_cost_raw": {"low": care_cost_low, "high": care_cost_high},
        "route_expansion_cost": f"${route_cost_increase:,}",
        "route_expansion_cost_raw": route_cost_increase,
        "total_annual_fiscal_exposure": f"${total_fiscal_low:,}-${total_fiscal_high:,}",
        "total_annual_fiscal_exposure_raw": {"low": total_fiscal_low, "high": total_fiscal_high},
        "as_pct_of_claimed_savings": {
            "low": round(total_fiscal_low / CLAIMED_SAVINGS_HIGH * 100, 1),
            "high": round(total_fiscal_high / CLAIMED_SAVINGS_LOW * 100, 1),
        },
    }


OPTION_A = build_comparison_row("Option A")
OPTION_B = build_comparison_row("Option B")
VARIANT_C = build_comparison_row("Variant C")


def print_results():
    configs = [OPTION_A, OPTION_B, VARIANT_C]

    print("=" * 70)
    print("TRANSPORT CONFIGURATION COMPARISON — SPEC-065")
    print("=" * 70)
    print()
    print(f"Reference: Claimed savings from school closure: ${CLAIMED_SAVINGS_LOW:,}-${CLAIMED_SAVINGS_HIGH:,}")
    print(f"Current transport budget: ~${TOTAL_TRANSPORT_BUDGET:,}/year")
    print()

    # Comparison table
    metrics = [
        ("Split families", "split_families"),
        ("MV exposure (annual)", "mv_exposure_annual"),
        ("SEA staffing gap", "sea_staffing_gap"),
        ("Bus tiers required", "bus_tiers"),
        ("Care gap (families)", "care_gap_families"),
        ("Care gap cost (annual)", "care_gap_annual_cost"),
        ("Route expansion cost", "route_expansion_cost"),
        ("TOTAL fiscal exposure", "total_annual_fiscal_exposure"),
    ]

    print(f"{'Metric':<28} {'Option A':<22} {'Option B':<22} {'Variant C':<22}")
    print("-" * 94)
    for label, key in metrics:
        vals = [cfg[key] for cfg in configs]
        print(f"{label:<28} {vals[0]:<22} {vals[1]:<22} {vals[2]:<22}")

    print()
    for cfg in configs:
        pct = cfg["as_pct_of_claimed_savings"]
        print(f"{cfg['configuration']}: Total fiscal exposure = "
              f"{pct['low']}-{pct['high']}% of claimed savings")

    return configs


def export_json(configs, path):
    output = {
        "spec": "SPEC-065",
        "title": "Transport Configuration Comparison",
        "initiative": "INITIATIVE-006",
        "date": "2026-03-31",
        "reference": {
            "claimed_savings": f"${CLAIMED_SAVINGS_LOW:,}-${CLAIMED_SAVINGS_HIGH:,}",
            "current_transport_budget": TOTAL_TRANSPORT_BUDGET,
            "transport_per_pupil": TRANSPORT_PER_PUPIL,
        },
        "configurations": configs,
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
            f"{configs[0]['as_pct_of_claimed_savings']['high']}% of the claimed savings."
        ),
        "limitations": [
            "All figures are order-of-magnitude estimates, not precise calculations",
            "Ranges reflect uncertainty in assumptions, not confidence intervals",
            "Route expansion cost uses aggregate model, not route-level analysis",
            "Care gap costs are borne by families, not the district budget",
            "MV and SPED obligations are federal mandates regardless of district budgeting",
            "This analysis does not recommend a configuration — it surfaces missing data",
        ],
        "invitation": (
            "The district has family-level enrollment data, route cost data, fleet size, "
            "SEA staffing breakdown, and care waitlist numbers that would replace every "
            "estimate in this comparison with facts. All methodology is documented and "
            "transparent. Corrections and data contributions are welcome."
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
