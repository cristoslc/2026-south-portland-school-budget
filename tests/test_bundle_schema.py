"""Tests for MeetingBundle dataclass — SPEC-016, AC1 and AC5.

RED phase: these tests define the expected behavior of MeetingBundle
before the implementation exists. All tests should FAIL (ImportError
or assertion) until task .2 (GREEN) implements the dataclass.

Derives from:
  AC1 — manifest contains: meeting date, meeting type, body, source list,
        optional agenda reference
  AC5 — schema validated by Python script; enforces required fields and
        rejects malformed manifests
"""

import datetime

import pytest
import yaml

from pipeline.bundle_schema import MeetingBundle, BundleSource


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

def _minimal_source():
    """Return a minimal valid BundleSource dict."""
    return {
        "source_id": "src-001",
        "source_type": "transcript",
        "title": "School Board Meeting Transcript",
        "path": "data/raw/2026-03-02-school-board/transcript.vtt",
    }


def _minimal_bundle_dict():
    """Return a minimal valid bundle manifest as a dict."""
    return {
        "schema_version": "1.0",
        "meeting_date": "2026-03-02",
        "meeting_type": "regular",
        "body": "school-board",
        "sources": [_minimal_source()],
    }


# ---------------------------------------------------------------------------
# AC1: Required fields
# ---------------------------------------------------------------------------

class TestRequiredFields:
    """AC1: manifest contains meeting date, type, body, and source list."""

    def test_valid_minimal_bundle(self):
        """A bundle with all required fields should construct successfully."""
        bundle = MeetingBundle.from_dict(_minimal_bundle_dict())
        assert bundle.meeting_date == datetime.date(2026, 3, 2)
        assert bundle.meeting_type == "regular"
        assert bundle.body == "school-board"
        assert len(bundle.sources) == 1

    def test_missing_meeting_date_raises(self):
        """Omitting meeting_date should raise ValueError."""
        data = _minimal_bundle_dict()
        del data["meeting_date"]
        with pytest.raises(ValueError, match="meeting_date"):
            MeetingBundle.from_dict(data)

    def test_missing_meeting_type_raises(self):
        """Omitting meeting_type should raise ValueError."""
        data = _minimal_bundle_dict()
        del data["meeting_type"]
        with pytest.raises(ValueError, match="meeting_type"):
            MeetingBundle.from_dict(data)

    def test_missing_body_raises(self):
        """Omitting body should raise ValueError."""
        data = _minimal_bundle_dict()
        del data["body"]
        with pytest.raises(ValueError, match="body"):
            MeetingBundle.from_dict(data)

    def test_missing_sources_raises(self):
        """Omitting sources should raise ValueError."""
        data = _minimal_bundle_dict()
        del data["sources"]
        with pytest.raises(ValueError, match="sources"):
            MeetingBundle.from_dict(data)

    def test_empty_sources_raises(self):
        """An empty source list should raise ValueError."""
        data = _minimal_bundle_dict()
        data["sources"] = []
        with pytest.raises(ValueError, match="sources"):
            MeetingBundle.from_dict(data)

    def test_missing_schema_version_raises(self):
        """Omitting schema_version should raise ValueError."""
        data = _minimal_bundle_dict()
        del data["schema_version"]
        with pytest.raises(ValueError, match="schema_version"):
            MeetingBundle.from_dict(data)


# ---------------------------------------------------------------------------
# AC1: Optional fields
# ---------------------------------------------------------------------------

class TestOptionalFields:
    """AC1: optional fields (agenda_ref, title, video_url, notes)."""

    def test_agenda_ref_accepted(self):
        """agenda_ref is optional and preserved when present."""
        data = _minimal_bundle_dict()
        data["agenda_ref"] = "data/raw/2026-03-02-school-board/agenda.pdf"
        bundle = MeetingBundle.from_dict(data)
        assert bundle.agenda_ref == "data/raw/2026-03-02-school-board/agenda.pdf"

    def test_agenda_ref_defaults_none(self):
        """agenda_ref defaults to None when omitted."""
        bundle = MeetingBundle.from_dict(_minimal_bundle_dict())
        assert bundle.agenda_ref is None

    def test_title_accepted(self):
        """title is optional and preserved when present."""
        data = _minimal_bundle_dict()
        data["title"] = "Regular Meeting of the School Board"
        bundle = MeetingBundle.from_dict(data)
        assert bundle.title == "Regular Meeting of the School Board"

    def test_video_url_accepted(self):
        """video_url is optional and preserved when present."""
        data = _minimal_bundle_dict()
        data["video_url"] = "https://vimeo.com/example"
        bundle = MeetingBundle.from_dict(data)
        assert bundle.video_url == "https://vimeo.com/example"

    def test_notes_accepted(self):
        """notes is optional and preserved when present."""
        data = _minimal_bundle_dict()
        data["notes"] = "Audio quality poor in first 10 minutes"
        bundle = MeetingBundle.from_dict(data)
        assert bundle.notes == "Audio quality poor in first 10 minutes"


# ---------------------------------------------------------------------------
# AC5: Field validation — date format
# ---------------------------------------------------------------------------

class TestDateValidation:
    """AC5: validates date format (YYYY-MM-DD)."""

    def test_valid_date_string(self):
        """A valid ISO date string should parse to datetime.date."""
        bundle = MeetingBundle.from_dict(_minimal_bundle_dict())
        assert isinstance(bundle.meeting_date, datetime.date)

    def test_invalid_date_format_raises(self):
        """A non-ISO date string should raise ValueError."""
        data = _minimal_bundle_dict()
        data["meeting_date"] = "03/02/2026"
        with pytest.raises(ValueError, match="meeting_date"):
            MeetingBundle.from_dict(data)

    def test_nonsense_date_raises(self):
        """A non-date string should raise ValueError."""
        data = _minimal_bundle_dict()
        data["meeting_date"] = "not-a-date"
        with pytest.raises(ValueError, match="meeting_date"):
            MeetingBundle.from_dict(data)

    def test_date_object_accepted(self):
        """PyYAML parses bare dates as datetime.date; these should be accepted."""
        data = _minimal_bundle_dict()
        data["meeting_date"] = datetime.date(2026, 3, 2)
        bundle = MeetingBundle.from_dict(data)
        assert bundle.meeting_date == datetime.date(2026, 3, 2)


# ---------------------------------------------------------------------------
# AC5: Field validation — enum values
# ---------------------------------------------------------------------------

class TestEnumValidation:
    """AC5: validates enum values for meeting_type, body, source_type."""

    @pytest.mark.parametrize("meeting_type", [
        "workshop", "regular", "special", "budget-forum",
        "budget-workshop", "joint",
    ])
    def test_valid_meeting_types(self, meeting_type):
        """All defined meeting types should be accepted."""
        data = _minimal_bundle_dict()
        data["meeting_type"] = meeting_type
        bundle = MeetingBundle.from_dict(data)
        assert bundle.meeting_type == meeting_type

    def test_invalid_meeting_type_raises(self):
        """An undefined meeting type should raise ValueError."""
        data = _minimal_bundle_dict()
        data["meeting_type"] = "informal"
        with pytest.raises(ValueError, match="meeting_type"):
            MeetingBundle.from_dict(data)

    @pytest.mark.parametrize("body", ["school-board", "city-council"])
    def test_valid_bodies(self, body):
        """All defined body values should be accepted."""
        data = _minimal_bundle_dict()
        data["body"] = body
        bundle = MeetingBundle.from_dict(data)
        assert bundle.body == body

    def test_invalid_body_raises(self):
        """An undefined body should raise ValueError."""
        data = _minimal_bundle_dict()
        data["body"] = "planning-board"
        with pytest.raises(ValueError, match="body"):
            MeetingBundle.from_dict(data)


# ---------------------------------------------------------------------------
# AC5: Source entry validation
# ---------------------------------------------------------------------------

class TestSourceValidation:
    """AC5: validates source entries within a bundle."""

    def test_valid_source_roundtrip(self):
        """A valid source dict should produce a BundleSource with correct fields."""
        src = BundleSource.from_dict(_minimal_source())
        assert src.source_id == "src-001"
        assert src.source_type == "transcript"
        assert src.title == "School Board Meeting Transcript"
        assert src.path == "data/raw/2026-03-02-school-board/transcript.vtt"

    def test_source_missing_source_id_raises(self):
        """source_id is required."""
        src = _minimal_source()
        del src["source_id"]
        with pytest.raises(ValueError, match="source_id"):
            BundleSource.from_dict(src)

    def test_source_missing_path_raises(self):
        """path is required."""
        src = _minimal_source()
        del src["path"]
        with pytest.raises(ValueError, match="path"):
            BundleSource.from_dict(src)

    def test_source_invalid_type_raises(self):
        """An undefined source_type should raise ValueError."""
        src = _minimal_source()
        src["source_type"] = "video"
        with pytest.raises(ValueError, match="source_type"):
            BundleSource.from_dict(src)

    @pytest.mark.parametrize("source_type", [
        "transcript", "agenda", "packet", "presentation",
        "spreadsheet", "document", "other",
    ])
    def test_valid_source_types(self, source_type):
        """All defined source types should be accepted."""
        src = _minimal_source()
        src["source_type"] = source_type
        parsed = BundleSource.from_dict(src)
        assert parsed.source_type == source_type

    def test_source_optional_fields(self):
        """Optional source fields are preserved when present."""
        src = _minimal_source()
        src["normalized_path"] = "docs/troves/school-board/transcript.md"
        src["evidence_pool"] = "school-board-budget-meetings"
        src["description"] = "Full meeting transcript"
        src["hash"] = "sha256:" + "a" * 64
        src["duration"] = "02:15:30"
        parsed = BundleSource.from_dict(src)
        assert parsed.normalized_path == src["normalized_path"]
        assert parsed.evidence_pool == src["evidence_pool"]
        assert parsed.description == src["description"]
        assert parsed.hash == src["hash"]
        assert parsed.duration == src["duration"]

    def test_source_hash_invalid_format_raises(self):
        """hash must match sha256:<64 hex chars>."""
        src = _minimal_source()
        src["hash"] = "md5:abc123"
        with pytest.raises(ValueError, match="hash"):
            BundleSource.from_dict(src)

    def test_source_duration_invalid_format_raises(self):
        """duration must match HH:MM:SS."""
        src = _minimal_source()
        src["duration"] = "2h15m"
        with pytest.raises(ValueError, match="duration"):
            BundleSource.from_dict(src)


# ---------------------------------------------------------------------------
# AC5: Reject unexpected fields (additionalProperties: false)
# ---------------------------------------------------------------------------

class TestUnexpectedFields:
    """AC5: malformed manifests are rejected."""

    def test_unexpected_top_level_field_raises(self):
        """Extra top-level keys should raise ValueError."""
        data = _minimal_bundle_dict()
        data["attendees"] = ["Alice", "Bob"]
        with pytest.raises(ValueError, match="attendees"):
            MeetingBundle.from_dict(data)

    def test_unexpected_source_field_raises(self):
        """Extra keys in a source entry should raise ValueError."""
        data = _minimal_bundle_dict()
        data["sources"][0]["speaker_count"] = 5
        with pytest.raises(ValueError, match="speaker_count"):
            MeetingBundle.from_dict(data)

    def test_wrong_schema_version_raises(self):
        """A schema_version other than '1.0' should raise ValueError."""
        data = _minimal_bundle_dict()
        data["schema_version"] = "2.0"
        with pytest.raises(ValueError, match="schema_version"):
            MeetingBundle.from_dict(data)


# ---------------------------------------------------------------------------
# YAML round-trip
# ---------------------------------------------------------------------------

class TestYamlRoundTrip:
    """Bundle can be loaded from and dumped to YAML."""

    def test_from_yaml_string(self):
        """MeetingBundle.from_yaml should parse a YAML string."""
        yaml_str = yaml.dump(_minimal_bundle_dict(), default_flow_style=False)
        bundle = MeetingBundle.from_yaml(yaml_str)
        assert bundle.meeting_type == "regular"
        assert len(bundle.sources) == 1

    def test_to_yaml_roundtrip(self):
        """to_yaml -> from_yaml should produce an equivalent bundle."""
        original = MeetingBundle.from_dict(_minimal_bundle_dict())
        yaml_str = original.to_yaml()
        restored = MeetingBundle.from_yaml(yaml_str)
        assert restored.meeting_date == original.meeting_date
        assert restored.meeting_type == original.meeting_type
        assert restored.body == original.body
        assert len(restored.sources) == len(original.sources)

    def test_to_dict_contains_required_keys(self):
        """to_dict should return a dict with all required keys."""
        bundle = MeetingBundle.from_dict(_minimal_bundle_dict())
        d = bundle.to_dict()
        assert "schema_version" in d
        assert "meeting_date" in d
        assert "meeting_type" in d
        assert "body" in d
        assert "sources" in d
