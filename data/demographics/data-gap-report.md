# SPEC-041: Supplementary Demographic Data — Collection Report

## Data Collected

### 1. Birth Records — Cumberland County (CDC WONDER)
- **Source:** CDC WONDER Natality, 2016-2024 expanded
- **Coverage:** 2016-2024 (9 years), county-level
- **South Portland estimates:** ~220-241 births/year (8.25% population share)
- **File:** `cdc-wonder-births-cumberland-county.json`
- **Limitation:** County-level proxy, not municipal. Actual South Portland births available from city clerk annual reports (575 birth records processed in 2024 per annual report).
- **Gap:** 2007-2015 birth data available via CDC WONDER natality-current.html but not yet collected. Needed for full kindergarten pipeline validation.

### 2. Residential Building Permits — Census BPS
- **Source:** U.S. Census Bureau Building Permits Survey, Annual Place Data
- **Coverage:** 2014-2024 (11 years), city-level
- **File:** `census-building-permits.csv`, `census-building-permits.json`
- **Key finding:** Major spikes in 2019 (222 units) and 2020 (275 units) from 5+ unit developments. Baseline single-family permits: 13-40/year.
- **LD 1829 context:** Maine housing density law (effective 2025) allows minimum 3-4 units per lot. No large projects documented under LD 1829 yet; impact expected 2026-2028.

### 3. School Choice Transfer Flows
- **Status:** NOT AVAILABLE from public sources
- **Finding:** Neither Maine DOE nor NCES publishes inter-district transfer flow data at the district level. The district has not published school choice data in budget presentations.
- **Implication:** The cohort survival model will treat South Portland as a closed system. Transfers in/out are a known unmodeled variable. A FOAA request could potentially obtain this data.

## Data Sources Identified but Not Yet Collected

| Source | Data | Status | Effort |
|--------|------|--------|--------|
| CDC WONDER natality-current | Cumberland County births 2007-2015 | Available, not collected | Low — same process as 2016-2024 |
| South Portland annual reports | Municipal birth records processed/year | Available, not extracted | Medium — parse 10+ PDFs |
| Maine CDC data request | Municipal-level births | Available via formal request | Medium — 2-4 week turnaround |

## Implications for Downstream SPECs

- **SPEC-044 (Cohort Survival Model):** Has enough data to build the model. County birth data provides kindergarten pipeline estimates. Building permit data provides LD 1829 scenario input. School choice gap documented as known limitation.
- **SPEC-045 (Scenario Brackets):** Housing permit data directly feeds the LD 1829 absorption scenario. Birth data feeds the kindergarten pipeline scenario.
