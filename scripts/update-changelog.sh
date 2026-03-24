#!/usr/bin/env bash
# Appends a dated entry to dist/changelog.md based on git diff since last entry.
# Called by track2-cron.sh after successful pipeline runs.
#
# Usage: ./scripts/update-changelog.sh [--dry-run]

set -euo pipefail

PROJECT_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
CHANGELOG="$PROJECT_ROOT/dist/changelog.md"
TODAY=$(date +%Y-%m-%d)
DRY_RUN=""
[ "${1:-}" = "--dry-run" ] && DRY_RUN=1

# Don't add duplicate entries for the same date
if grep -q "^## $TODAY" "$CHANGELOG" 2>/dev/null; then
    echo "Changelog already has entry for $TODAY"
    exit 0
fi

# Collect what changed
ITEMS=()

# New fold files
NEW_FOLDS=$(git diff --name-only --diff-filter=A HEAD~1 -- 'data/interpretation/cumulative/*/20*.md' 2>/dev/null | wc -l | tr -d ' ')
if [ "$NEW_FOLDS" -gt 0 ]; then
    # Extract meeting dates from fold filenames
    MEETINGS=$(git diff --name-only --diff-filter=A HEAD~1 -- 'data/interpretation/cumulative/*/20*.md' 2>/dev/null \
        | sed 's|.*/||; s|\.md||' | sort -u | tr '\n' ', ' | sed 's/,$//')
    ITEMS+=("Added cumulative folds for $NEW_FOLDS persona(s) ($MEETINGS)")
fi

# Updated briefs
BRIEF_COUNT=$(git diff --name-only HEAD~1 -- 'data/interpretation/briefs/' 2>/dev/null | wc -l | tr -d ' ')
if [ "$BRIEF_COUNT" -gt 0 ]; then
    BRIEF_DATE=$(ls -1 data/interpretation/briefs/ 2>/dev/null | sort | tail -1)
    ITEMS+=("Regenerated $BRIEF_COUNT briefings for $BRIEF_DATE")
fi

# Published briefs
PUBLISHED=$(git diff --name-only HEAD~1 -- 'dist/briefings/' 2>/dev/null | wc -l | tr -d ' ')
if [ "$PUBLISHED" -gt 0 ]; then
    ITEMS+=("Published $PUBLISHED briefings to site")
fi

# New evidence
NEW_EVIDENCE=$(git diff --name-only --diff-filter=A HEAD~1 -- 'data/school-board/' 'data/city-council/' 2>/dev/null | wc -l | tr -d ' ')
if [ "$NEW_EVIDENCE" -gt 0 ]; then
    ITEMS+=("New evidence: $NEW_EVIDENCE file(s) collected")
fi

# New trove sources
NEW_TROVES=$(git diff --name-only --diff-filter=A HEAD~1 -- 'docs/troves/*/sources/' 2>/dev/null | wc -l | tr -d ' ')
if [ "$NEW_TROVES" -gt 0 ]; then
    ITEMS+=("Normalized $NEW_TROVES new evidence source(s)")
fi

if [ ${#ITEMS[@]} -eq 0 ]; then
    echo "No notable changes to log"
    exit 0
fi

# Build the entry
ENTRY="## $TODAY"
for item in "${ITEMS[@]}"; do
    ENTRY="$ENTRY
- $item"
done

if [ -n "$DRY_RUN" ]; then
    echo "Would prepend to $CHANGELOG:"
    echo "$ENTRY"
    exit 0
fi

# Prepend after the "# Site Updates" header
if [ -f "$CHANGELOG" ]; then
    # Insert after first line (the # header)
    sed -i '' "2i\\
\\
$ENTRY" "$CHANGELOG"
else
    echo "# Site Updates

$ENTRY" > "$CHANGELOG"
fi

echo "Added changelog entry for $TODAY"
