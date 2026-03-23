#!/usr/bin/env bash
# Track 2 cron wrapper — runs poll_interpret.py with pull + auto-brief + publish,
# commits results, and sends a macOS notification on completion.
#
# Writes progress to .local/track2-status.json for the SwiftBar plugin.
#
# Designed for launchd scheduling. Safe to run when nothing is new (no-op).
#
# Usage:
#   ./scripts/track2-cron.sh              # normal run
#   ./scripts/track2-cron.sh --dry-run    # preview only

set -euo pipefail

PROJECT_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
LOG_DIR="$PROJECT_ROOT/.local/logs"
LOG_FILE="$LOG_DIR/track2-$(date +%Y-%m-%d_%H%M%S).log"
LOCK_FILE="$PROJECT_ROOT/.local/track2.lock"
STATUS_FILE="$PROJECT_ROOT/.local/track2-status.json"

mkdir -p "$LOG_DIR"

# --- Status helpers ---
write_status() {
    echo "$1" > "$STATUS_FILE"
}

status_running() {
    local step="$1" detail="${2:-}" progress="${3:-}" meeting="${4:-}" meetings_done="${5:-0}" meetings_total="${6:-0}"
    write_status "{\"state\":\"running\",\"step\":\"$step\",\"detail\":\"$detail\",\"progress\":\"$progress\",\"meeting\":\"$meeting\",\"meetings_done\":$meetings_done,\"meetings_total\":$meetings_total}"
}

status_done() {
    local result="$1" error="${2:-}"
    local now
    now=$(date '+%Y-%m-%d %H:%M')
    write_status "{\"state\":\"$result\",\"last_result\":\"$result\",\"last_time\":\"$now\",\"error\":$([ -n "$error" ] && echo "\"$error\"" || echo "null")}"
}

# --- Lock (prevent overlapping runs) ---
if [ -f "$LOCK_FILE" ]; then
    pid=$(cat "$LOCK_FILE" 2>/dev/null || echo "")
    if [ -n "$pid" ] && kill -0 "$pid" 2>/dev/null; then
        echo "Track 2 already running (PID $pid), skipping." | tee -a "$LOG_FILE"
        exit 0
    fi
    rm -f "$LOCK_FILE"
fi
echo $$ > "$LOCK_FILE"
trap 'rm -f "$LOCK_FILE"' EXIT

# --- Notify helper ---
notify() {
    local title="$1" body="$2" sound="${3:-default}"
    osascript -e "display notification \"$body\" with title \"$title\" sound name \"$sound\"" 2>/dev/null || true
}

# --- Determine next upcoming meeting date ---
next_brief_date() {
    local today
    today=$(date +%Y-%m-%d)
    local bundles_dir="$PROJECT_ROOT/data/interpretation/bundles"
    if [ ! -d "$bundles_dir" ]; then
        echo ""
        return
    fi
    for d in $(ls -1 "$bundles_dir" 2>/dev/null | sort); do
        local bundle_date="${d:0:10}"
        if [[ "$bundle_date" > "$today" || "$bundle_date" == "$today" ]]; then
            echo "$bundle_date"
            return
        fi
    done
    echo "$today"
}

# --- Main ---
DRY_RUN=""
if [[ "${1:-}" == "--dry-run" ]]; then
    DRY_RUN="--dry-run"
fi

{
    echo "=== Track 2 Cron — $(date) ==="
    echo "Project: $PROJECT_ROOT"

    status_running "init" "Starting up"

    # Ensure we're on main
    cd "$PROJECT_ROOT"
    branch=$(git rev-parse --abbrev-ref HEAD)
    if [ "$branch" != "main" ]; then
        echo "Not on main branch ($branch), skipping."
        status_done "skipped" "Not on main ($branch)"
        notify "Track 2 Skipped" "Not on main branch: $branch"
        exit 0
    fi

    # Stash only tracked changes (not untracked) to avoid pop conflicts
    STASHED=false
    if ! git diff --quiet HEAD 2>/dev/null; then
        echo "Stashing tracked changes..."
        git stash push -m "track2-cron auto-stash $(date +%Y-%m-%d_%H%M%S)"
        STASHED=true
    fi

    status_running "pull" "Pulling latest"

    # Build poll_interpret args
    BRIEF_DATE=$(next_brief_date)
    ARGS="--pull --workers 4"
    if [ -n "$BRIEF_DATE" ]; then
        ARGS="$ARGS --brief $BRIEF_DATE --publish"
    fi
    if [ -n "$DRY_RUN" ]; then
        ARGS="$ARGS --dry-run"
    fi

    echo "Args: $ARGS"
    echo ""

    # Run Track 2 with a monitoring sidecar that parses log lines for progress.
    # Uses a named pipe so we can capture the real exit code from poll_interpret.
    FIFO="$PROJECT_ROOT/.local/track2-fifo-$$"
    mkfifo "$FIFO"

    # Background reader: parse output lines and update status file
    (while IFS= read -r line; do
        echo "$line"
        if [[ "$line" == *"Needs fold:"* ]]; then
            total=$(echo "$line" | grep -o '[0-9]\+' | head -1)
            status_running "detect" "Found $total meeting(s) to fold" "" "" "0" "${total:-0}"
        elif [[ "$line" == *"Needs interpretation:"* ]]; then
            count=$(echo "$line" | grep -o '[0-9]\+' | head -1)
            [ "${count:-0}" -gt 0 ] && status_running "detect" "$count meeting(s) need interpretation"
        elif [[ "$line" == *"Step 1: Interpretation"* ]] && [[ "$line" != *"nothing to do"* ]]; then
            status_running "interpret" "Running interpretations"
        elif [[ "$line" == *"[exec] interpret_meeting.py"* ]]; then
            persona=$(echo "$line" | grep -o 'PERSONA-[0-9]\+' || true)
            status_running "interpret" "$persona"
        elif [[ "$line" == *"Step 2: Cumulative Fold"* ]]; then
            total=$(echo "$line" | grep -o '[0-9]\+' | head -1)
            status_running "fold" "Starting" "0/${total:-?}" "" "0" "${total:-0}"
        elif [[ "$line" == *"] Folding..."* ]]; then
            meeting=$(echo "$line" | grep -o '\[.*\]' | tr -d '[]')
            status_running "fold" "$meeting" "" "$meeting"
        elif [[ "$line" == *"[exec] fold_meeting.py"* ]]; then
            persona=$(echo "$line" | grep -o 'PERSONA-[0-9]\+' || true)
            status_running "fold" "$persona"
        elif [[ "$line" == *"Step 3: Brief Generation"* ]]; then
            status_running "brief" "Generating briefs"
        elif [[ "$line" == *"Step 4: Publishing"* ]]; then
            status_running "publish" "Publishing to dist/"
        fi
    done < "$FIFO") &
    READER_PID=$!

    # Run poll_interpret — capture its real exit code
    python3 scripts/poll_interpret.py $ARGS > "$FIFO" 2>&1
    POLL_EXIT=$?

    wait "$READER_PID" 2>/dev/null || true
    rm -f "$FIFO"

    if [ "$POLL_EXIT" -eq 0 ]; then
        STATUS="success"
    else
        STATUS="failure"
    fi

    echo ""
    echo "Status: $STATUS"

    # Commit + push if there are changes (and not dry-run)
    if [ -z "$DRY_RUN" ] && [ "$STATUS" = "success" ]; then
        status_running "commit" "Checking for changes"
        if ! git diff --quiet HEAD 2>/dev/null || [ -n "$(git ls-files --others --exclude-standard data/ dist/)" ]; then
            echo ""
            echo "--- Committing results ---"
            git add data/interpretation/ dist/briefings/ 2>/dev/null || true
            if ! git diff --cached --quiet; then
                status_running "commit" "Pushing"
                git commit -m "auto: Track 2 interpret + fold + brief ($(date +%Y-%m-%d))"
                git push
                echo "Committed and pushed."
            else
                echo "Nothing to commit."
            fi
        else
            echo "No changes to commit."
        fi
    fi

    # Restore stashed changes (after commit, so no conflict with cron output)
    if [ "$STASHED" = true ]; then
        echo ""
        echo "--- Restoring stashed changes ---"
        git stash pop || echo "WARNING: stash pop conflict — run 'git stash list' to recover"
    fi

    # Final status + notify
    if [ "$STATUS" = "success" ]; then
        status_done "success"
        notify "Track 2 Complete" "Pipeline finished successfully." "Glass"
    else
        status_done "failure" "Check log"
        notify "Track 2 Failed" "Check log: $LOG_FILE" "Basso"
    fi

    echo ""
    echo "=== Done — $(date) ==="

} 2>&1 | tee "$LOG_FILE"

# Prune logs older than 14 days
find "$LOG_DIR" -name "track2-*.log" -mtime +14 -delete 2>/dev/null || true
