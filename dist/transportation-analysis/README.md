# Independent Transportation Analysis

**Initiative:** [INITIATIVE-006](../../docs/initiative/Active/(INITIATIVE-006)-Independent-Transportation-Analysis/(INITIATIVE-006)-Independent-Transportation-Analysis.md)
**Status:** V2 -- updated with 3/30/2026 BoE meeting data + multi-year DOE trends
**Date:** 2026-03-31

---

The South Portland School Board has been asked to choose between elementary reconfiguration options with materially different transportation implications, without transportation analysis. The Superintendent confirmed at the 3/30/2026 meeting that transport logistics are "underway with a partner" but will be operationalized after the board votes, not before.

This folder contains the independent analysis that should have existed before the vote.

## Key Finding

**Option A's total fiscal exposure is $946,449-$1,679,845/year -- representing 43-112% of the claimed $1.5-2.2M savings.** Of that, $802,809-$876,325 is district-borne cost (route expansion + McKinney-Vento obligations) and $143,640-$803,520 is family-borne cost (before/after care gaps). Option B preserves nearly all savings with zero split families but still faces a driver shortfall.

**New in V2:** All three configurations show a driver shortfall against the confirmed fleet of 20 drivers. Even Option B, the lowest-impact option, needs 24 drivers -- 4-7 more than available. This finding emerged from the 3/30 meeting confirmation of actual driver headcount, replacing the previous percentage-based estimate.

## Contents

### Analysis Documents

| Document | What It Covers |
|----------|---------------|
| [Configuration Comparison](transport-configuration-comparison.md) | Side-by-side comparison of all metrics across 3 configurations (capstone) |
| [Methodology](METHODOLOGY.md) | All assumptions, data sources, error ranking, and what district data would replace |
| [Split-Family Model](split-family-model.md) | How many families would have children in two different buildings |
| [McKinney-Vento Exposure](mckinney-vento-exposure.md) | Federal transport obligations triggered by school closure |
| [SEA Staffing Assessment](sea-staffing-assessment.md) | Whether 20 drivers can cover expanded routes |
| [Bell Schedule Analysis](bell-schedule-analysis.md) | Bus tier requirements under each configuration |
| [Before/After Care Gap](before-after-care-gap.md) | Care capacity impact and family cost burden |

### Persona Briefs

The [briefings/](briefings/) folder contains 16 transportation impact briefs: one for each of the 15 project personas plus a general community brief. Each brief frames the same underlying analysis through the persona's specific concerns.

### Machine-Readable Data

| File | Format | Description |
|------|--------|-------------|
| [transport-comparison.json](../../data/transport-comparison.json) | JSON | Structured comparison data for site consumption |

## Configurations Compared

| Config | Structure | Split Families | Drivers Needed | Driver Gap | Total Exposure | % of Savings |
|--------|-----------|:--------------:|:--------------:|:----------:|:--------------:|:------------:|
| **Option A** (admin recommendation) | 2 primary (PreK-1) + 2 intermediate (2-4), Kaler closed | 139-169 | 30 | -10 to -13 | $946,449-$1,679,845 | 43-112% |
| **Option B** (board alternative) | 4 buildings K-4, Kaler closed, redistrict by proximity | 0 | 24 | -4 to -7 | $30,365-$79,908 | 1.4-5.3% |
| **Variant C** (citizen alternative) | 3 buildings PreK-2 + 1 building 3-4, Kaler closed | 123-150 | 29 | -9 to -12 | $796,613-$1,449,837 | 36-97% |

Driver gap is calculated against 17-20 available drivers (20 confirmed, minus 0-3 from SEA cuts).

## Source Data

All analysis draws from publicly available data:

- **Enrollment by grade:** NCES Common Core of Data, district redistricting tool
- **Transport expenditure:** Maine DOE Resident Expenditure Per Pupil, FY23-FY25
- **Driver count:** Director of Operations Mike Natalie, 3/30/2026 BoE meeting (20 drivers)
- **Driver schedule:** Same meeting (7 AM-4 PM, idle 9:30-1:30, confirming 3-tier structure)
- **Bell schedules:** SPSD website (verified 2026-03-31)
- **Care rates:** South Portland Recreation Department SoPo Kids Club (verified 2026-03-31)
- **McKinney-Vento rate:** District evidence pools (10% of student body)
- **SEA staffing:** FY27 budget documents (100 FTE to 86 FTE)
- **Multi-year DOE trends:** South Portland per-pupil transport costs rose 50.2% FY23-FY25 (vs. state +10.5%)
- **Diesel risk:** Board member Feller flagged 25-50% increase; Dir. of Operations called impact "considerable" but unquantified

## How to Improve This Analysis

Every estimate can be replaced with facts the district possesses. See [METHODOLOGY.md](METHODOLOGY.md) for the full list of assumptions, ranked sources of error, and what data would replace each estimate.

## Disclaimer

This is an independent analysis using publicly available data. It is not affiliated with or endorsed by the South Portland School Department. All figures are order-of-magnitude estimates presented as ranges. This analysis separates district-budget costs from family-borne costs -- both are real economic impacts of reconfiguration, but only district costs affect the claimed savings calculation directly. The goal is to surface missing analysis, not to recommend a configuration.
