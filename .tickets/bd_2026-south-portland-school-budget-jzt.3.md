---
id: bd_2026-south-portland-school-budget-jzt.3
status: closed
deps: []
links: []
created: 2026-03-11T13:03:20Z
type: task
priority: 2
---
# Update pipeline.yml: self-hosted + fallback + 2x/day

Dual-job strategy: primary job runs-on self-hosted, fallback job runs-on ubuntu-latest with if: needs.primary.result == 'failure'. Schedule 2x/day at 8 AM and 8 PM ET (both EDT and EST UTC offsets).


