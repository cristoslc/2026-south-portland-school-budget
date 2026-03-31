"""Tests for SPC-TV TelVue connector — SPEC-071.

AC1 — discovers videos by title pattern from TelVue VOD listing
AC2 — extracts VTT captions to standard path
AC3 — skips download when transcript already exists on disk (disk-diff gate)
AC4 — respects DiscoveryHistory backoff on failed attempts
AC5 — --check-only lists without downloading
AC6 — routes meetings to correct data directory by title
"""

import json
import os
import tempfile
from unittest.mock import MagicMock, patch, call

import scripts.connectors.telvue as connector


# ---------------------------------------------------------------------------
# Sample TelVue VOD page HTML (simplified)
# ---------------------------------------------------------------------------

SAMPLE_VOD_HTML = """
<div class="main">
  <a href="/player/NzN-Z2CpIDNbXMWB16nIzGKjRlHJozGq/media/1013186">
    <span>South Portland Board of Education - March 30 2026</span>
  </a>
  <span>05:02:24</span>
  <a href="/player/NzN-Z2CpIDNbXMWB16nIzGKjRlHJozGq/media/1013180">
    <span>South Portland Board of Appeals - March 30 2026</span>
  </a>
  <span>00:25:14</span>
  <a href="/player/NzN-Z2CpIDNbXMWB16nIzGKjRlHJozGq/media/1011963">
    <span>South Portland Board of Education - Budget Workshop II - March 23 2026</span>
  </a>
  <span>05:08:17</span>
  <a href="/player/NzN-Z2CpIDNbXMWB16nIzGKjRlHJozGq/media/1011566">
    <span>South Portland City Council - March 19 2026</span>
  </a>
  <span>04:22:23</span>
  <a href="/player/NzN-Z2CpIDNbXMWB16nIzGKjRlHJozGq/media/1009623">
    <span>South Portland City Council Workshop - March 10 2026</span>
  </a>
  <span>03:56:38</span>
  <a href="/player/NzN-Z2CpIDNbXMWB16nIzGKjRlHJozGq/media/1008182">
    <span>Budget Workshop I - March 2 2026</span>
  </a>
  <span>03:32:23</span>
</div>
"""


class TestParseTelvuePage:
    """AC1: Parse TelVue VOD listing to extract video entries."""

    def test_extracts_video_entries(self):
        videos = connector.parse_telvue_page(SAMPLE_VOD_HTML)
        assert len(videos) == 6

    def test_extracts_media_id(self):
        videos = connector.parse_telvue_page(SAMPLE_VOD_HTML)
        assert videos[0]["media_id"] == "1013186"
        assert videos[1]["media_id"] == "1013180"

    def test_extracts_title(self):
        videos = connector.parse_telvue_page(SAMPLE_VOD_HTML)
        assert videos[0]["title"] == "South Portland Board of Education - March 30 2026"

    def test_extracts_duration(self):
        videos = connector.parse_telvue_page(SAMPLE_VOD_HTML)
        assert videos[0]["duration"] == "05:02:24"

    def test_handles_empty_page(self):
        videos = connector.parse_telvue_page("<div></div>")
        assert videos == []


class TestInferDateFromTitle:
    """Test date parsing from TelVue title formats."""

    def test_month_day_year(self):
        assert connector.infer_date_from_title(
            "South Portland Board of Education - March 30 2026"
        ) == "2026-03-30"

    def test_budget_workshop_title(self):
        assert connector.infer_date_from_title(
            "South Portland Board of Education - Budget Workshop II - March 23 2026"
        ) == "2026-03-23"

    def test_short_title_with_date(self):
        assert connector.infer_date_from_title(
            "Budget Workshop I - March 2 2026"
        ) == "2026-03-02"

    def test_no_date_returns_unknown(self):
        assert connector.infer_date_from_title("Some Random Title") == "unknown"


class TestInferMeetingType:
    """AC6: Route meetings to correct data directory by title."""

    def test_board_of_education(self):
        assert connector.infer_meeting_type(
            "South Portland Board of Education - March 30 2026"
        ) == "school-board"

    def test_city_council(self):
        assert connector.infer_meeting_type(
            "South Portland City Council - March 19 2026"
        ) == "city-council"

    def test_city_council_workshop(self):
        assert connector.infer_meeting_type(
            "South Portland City Council Workshop - March 10 2026"
        ) == "city-council"

    def test_board_of_appeals_excluded(self):
        """Board of Appeals is not a meeting type we track."""
        assert connector.infer_meeting_type(
            "South Portland Board of Appeals - March 30 2026"
        ) is None

    def test_budget_workshop_is_school_board(self):
        assert connector.infer_meeting_type(
            "Budget Workshop I - March 2 2026"
        ) == "school-board"

    def test_comprehensive_plan_excluded(self):
        assert connector.infer_meeting_type(
            "South Portland Comprehensive Plan Committee - March 25 2026"
        ) is None


class TestInferSubtype:
    """Test meeting subtype inference."""

    def test_regular_meeting(self):
        assert connector.infer_subtype(
            "South Portland Board of Education - March 30 2026"
        ) == "regular-meeting"

    def test_budget_workshop(self):
        assert connector.infer_subtype(
            "South Portland Board of Education - Budget Workshop II - March 23 2026"
        ) == "budget-workshop"

    def test_budget_workshop_short_title(self):
        assert connector.infer_subtype(
            "Budget Workshop I - March 2 2026"
        ) == "budget-workshop"

    def test_city_council_workshop(self):
        assert connector.infer_subtype(
            "South Portland City Council Workshop - March 10 2026"
        ) == "workshop"


class TestMatchesFilters:
    """AC6: Filter to relevant meeting types only."""

    def test_board_of_education_matches(self):
        video = {"title": "South Portland Board of Education - March 30 2026", "media_id": "1013186"}
        assert connector.matches_filters(video) is True

    def test_city_council_matches(self):
        video = {"title": "South Portland City Council - March 19 2026", "media_id": "1011566"}
        assert connector.matches_filters(video) is True

    def test_board_of_appeals_excluded(self):
        video = {"title": "South Portland Board of Appeals - March 30 2026", "media_id": "1013180"}
        assert connector.matches_filters(video) is False

    def test_comprehensive_plan_excluded(self):
        video = {"title": "South Portland Comprehensive Plan Committee - March 25 2026", "media_id": "1012476"}
        assert connector.matches_filters(video) is False

    def test_date_cutoff_excludes_old(self):
        video = {"title": "South Portland Board of Education - November 1 2025", "media_id": "999999"}
        assert connector.matches_filters(video) is False

    def test_date_cutoff_includes_recent(self):
        video = {"title": "South Portland Board of Education - December 8 2025", "media_id": "999998"}
        assert connector.matches_filters(video) is True


class TestInferMetadata:
    """Test full metadata inference pipeline."""

    def test_board_meeting_metadata(self):
        video = {
            "title": "South Portland Board of Education - March 30 2026",
            "media_id": "1013186",
            "duration": "05:02:24",
        }
        meta = connector.infer_metadata(video)
        assert meta["type"] == "school-board"
        assert meta["subtype"] == "regular-meeting"
        assert meta["date"] == "2026-03-30"
        assert meta["media_id"] == "1013186"
        assert meta["output"] == "data/school-board/meetings/2026-03-30/transcript.en-x-autogen.vtt"

    def test_budget_workshop_metadata(self):
        video = {
            "title": "South Portland Board of Education - Budget Workshop II - March 23 2026",
            "media_id": "1011963",
            "duration": "05:08:17",
        }
        meta = connector.infer_metadata(video)
        assert meta["type"] == "school-board"
        assert meta["subtype"] == "budget-workshop"
        assert meta["date"] == "2026-03-23"
        assert meta["output"] == "data/school-board/meetings/2026-03-23-budget-workshop/transcript.en-x-autogen.vtt"

    def test_city_council_workshop_metadata(self):
        video = {
            "title": "South Portland City Council Workshop - March 10 2026",
            "media_id": "1009623",
            "duration": "03:56:38",
        }
        meta = connector.infer_metadata(video)
        assert meta["type"] == "city-council"
        assert meta["subtype"] == "workshop"
        assert meta["date"] == "2026-03-10"
        assert meta["output"] == "data/city-council/meetings/2026-03-10-workshop/transcript.en-x-autogen.vtt"


class TestDiskDiffGate:
    """AC3: Skip download when transcript already exists on disk."""

    def test_skips_when_file_exists(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            output_path = os.path.join(tmpdir, "transcript.en-x-autogen.vtt")
            with open(output_path, "w") as f:
                f.write("WEBVTT\n\n00:00.000 --> 00:01.000\nHello")
            assert connector.should_skip_existing(output_path) is True

    def test_does_not_skip_when_missing(self):
        assert connector.should_skip_existing("/nonexistent/path.vtt") is False


class TestCheckOnlyMode:
    """AC5: --check-only lists without downloading."""

    @patch("scripts.connectors.telvue.fetch_telvue_page")
    def test_check_only_does_not_download(self, mock_fetch):
        mock_fetch.return_value = SAMPLE_VOD_HTML
        with tempfile.TemporaryDirectory() as tmpdir:
            # No files exist → everything would be downloaded
            result = connector.run(
                check_only=True,
                project_root=tmpdir,
            )
            assert result == 0
            # Verify no VTT files were created
            vtt_files = []
            for root, dirs, files in os.walk(tmpdir):
                for f in files:
                    if f.endswith(".vtt"):
                        vtt_files.append(f)
            assert len(vtt_files) == 0
