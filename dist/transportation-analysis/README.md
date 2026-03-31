# Independent Transportation Analysis

**Initiative:** [INITIATIVE-006](../../docs/initiative/Active/(INITIATIVE-006)-Independent-Transportation-Analysis/(INITIATIVE-006)-Independent-Transportation-Analysis.md)
**Status:** V1 Complete (2026-03-31)

---

The South Portland School Board has been asked to choose between elementary reconfiguration options with materially different transportation implications, without transportation analysis. The Director of Operations confirmed on the record that no modeling exists and none will be done before the board votes.

This folder contains the independent analysis that should have existed before the vote.

## Key Finding

**Option A's total fiscal exposure ($1.05M-$1.79M/yr) could offset 48-119% of the claimed $1.5-2.2M savings from school closure.** Option B preserves nearly all savings with zero split families.

## Contents

### Analysis Documents

| Document | What It Covers |
|----------|---------------|
| [Configuration Comparison](transport-configuration-comparison.md) | Side-by-side comparison of all metrics across 3 configurations (capstone) |
| [Split-Family Model](split-family-model.md) | How many families would have children in two different buildings |
| [McKinney-Vento Exposure](mckinney-vento-exposure.md) | Federal transport obligations triggered by school closure |
| [SEA Staffing Assessment](sea-staffing-assessment.md) | Whether 86 post-cut FTEs can cover expanded routes |
| [Bell Schedule Analysis](bell-schedule-analysis.md) | Bus tier requirements under each configuration |
| [Before/After Care Gap](before-after-care-gap.md) | Care capacity impact and family cost burden |

### Persona Briefs

The [briefings/](briefings/) folder contains 16 transportation impact briefs: one for each of the 15 project personas plus a general community brief. Each brief frames the same underlying analysis through the persona's specific concerns.

### Machine-Readable Data

| File | Format | Description |
|------|--------|-------------|
| [transport-comparison.json](transport-comparison.json) | JSON | Structured comparison data for site consumption |

## Configurations Compared

| Config | Structure | Key Transport Feature |
|--------|-----------|----------------------|
| **Option A** (admin recommendation) | 2 primary (PreK-1) + 2 intermediate (2-4), Kaler closed | Grade-band split creates 139-169 split families |
| **Option B** (board alternative) | 4 buildings K-4, Kaler closed, redistrict by proximity | No grade-band split; zero split families |
| **Variant C** (citizen alternative) | 3 buildings PreK-2 + 1 building Grades 3-4, Kaler closed | Grade-band split creates 123-150 split families |

## Source Data

All analysis draws from publicly available data:

- **Enrollment by grade:** NCES Common Core of Data, district redistricting tool
- **Transport expenditure:** Maine DOE FY25 per-pupil expenditure report
- **Bell schedules:** SPSD website (verified 2026-03-31)
- **Care rates:** South Portland Recreation Department SoPo Kids Club (verified 2026-03-31)
- **McKinney-Vento rate:** District evidence pools (10% of student body)
- **SEA staffing:** FY27 budget documents (100 FTE to 86 FTE)

## How to Improve This Analysis

Every estimate can be replaced with facts the district possesses. See [METHODOLOGY.md](METHODOLOGY.md) for the full list of assumptions and what data would replace them.

## Disclaimer

This is an independent analysis using publicly available data. It is not affiliated with or endorsed by the South Portland School Department. All figures are order-of-magnitude estimates. The goal is to surface missing analysis, not to recommend a configuration.
