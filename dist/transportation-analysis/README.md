# Independent Transportation Analysis

**Initiative:** [INITIATIVE-006](../../docs/initiative/Active/(INITIATIVE-006)-Independent-Transportation-Analysis/(INITIATIVE-006)-Independent-Transportation-Analysis.md)
**Status:** Post-decision update
**Date:** 2026-03-31

---

On March 30, 2026, the South Portland Board of Education voted 4-2 to adopt Option A -- a primary/intermediate grade-band reconfiguration that closes Kaler Elementary and splits the remaining four buildings into PreK-1 and 2-4 schools. The same meeting confirmed that the district employs 20 bus drivers and that transport logistics would be operationalized after the vote, not before.

No transportation analysis existed when the board voted. This is that analysis.

## What the Board Approved

| Decision | Vote | Effective |
|----------|:----:|-----------|
| Close Kaler Elementary | 6-1 | End of 2025-26 |
| Adopt Option A (grade-band reconfiguration) | 4-2 | Fall 2026 |
| Adopt FY27 budget ($75.85M) | **Failed** 2-5 | Follow-up April 2 |

The configuration passed but the budget to fund it did not.

## What Option A Means for Transportation

| Metric | Value | Source |
|--------|-------|--------|
| Split families | 139-169 (18-24% of elementary families) | Grade boundary probability model |
| Drivers needed | 30 | Route estimation from confirmed fleet |
| Drivers available post-cut | 17-20 | 20 confirmed minus 0-3 from SEA reduction |
| **Driver shortfall** | **10-13** | Headcount gap -- structural, not estimable away |
| District cost (annual) | $802,809-$876,325 | Route expansion + McKinney-Vento obligations |
| Family cost (annual) | $143,640-$803,520 | Before/after care gap (4/5 schools at capacity) |
| **Total fiscal exposure** | **$946,449-$1,679,845** | **43-112% of the claimed $1.5-2.2M savings** |

Every configuration shows a driver shortfall -- even Option B (the lowest-impact alternative) would need 24 drivers against 17-20 available. But the board chose the configuration with the largest gap.

## What Needs to Happen Before September

The [Post-Decision Brief](POST-DECISION-BRIEF.md) details the implementation risks and timeline. The short version:

1. **Hire 10-13 drivers** or contract out routes -- the current fleet cannot serve 30 routes
2. **Draw attendance boundaries** with transport implications modeled -- none exist yet
3. **Resolve the 3-tier vs. 4-tier bell schedule question** -- a 4th tier doesn't fit the current driver workday (7 AM-4 PM) without overtime, and creates 30-minute drop-off gaps for split families
4. **Address the care gap** -- after-school care is full at 4 of 5 schools, and the only school with openings is the one being closed
5. **Pass a budget** -- the FY27 budget failed 2-5; transport costs aren't funded

## Contents

### Analysis Documents

| Document | What It Covers |
|----------|---------------|
| [Post-Decision Brief](POST-DECISION-BRIEF.md) | Implementation risks now that Option A is approved |
| [Board Letter Draft](BOARD-LETTER-DRAFT.md) | Template letter to the board with specific asks for April 7 |
| [Configuration Comparison](transport-configuration-comparison.md) | Side-by-side metrics across all 3 configurations |
| [Methodology](METHODOLOGY.md) | All assumptions, ranked error sources, and what district data would replace each |
| [Split-Family Model](split-family-model.md) | How many families will have children in two different buildings |
| [McKinney-Vento Exposure](mckinney-vento-exposure.md) | Federal transport obligations triggered by school closure |
| [SEA Staffing Assessment](sea-staffing-assessment.md) | Whether 20 drivers can cover 30 routes (they cannot) |
| [Bell Schedule Analysis](bell-schedule-analysis.md) | Bus tier requirements and the 4th-tier pressure |
| [Before/After Care Gap](before-after-care-gap.md) | Care capacity crisis and family cost burden |

### Persona Briefs

The [briefings/](briefings/) folder contains 16 transportation impact briefs -- one for each of the 15 project personas plus a general community brief. Each frames the same analysis through a different stakeholder's concerns.

### Machine-Readable Data

| File | Format | Description |
|------|--------|-------------|
| [transport-comparison.json](../../data/transport-comparison.json) | JSON | Structured comparison data for all configurations |

## Source Data

All analysis draws from publicly available data:

- **Driver count and schedule:** Director of Operations Mike Natalie, 3/30/2026 BoE meeting (20 drivers, 7 AM-4 PM, idle 9:30-1:30)
- **Vote results:** Board meeting transcript, 3/30/2026 (Kaler closure 6-1, Option A 4-2, budget failed 2-5)
- **Enrollment by grade:** NCES Common Core of Data, district redistricting tool
- **Transport expenditure:** Maine DOE Resident Expenditure Per Pupil, FY23-FY25
- **Bell schedules:** SPSD website (verified 2026-03-31)
- **Care rates and capacity:** South Portland Recreation Department SoPo Kids Club (verified 2026-03-31)
- **McKinney-Vento rate:** District evidence pools (10% of student body)
- **SEA staffing:** FY27 budget documents (100 FTE to 86 FTE, 14% cut)
- **Multi-year transport trend:** South Portland per-pupil transport costs rose 50.2% FY23-FY25 ($709 to $1,065) vs. state average +10.5%
- **Diesel cost risk:** Flagged as "considerable" at 3/30 meeting; unquantified

## Sources of Error

This is order-of-magnitude analysis, not route-level precision. The ranked error sources (from [METHODOLOGY.md](METHODOLOGY.md)):

1. **Route expansion cost** -- largest and softest number; aggregate heuristics, not route modeling
2. **Care gap rates** -- 30%/85% need estimates are logistics judgment, not survey data
3. **Post-cut driver allocation** -- which of the 14 SEA cuts are drivers is unknown
4. **Walkability assumptions** -- 35-40% walker rate without GIS or walk-zone data
5. **FY25 transport baseline anomaly** -- the 50.2% cost increase is unexplained; sensitivity analysis brackets it

The driver shortfall finding (10-13 short) is the most robust result because it depends on confirmed headcount, not dollar estimates.

## How to Improve This Analysis

The district has family-level enrollment data, route manifests, fleet vehicle counts, SEA cut allocation, and a transport consultant's preliminary findings. Any of these would replace estimates with facts. See [METHODOLOGY.md](METHODOLOGY.md) for the complete assumption table.

## Disclaimer

This is an independent analysis by a South Portland resident using publicly available data. It is not affiliated with or endorsed by the South Portland School Department. All figures are order-of-magnitude estimates presented as ranges. District-budget costs and family-borne costs are separated throughout. The goal is to surface the transportation analysis that did not exist when the board voted -- and to identify what needs to happen before fall 2026.
