---
id: bd_2026-south-portland-school-budget-8s2.2
status: closed
deps: []
links: []
created: 2026-03-12T04:36:53Z
type: task
priority: 2
assignee: Cristos L-C
---
# Implement fold runner

Script (scripts/fold_meeting.py) iterates over 14 personas for a given meeting-id. For each: load cumulative + meeting interpretation, call LLM with fold prompt, validate output, write updated cumulative. Support --persona flag.


