# Transportation Analysis Methodology

**Initiative:** INITIATIVE-006 | **Date:** 2026-03-31

---

This document describes the methodology, assumptions, and limitations of each analysis in the independent transportation study. Every assumption is documented so that corrections can be applied directly when better data becomes available.

## General Approach

This is **order-of-magnitude analysis**, not route-level precision. We use publicly available data, published research, and documented assumptions to estimate the transportation implications of three reconfiguration options. All outputs are presented as ranges, not point estimates. The analysis does not recommend a configuration — it surfaces data that should have been part of the decision.

## SPEC-060: Split-Family Count Model

**Method:** Grade boundary probability model with sibling co-enrollment rates.

| Assumption | Value | Source | What Would Replace It |
|------------|-------|--------|----------------------|
| Multi-child family rate | 30-40% | Census Bureau SIPP; NCES | District family-level enrollment data |
| Avg children per multi-child family | 2.3 | National elementary data | District data |
| Sibling grade-gap distribution | Approximately uniform | Simplifying assumption | Actual sibling grade distributions |
| Total K-4 enrollment | 1,013 | school-geography trove | District enrollment report |

**Calculation:** For each configuration, identify the grade boundary, compute the probability that a multi-child family spans it, multiply by the estimated number of multi-child families.

**Script:** `pipeline/transport/split_family.py`

## SPEC-061: McKinney-Vento Exposure

**Method:** Proportional eligibility rate applied to displaced student population, with incremental transport cost multiplier.

| Assumption | Value | Source | What Would Replace It |
|------------|-------|--------|----------------------|
| MV eligibility rate | 10% of student body | Evidence pool synthesis | District MV roster by school |
| Incremental cost multiplier | 1.5-3.0x per-pupil baseline | National MV transport research | Actual route-level cost data |
| Obligation duration | 1.5-3.0 years average | Federal law + grade distribution | Actual displaced student grade levels |
| Additional displacement (Option A) | ~200 students | Full system reorganization estimate | District redistricting plan |
| Additional displacement (Option B) | ~50 students | Proximity reassignment estimate | District redistricting plan |
| Additional displacement (Variant C) | ~150 students | Grade 3-4 consolidation estimate | District redistricting plan |

**Legal basis:** 42 U.S.C. Section 11432 (McKinney-Vento Homeless Assistance Act)

**Script:** `pipeline/transport/mckinney_vento.py`

## SPEC-062: SEA Staffing Adequacy

**Method:** Estimate transport-specific FTE share of SEA unit, estimate route requirements per configuration, compare.

| Assumption | Value | Source | What Would Replace It |
|------------|-------|--------|----------------------|
| SEA transport share | 30-35% of total FTE | NCES national benchmarks | District SEA function-level staffing |
| Students per route | ~33 | Maine district averages | District current route data |
| Building reduction factor | +10% routes per lost building | National research | Route-level modeling |
| Grade-band factor | +15% routes per additional band | Deadhead route estimation | Route-level modeling |
| Walkability by config | 35-40% | Redistricting tool + adjustment | District walk zone data |

**Script:** `pipeline/transport/sea_staffing.py`

## SPEC-063: Bell Schedule Tier Analysis

**Method:** Qualitative feasibility assessment of bus tier requirements under each configuration.

| Assumption | Value | Source | What Would Replace It |
|------------|-------|--------|----------------------|
| Current bell schedule | HS 8:10, MS 8:30, Elem 9:05 | SPSD website (verified) | N/A (verified data) |
| Bus turnaround time | ~25 minutes between tiers | South Portland geography estimate | District fleet data |
| Max feasible tiers | 3 (typical for comparable districts) | National research | District fleet and routing analysis |

**Script:** `pipeline/transport/bell_schedule.py`

## SPEC-064: Before/After Care Gap

**Method:** Combine split-family counts with bell schedule scenarios to estimate new care demand, price at market rates.

| Assumption | Value | Source | What Would Replace It |
|------------|-------|--------|----------------------|
| SoPo Kids Club rates | $95/wk after, $155/wk full | City rec dept website (verified) | N/A (verified data) |
| School weeks per year | 36 | Standard school calendar | District calendar |
| Care gap rate (3-tier) | 30% of split families | Logistics estimation | Survey of affected families |
| Care gap rate (4-tier) | 85% of split families | Hard scheduling conflict | Survey of affected families |
| Care capacity status | FULL at 4/5 schools | City rec dept website (verified) | Actual waitlist numbers |

**Script:** `pipeline/transport/care_gap.py`

## SPEC-065: Configuration Comparison

**Method:** Assembly of all metric outputs into structured comparison. Route expansion cost estimated from DOE per-pupil data scaled by route increase percentage.

| Assumption | Value | Source | What Would Replace It |
|------------|-------|--------|----------------------|
| Current transport budget | ~$2.99M | DOE data ($1,065/pupil x 2,810) | District transport budget line |
| Route expansion scaling | Linear with route count | Simplifying assumption | Route-level cost modeling |
| Claimed savings | $1.5-2.2M | District budget presentations | Independently verified savings |

**Script:** `pipeline/transport/configuration_comparison.py`

## What District Data Would Change

The following data, all held by the district, would substantially improve this analysis:

1. **Family-level enrollment** — Exact split-family counts (replaces sibling rate estimates)
2. **McKinney-Vento roster by school** — Exact MV student counts (replaces proportional estimates)
3. **SEA function-level staffing** — Actual transport FTE (replaces national benchmark estimates)
4. **Fleet size and route data** — Actual route requirements and tier feasibility
5. **Care waitlist numbers** — Quantified unmet demand (replaces binary FULL/Available)
6. **Walk zone policy** — Not publicly available; needed for walker/rider classification
7. **Transport consultant scope** — $60-125K budgeted but not hired; scope and timeline unknown

## Reproducibility

All calculation scripts are in `pipeline/transport/`. All input data is in `data/` and `docs/troves/`. The analysis can be fully reproduced from these inputs. Running any script produces both human-readable output and machine-readable JSON in `data/`.
