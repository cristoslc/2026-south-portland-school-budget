---
id: spsbF-dvj2
status: closed
deps: []
links: []
created: 2026-03-21T03:39:55Z
type: task
priority: 2
assignee: cristos
tags: [spec:SPEC-023]
---
# Add inter-meeting deck and refresh briefs

Pull the requested Google Slides deck into the repo as inter-meeting evidence, normalize it, update the inter-meeting manifest, and rerun fold/brief generation so current briefings include it.


## Notes

**2026-03-21T04:41:33Z**

Imported the March 23 board workshop Google Slides deck as inter-meeting evidence, validated data/interpretation/inter-meeting/manifest.yaml with 'uv run python3 scripts/validate_bundle.py --inter-meeting data/interpretation/inter-meeting/manifest.yaml' (exit 0), and regenerated March 23 briefs with 'uv run python3 scripts/generate_briefs.py 2026-03-23 --force' (14 processed, 0 failed). Sample refreshed briefs now show inter_meeting_evidence_count: 1.

**2026-03-21T13:05:35Z**

Root cause of the apparent stale output: regenerated briefs were written to data/interpretation/briefs/2026-03-23, but dist/briefings still contained the previously published March 19 set. Fixed by running publish_briefs('2026-03-23'). Verified dist/briefings/persona-001-concerned-elementary-parent.md and persona-011-group-chat-relay.md now match their 2026-03-23 source briefs exactly and show inter_meeting_evidence_count: 1.
