# McKinney-Vento Exposure Analysis

**Spec:** SPEC-061 | **Epic:** EPIC-031 | **Initiative:** INITIATIVE-006
**Date:** 2026-03-31

---

## Summary

Closing Kaler Elementary and redistricting students triggers federal transportation obligations under the McKinney-Vento Homeless Assistance Act (42 U.S.C. § 11432). An estimated **19-40 McKinney-Vento eligible elementary students** face displacement depending on configuration, creating annual incremental transportation costs of **$30,000-$128,000** — costs that do not appear in the administration's $1.5-2.2M savings estimate.

Over the full obligation period, total McKinney-Vento transportation exposure ranges from **$46,000 to $384,000** across configurations.

## Background: McKinney-Vento in South Portland

South Portland's McKinney-Vento eligible population is approximately **10% of the student body** (~274 students district-wide, ~108 at the elementary level). This is a notably high rate — well above the national average of approximately 2.5%. Under federal law, MV-eligible students displaced by school closure or redistricting have the right to:

1. **Continue attending their school of origin** with district-provided transportation
2. **Transfer to their new assigned school** with comparable services

The critical obligation: if a MV-eligible student's school closes, the district must provide transportation to whichever school the family chooses — potentially for years, until the student completes the terminal grade.

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
| **Option A** | $54,000-$128,000 | $82,000-$384,000 | 2.5-8.5% annually |
| **Option B** | $30,000-$80,000 | $46,000-$240,000 | 1.4-5.3% annually |
| **Variant C** | $46,000-$112,000 | $70,000-$336,000 | 2.1-7.5% annually |

### Context: The Unfunded Mandate

These costs are **not discretionary** — they are federal obligations. The district cannot decline to provide MV transportation. Yet the $1.5-2.2M savings estimate from school closure makes no mention of McKinney-Vento obligations. Even at the low end, this represents a cost category that was not analyzed.

The exposure is largest under Option A because the full-system grade-band reorganization displaces the most students. Under Option B, the exposure is contained to the Kaler closure footprint.

## Compounding Factors Not Quantified

1. **Undercount risk:** MV eligibility is self-reported and widely acknowledged to be undercounted. The 10% rate may understate the actual eligible population. National research suggests actual rates may be 1.5-2x reported rates in some districts.

2. **SPED overlap:** Approximately 23% of South Portland students have IEPs. Students who are both MV-eligible and have transportation in their IEP face compounding obligations. SPED transport is a separate federal mandate (IDEA) with door-to-door requirements.

3. **Duration uncertainty:** The obligation persists until a student completes the terminal grade at their school of origin. For a displaced kindergartener, that could mean 5 years of transport obligation. Our 1.5-3 year average assumes a mix of grade levels.

4. **Portland bus agreement:** South Portland has a cross-billing bus service agreement with Portland (TC-017). MV transport routes may complicate this arrangement if they cross district boundaries.

## Limitations

- The 10% district-wide MV rate is applied proportionally. Kaler's actual rate may be higher or lower.
- Incremental per-student transport costs are estimated via multiplier, not route-level modeling. Actual costs depend on where displaced students live relative to their school of origin.
- This analysis covers McKinney-Vento only. SPED transport obligations (a larger category) are not included.
- Self-reported eligibility means the true MV population may be larger than estimated.

## Data Sources

- MV eligibility rate: Evidence pool synthesis (persona briefings, budget documents)
- Elementary enrollment: `docs/troves/school-geography/schools.json`
- Transport per-pupil cost: `docs/troves/maine-doe-transport-expenditure/transport-per-pupil.csv`
- Legal framework: 42 U.S.C. § 11432 (McKinney-Vento Homeless Assistance Act)
- Calculation script: `pipeline/transport/mckinney_vento.py`
- Machine-readable output: `data/mckinney-vento-exposure.json`

## Invitation to Improve

The district knows the exact number of McKinney-Vento eligible students at each school. Providing that data would replace the proportional estimate with exact counts. The district also has route-level cost data that would replace the multiplier-based estimate with actual incremental costs.
