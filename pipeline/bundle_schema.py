"""Meeting Bundle Schema — Python dataclass layer (SPEC-016).

Provides MeetingBundle and BundleSource dataclasses with validation,
YAML serialization, and dict conversion. Enforces the same constraints
as data/interpretation/schema/bundle-manifest-schema.yaml.
"""

from __future__ import annotations

import datetime
import re
from dataclasses import dataclass, field
from typing import Optional

import yaml

# --- Schema constants (mirrored from bundle-manifest-schema.yaml) ---

SCHEMA_VERSION = "1.0"

VALID_MEETING_TYPES = frozenset({
    "workshop", "regular", "special",
    "budget-forum", "budget-workshop", "joint",
})

VALID_BODIES = frozenset({"school-board", "city-council"})

VALID_SOURCE_TYPES = frozenset({
    "transcript", "agenda", "packet", "presentation",
    "spreadsheet", "document", "other",
})

_HASH_RE = re.compile(r"^sha256:[a-f0-9]{64}$")
_DURATION_RE = re.compile(r"^\d{2}:\d{2}:\d{2}$")

# --- Known field sets (for additionalProperties: false enforcement) ---

_BUNDLE_KNOWN_FIELDS = frozenset({
    "schema_version", "meeting_date", "meeting_type", "body",
    "title", "sources", "agenda_ref", "video_url", "notes",
})

_SOURCE_KNOWN_FIELDS = frozenset({
    "source_id", "source_type", "title", "path", "normalized_path",
    "evidence_pool", "description", "hash", "duration",
})


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
class BundleSource:
    """A single evidence source within a meeting bundle."""

    source_id: str
    source_type: str
    title: str
    path: str
    normalized_path: Optional[str] = None
    evidence_pool: Optional[str] = None
    description: Optional[str] = None
    hash: Optional[str] = None
    duration: Optional[str] = None

    @classmethod
    def from_dict(cls, data: dict) -> BundleSource:
        """Create a BundleSource from a dict, with validation."""
        errors = []

        # Check for unexpected fields
        for key in data:
            if key not in _SOURCE_KNOWN_FIELDS:
                errors.append(f"unexpected field '{key}'")

        # Required fields
        for req in ("source_id", "source_type", "title", "path"):
            if req not in data:
                errors.append(f"missing required field: {req}")

        # source_type enum
        st = data.get("source_type")
        if st is not None and st not in VALID_SOURCE_TYPES:
            errors.append(
                f"source_type: invalid value '{st}' — "
                f"expected one of: {', '.join(sorted(VALID_SOURCE_TYPES))}"
            )

        # hash format
        h = data.get("hash")
        if h is not None and not _HASH_RE.match(h):
            errors.append(
                f"hash: expected format 'sha256:<64 hex chars>', got '{h}'"
            )

        # duration format
        dur = data.get("duration")
        if dur is not None and not _DURATION_RE.match(dur):
            errors.append(
                f"duration: invalid format '{dur}' — expected HH:MM:SS"
            )

        if errors:
            raise ValueError("; ".join(errors))

        return cls(
            source_id=data["source_id"],
            source_type=data["source_type"],
            title=data["title"],
            path=data["path"],
            normalized_path=data.get("normalized_path"),
            evidence_pool=data.get("evidence_pool"),
            description=data.get("description"),
            hash=data.get("hash"),
            duration=data.get("duration"),
        )

    def to_dict(self) -> dict:
        """Convert to a dict suitable for YAML serialization."""
        d = {
            "source_id": self.source_id,
            "source_type": self.source_type,
            "title": self.title,
            "path": self.path,
        }
        for opt in ("normalized_path", "evidence_pool", "description", "hash", "duration"):
            val = getattr(self, opt)
            if val is not None:
                d[opt] = val
        return d


@dataclass(frozen=True)
class MeetingBundle:
    """A meeting bundle manifest (SPEC-016)."""

    schema_version: str
    meeting_date: datetime.date
    meeting_type: str
    body: str
    sources: list[BundleSource]
    title: Optional[str] = None
    agenda_ref: Optional[str] = None
    video_url: Optional[str] = None
    notes: Optional[str] = None

    @classmethod
    def from_dict(cls, data: dict) -> MeetingBundle:
        """Create a MeetingBundle from a dict, with validation."""
        errors = []

        # Check for unexpected fields
        for key in data:
            if key not in _BUNDLE_KNOWN_FIELDS:
                errors.append(f"unexpected field '{key}'")

        # schema_version
        sv = data.get("schema_version")
        if sv is None:
            errors.append("missing required field: schema_version")
        elif str(sv) != SCHEMA_VERSION:
            errors.append(
                f"schema_version: expected '{SCHEMA_VERSION}', got '{sv}'"
            )

        # meeting_date
        meeting_date = None
        md = data.get("meeting_date")
        if md is None:
            errors.append("missing required field: meeting_date")
        else:
            try:
                meeting_date = _parse_date(md, "meeting_date")
            except ValueError as e:
                errors.append(str(e))

        # meeting_type
        mt = data.get("meeting_type")
        if mt is None:
            errors.append("missing required field: meeting_type")
        elif mt not in VALID_MEETING_TYPES:
            errors.append(
                f"meeting_type: invalid value '{mt}' — "
                f"expected one of: {', '.join(sorted(VALID_MEETING_TYPES))}"
            )

        # body
        body = data.get("body")
        if body is None:
            errors.append("missing required field: body")
        elif body not in VALID_BODIES:
            errors.append(
                f"body: invalid value '{body}' — "
                f"expected one of: {', '.join(sorted(VALID_BODIES))}"
            )

        # sources
        raw_sources = data.get("sources")
        sources = []
        if raw_sources is None:
            errors.append("missing required field: sources")
        elif not isinstance(raw_sources, list):
            errors.append("sources: expected a list")
        elif len(raw_sources) == 0:
            errors.append("sources: must contain at least one entry")
        else:
            for i, src in enumerate(raw_sources):
                try:
                    sources.append(BundleSource.from_dict(src))
                except ValueError as e:
                    errors.append(f"sources[{i}]: {e}")

        if errors:
            raise ValueError("; ".join(errors))

        return cls(
            schema_version=sv,
            meeting_date=meeting_date,
            meeting_type=mt,
            body=body,
            sources=sources,
            title=data.get("title"),
            agenda_ref=data.get("agenda_ref"),
            video_url=data.get("video_url"),
            notes=data.get("notes"),
        )

    @classmethod
    def from_yaml(cls, yaml_str: str) -> MeetingBundle:
        """Parse a YAML string into a MeetingBundle."""
        data = yaml.safe_load(yaml_str)
        if not isinstance(data, dict):
            raise ValueError("expected a YAML mapping at top level")
        return cls.from_dict(data)

    def to_dict(self) -> dict:
        """Convert to a dict suitable for YAML serialization."""
        d = {
            "schema_version": self.schema_version,
            "meeting_date": self.meeting_date.isoformat(),
            "meeting_type": self.meeting_type,
            "body": self.body,
            "sources": [s.to_dict() for s in self.sources],
        }
        for opt in ("title", "agenda_ref", "video_url", "notes"):
            val = getattr(self, opt)
            if val is not None:
                d[opt] = val
        return d

    def to_yaml(self) -> str:
        """Serialize to a YAML string."""
        return yaml.dump(
            self.to_dict(),
            default_flow_style=False,
            sort_keys=False,
            allow_unicode=True,
        )
