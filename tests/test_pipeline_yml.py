"""
Tests validating .github/workflows/pipeline.yml structure for ADR-002
two-track architecture (evidence pipeline + meeting bundler with separate commits).
"""

import pathlib
import pytest
import yaml

REPO_ROOT = pathlib.Path(__file__).resolve().parent.parent
PIPELINE_PATH = REPO_ROOT / ".github" / "workflows" / "pipeline.yml"


@pytest.fixture(scope="module")
def workflow():
    with open(PIPELINE_PATH) as f:
        return yaml.safe_load(f)


@pytest.fixture(scope="module")
def primary_steps(workflow):
    return workflow["jobs"]["update-evidence"]["steps"]


@pytest.fixture(scope="module")
def fallback_steps(workflow):
    return workflow["jobs"]["update-evidence-fallback"]["steps"]


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _step_names(steps):
    return [s["name"] for s in steps]


def _find_step(steps, name):
    for s in steps:
        if s["name"] == name:
            return s
    return None


# ---------------------------------------------------------------------------
# 1. Primary job step ordering
# ---------------------------------------------------------------------------

EXPECTED_ORDER = [
    "Checkout",
    "Run evidence pipeline",
    "Commit evidence changes",
    "Run meeting bundler",
    "Commit bundle changes",
    "Push changes",
]


class TestPrimaryJobStructure:
    def test_expected_steps_present(self, primary_steps):
        names = _step_names(primary_steps)
        for expected in EXPECTED_ORDER:
            assert expected in names, f"Missing step: {expected}"

    def test_step_order(self, primary_steps):
        names = _step_names(primary_steps)
        indices = [names.index(n) for n in EXPECTED_ORDER]
        assert indices == sorted(indices), (
            f"Steps out of order. Got indices {indices} for {EXPECTED_ORDER}"
        )

    def test_checkout_is_first(self, primary_steps):
        assert primary_steps[0]["name"] == "Checkout"

    def test_evidence_pipeline_runs_pipeline_py(self, primary_steps):
        step = _find_step(primary_steps, "Run evidence pipeline")
        assert "pipeline.py" in step["run"]

    def test_meeting_bundler_runs_bundle_meetings(self, primary_steps):
        step = _find_step(primary_steps, "Run meeting bundler")
        assert "bundle_meetings.py" in step["run"]
        assert "--stage" in step["run"]

    def test_evidence_commit_before_bundler(self, primary_steps):
        names = _step_names(primary_steps)
        assert names.index("Commit evidence changes") < names.index("Run meeting bundler")

    def test_bundle_commit_after_bundler(self, primary_steps):
        names = _step_names(primary_steps)
        assert names.index("Run meeting bundler") < names.index("Commit bundle changes")

    def test_push_is_last(self, primary_steps):
        assert primary_steps[-1]["name"] == "Push changes"


# ---------------------------------------------------------------------------
# 2. Fallback job mirrors primary structure
# ---------------------------------------------------------------------------

class TestFallbackJobStructure:
    def test_fallback_job_exists(self, workflow):
        assert "update-evidence-fallback" in workflow["jobs"]

    def test_fallback_has_expected_steps(self, fallback_steps):
        names = _step_names(fallback_steps)
        for expected in EXPECTED_ORDER:
            assert expected in names, f"Fallback missing step: {expected}"

    def test_fallback_step_order(self, fallback_steps):
        names = _step_names(fallback_steps)
        indices = [names.index(n) for n in EXPECTED_ORDER]
        assert indices == sorted(indices), (
            f"Fallback steps out of order. Got indices {indices} for {EXPECTED_ORDER}"
        )

    def test_fallback_evidence_runs_pipeline_py(self, fallback_steps):
        step = _find_step(fallback_steps, "Run evidence pipeline")
        assert "pipeline.py" in step["run"]

    def test_fallback_bundler_runs_bundle_meetings(self, fallback_steps):
        step = _find_step(fallback_steps, "Run meeting bundler")
        assert "bundle_meetings.py" in step["run"]
        assert "--stage" in step["run"]

    def test_fallback_push_is_last(self, fallback_steps):
        assert fallback_steps[-1]["name"] == "Push changes"


# ---------------------------------------------------------------------------
# 3. Both jobs use same commit message patterns
# ---------------------------------------------------------------------------

class TestCommitMessagePatterns:
    @pytest.mark.parametrize("job_key", ["update-evidence", "update-evidence-fallback"])
    def test_evidence_commit_message(self, workflow, job_key):
        steps = workflow["jobs"][job_key]["steps"]
        step = _find_step(steps, "Commit evidence changes")
        assert 'chore(pipeline): auto-update evidence pools' in step["run"]

    @pytest.mark.parametrize("job_key", ["update-evidence", "update-evidence-fallback"])
    def test_bundle_commit_message(self, workflow, job_key):
        steps = workflow["jobs"][job_key]["steps"]
        step = _find_step(steps, "Commit bundle changes")
        assert 'chore(pipeline): auto-update meeting bundles' in step["run"]

    @pytest.mark.parametrize("job_key", ["update-evidence", "update-evidence-fallback"])
    def test_separate_step_ids(self, workflow, job_key):
        """Evidence and bundle commits use distinct step IDs."""
        steps = workflow["jobs"][job_key]["steps"]
        evidence = _find_step(steps, "Commit evidence changes")
        bundles = _find_step(steps, "Commit bundle changes")
        assert evidence.get("id") == "evidence"
        assert bundles.get("id") == "bundles"


# ---------------------------------------------------------------------------
# 4. Push step is conditional on either having changes
# ---------------------------------------------------------------------------

class TestPushConditional:
    @pytest.mark.parametrize("job_key", ["update-evidence", "update-evidence-fallback"])
    def test_push_conditional_on_changes(self, workflow, job_key):
        steps = workflow["jobs"][job_key]["steps"]
        push = _find_step(steps, "Push changes")
        condition = push.get("if", "")
        assert "steps.evidence.outputs.has_changes" in condition
        assert "steps.bundles.outputs.has_changes" in condition
        assert "||" in condition, "Push condition should OR both change flags"
