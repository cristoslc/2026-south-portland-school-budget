"""Tests for budget_page connector — SPEC-023 (Google Slides) and SPEC-024 (Meaningful Filenames).

SPEC-023 coverage:
  AC1 — classify_url returns slides_pdf + correct export URL for edit URLs
  AC2 — classify_url returns slides_pdf + correct export URL for pubembed URLs
  AC3 — full run() downloads slides as PDFs and records ok in history
  AC4 — failed Slides download records 'failed' in history; run() exits 0
  AC5 — skip-existing logic applies to Slides just like other types
  AC6 — --check-only logs WOULD DOWNLOAD without downloading

SPEC-024 coverage:
  AC1 — Content-Disposition filename used as final name (RFC 5987 preferred)
  AC2 — fallback to doc-ID (not path verb) when no label and no Content-Disposition
  AC3 — skip-existing uses history local_path on subsequent runs
  AC4 — check-only resolves candidate filename without downloading
  AC5 — multiple docs with different IDs get distinct filenames
"""

import json
from unittest.mock import MagicMock, patch

import scripts.connectors.budget_page as connector

# Real URLs observed on spsdme.org/budget27
EDIT_URL = (
    "https://docs.google.com/presentation/d/"
    "1lNX2v1rq33OxDSmGwbsmSTjoI9z-My6mDO9qgSo3QIA/edit?usp=sharing"
)
EDIT_ID = "1lNX2v1rq33OxDSmGwbsmSTjoI9z-My6mDO9qgSo3QIA"

PUBEMBED_URL = (
    "https://docs.google.com/presentation/d/e/"
    "2PACX-1vRoMdePZnlhIbatO3I46wxlpkTYuFDgxiylQi14FugYxWCJNzrM6tRFr9vj2M2ZgIl0sX0Bj15gVGmE"
    "/pubembed?start=false&loop=false&delayms=3000"
)
PUBEMBED_ID = (
    "2PACX-1vRoMdePZnlhIbatO3I46wxlpkTYuFDgxiylQi14FugYxWCJNzrM6tRFr9vj2M2ZgIl0sX0Bj15gVGmE"
)

DRIVE_URL = "https://drive.google.com/file/d/1DriveFileIdABCDEFGHIJKLMNO/view"
DRIVE_ID = "1DriveFileIdABCDEFGHIJKLMNO"

FAKE_PDF = b"%PDF-1.4 fake pdf content for testing" + b"x" * 200

# Real Content-Disposition observed from Google's export endpoint
REAL_CD = (
    'attachment; filename="FY27Budget3.9.26BoardMeeting.pdf"; '
    "filename*=UTF-8''FY27%20Budget%203.9.26%20Board%20Meeting.pdf"
)


def _fake_html(slide_urls):
    """Build minimal HTML with labeled anchor links (label = 'Presentation N')."""
    links = "\n".join(
        f'<a href="{url}">Presentation {i+1}</a>'
        for i, url in enumerate(slide_urls)
    )
    return f"<html><body>{links}</body></html>"


def _bare_html(urls):
    """Build minimal HTML with bare links (no anchor text) to exercise ID-based naming."""
    links = "\n".join(f'<a href="{url}"></a>' for url in urls)
    return f"<html><body>{links}</body></html>"


def _make_urlopen_mock(page_html, pdf_bytes=None, content_disposition=None):
    """Return a urlopen mock: serves page_html for the budget page URL,
    pdf_bytes for any other URL, optionally with a Content-Disposition header."""
    if pdf_bytes is None:
        pdf_bytes = FAKE_PDF

    def _urlopen(req, timeout=None):
        url = req.full_url if hasattr(req, "full_url") else str(req)
        resp = MagicMock()
        resp.__enter__ = lambda s: s
        resp.__exit__ = MagicMock(return_value=False)
        headers = MagicMock()
        if connector.BUDGET_PAGE_URL in url:
            resp.read.return_value = page_html.encode("utf-8")
            headers.get.return_value = ""
        else:
            resp.read.return_value = pdf_bytes
            headers.get.return_value = content_disposition or ""
        resp.headers = headers
        return resp

    return _urlopen


# ---------------------------------------------------------------------------
# SPEC-023 — classify_url
# ---------------------------------------------------------------------------

class TestClassifyUrl:
    """AC1, AC2: URL classification returns slides_pdf for both URL variants."""

    def test_edit_url_classified_as_slides_pdf(self):
        url_type, export_url, ext = connector.classify_url(EDIT_URL)
        assert url_type == "slides_pdf"
        assert export_url == (
            f"https://docs.google.com/presentation/d/{EDIT_ID}/export?format=pdf"
        )
        assert ext == ".pdf"

    def test_pubembed_url_classified_as_slides_pdf(self):
        url_type, export_url, ext = connector.classify_url(PUBEMBED_URL)
        assert url_type == "slides_pdf"
        assert export_url == (
            f"https://docs.google.com/presentation/d/e/{PUBEMBED_ID}/export?format=pdf"
        )
        assert ext == ".pdf"

    def test_slides_edit_without_query_params(self):
        url = f"https://docs.google.com/presentation/d/{EDIT_ID}/edit"
        url_type, export_url, _ = connector.classify_url(url)
        assert url_type == "slides_pdf"
        assert f"/d/{EDIT_ID}/export?format=pdf" in export_url

    def test_slides_never_returns_unsupported(self):
        for url in [EDIT_URL, PUBEMBED_URL]:
            url_type, _, _ = connector.classify_url(url)
            assert url_type != "slides_unsupported", (
                f"classify_url must not return slides_unsupported for {url}"
            )

    def test_drive_pdf_unaffected(self):
        url_type, _, ext = connector.classify_url(DRIVE_URL)
        assert url_type == "drive_pdf"
        assert ext == ".pdf"

    def test_sheets_xlsx_unaffected(self):
        url_type, _, ext = connector.classify_url(
            "https://docs.google.com/spreadsheets/d/1SheetId/edit"
        )
        assert url_type == "sheets_xlsx"
        assert ext == ".xlsx"

    def test_unrecognised_url(self):
        url_type, export_url, ext = connector.classify_url("https://example.com/file.zip")
        assert url_type is None
        assert export_url is None
        assert ext is None


# ---------------------------------------------------------------------------
# SPEC-024 — _extract_doc_id
# ---------------------------------------------------------------------------

class TestExtractDocId:
    """AC2, AC5: doc-ID extraction gives distinct, non-verb fallback names."""

    def test_drive_url(self):
        assert connector._extract_doc_id(DRIVE_URL) == DRIVE_ID

    def test_slides_edit_url(self):
        assert connector._extract_doc_id(EDIT_URL) == EDIT_ID

    def test_slides_pubembed_url(self):
        assert connector._extract_doc_id(PUBEMBED_URL) == PUBEMBED_ID

    def test_docs_url(self):
        doc_id = "1DocIdABCDEFGHIJKLMNOPQRSTUVWXYZ"
        url = f"https://docs.google.com/document/d/{doc_id}/edit"
        assert connector._extract_doc_id(url) == doc_id

    def test_sheets_url(self):
        sheet_id = "1SheetIdXYZABCDEF"
        url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/edit"
        assert connector._extract_doc_id(url) == sheet_id

    def test_unrecognised_returns_none(self):
        assert connector._extract_doc_id("https://example.com/file.zip") is None


# ---------------------------------------------------------------------------
# SPEC-024 — _parse_content_disposition
# ---------------------------------------------------------------------------

class TestParseContentDisposition:
    """AC1: Content-Disposition parsing prefers RFC 5987, sanitizes properly."""

    def test_rfc5987_preferred_over_plain(self):
        result = connector._parse_content_disposition(REAL_CD, ".pdf")
        # RFC 5987 decoded: "FY27 Budget 3.9.26 Board Meeting"
        assert result == "FY27-Budget-3.9.26-Board-Meeting.pdf"

    def test_plain_filename_fallback(self):
        cd = 'attachment; filename="My Document.pdf"'
        result = connector._parse_content_disposition(cd, ".pdf")
        assert result == "My-Document.pdf"

    def test_none_when_no_header(self):
        assert connector._parse_content_disposition("", ".pdf") is None
        assert connector._parse_content_disposition(None, ".pdf") is None

    def test_extension_appended_when_cd_has_no_ext(self):
        cd = "attachment; filename*=UTF-8''Budget%20Report"
        result = connector._parse_content_disposition(cd, ".pdf")
        assert result is not None
        assert result == "Budget-Report.pdf"


# ---------------------------------------------------------------------------
# SPEC-024 — local_filename fallback (distinct, not path-verb)
# ---------------------------------------------------------------------------

class TestLocalFilename:
    """AC2, AC5: local_filename uses doc-ID as fallback, never path verbs."""

    def test_label_takes_priority(self):
        name = connector.local_filename(EDIT_URL, "Budget Workshop Slides", ".pdf")
        assert name == "budget-workshop-slides.pdf"

    def test_no_label_uses_doc_id_not_edit(self):
        name = connector.local_filename(EDIT_URL, "", ".pdf")
        assert name == f"{EDIT_ID}.pdf"
        assert "edit" not in name

    def test_no_label_drive_url_uses_doc_id_not_view(self):
        name = connector.local_filename(DRIVE_URL, "", ".pdf")
        assert name == f"{DRIVE_ID}.pdf"
        assert "view" not in name

    def test_pubembed_uses_pubid_not_pubembed(self):
        name = connector.local_filename(PUBEMBED_URL, "", ".pdf")
        assert name == f"{PUBEMBED_ID}.pdf"
        assert "pubembed" not in name

    def test_distinct_names_for_different_ids(self):
        url_a = f"https://drive.google.com/file/d/AAA111/view"
        url_b = f"https://drive.google.com/file/d/BBB222/view"
        assert connector.local_filename(url_a, "", ".pdf") != connector.local_filename(url_b, "", ".pdf")


# ---------------------------------------------------------------------------
# SPEC-023 + SPEC-024 — run() end-to-end
# ---------------------------------------------------------------------------

class TestRunSlidesDownload:
    """Full run() with mocked HTTP — SPEC-023 AC3-6 and SPEC-024 AC1-3."""

    def test_edit_slides_downloaded_with_cd_name(self, tmp_path):
        """AC3 (S023), AC1 (S024): run() downloads slide and renames to CD name."""
        html = _fake_html([EDIT_URL])
        urlopen_mock = _make_urlopen_mock(html, content_disposition=REAL_CD)

        with (
            patch.object(connector, "DOCUMENTS_DIR", str(tmp_path / "docs")),
            patch.object(connector, "SNAPSHOTS_DIR", str(tmp_path / "snaps")),
            patch.object(connector, "HISTORY_PATH", str(tmp_path / "discovery.jsonl")),
            patch("scripts.connectors.budget_page.urlopen", side_effect=urlopen_mock),
        ):
            result = connector.run()

        assert result == 0
        pdfs = list((tmp_path / "docs").glob("*.pdf"))
        assert len(pdfs) == 1
        assert pdfs[0].name == "FY27-Budget-3.9.26-Board-Meeting.pdf"

        records = [
            json.loads(line)
            for line in (tmp_path / "discovery.jsonl").read_text().splitlines()
        ]
        ok = [r for r in records if r["status"] == "ok"]
        assert len(ok) == 1
        assert ok[0]["local_path"] == "FY27-Budget-3.9.26-Board-Meeting.pdf"

    def test_no_cd_header_uses_doc_id_filename(self, tmp_path):
        """AC2 (S024): without Content-Disposition or label, filename is doc-ID, not 'edit'."""
        html = _bare_html([EDIT_URL])
        urlopen_mock = _make_urlopen_mock(html, content_disposition="")

        with (
            patch.object(connector, "DOCUMENTS_DIR", str(tmp_path / "docs")),
            patch.object(connector, "SNAPSHOTS_DIR", str(tmp_path / "snaps")),
            patch.object(connector, "HISTORY_PATH", str(tmp_path / "discovery.jsonl")),
            patch("scripts.connectors.budget_page.urlopen", side_effect=urlopen_mock),
        ):
            connector.run()

        pdfs = list((tmp_path / "docs").glob("*.pdf"))
        assert len(pdfs) == 1
        assert pdfs[0].name == f"{EDIT_ID}.pdf"
        assert "edit" not in pdfs[0].name

    def test_pubembed_downloaded_with_cd_name(self, tmp_path):
        """AC3 (S023): pubembed slide downloaded and renamed to CD name."""
        html = _fake_html([PUBEMBED_URL])
        cd = "attachment; filename*=UTF-8''Budget%20Overview%20Slides.pdf"
        urlopen_mock = _make_urlopen_mock(html, content_disposition=cd)

        with (
            patch.object(connector, "DOCUMENTS_DIR", str(tmp_path / "docs")),
            patch.object(connector, "SNAPSHOTS_DIR", str(tmp_path / "snaps")),
            patch.object(connector, "HISTORY_PATH", str(tmp_path / "discovery.jsonl")),
            patch("scripts.connectors.budget_page.urlopen", side_effect=urlopen_mock),
        ):
            connector.run()

        pdfs = list((tmp_path / "docs").glob("*.pdf"))
        assert len(pdfs) == 1
        assert pdfs[0].name == "Budget-Overview-Slides.pdf"

    def test_skip_existing_via_history_local_path(self, tmp_path):
        """AC3 (S024): second run skips URL using local_path stored in history."""
        html = _fake_html([EDIT_URL])
        urlopen_mock = _make_urlopen_mock(html, content_disposition=REAL_CD)
        docs_dir = tmp_path / "docs"

        with (
            patch.object(connector, "DOCUMENTS_DIR", str(docs_dir)),
            patch.object(connector, "SNAPSHOTS_DIR", str(tmp_path / "snaps")),
            patch.object(connector, "HISTORY_PATH", str(tmp_path / "discovery.jsonl")),
            patch("scripts.connectors.budget_page.urlopen", side_effect=urlopen_mock),
        ):
            connector.run()  # first run — downloads and records local_path

        # Second run — file exists under CD name; doc-ID path does not
        download_calls = []
        orig = connector.download_file

        def _spy(export_url, output_path, extension=".pdf"):
            download_calls.append(export_url)
            return orig(export_url, output_path, extension)

        with (
            patch.object(connector, "DOCUMENTS_DIR", str(docs_dir)),
            patch.object(connector, "SNAPSHOTS_DIR", str(tmp_path / "snaps")),
            patch.object(connector, "HISTORY_PATH", str(tmp_path / "discovery.jsonl")),
            patch("scripts.connectors.budget_page.urlopen", side_effect=urlopen_mock),
            patch("scripts.connectors.budget_page.download_file", side_effect=_spy),
        ):
            connector.run()

        assert download_calls == [], "Second run must not re-download an already-saved file"

    def test_failed_download_records_failed_exits_0(self, tmp_path):
        """AC4 (S023): HTTP error records 'failed'; run() still returns 0."""
        from urllib.error import HTTPError

        html = _fake_html([EDIT_URL])

        def _urlopen(req, timeout=None):
            url = req.full_url if hasattr(req, "full_url") else str(req)
            resp = MagicMock()
            resp.__enter__ = lambda s: s
            resp.__exit__ = MagicMock(return_value=False)
            resp.headers = MagicMock()
            resp.headers.get.return_value = ""
            if connector.BUDGET_PAGE_URL in url:
                resp.read.return_value = html.encode("utf-8")
                return resp
            raise HTTPError(url, 403, "Forbidden", {}, None)

        with (
            patch.object(connector, "DOCUMENTS_DIR", str(tmp_path / "docs")),
            patch.object(connector, "SNAPSHOTS_DIR", str(tmp_path / "snaps")),
            patch.object(connector, "HISTORY_PATH", str(tmp_path / "discovery.jsonl")),
            patch("scripts.connectors.budget_page.urlopen", side_effect=_urlopen),
        ):
            result = connector.run()

        assert result == 0
        records = [
            json.loads(line)
            for line in (tmp_path / "discovery.jsonl").read_text().splitlines()
        ]
        assert any(r["status"] == "failed" and r["url"] == EDIT_URL for r in records)

    def test_check_only_does_not_download(self, tmp_path):
        """AC6 (S023), AC4 (S024): check-only creates no files."""
        html = _fake_html([EDIT_URL, PUBEMBED_URL])
        urlopen_mock = _make_urlopen_mock(html, content_disposition=REAL_CD)

        with (
            patch.object(connector, "DOCUMENTS_DIR", str(tmp_path / "docs")),
            patch.object(connector, "SNAPSHOTS_DIR", str(tmp_path / "snaps")),
            patch.object(connector, "HISTORY_PATH", str(tmp_path / "discovery.jsonl")),
            patch("scripts.connectors.budget_page.urlopen", side_effect=urlopen_mock),
        ):
            result = connector.run(check_only=True)

        assert result == 0
        docs_dir = tmp_path / "docs"
        pdfs = list(docs_dir.glob("*.pdf")) if docs_dir.exists() else []
        assert pdfs == []

    def test_distinct_filenames_multiple_docs(self, tmp_path):
        """AC5 (S024): two docs with different IDs get distinct filenames."""
        url_a = "https://drive.google.com/file/d/AAAA111111/view"
        url_b = "https://drive.google.com/file/d/BBBB222222/view"
        html = _bare_html([url_a, url_b])
        urlopen_mock = _make_urlopen_mock(html, content_disposition="")

        with (
            patch.object(connector, "DOCUMENTS_DIR", str(tmp_path / "docs")),
            patch.object(connector, "SNAPSHOTS_DIR", str(tmp_path / "snaps")),
            patch.object(connector, "HISTORY_PATH", str(tmp_path / "discovery.jsonl")),
            patch("scripts.connectors.budget_page.urlopen", side_effect=urlopen_mock),
        ):
            connector.run()

        pdfs = sorted(p.name for p in (tmp_path / "docs").glob("*.pdf"))
        assert len(pdfs) == 2
        assert pdfs[0] != pdfs[1]
        assert "AAAA111111" in pdfs[0] or "AAAA111111" in pdfs[1]
