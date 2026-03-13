---
id: bd_2026-south-portland-school-budget-bfr.1
status: closed
deps: []
links: []
created: 2026-03-12T13:26:49Z
type: task
priority: 2
assignee: Cristos L-C
---
# RED: Test bundle manifest dataclass (AC1, AC5)

Write failing tests for the MeetingBundle dataclass: required fields (date, meeting_type, body, sources), optional fields (agenda_ref), field validation (date format, enum values for type/body), and rejection of malformed manifests. Derives from AC1 and AC5.


