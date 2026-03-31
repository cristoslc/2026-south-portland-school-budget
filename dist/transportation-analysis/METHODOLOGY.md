# Transportation Analysis Methodology

**Initiative:** INITIATIVE-006 | **Date:** 2026-03-31
**Version:** V2 -- updated with 3/30/2026 BoE meeting data + multi-year DOE trends

---

This document describes the methodology, assumptions, and limitations of each analysis in the independent transportation study. Every assumption is documented so that corrections can be applied directly when better data becomes available.

## General Approach

This is **order-of-magnitude analysis**, not route-level precision. We use publicly available data, published research, and documented assumptions to estimate the transportation implications of three reconfiguration options. All outputs are presented as ranges, not point estimates. The analysis does not recommend a configuration -- it surfaces data that should have been part of the decision.

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

**Method:** Compare confirmed driver count against route requirements per configuration.

**V2 update:** The 3/30/2026 BoE meeting provided the actual driver count (20 drivers, confirmed by Director of Operations Mike Natalie). This replaces the V1 approach of estimating transport-specific FTE as a 30-35% share of the 86 post-cut SEA total. The available driver pool is 17-20 (20 confirmed, minus 0-3 potentially lost to the SEA cut from 100 to 86 FTE -- cut allocation is unknown).

| Assumption | Value | Source | What Would Replace It |
|------------|-------|--------|----------------------|
| Current driver count | 20 | Dir. of Operations, 3/30/2026 BoE meeting | N/A (confirmed data) |
| Available drivers post-cut | 17-20 | 20 minus 0-3 from SEA cut (allocation unknown) | District confirmation of which positions are cut |
| Students per route | ~33 | Maine district averages | District current route data |
| Building reduction factor | +10% routes per lost building | National research | Route-level modeling |
| Grade-band factor | +15% routes per additional band | Deadhead route estimation | Route-level modeling |
| Walkability by config | 35-40% | Redistricting tool + adjustment | District walk zone data |

**Driver gap by configuration:**

| Configuration | Drivers Needed | Available | Gap |
|---------------|:--------------:|:---------:|:---:|
| Option A | 30 | 17-20 | -10 to -13 |
| Option B | 24 | 17-20 | -4 to -7 |
| Variant C | 29 | 17-20 | -9 to -12 |

All configurations show a shortfall. This is a structural finding: even the lowest-impact option requires more drivers than the district has.

**Script:** `pipeline/transport/sea_staffing.py`

## SPEC-063: Bell Schedule Tier Analysis

**Method:** Qualitative feasibility assessment of bus tier requirements under each configuration.

**V2 update:** The 3/30/2026 meeting confirmed driver schedule as 7 AM-4 PM with an idle window from 9:30-1:30. This is consistent with the existing 3-tier structure (HS, MS, elementary) and confirms that a 3-tier system is feasible with the current schedule. A 4th tier would require extending the driver workday or adding drivers.

| Assumption | Value | Source | What Would Replace It |
|------------|-------|--------|----------------------|
| Current bell schedule | HS 8:10, MS 8:30, Elem 9:05 | SPSD website (verified) | N/A (verified data) |
| Driver schedule | 7 AM-4 PM, idle 9:30-1:30 | Dir. of Operations, 3/30/2026 BoE meeting | N/A (confirmed data) |
| Bus turnaround time | ~25 minutes between tiers | South Portland geography estimate | District fleet data |
| Max feasible tiers | 3 (typical for comparable districts) | National research + driver schedule confirmation | District fleet and routing analysis |

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

**V2 update:** Added sensitivity analysis comparing FY25 baseline ($2.99M) against FY23 baseline ($2.18M) to account for the anomalous 50.2% transport cost increase. All configurations are reported under both baselines. District and family costs are now separated explicitly.

| Assumption | Value | Source | What Would Replace It |
|------------|-------|--------|----------------------|
| Current transport budget (FY25) | ~$2.99M ($1,065/pupil x 2,810) | DOE FY25 per-pupil data | District transport budget line |
| Pre-anomaly transport budget (FY23) | ~$2.18M ($709/pupil x 3,074) | DOE FY23 per-pupil data | District transport budget line |
| Route expansion scaling | Linear with route count | Simplifying assumption | Route-level cost modeling |
| Claimed savings | $1.5-2.2M | District budget presentations | Independently verified savings |

**Sensitivity output (Option A):**

| Baseline | Route Expansion | District Cost | Family Cost | Total Exposure | % of Savings |
|----------|:--------------:|:-------------:|:-----------:|:--------------:|:------------:|
| FY25 | $748,472 | $802,809-$876,325 | $143,640-$803,520 | $946,449-$1,679,845 | 43-112% |
| FY23 | $545,243 | $599,580-$673,096 | $143,640-$803,520 | $743,220-$1,476,616 | 34-98% |

**Script:** `pipeline/transport/configuration_comparison.py`

## Multi-Year DOE Transport Cost Data

Maine DOE Resident Expenditure Per Pupil reports for FY23-FY25 reveal that South Portland's transport costs are rising anomalously fast:

| District | FY23 | FY24 | FY25 | FY23-25 Change |
|----------|:----:|:----:|:----:|:--------------:|
| State Total | $989 | $1,015 | $1,093 | +10.5% |
| **South Portland** | **$709** | **$940** | **$1,065** | **+50.2%** |
| Peer average (excl. SoPo) | $708 | $749 | $829 | +17.1% |

South Portland's per-pupil transport costs rose 50.2% in two years -- nearly 5x the state average -- while enrollment fell 8.6%. The cause is unknown (contract renegotiation, SPED transport growth, or reporting reclassification are possibilities). This affects the route expansion estimate in two ways:

1. **If the FY25 baseline is correct:** The route expansion estimates stand, but the district is already spending significantly more on transport than peers -- further increases compound on an already-stressed budget line.
2. **If FY23 is more representative:** The baseline should be ~$2.18M, not $2.99M, and route expansion estimates shrink accordingly. The sensitivity analysis presents both.

Source: `data/transport-per-pupil-multiyear.csv`

## Sources of Error

Ranked by estimated impact on the final comparison (highest first):

1. **Route expansion cost** -- the largest and softest number. Derived from aggregate per-pupil data with adjustment heuristics (+10% per lost building, +15% per additional grade band), not route-level analysis. This is the single assumption most likely to move the total by a large amount in either direction.
2. **Care gap rates** -- the 30%/85% care-need rates for 3-tier/4-tier schedules are logistics estimates, not survey data. If fewer split families actually need paid care, the family-borne cost drops. If more do (or if informal care networks are thinner than assumed), it rises.
3. **McKinney-Vento displacement counts** -- the number of students who change schools under each option is estimated from the configuration structure, not from actual redistricting plans. The displacement estimate drives the MV cost.
4. **Walkability assumptions** -- the 35-40% walker rate affects how many students need bus service. Actual walk zones are not publicly available; GIS-derived walkability from the redistricting tool is an approximation.
5. **Sibling co-enrollment rates** -- the 30-40% multi-child family rate is a national average. South Portland's actual rate could be higher or lower.
6. **FY25 transport baseline anomaly** -- South Portland's 50.2% per-pupil increase FY23-FY25 is unexplained. If the FY25 figure includes one-time costs or reclassified expenditures, the baseline is inflated and route expansion costs would be lower. The sensitivity analysis brackets this.
7. **Driver cut allocation** -- the SEA cut (100 to 86 FTE) will remove 14 positions, but which positions is unknown. If drivers are spared entirely, the available pool stays at 20. If 3 drivers are cut, it drops to 17. The 17-20 range reflects this uncertainty.

All figures are order-of-magnitude estimates. The actual values could fall outside the stated ranges.

## What District Data Would Change

The following data, all held by the district, would substantially improve this analysis:

1. **Family-level enrollment** -- Exact split-family counts (replaces sibling rate estimates)
2. **McKinney-Vento roster by school** -- Exact MV student counts (replaces proportional estimates)
3. **SEA position-level cut list** -- Which of the 14 cut FTEs are drivers (replaces the 17-20 range)
4. **Fleet size and route data** -- Actual route requirements and tier feasibility
5. **Care waitlist numbers** -- Quantified unmet demand (replaces binary FULL/Available)
6. **Walk zone policy** -- Not publicly available; needed for walker/rider classification
7. **Transport consultant analysis** -- Confirmed "underway with a partner" at 3/30/2026 meeting; scope and timeline unknown

## Reproducibility

All calculation scripts are in `pipeline/transport/`. All input data is in `data/` and `docs/troves/`. The analysis can be fully reproduced from these inputs. Running any script produces both human-readable output and machine-readable JSON in `data/`.
