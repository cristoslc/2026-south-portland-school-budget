# McKinney-Vento Exposure Analysis

**Spec:** SPEC-061 | **Epic:** EPIC-031 | **Initiative:** INITIATIVE-006
**Date:** 2026-03-31 | **Version:** V2 — updated with 3/30/2026 meeting data

---

## Summary

Closing Kaler Elementary and redistricting students triggers federal transportation obligations under the McKinney-Vento Homeless Assistance Act (42 U.S.C. § 11432). An estimated **19-40 McKinney-Vento eligible elementary students** face displacement depending on configuration, creating annual incremental transportation costs of **$30,000-$128,000** — costs that do not appear in the administration's $1.5-2.2M savings estimate.

Over the full obligation period, total McKinney-Vento transportation exposure ranges from **$46,000 to $384,000** across configurations.

## Background: McKinney-Vento in South Portland

South Portland's McKinney-Vento eligible population is approximately **10% of the student body** (~274 students district-wide, ~108 at the elementary level). This is a notably high rate — well above the national average of approximately 2.5%. Under federal law, MV-eligible students displaced by school closure or redistricting have the right to:

1. **Continue attending their school of origin** with district-provided transportation
2. **Transfer to their new assigned school** with comparable services

The critical obligation: if a MV-eligible student's school closes, the district must provide transportation to whichever school the family chooses — potentially for years, until the student completes the terminal grade.

## Multi-Year Transport Cost Context

South Portland's per-pupil transport costs have risen sharply in recent years:

| Fiscal Year | Transport/Pupil | Resident Pupils | Change |
|:-----------:|:--------------:|:---------------:|:------:|
| FY23 | $709 | 3,074 | — |
| FY24 | $940 | 2,937 | +32.6% |
| FY25 | $1,065 | 2,810 | +13.3% |

The cumulative increase is **+50.2% over two years** — far outpacing the state average increase of +10.5% over the same period ($989 to $1,093). The cause of this acceleration is unknown but relevant: MV transport costs compound on an already-rising baseline.

## Analysis by Configuration

### Displacement Estimates

| Configuration | Kaler students displaced | Additional redistricting displacement | Total displaced | MV-eligible displaced (est.) |
|---------------|:------------------------:|:-------------------------------------:|:---------------:|:---------------------------:|
| **Option A** | 135 | ~200 (all students reassigned to grade-band schools) | ~335 | 34-40 |
| **Option B** | 135 | ~50 (only proximity reassignment near Kaler) | ~185 | 19-25 |
| **Variant C** | 135 | ~150 (grade 3-4 consolidation) | ~285 | 29-35 |

**Why Option A has the highest displacement:** Under Option A, *every* elementary student is reassigned — the entire system shifts from K-4 neighborhood schools to grade-band schools (PreK-1 primary, 2-4 intermediate). This means every MV-eligible student in the district is potentially displaced, not just those at Kaler.

**Why Option B has the lowest:** Only Kaler students change schools. Remaining students stay at their neighborhood K-4 school.

### Cost Estimates

Incremental MV transport costs are **higher than average per-pupil transport** because these are often individual or small-group routes to non-neighborhood schools, not marginal additions to existing bus runs. We apply a multiplier of 1.5-3.0x the baseline per-pupil cost ($1,065).

| Configuration | Annual incremental cost | Total obligation (1.5-3 years) | As % of claimed $1.5-2.2M savings |
|---------------|:-----------------------:|:------------------------------:|:----------------------------------:|
| **Option A** | $54,337-$127,853 | $81,506-$383,558 | 2.5-8.5% annually |
| **Option B** | $30,365-$79,908 | $45,548-$239,724 | 1.4-5.3% annually |
| **Variant C** | $46,347-$111,871 | $69,520-$335,614 | 2.1-7.5% annually |

### Context: The Unfunded Mandate

These costs are **not discretionary** — they are federal obligations. The district cannot decline to provide MV transportation. Yet the $1.5-2.2M savings estimate from school closure makes no mention of McKinney-Vento obligations. Even at the low end, this represents a cost category that was not analyzed.

The exposure is largest under Option A because the full-system grade-band reorganization displaces the most students. Under Option B, the exposure is contained to the Kaler closure footprint.

## Compounding Factors Not Quantified

1. **Undercount risk:** MV eligibility is self-reported and widely acknowledged to be undercounted. The 10% rate may understate the actual eligible population. National research suggests actual rates may be 1.5-2x reported rates in some districts.

2. **SPED overlap:** Approximately 23% of South Portland students have IEPs. Students who are both MV-eligible and have transportation in their IEP face compounding obligations. SPED transport is a separate federal mandate (IDEA) with door-to-door requirements.

3. **Duration uncertainty:** The obligation persists until a student completes the terminal grade at their school of origin. For a displaced kindergartener, that could mean 5 years of transport obligation. Our 1.5-3 year average assumes a mix of grade levels.

4. **Portland bus agreement:** South Portland has a cross-billing bus service agreement with Portland (TC-017). MV transport routes may complicate this arrangement if they cross district boundaries.

5. **Rising baseline:** The 50.2% increase in per-pupil transport costs over FY23-FY25 means the MV cost multiplier is applied to a moving target. If costs continue rising, the incremental MV exposure rises proportionally.

## Sources of Error

This analysis could be wrong in the following ways:

1. **MV rate applied proportionally.** The 10% district-wide MV rate is applied uniformly. Kaler's actual rate may be higher (closer to high-poverty schools) or lower. A 5-percentage-point difference in Kaler's rate changes the displaced MV count by 7-10 students.

2. **Cost multiplier is a heuristic.** The 1.5-3.0x multiplier for incremental MV transport is based on national studies of per-student transport costs for non-neighborhood routes. South Portland's actual incremental cost per MV student depends on where they live relative to their school of origin — routes could be shorter or longer than average.

3. **Obligation duration is estimated.** We use 1.5-3 years as the average obligation period. If most displaced MV students are in lower grades (longer remaining enrollment), the actual obligation period could be longer. If most are in upper grades, it could be shorter.

4. **Self-reported eligibility likely undercounts.** This means our MV population estimate may be *too low*, not too high. The error direction is toward underestimating costs.

5. **SPED transport is excluded.** Students who are both MV-eligible and have transportation in their IEP face higher per-student costs. This analysis covers MV obligations only.

**What would fix it:** The district knows the exact number of MV-eligible students at each school. Providing school-level MV counts and route-level cost data would replace every estimate with actuals.

## Data Sources

- MV eligibility rate: Evidence pool synthesis (persona briefings, budget documents)
- Elementary enrollment: `docs/troves/school-geography/schools.json`
- Transport per-pupil cost: `docs/troves/maine-doe-transport-expenditure/transport-per-pupil.csv`
- Multi-year transport trend: `data/transport-per-pupil-multiyear.csv` (Maine DOE FY23-FY25)
- Legal framework: 42 U.S.C. § 11432 (McKinney-Vento Homeless Assistance Act)
- Calculation script: `pipeline/transport/mckinney_vento.py`
- Machine-readable output: `data/mckinney-vento-exposure.json`

## Invitation to Improve

The district knows the exact number of McKinney-Vento eligible students at each school. Providing that data would replace the proportional estimate with exact counts. The district also has route-level cost data that would replace the multiplier-based estimate with actual incremental costs. If the district's MV liaison has projections for how many families would elect school-of-origin transport vs. transfer, that would further refine the cost range.
