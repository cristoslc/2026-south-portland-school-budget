"""Tests for pending state infrastructure.

TDD Cycle 1: Sidecar Generation
TDD Cycle 2: Stage Detection
"""

import tempfile
from pathlib import Path

import pytest

from pipeline.pending import generate_sidecars, get_stage, resolve_bundle


class TestGenerateSidecars:
    """Tests for AC1: Sidecar Generation."""

    def test_generate_sidecars_creates_pending_directories(self, tmp_path: Path) -> None:
        """Test that generate_sidecars creates .pending/PERSONA-NNN/ directories."""
        # Arrange
        bundle = tmp_path / "bundle"
        bundle.mkdir()
        (bundle / "manifest.yaml").write_text("meeting_id: test-meeting\n")

        personas = [
            {"id": "PERSONA-001", "name": "Teacher", "body": "You are a teacher."},
            {"id": "PERSONA-002", "name": "Parent", "body": "You are a parent."},
        ]

        # Act
        generate_sidecars(bundle, stage="interpret", personas=personas)

        # Assert
        pending_dir = bundle / ".pending"
        assert pending_dir.exists(), ".pending/ directory should be created"
        assert (pending_dir / "PERSONA-001").is_dir()
        assert (pending_dir / "PERSONA-002").is_dir()

    def test_sidecar_template_includes_context_and_prompt(self, tmp_path: Path) -> None:
        """Test that sidecar templates include persona context and task prompt."""
        # Arrange
        bundle = tmp_path / "bundle"
        bundle.mkdir()
        (bundle / "manifest.yaml").write_text("meeting_id: test-meeting\n")

        personas = [
            {"id": "PERSONA-001", "name": "Teacher", "body": "You are a teacher."},
        ]

        # Act
        generate_sidecars(bundle, stage="interpret", personas=personas)

        # Assert
        template_path = bundle / ".pending" / "PERSONA-001" / "interpret.j2"
        assert template_path.exists(), "Template file should be created"
        
        content = template_path.read_text()
        assert "PERSONA-001" in content, "Template should include persona ID"
        assert "Teacher" in content, "Template should include persona name"
        assert "You are a teacher" in content, "Template should include persona body"

    def test_generate_sidecars_performance_five_seconds(self, tmp_path: Path) -> None:
        """Test that sidecar generation completes in <5 seconds for 15 personas."""
        import time

        # Arrange
        bundle = tmp_path / "bundle"
        bundle.mkdir()
        (bundle / "manifest.yaml").write_text("meeting_id: test-meeting\n")

        personas = [
            {"id": f"PERSONA-{i:03d}", "name": f"Persona {i}", "body": f"You are persona {i}."}
            for i in range(1, 16)  # 15 personas
        ]

        # Act
        start = time.time()
        generate_sidecars(bundle, stage="interpret", personas=personas)
        elapsed = time.time() - start

        # Assert
        assert elapsed < 5.0, f"Generation should take <5 seconds, took {elapsed:.2f}s"

    def test_generate_sidecar_skips_existing_pending(self, tmp_path: Path) -> None:
        """Test that generate_sidecars skips personas that already have templates."""
        # Arrange
        bundle = tmp_path / "bundle"
        bundle.mkdir()
        (bundle / "manifest.yaml").write_text("meeting_id: test-meeting\n")

        # Pre-create a pending sidecar for PERSONA-001
        pending_dir = bundle / ".pending" / "PERSONA-001"
        pending_dir.mkdir(parents=True)
        (pending_dir / "interpret.j2").write_text("existing template")

        personas = [
            {"id": "PERSONA-001", "name": "Teacher", "body": "You are a teacher."},
            {"id": "PERSONA-002", "name": "Parent", "body": "You are a parent."},
        ]

        # Act
        generate_sidecars(bundle, stage="interpret", personas=personas)

        # Assert - existing template should be preserved
        existing = (bundle / ".pending" / "PERSONA-001" / "interpret.j2").read_text()
        assert existing == "existing template", "Existing template should not be overwritten"


class TestGetStage:
    """Tests for AC2: Stage Detection."""

    def test_get_stage_returns_pending_when_template_exists(self, tmp_path: Path) -> None:
        """Test that get_stage returns 'pending-interpret' when template exists but no output."""
        # Arrange
        bundle = tmp_path / "bundle"
        bundle.mkdir()
        
        pending_dir = bundle / ".pending" / "PERSONA-001"
        pending_dir.mkdir(parents=True)
        (pending_dir / "interpret.j2").write_text("# Template content")

        # Act
        stage = get_stage(bundle, "PERSONA-001")

        # Assert
        assert stage == "pending-interpret", f"Expected 'pending-interpret', got '{stage}'"

    def test_get_stage_returns_ready_when_output_exists(self, tmp_path: Path) -> None:
        """Test that get_stage returns 'ready-to-resolve' when output.md exists."""
        # Arrange
        bundle = tmp_path / "bundle"
        bundle.mkdir()
        
        pending_dir = bundle / ".pending" / "PERSONA-001"
        pending_dir.mkdir(parents=True)
        (pending_dir / "interpret.j2").write_text("# Template")
        (pending_dir / "interpret.md").write_text("# Output")

        # Act
        stage = get_stage(bundle, "PERSONA-001")

        # Assert
        assert stage == "ready-to-resolve", f"Expected 'ready-to-resolve', got '{stage}'"

    def test_get_stage_returns_done_when_no_pending(self, tmp_path: Path) -> None:
        """Test that get_stage returns 'done' when no .pending directory exists."""
        # Arrange
        bundle = tmp_path / "bundle"
        bundle.mkdir()

        # Act
        stage = get_stage(bundle, "PERSONA-001")

        # Assert
        assert stage == "done", f"Expected 'done', got '{stage}'"

    def test_get_stage_performance_one_second(self, tmp_path: Path) -> None:
        """Test that stage detection completes in <1 second."""
        import time

        # Arrange
        bundle = tmp_path / "bundle"
        bundle.mkdir()
        
        # Create 100 persona directories
        for i in range(100):
            pending_dir = bundle / ".pending" / f"PERSONA-{i:03d}"
            pending_dir.mkdir(parents=True)
            if i < 50:
                (pending_dir / "interpret.j2").write_text("# Template")
            else:
                (pending_dir / "interpret.j2").write_text("# Template")
                (pending_dir / "interpret.md").write_text("# Output")

        # Act
        start = time.time()
        for i in range(100):
            _ = get_stage(bundle, f"PERSONA-{i:03d}")
        elapsed = time.time() - start

        # Assert
        assert elapsed < 1.0, f"100 stage checks should take <1 second, took {elapsed:.2f}s"


class TestResolveScanner:
    """Tests for AC3: Resolve Scanner."""

    def test_resolve_applies_completed_outputs(self, tmp_path: Path) -> None:
        """Test that resolve applies completed sidecars to final location."""
        # Arrange
        bundle = tmp_path / "bundle"
        bundle.mkdir()
        
        # Create completed sidecars
        for persona_id in ["PERSONA-001", "PERSONA-002", "PERSONA-003"]:
            pending_dir = bundle / ".pending" / persona_id
            pending_dir.mkdir(parents=True)
            (pending_dir / "interpret.j2").write_text("# Template")
            (pending_dir / "interpret.md").write_text(f"# Interpretation for {persona_id}")

        output_dir = tmp_path / "outputs"

        # Act
        result = resolve_bundle(bundle, stage="interpret", output_dir=output_dir)

        # Assert
        assert result["applied"] == 3
        assert result["pending"] == 0
        assert result["failed"] == 0
        assert (output_dir / "PERSONA-001.md").exists()
        assert (output_dir / "PERSONA-002.md").exists()
        assert (output_dir / "PERSONA-003.md").exists()

    def test_resolve_cleans_up_pending_directories(self, tmp_path: Path) -> None:
        """Test that resolve removes .pending/ directories for resolved items."""
        # Arrange
        bundle = tmp_path / "bundle"
        bundle.mkdir()
        
        pending_dir = bundle / ".pending" / "PERSONA-001"
        pending_dir.mkdir(parents=True)
        (pending_dir / "interpret.j2").write_text("# Template")
        (pending_dir / "interpret.md").write_text("# Interpretation")

        output_dir = tmp_path / "outputs"

        # Act
        resolve_bundle(bundle, stage="interpret", output_dir=output_dir)

        # Assert - .pending should be cleaned up after resolution
        assert not (bundle / ".pending" / "PERSONA-001").exists()

    def test_resolve_reports_pending_count(self, tmp_path: Path) -> None:
        """Test that resolve reports correct pending count."""
        # Arrange
        bundle = tmp_path / "bundle"
        bundle.mkdir()
        
        # Create completed sidecar
        done_dir = bundle / ".pending" / "PERSONA-001"
        done_dir.mkdir(parents=True)
        (done_dir / "interpret.j2").write_text("# Template")
        (done_dir / "interpret.md").write_text("# Interpretation")

        # Create pending sidecars (template only)
        for persona_id in ["PERSONA-002", "PERSONA-003", "PERSONA-004"]:
            pending_dir = bundle / ".pending" / persona_id
            pending_dir.mkdir(parents=True)
            (pending_dir / "interpret.j2").write_text("# Template")

        output_dir = tmp_path / "outputs"

        # Act
        result = resolve_bundle(bundle, stage="interpret", output_dir=output_dir)

        # Assert
        assert result["applied"] == 1
        assert result["pending"] == 3
        assert result["failed"] == 0

    def test_resolve_isolates_failures(self, tmp_path: Path) -> None:
        """Test that resolve reports failures without blocking other sidecars."""
        # Arrange
        bundle = tmp_path / "bundle"
        bundle.mkdir()
        
        # Create valid sidecar
        valid_dir = bundle / ".pending" / "PERSONA-001"
        valid_dir.mkdir(parents=True)
        (valid_dir / "interpret.j2").write_text("# Template")
        (valid_dir / "interpret.md").write_text("# Valid interpretation")

        # Create invalid sidecar (missing required sections)
        invalid_dir = bundle / ".pending" / "PERSONA-002"
        invalid_dir.mkdir(parents=True)
        (invalid_dir / "interpret.j2").write_text("# Template")
        (invalid_dir / "interpret.md").write_text("")  # Empty output

        output_dir = tmp_path / "outputs"

        # Act
        result = resolve_bundle(bundle, stage="interpret", output_dir=output_dir)

        # Assert
        assert result["applied"] == 1
        assert result["pending"] == 0
        assert result["failed"] == 1
        assert len(result["errors"]) == 1
        assert "PERSONA-002" in result["errors"][0]


class TestStreamingResolve:
    """Tests for AC4: Streaming Resolve."""

    def test_streaming_resolve_applies_partial_completion(self, tmp_path: Path) -> None:
        """Test that streaming resolve applies completed items and leaves pending."""
        # Arrange
        bundle = tmp_path / "bundle"
        bundle.mkdir()
        
        # Create completed sidecars
        for persona_id in ["PERSONA-001", "PERSONA-002"]:
            pending_dir = bundle / ".pending" / persona_id
            pending_dir.mkdir(parents=True)
            (pending_dir / "interpret.j2").write_text("# Template")
            (pending_dir / "interpret.md").write_text(f"# Interpretation {persona_id}")

        # Create pending sidecars
        for persona_id in ["PERSONA-003", "PERSONA-004"]:
            pending_dir = bundle / ".pending" / persona_id
            pending_dir.mkdir(parents=True)
            (pending_dir / "interpret.j2").write_text("# Template")

        output_dir = tmp_path / "outputs"

        # Act
        result = resolve_bundle(bundle, stage="interpret", streaming=True, output_dir=output_dir)

        # Assert
        assert result["applied"] == 2
        assert result["pending"] == 2
        
        # Completed items resolved
        assert (output_dir / "PERSONA-001.md").exists()
        assert (output_dir / "PERSONA-002.md").exists()
        
        # Pending items still in .pending
        assert (bundle / ".pending" / "PERSONA-003" / "interpret.j2").exists()
        assert (bundle / ".pending" / "PERSONA-004" / "interpret.j2").exists()


class TestIntegration:
    """Tests for AC5: Integration (full cycle and visibility)."""

    def test_full_cycle_generate_fill_resolve(self, tmp_path: Path) -> None:
        """Test complete cycle: generate sidecars, fill, then resolve."""
        # Arrange
        bundle = tmp_path / "bundle"
        bundle.mkdir()
        (bundle / "manifest.yaml").write_text("meeting_id: test-meeting\n")

        personas = [
            {"id": "PERSONA-001", "name": "Teacher", "body": "You are a teacher."},
            {"id": "PERSONA-002", "name": "Parent", "body": "You are a parent."},
        ]

        output_dir = tmp_path / "outputs"

        # Act - Generate phase
        generate_sidecars(bundle, stage="interpret", personas=personas)

        # Assert - Templates created
        assert (bundle / ".pending" / "PERSONA-001" / "interpret.j2").exists()
        assert (bundle / ".pending" / "PERSONA-002" / "interpret.j2").exists()

        # Simulate fill phase (agent fills templates)
        for persona_id in ["PERSONA-001", "PERSONA-002"]:
            output_file = bundle / ".pending" / persona_id / "interpret.md"
            output_file.write_text(f"# Interpretation for {persona_id}\n\nStructured points...")

        # Act - Resolve phase
        result = resolve_bundle(bundle, stage="interpret", output_dir=output_dir)

        # Assert - All resolved
        assert result["applied"] == 2
        assert result["pending"] == 0
        assert result["failed"] == 0
        assert (output_dir / "PERSONA-001.md").exists()
        assert (output_dir / "PERSONA-002.md").exists()
        assert not (bundle / ".pending" / "PERSONA-001").exists()

    def test_visibility_commands(self, tmp_path: Path) -> None:
        """Test that visibility commands (find, ls) work on .pending structure."""
        # Arrange
        bundle = tmp_path / "bundle"
        bundle.mkdir()

        personas = [
            {"id": f"PERSONA-{i:03d}", "name": f"Persona {i}", "body": f"You are persona {i}."}
            for i in range(1, 6)  # 5 personas
        ]

        # Generate
        generate_sidecars(bundle, stage="interpret", personas=personas)

        # Fill 2 of them
        for persona_id in ["PERSONA-001", "PERSONA-002"]:
            output_file = bundle / ".pending" / persona_id / "interpret.md"
            output_file.write_text(f"# Interpretation for {persona_id}")

        # Act - Visibility commands (using pathlib equivalents)
        # Count pending: has .j2 but no .md
        pending_count = 0
        completed_count = 0
        for persona_dir in (bundle / ".pending").iterdir():
            if persona_dir.is_dir():
                has_j2 = (persona_dir / "interpret.j2").exists()
                has_md = (persona_dir / "interpret.md").exists()
                if has_j2 and not has_md:
                    pending_count += 1
                if has_md:
                    completed_count += 1
        total_count = len(list((bundle / ".pending").iterdir()))

        # Assert
        assert pending_count == 3, f"Expected 3 pending, found {pending_count}"
        assert completed_count == 2, f"Expected 2 completed, found {completed_count}"
        assert total_count == 5, f"Expected 5 total persona directories, found {total_count}"