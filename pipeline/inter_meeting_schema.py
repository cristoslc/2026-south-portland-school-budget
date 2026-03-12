"""Inter-Meeting Evidence Schema — Python dataclass layer (SPEC-016, AC4).

Provides InterMeetingManifest and InterMeetingEntry dataclasses with
validation, YAML serialization, and dict conversion. Enforces the same
constraints as data/interpretation/schema/inter-meeting-manifest-schema.yaml.
"""

from __future__ import annotations

import datetime
from dataclasses import dataclass
from typing import Optional

import yaml

SCHEMA_VERSION = "1.0"

VALID_SOURCE_TYPES = frozenset({
    "news-article", "public-statement", "document",
    "letter", "announcement", "other",
})

VALID_BODIES = frozenset({"school-board", "city-council", "both"})

_MANIFEST_KNOWN_FIELDS = frozenset({"schema_version", "entries"})

_ENTRY_KNOWN_FIELDS = frozenset({
    "entry_id", "date_posted", "source_type", "source_path",
    "title", "description", "date_range", "body", "normalized_path",
})

_DATE_RANGE_KNOWN_FIELDS = frozenset({"posted_after", "posted_before"})


def _parse_date(value, field_name: str) -> datetime.date:
    """Parse a date value (string or datetime.date). Raises ValueError on failure."""
    if isinstance(value, datetime.date) and not isinstance(value, datetime.datetime):
        return value
    if not isinstance(value, str):
        raise ValueError(f"{field_name}: expected date string, got {type(value).__name__}")
    try:
        return datetime.date.fromisoformat(value)
    except ValueError:
        raise ValueError(
            f"{field_name}: invalid date format '{value}' — expected YYYY-MM-DD"
        )


@dataclass(frozen=True)
class InterMeetingEntry:
    """A single inter-meeting evidence entry."""

    entry_id: str
    date_posted: datetime.date
    source_type: str
    source_path: str
    description: str
    date_range_after: datetime.date
    date_range_before: datetime.date
    title: Optional[str] = None
    body: Optional[str] = None
    normalized_path: Optional[str] = None

    @classmethod
    def from_dict(cls, data: dict) -> InterMeetingEntry:
        errors = []

        # Unexpected fields
        for key in data:
            if key not in _ENTRY_KNOWN_FIELDS:
                errors.append(f"unexpected field '{key}'")

        # Required fields
        for req in ("entry_id", "date_posted", "source_type", "source_path",
                     "description", "date_range"):
            if req not in data:
                errors.append(f"missing required field: {req}")

        # date_posted
        date_posted = None
        dp = data.get("date_posted")
        if dp is not None:
            try:
                date_posted = _parse_date(dp, "date_posted")
            except ValueError as e:
                errors.append(str(e))

        # source_type enum
        st = data.get("source_type")
        if st is not None and st not in VALID_SOURCE_TYPES:
            errors.append(
                f"source_type: invalid value '{st}' — "
                f"expected one of: {', '.join(sorted(VALID_SOURCE_TYPES))}"
            )

        # body enum (optional)
        body = data.get("body")
        if body is not None and body not in VALID_BODIES:
            errors.append(
                f"body: invalid value '{body}' — "
                f"expected one of: {', '.join(sorted(VALID_BODIES))}"
            )

        # date_range
        date_range_after = None
        date_range_before = None
        dr = data.get("date_range")
        if dr is not None:
            if not isinstance(dr, dict):
                errors.append("date_range: expected a mapping")
            else:
                # Unexpected fields in date_range
                for key in dr:
                    if key not in _DATE_RANGE_KNOWN_FIELDS:
                        errors.append(f"date_range: unexpected field '{key}'")

                pa = dr.get("posted_after")
                pb = dr.get("posted_before")

                if pa is None:
                    errors.append("date_range: missing required field 'posted_after'")
                else:
                    try:
                        date_range_after = _parse_date(pa, "date_range.posted_after")
                    except ValueError as e:
                        errors.append(str(e))

                if pb is None:
                    errors.append("date_range: missing required field 'posted_before'")
                else:
                    try:
                        date_range_before = _parse_date(pb, "date_range.posted_before")
                    except ValueError as e:
                        errors.append(str(e))

                if date_range_after and date_range_before:
                    if date_range_after >= date_range_before:
                        errors.append(
                            f"date_range: posted_after ({date_range_after}) must be "
                            f"before posted_before ({date_range_before})"
                        )

        if errors:
            raise ValueError("; ".join(errors))

        return cls(
            entry_id=data["entry_id"],
            date_posted=date_posted,
            source_type=data["source_type"],
            source_path=data["source_path"],
            description=data["description"],
            date_range_after=date_range_after,
            date_range_before=date_range_before,
            title=data.get("title"),
            body=data.get("body"),
            normalized_path=data.get("normalized_path"),
        )

    def to_dict(self) -> dict:
        d = {
            "entry_id": self.entry_id,
            "date_posted": self.date_posted.isoformat(),
            "source_type": self.source_type,
            "source_path": self.source_path,
            "description": self.description,
            "date_range": {
                "posted_after": self.date_range_after.isoformat(),
                "posted_before": self.date_range_before.isoformat(),
            },
        }
        for opt in ("title", "body", "normalized_path"):
            val = getattr(self, opt)
            if val is not None:
                d[opt] = val
        return d


@dataclass(frozen=True)
class InterMeetingManifest:
    """Top-level inter-meeting evidence manifest."""

    schema_version: str
    entries: list[InterMeetingEntry]

    @classmethod
    def from_dict(cls, data: dict) -> InterMeetingManifest:
        errors = []

        # Unexpected fields
        for key in data:
            if key not in _MANIFEST_KNOWN_FIELDS:
                errors.append(f"unexpected field '{key}'")

        # schema_version
        sv = data.get("schema_version")
        if sv is None:
            errors.append("missing required field: schema_version")
        elif str(sv) != SCHEMA_VERSION:
            errors.append(f"schema_version: expected '{SCHEMA_VERSION}', got '{sv}'")

        # entries
        raw_entries = data.get("entries")
        entries = []
        if raw_entries is None:
            errors.append("missing required field: entries")
        elif not isinstance(raw_entries, list):
            errors.append("entries: expected a list")
        else:
            for i, entry in enumerate(raw_entries):
                try:
                    entries.append(InterMeetingEntry.from_dict(entry))
                except ValueError as e:
                    errors.append(f"entries[{i}]: {e}")

        if errors:
            raise ValueError("; ".join(errors))

        return cls(schema_version=sv, entries=entries)

    @classmethod
    def from_yaml(cls, yaml_str: str) -> InterMeetingManifest:
        data = yaml.safe_load(yaml_str)
        if not isinstance(data, dict):
            raise ValueError("expected a YAML mapping at top level")
        return cls.from_dict(data)

    def to_dict(self) -> dict:
        return {
            "schema_version": self.schema_version,
            "entries": [e.to_dict() for e in self.entries],
        }

    def to_yaml(self) -> str:
        return yaml.dump(
            self.to_dict(),
            default_flow_style=False,
            sort_keys=False,
            allow_unicode=True,
        )
