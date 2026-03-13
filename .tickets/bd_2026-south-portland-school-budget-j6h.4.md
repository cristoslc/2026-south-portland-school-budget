---
id: bd_2026-south-portland-school-budget-j6h.4
status: closed
deps: []
links: []
created: 2026-03-12T04:36:24Z
type: task
priority: 2
---
# Implement runner loop with schema validation

Main runner: iterate over 14 personas, call LLM for each, parse output, validate against SPEC-018 schema, write to data/interpretation/meetings/<meeting-id>/. Log failures per persona, continue with remaining.


