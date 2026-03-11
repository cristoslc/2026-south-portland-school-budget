#!/bin/bash
set -euo pipefail

# Deregister runner on container stop
cleanup() {
    echo "Removing runner..."
    ./config.sh remove --token "${RUNNER_TOKEN}" 2>/dev/null || true
}
trap cleanup EXIT

# Configure the runner if not already configured
if [ ! -f ".runner" ]; then
    echo "Configuring runner..."
    ./config.sh \
        --url "https://github.com/${GITHUB_REPOSITORY}" \
        --token "${RUNNER_TOKEN}" \
        --name "${RUNNER_NAME:-$(hostname)}" \
        --labels "${RUNNER_LABELS:-self-hosted,linux,x64}" \
        --unattended \
        --replace
fi

echo "Starting runner..."
exec ./run.sh
