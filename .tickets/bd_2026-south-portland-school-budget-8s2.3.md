---
id: bd_2026-south-portland-school-budget-8s2.3
status: closed
deps: []
links: []
created: 2026-03-12T04:36:53Z
type: task
priority: 2
assignee: Cristos L-C
---
# Add idempotency check

Compare meeting-id against cumulative's last_folded_meeting frontmatter. Skip if already folded (unless --force). Prevents double-folding and ensures chronological ordering.


