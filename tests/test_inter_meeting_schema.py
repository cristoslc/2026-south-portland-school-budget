"""Tests for InterMeetingEvidence dataclass — SPEC-016, AC4.

RED phase: these tests define the expected behavior of InterMeetingManifest
and InterMeetingEntry before the implementation exists.

Derives from:
  AC4 — inter-meeting evidence has a date range (posted_after / posted_before)
        and is accessible to the upcoming-event brief generator
"""

import datetime

import pytest
import yaml

from pipeline.inter_meeting_schema import InterMeetingManifest, InterMeetingEntry


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

def _minimal_entry():
    """Return a minimal valid inter-meeting entry dict."""
    return {
        "entry_id": "im-001",
        "date_posted": "2026-03-04",
        "source_type": "news-article",
        "source_path": "data/news/2026-03-04-budget-article.md",
        "description": "Local news coverage of the budget workshop.",
        "date_range": {
            "posted_after": "2026-03-02",
            "posted_before": "2026-03-05",
        },
    }


def _minimal_manifest_dict():
    """Return a minimal valid inter-meeting manifest dict."""
    return {
        "schema_version": "1.0",
        "entries": [_minimal_entry()],
    }


# ---------------------------------------------------------------------------
# AC4: Required fields — entry level
# ---------------------------------------------------------------------------

class TestEntryRequiredFields:
    """AC4: inter-meeting entries have required fields."""

    def test_valid_minimal_entry(self):
        """An entry with all required fields should construct successfully."""
        entry = InterMeetingEntry.from_dict(_minimal_entry())
        assert entry.entry_id == "im-001"
        assert entry.date_posted == datetime.date(2026, 3, 4)
        assert entry.source_type == "news-article"

    def test_missing_entry_id_raises(self):
        data = _minimal_entry()
        del data["entry_id"]
        with pytest.raises(ValueError, match="entry_id"):
            InterMeetingEntry.from_dict(data)

    def test_missing_date_posted_raises(self):
        data = _minimal_entry()
        del data["date_posted"]
        with pytest.raises(ValueError, match="date_posted"):
            InterMeetingEntry.from_dict(data)

    def test_missing_source_type_raises(self):
        data = _minimal_entry()
        del data["source_type"]
        with pytest.raises(ValueError, match="source_type"):
            InterMeetingEntry.from_dict(data)

    def test_missing_source_path_raises(self):
        data = _minimal_entry()
        del data["source_path"]
        with pytest.raises(ValueError, match="source_path"):
            InterMeetingEntry.from_dict(data)

    def test_missing_description_raises(self):
        data = _minimal_entry()
        del data["description"]
        with pytest.raises(ValueError, match="description"):
            InterMeetingEntry.from_dict(data)

    def test_missing_date_range_raises(self):
        data = _minimal_entry()
        del data["date_range"]
        with pytest.raises(ValueError, match="date_range"):
            InterMeetingEntry.from_dict(data)


# ---------------------------------------------------------------------------
# AC4: Date range validation
# ---------------------------------------------------------------------------

class TestDateRange:
    """AC4: date range has posted_after and posted_before, correctly ordered."""

    def test_valid_date_range(self):
        """posted_after < posted_before should work."""
        entry = InterMeetingEntry.from_dict(_minimal_entry())
        assert entry.date_range_after == datetime.date(2026, 3, 2)
        assert entry.date_range_before == datetime.date(2026, 3, 5)

    def test_missing_posted_after_raises(self):
        data = _minimal_entry()
        del data["date_range"]["posted_after"]
        with pytest.raises(ValueError, match="posted_after"):
            InterMeetingEntry.from_dict(data)

    def test_missing_posted_before_raises(self):
        data = _minimal_entry()
        del data["date_range"]["posted_before"]
        with pytest.raises(ValueError, match="posted_before"):
            InterMeetingEntry.from_dict(data)

    def test_posted_after_not_before_posted_before_raises(self):
        """posted_after >= posted_before should raise ValueError."""
        data = _minimal_entry()
        data["date_range"]["posted_after"] = "2026-03-05"
        data["date_range"]["posted_before"] = "2026-03-02"
        with pytest.raises(ValueError, match="posted_after.*before.*posted_before"):
            InterMeetingEntry.from_dict(data)

    def test_equal_dates_raises(self):
        """posted_after == posted_before should raise ValueError."""
        data = _minimal_entry()
        data["date_range"]["posted_after"] = "2026-03-02"
        data["date_range"]["posted_before"] = "2026-03-02"
        with pytest.raises(ValueError, match="posted_after.*before.*posted_before"):
            InterMeetingEntry.from_dict(data)

    def test_invalid_posted_after_format_raises(self):
        data = _minimal_entry()
        data["date_range"]["posted_after"] = "March 2"
        with pytest.raises(ValueError, match="posted_after"):
            InterMeetingEntry.from_dict(data)

    def test_date_objects_accepted(self):
        """PyYAML parses bare dates as datetime.date."""
        data = _minimal_entry()
        data["date_posted"] = datetime.date(2026, 3, 4)
        data["date_range"]["posted_after"] = datetime.date(2026, 3, 2)
        data["date_range"]["posted_before"] = datetime.date(2026, 3, 5)
        entry = InterMeetingEntry.from_dict(data)
        assert entry.date_range_after == datetime.date(2026, 3, 2)

    def test_unexpected_date_range_field_raises(self):
        data = _minimal_entry()
        data["date_range"]["meeting_id"] = "mtg-001"
        with pytest.raises(ValueError, match="meeting_id"):
            InterMeetingEntry.from_dict(data)


# ---------------------------------------------------------------------------
# AC4: Enum validation
# ---------------------------------------------------------------------------

class TestEntryEnumValidation:
    """Validates enum fields on inter-meeting entries."""

    @pytest.mark.parametrize("source_type", [
        "news-article", "public-statement", "document",
        "letter", "announcement", "other",
    ])
    def test_valid_source_types(self, source_type):
        data = _minimal_entry()
        data["source_type"] = source_type
        entry = InterMeetingEntry.from_dict(data)
        assert entry.source_type == source_type

    def test_invalid_source_type_raises(self):
        data = _minimal_entry()
        data["source_type"] = "blog-post"
        with pytest.raises(ValueError, match="source_type"):
            InterMeetingEntry.from_dict(data)

    @pytest.mark.parametrize("body", ["school-board", "city-council", "both"])
    def test_valid_body_values(self, body):
        data = _minimal_entry()
        data["body"] = body
        entry = InterMeetingEntry.from_dict(data)
        assert entry.body == body

    def test_invalid_body_raises(self):
        data = _minimal_entry()
        data["body"] = "planning-board"
        with pytest.raises(ValueError, match="body"):
            InterMeetingEntry.from_dict(data)


# ---------------------------------------------------------------------------
# AC4: Optional fields
# ---------------------------------------------------------------------------

class TestEntryOptionalFields:
    """Optional fields on inter-meeting entries."""

    def test_title_preserved(self):
        data = _minimal_entry()
        data["title"] = "Budget Coverage — March 4"
        entry = InterMeetingEntry.from_dict(data)
        assert entry.title == "Budget Coverage — March 4"

    def test_body_preserved(self):
        data = _minimal_entry()
        data["body"] = "school-board"
        entry = InterMeetingEntry.from_dict(data)
        assert entry.body == "school-board"

    def test_normalized_path_preserved(self):
        data = _minimal_entry()
        data["normalized_path"] = "docs/evidence-pools/news/article.md"
        entry = InterMeetingEntry.from_dict(data)
        assert entry.normalized_path == "docs/evidence-pools/news/article.md"

    def test_optional_fields_default_none(self):
        entry = InterMeetingEntry.from_dict(_minimal_entry())
        assert entry.title is None
        assert entry.body is None
        assert entry.normalized_path is None


# ---------------------------------------------------------------------------
# Manifest-level validation
# ---------------------------------------------------------------------------

class TestManifestLevel:
    """InterMeetingManifest top-level validation."""

    def test_valid_minimal_manifest(self):
        manifest = InterMeetingManifest.from_dict(_minimal_manifest_dict())
        assert manifest.schema_version == "1.0"
        assert len(manifest.entries) == 1

    def test_empty_entries_allowed(self):
        """An empty entries list is valid (no inter-meeting evidence yet)."""
        data = {"schema_version": "1.0", "entries": []}
        manifest = InterMeetingManifest.from_dict(data)
        assert len(manifest.entries) == 0

    def test_missing_schema_version_raises(self):
        data = _minimal_manifest_dict()
        del data["schema_version"]
        with pytest.raises(ValueError, match="schema_version"):
            InterMeetingManifest.from_dict(data)

    def test_wrong_schema_version_raises(self):
        data = _minimal_manifest_dict()
        data["schema_version"] = "2.0"
        with pytest.raises(ValueError, match="schema_version"):
            InterMeetingManifest.from_dict(data)

    def test_missing_entries_raises(self):
        data = {"schema_version": "1.0"}
        with pytest.raises(ValueError, match="entries"):
            InterMeetingManifest.from_dict(data)

    def test_unexpected_field_raises(self):
        data = _minimal_manifest_dict()
        data["description"] = "should not be here"
        with pytest.raises(ValueError, match="description"):
            InterMeetingManifest.from_dict(data)

    def test_unexpected_entry_field_raises(self):
        data = _minimal_manifest_dict()
        data["entries"][0]["priority"] = "high"
        with pytest.raises(ValueError, match="priority"):
            InterMeetingManifest.from_dict(data)


# ---------------------------------------------------------------------------
# YAML round-trip
# ---------------------------------------------------------------------------

class TestInterMeetingYamlRoundTrip:
    """InterMeetingManifest can be loaded from and dumped to YAML."""

    def test_from_yaml_string(self):
        yaml_str = yaml.dump(_minimal_manifest_dict(), default_flow_style=False)
        manifest = InterMeetingManifest.from_yaml(yaml_str)
        assert len(manifest.entries) == 1

    def test_to_yaml_roundtrip(self):
        original = InterMeetingManifest.from_dict(_minimal_manifest_dict())
        yaml_str = original.to_yaml()
        restored = InterMeetingManifest.from_yaml(yaml_str)
        assert len(restored.entries) == len(original.entries)
        assert restored.entries[0].entry_id == original.entries[0].entry_id

    def test_to_dict_contains_required_keys(self):
        manifest = InterMeetingManifest.from_dict(_minimal_manifest_dict())
        d = manifest.to_dict()
        assert "schema_version" in d
        assert "entries" in d
