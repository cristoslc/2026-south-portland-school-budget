# SEA Staffing Adequacy Assessment

**Spec:** SPEC-062 | **Epic:** EPIC-031 | **Initiative:** INITIATIVE-006
**Date:** 2026-03-31

---

## Summary

The SEA bargaining unit (Facilities/Food/Transport) faces the steepest percentage cut in the FY27 budget: **100 FTE → 86 FTE (14% reduction)**. Our aggregate model suggests the post-cut transport workforce *may* be numerically adequate for regular routes under all three configurations — but this finding comes with critical caveats about specialized routes, the untested interaction between simultaneous route expansion and staff reduction, and the fact that **the cut was decided before any route modeling existed**.

The core finding is not "will there be enough drivers?" — it is that **nobody checked before making the cut**.

## Staffing Baseline

### SEA Composition

The SEA bargaining unit covers three functions:
- **Facilities** (custodians, maintenance)
- **Food service** (cafeteria workers)
- **Transportation** (bus drivers, aides, dispatchers, mechanics)

The FY27 budget documents do not break out transport-specific FTE within the SEA unit. We estimate the transport share at **30-35%** of total SEA FTE, based on national benchmarks from the NCES School District Finance Survey for districts of comparable size.

| Metric | Pre-Cut | Post-Cut | Change |
|--------|:-------:|:--------:|:------:|
| Total SEA FTE | 100 | 86 | -14 (14%) |
| Estimated transport FTE | 30-35 | 26-30 | -4 to -5 |
| Estimated facilities FTE | 40-45 | 34-39 | -6 to -7 |
| Estimated food service FTE | 25-30 | 21-26 | -4 to -5 |

**Note:** The cut distribution across functions is not specified in budget documents. We assume proportional cuts, but the district may concentrate cuts in one function.

## Route Estimation by Configuration

### Method

Routes are estimated using:
1. Total bused students (enrollment × (1 - walkable percentage))
2. Students per route (~33, typical for Maine districts)
3. Building reduction factor (fewer schools = wider catchments = more routes)
4. Grade-band factor (split grade bands add deadhead routes)

Walkability decreases from the current 44% as catchments widen and grade-band assignments replace proximity assignments.

### Results

| Metric | Option A | Option B | Variant C |
|--------|:--------:|:--------:|:---------:|
| Grade bands | 2 (PreK-1, 2-4) | 1 (K-4) | 2 (PreK-2, 3-4) |
| Walkable % (est.) | 35% | 40% | 37% |
| Bused students | ~696 | ~643 | ~675 |
| Estimated routes | ~27 | ~21 | ~25 |
| Driver FTE needed | 14-18 | 10-14 | 12-17 |
| **Post-cut FTE available** | **26-30** | **26-30** | **26-30** |
| **Surplus/(Shortfall)** | **+8 to +16** | **+12 to +20** | **+9 to +18** |

### Raw Numbers Look Adequate — But...

The aggregate model shows numerical surplus under all configurations. However, this analysis only covers **regular elementary routes**. The transport operation includes:

1. **SPED door-to-door routes:** 23% of South Portland students have IEPs, many with transportation in their service plans. These are individual or small-group routes that consume driver FTE disproportionate to student count. These routes are **not optional** — they're federal mandates.

2. **McKinney-Vento routes:** As documented in SPEC-061, displacement creates incremental transport obligations for an estimated 19-40 students. Each may require a dedicated or modified route.

3. **Middle and high school routes:** The same SEA transport staff serve all levels, not just elementary. Route expansion at the elementary level competes for the same drivers.

4. **Substitute/absence coverage:** 86 FTE is the authorized headcount, not daily available staff. Bus driver absence rates in Maine typically run 8-12%, requiring substitutes or route consolidation.

5. **Non-driver transport staff:** The 26-30 estimated transport FTE include dispatchers, mechanics, and aides — not all are drivers. Actual available driver FTE may be 20-25.

## The Core Problem: Sequencing

The most concerning finding is not the staffing gap analysis itself — it's the sequencing:

1. **March 9:** Administration presents 14% SEA cut (TC-016)
2. **March 23:** Director of Operations confirms no transport modeling exists (TC-014)
3. **Board vote:** Scheduled without route analysis

The 14% cut was set **before anyone determined how many routes the reconfigured system needs**. This is like deciding how many firefighters to lay off before knowing how many stations you're closing.

Even if the raw numbers work out, the absence of modeling means the district is accepting risk it hasn't measured. A responsible sequence would be:

1. Model routes for each configuration
2. Determine staffing requirements
3. Set staffing levels to match
4. Budget accordingly

What happened instead:

1. Set staffing reduction target (14%)
2. Propose configuration change
3. Vote on configuration
4. Model routes (someday)
5. Discover whether the budget works

## Peer District Context

From the Maine DOE transport expenditure data:

| District | Transport/Pupil | Students | Implied Transport Budget |
|----------|:--------------:|:--------:|:------------------------:|
| South Portland | $1,065 | 2,810 | ~$2.99M |
| Gorham (closest peer) | $946 | 2,815 | ~$2.66M |
| Portland | $626 | 6,511 | ~$4.07M |

South Portland already spends 70% more per pupil on transport than Portland and 13% more than the closest peer (Gorham). Adding routes while cutting staff increases per-pupil costs further, potentially moving South Portland above the state average ($1,093/pupil).

## Conclusions

1. **Regular routes appear numerically covered** under all configurations with the post-cut workforce, but the margin is thin under Option A.
2. **Specialized routes (SPED, MV) are the unmodeled risk.** The aggregate model doesn't account for these mandatory, high-cost-per-student routes.
3. **The staffing decision preceded the route analysis.** This is the fundamental problem — not whether the numbers work, but that nobody checked.
4. **Option B requires the fewest routes** and has the most staffing headroom. Option A requires the most routes and has the least headroom.

## Limitations

- SEA transport share (30-35%) is estimated from national data, not South Portland's actual allocation
- Route estimation uses an aggregate model, not route-level GIS analysis
- Does not model SPED routes, MV routes, or middle/high school routes
- Walkability reduction from reconfiguration is estimated, not measured
- Driver absence and substitute availability not modeled
- No data on current fleet size or vehicle allocation

## Data Sources

- SEA staffing: TC-016, FY27 budget documents
- Transport expenditure: `docs/troves/maine-doe-transport-expenditure/transport-per-pupil.csv`
- Enrollment: `docs/troves/school-geography/schools.json`
- Calculation script: `pipeline/transport/sea_staffing.py`
- Machine-readable output: `data/sea-staffing-assessment.json`

## Invitation to Improve

The district has the actual SEA function-level staffing breakdown, current route count, fleet size, and driver roster. Providing this data would replace every estimate in this analysis with facts. The methodology is documented and transparent — corrections can be applied directly to the model.
