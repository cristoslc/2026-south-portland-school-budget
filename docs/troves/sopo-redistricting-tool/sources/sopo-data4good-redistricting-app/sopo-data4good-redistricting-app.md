---
source-id: "sopo-data4good-redistricting-app"
title: "South Portland Elementary School Redistricting Tool"
type: web
url: "https://sopo-data4good.vercel.app/"
fetched: 2026-03-31T02:14:00Z
hash: "0d43e017dbe7ec5901eed42f972cb5c448e4aa2b0bfdc31f9fdc48d463609e3a"
---

# South Portland Elementary School Redistricting Tool

An interactive, community-built web tool that models what South Portland elementary school redistricting could look like if one school were closed. Built with Leaflet maps and hosted on Vercel. Created independently by a South Portland parent — no affiliation with the school department or school board.

## Four Closure Scenarios

Each tab represents one school being closed. Skillin is excluded because the remaining four schools lack combined capacity for all K-4 students.

| School  | Capacity | Notes                                    |
|---------|----------|------------------------------------------|
| Brown   | 260      |                                          |
| Dyer    | 240      | Current PreK pilot site (29 students)    |
| Small   | 280      |                                          |
| Skillin | 380      | Not modeled as a closure option          |
| Kaler   | 240      | Current PreK pilot site (29 students)    |

## Viewing Modes

Three organizational models available per closure scenario:

- **Community Schools** — each building houses all grades K-4 (status quo model). PreK toggle compares the current pilot (Dyer and Kaler only) against full expansion (every open school hosts 29 PreK students).
- **Grade Centers: PreK-1** — two buildings become early-childhood centers serving PreK through 1st grade. PreK toggle shows difference between 29 and 58 PreK seats per center.
- **Grade Centers: 2-4** — the other two buildings serve Grades 2-4.

## Scenario: Close Brown (Community - Current PreK)

| School  | Enrolled / Capacity | Walkable | Avg Drive | Max Drive |
|---------|---------------------|----------|-----------|-----------|
| Dyer    | 230 / 240 (incl. 29 PreK) | 40% (80 students within 0.75 mi) | 1.61 mi | 2.16 mi |
| Small   | 267 / 280           | 53% (140 students within 0.75 mi) | 1.12 mi | 1.72 mi |
| Skillin | 347 / 380           | 34% (117 students within 0.75 mi) | 1.38 mi | 2.98 mi |
| Kaler   | 227 / 240 (incl. 29 PreK) | 39% (78 students within 0.75 mi) | 2.33 mi | 2.98 mi |

**42% of students change schools.**

## Scenario: Close Dyer (Community - Current PreK)

| School  | Enrolled / Capacity | Walkable | Avg Drive | Max Drive |
|---------|---------------------|----------|-----------|-----------|
| Brown   | 252 / 260           | 47% (118 students within 0.75 mi) | 2.29 mi | 4.55 mi |
| Small   | 209 / 280 (incl. 29 PreK) | 75% (135 students within 0.75 mi) | 2.07 mi | 4.96 mi |
| Skillin | 371 / 380           | 31% (117 students within 0.75 mi) | 1.20 mi | 1.76 mi |
| Kaler   | 238 / 240 (incl. 29 PreK) | 37% (78 students within 0.75 mi) | 1.18 mi | 1.54 mi |

**34% of students change schools.**

## Scenario: Close Kaler (Community - Current PreK)

| School  | Enrolled / Capacity | Walkable | Avg Drive | Max Drive |
|---------|---------------------|----------|-----------|-----------|
| Brown   | 251 / 260           | 47% (118 students within 0.75 mi) | 2.09 mi | 4.55 mi |
| Dyer    | 236 / 240 (incl. 29 PreK) | 39% (81 students within 0.75 mi) | 1.19 mi | 1.50 mi |
| Small   | 209 / 280 (incl. 29 PreK) | 75% (135 students within 0.75 mi) | 2.07 mi | 4.96 mi |
| Skillin | 374 / 380           | 31% (117 students within 0.75 mi) | 1.21 mi | 1.76 mi |

**27% of students change schools.**

## Scenario: Close Small (Community - Current PreK)

| School  | Enrolled / Capacity | Walkable | Avg Drive | Max Drive |
|---------|---------------------|----------|-----------|-----------|
| Brown   | 252 / 260           | 50% (126 students within 0.75 mi) | 0.88 mi | 1.17 mi |
| Dyer    | 230 / 240 (incl. 29 PreK) | 40% (80 students within 0.75 mi) | 1.93 mi | 3.15 mi |
| Skillin | 376 / 380           | 31% (117 students within 0.75 mi) | 1.23 mi | 1.76 mi |
| Kaler   | 212 / 240 (incl. 29 PreK) | 43% (78 students within 0.75 mi) | 2.15 mi | 2.66 mi |

**41% of students change schools.**

## Zone Boundary Methodology

Boundaries are generated automatically (not hand-drawn), prioritizing:

1. **Walkability first** — neighborhoods within 0.75-mile walk assigned to nearest school. Walk distances use real sidewalk and road network data (highways and rail lines correctly block walking routes).
2. **Capacity limits** — no school assigned more students than capacity. Overflow redirected to nearest school with space.
3. **Neighborhood cohesion** — nearby blocks kept together so neighbors attend the same school.

Student counts are estimates based on Census 2020 population data, not official enrollment records by home address.

## Interactive Features

- Switch between closure scenarios via tabs
- Toggle PreK models (current pilot vs full expansion)
- View "% Change Schools" to highlight affected blocks
- Click blocks on map to reassign to different schools (stats update live)
- Export zone maps as GeoJSON
- Upload zone files from others to see live statistics
- Reset to base scenario

## Disclaimers

Walk and drive distances reflect actual road network routing, not straight-line distances. They do not account for crossing guard locations, sidewalk quality, or family circumstances. Enrollment figures are estimates.

This is an unofficial tool. Zone assignments are computer-generated estimates, not official school district boundaries.
