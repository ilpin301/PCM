from extract import join_dehyphenated, find_running_lines, is_heading, is_scanned


def test_is_heading_levels():
    assert is_heading(20.0, 10.0) == 2   # 2.0x -> h2
    assert is_heading(12.5, 10.0) == 3   # 1.25x -> h3
    assert is_heading(10.5, 10.0) == 0   # ~body -> not a heading


def test_is_heading_zero_body_median_is_safe():
    assert is_heading(12.0, 0.0) == 0


def test_is_scanned_threshold():
    assert is_scanned(20.0) is True
    assert is_scanned(5000.0) is False
    assert is_scanned(100.0) is False    # boundary is exclusive


def test_join_dehyphenated_merges_hyphenated_break():
    lines = ["This is an exam-", "ple of wrapped text."]
    assert join_dehyphenated(lines) == "This is an example of wrapped text."


def test_join_dehyphenated_joins_plain_lines_with_space():
    lines = ["first line", "second line"]
    assert join_dehyphenated(lines) == "first line second line"


def test_join_dehyphenated_single_line():
    assert join_dehyphenated(["just one"]) == "just one"


def test_find_running_lines_detects_repeated_header():
    pages = [
        ["Journal of PCM", "intro text", "1"],
        ["Journal of PCM", "more text", "2"],
        ["Journal of PCM", "conclusion", "3"],
    ]
    running = find_running_lines(pages, min_ratio=0.6)
    assert "Journal of PCM" in running
    assert "intro text" not in running
    # bare page numbers normalize to '' and are not returned here
    assert "" not in running


def test_find_running_lines_long_line_furniture_by_recurrence():
    long_line = "x" * 120
    # appears on 3/3 pages -> furniture even though it is long
    pages_all = [[long_line], [long_line], [long_line]]
    assert long_line in find_running_lines(pages_all, min_ratio=0.6)
    # appears on 1/3 pages -> real content, not furniture
    pages_one = [[long_line], ["other a"], ["other b"]]
    assert long_line not in find_running_lines(pages_one, min_ratio=0.6)


from extract import build_body


def test_build_body_emits_headings_and_paragraphs():
    pages = [
        [
            ("Introduction", 20.0),
            ("This sentence is", 10.0),
            ("on two lines.", 10.0),
        ],
    ]
    out = build_body(pages)
    assert "## Introduction" in out
    assert "This sentence is on two lines." in out


def test_build_body_drops_running_furniture():
    pages = [
        [("Journal X", 10.0), ("real body one", 10.0)],
        [("Journal X", 10.0), ("real body two", 10.0)],
    ]
    out = build_body(pages)
    assert "Journal X" not in out
    assert "real body one" in out
    assert "real body two" in out


def test_build_body_dehyphenates_across_lines():
    pages = [[("hyphen-", 10.0), ("ation works", 10.0)]]
    assert "hyphenation works" in build_body(pages)


import fitz  # PyMuPDF, used only to synthesize a test PDF
from extract import extract_pages


def _make_pdf(path):
    doc = fitz.open()
    page = doc.new_page()
    page.insert_text((72, 72), "Big Heading", fontsize=20)
    # Add substantial body text so avg_chars_per_page > 100 (non-scanned threshold)
    body_text = "Normal body sentence here. " * 6
    page.insert_text((72, 110), body_text, fontsize=11)
    doc.save(str(path))
    doc.close()


def test_extract_pages_fitz_captures_sizes_and_headings(tmp_path):
    pdf = tmp_path / "sample.pdf"
    _make_pdf(pdf)
    result = extract_pages(str(pdf), engine="fitz")
    assert result["engine"] == "fitz"
    assert result["page_count"] == 1
    assert result["avg_chars_per_page"] > 0
    sizes = {round(size) for page in result["pages"] for _, size in page}
    assert 20 in sizes and 11 in sizes
    from extract import build_body
    assert "## Big Heading" in build_body(result["pages"])


def test_extract_pages_pdftotext_fallback_has_text_no_headings(tmp_path):
    pdf = tmp_path / "sample.pdf"
    _make_pdf(pdf)
    result = extract_pages(str(pdf), engine="pdftotext")
    assert result["engine"] == "pdftotext"
    assert "Big Heading" in result["first_pages_text"]
    assert all(size == 1.0 for page in result["pages"] for _, size in page)


import json
import subprocess
import sys
from pathlib import Path

EXTRACT = str(Path(__file__).resolve().parent.parent / "extract.py")


def test_cli_prints_expected_json(tmp_path):
    pdf = tmp_path / "sample.pdf"
    _make_pdf(pdf)
    proc = subprocess.run(
        [sys.executable, EXTRACT, str(pdf), "--engine", "fitz"],
        capture_output=True, text=True, check=True,
    )
    data = json.loads(proc.stdout)
    assert set(data) == {
        "body", "first_pages_text", "page_count",
        "avg_chars_per_page", "scanned", "engine",
    }
    assert data["scanned"] is False
    assert "## Big Heading" in data["body"]


def test_cli_handles_non_ascii_body(tmp_path):
    """CLI must not crash on non-ASCII text (UnicodeEncodeError on Windows cp1251)."""
    pdf = tmp_path / "nonascii.pdf"
    doc = fitz.open()
    page = doc.new_page()
    page.insert_text((72, 72), "Frühjahr Müller ú ñ", fontsize=11)
    body_text = "Frühjahr Müller ú ñ sentence. " * 6
    page.insert_text((72, 110), body_text, fontsize=11)
    doc.save(str(pdf))
    doc.close()

    proc = subprocess.run(
        [sys.executable, EXTRACT, str(pdf), "--engine", "fitz"],
        capture_output=True, text=True, encoding="utf-8", check=True,
    )
    data = json.loads(proc.stdout)
    assert "Müller" in data["body"] or "Frühjahr" in data["body"]


def test_find_running_lines_collapses_trailing_page_number():
    # same footer differing only by trailing page number must collapse to one key
    pages = [
        ["Vol. 18, No. 17 / OPTICS EXPRESS  18383", "body one"],
        ["Vol. 18, No. 17 / OPTICS EXPRESS  18384", "body two"],
        ["Vol. 18, No. 17 / OPTICS EXPRESS  18385", "body three"],
    ]
    running = find_running_lines(pages, min_ratio=0.6)
    assert "Vol. 18, No. 17 / OPTICS EXPRESS" in running


def test_build_body_drops_pagenumber_footers_and_bare_numbers():
    pages = [
        [
            ("Real sentence on page one.", 10.0),
            ("Vol. 18, No. 17 / OPTICS EXPRESS  18383", 9.0),
            ("7", 9.0),
        ],
        [
            ("Real sentence on page two.", 10.0),
            ("Vol. 18, No. 17 / OPTICS EXPRESS  18384", 9.0),
            ("8", 9.0),
        ],
    ]
    out = build_body(pages)
    assert "Real sentence on page one." in out
    assert "Real sentence on page two." in out
    assert "OPTICS EXPRESS" not in out      # footer collapsed + dropped
    assert "18383" not in out and "18384" not in out
    # bare page-number lines dropped
    assert "\n7\n" not in out and not out.strip().endswith("7")
