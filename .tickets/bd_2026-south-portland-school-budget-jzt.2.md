---
id: bd_2026-south-portland-school-budget-jzt.2
status: closed
deps: []
links: []
created: 2026-03-11T13:03:12Z
type: task
priority: 2
---
# Create docker-compose.yml and start.sh entrypoint

docker-compose.yml with restart:unless-stopped, env_file, volume mount for work dir. start.sh handles runner registration (config.sh) and starts the listener (run.sh). Re-uses existing config on restart.


