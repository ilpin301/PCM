# llm-wiki-pdf-extract-local Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build a low-token, offline Claude Code skill that turns PDFs in `Raw/Files/` into ingest-ready `<name>.pdf.md` companions via deterministic local extraction, using a cheap model only to write a short header.

**Architecture:** A pure-Python module (`extract.py`) does all text work with PyMuPDF (`fitz`), falling back to `pdftotext`. It prints a single JSON object (body markdown + first-2-pages text + stats) to stdout. A `SKILL.md` orchestrates: find PDFs lacking a companion, run the script, dispatch a Haiku subagent on the first 2 pages to produce a `# Title` + source line, assemble `header + body`, and write the companion. The document body never enters a model's context.

**Tech Stack:** Python 3, PyMuPDF (`fitz`) with `pdftotext` (poppler) fallback, pytest. The skill's runtime model offload uses a Claude Code Haiku subagent (no API key).

## Global Constraints

- Python 3; PyMuPDF (`fitz`, installed: 1.27.2) is the primary engine, `pdftotext` (installed) is the fallback. No new heavyweight deps; no OCR.
- Output path is exactly `Raw/Files/<original-name>.pdf.md`. **No YAML frontmatter** — start with `# <Title>`, then a source line, then the body. (Frontmatter is added later by `scripts/add_frontmatter.py`.)
- Default run processes only PDFs that have **no** existing `.pdf.md`; never overwrite a companion unless `--force`/explicit refresh is requested.
- Scanned/no-text detection threshold: `avg_chars_per_page < 100.0` → write nothing, flag the PDF for the NotebookLM path (`llm-wiki-pdf-extract`).
- The document body must never be sent to any model. Only the first ~2 pages go to the Haiku subagent for the header.
- **Source-of-truth lives in the repo** at `skills/llm-wiki-pdf-extract-local/` (so it is version-controlled). The **runtime install** is a copy at `~/.claude/skills/llm-wiki-pdf-extract-local/` (global, not a git repo). All `git` commits target the PCM repo source.
- All pytest commands are run from the PCM repo root. A `conftest.py` at the skill source dir puts `extract.py` on `sys.path`.

---

## File Structure

- Create: `skills/llm-wiki-pdf-extract-local/extract.py` — extraction + cleanup module and CLI.
- Create: `skills/llm-wiki-pdf-extract-local/conftest.py` — empty; makes pytest add the skill dir to `sys.path`.
- Create: `skills/llm-wiki-pdf-extract-local/tests/test_extract.py` — unit + integration tests.
- Create: `skills/llm-wiki-pdf-extract-local/SKILL.md` — orchestration instructions.
- Install (Task 8): copy `extract.py` + `SKILL.md` to `~/.claude/skills/llm-wiki-pdf-extract-local/`.

---

### Task 1: Scaffold + `join_dehyphenated`

**Files:**
- Create: `skills/llm-wiki-pdf-extract-local/extract.py`
- Create: `skills/llm-wiki-pdf-extract-local/conftest.py`
- Test: `skills/llm-wiki-pdf-extract-local/tests/test_extract.py`

**Interfaces:**
- Produces: `join_dehyphenated(lines: list[str]) -> str` — joins wrapped lines into one paragraph string, fixing end-of-line hyphenation.

- [ ] **Step 1: Create the empty conftest so imports resolve**

Create `skills/llm-wiki-pdf-extract-local/conftest.py` with exactly:

```python
# Present so pytest adds this directory to sys.path, making `import extract` work.
```

- [ ] **Step 2: Write the failing test**

Create `skills/llm-wiki-pdf-extract-local/tests/test_extract.py`:

```python
from extract import join_dehyphenated


def test_join_dehyphenated_merges_hyphenated_break():
    lines = ["This is an exam-", "ple of wrapped text."]
    assert join_dehyphenated(lines) == "This is an example of wrapped text."


def test_join_dehyphenated_joins_plain_lines_with_space():
    lines = ["first line", "second line"]
    assert join_dehyphenated(lines) == "first line second line"


def test_join_dehyphenated_single_line():
    assert join_dehyphenated(["just one"]) == "just one"
```

- [ ] **Step 3: Run test to verify it fails**

Run: `python -m pytest skills/llm-wiki-pdf-extract-local/tests/test_extract.py -v`
Expected: FAIL — `ModuleNotFoundError: No module named 'extract'` (or ImportError for `join_dehyphenated`).

- [ ] **Step 4: Write minimal implementation**

Create `skills/llm-wiki-pdf-extract-local/extract.py`:

```python
#!/usr/bin/env python3
"""Low-token local PDF -> markdown extractor for llm-wiki-pdf-extract-local."""


def join_dehyphenated(lines):
    """Join wrapped lines into one paragraph, fixing end-of-line hyphenation."""
    out = ""
    for raw in lines:
        ln = raw.rstrip()
        if not out:
            out = ln
        elif out.endswith("-"):
            out = out[:-1] + ln.lstrip()
        else:
            out = out + " " + ln.lstrip()
    return out
```

- [ ] **Step 5: Run test to verify it passes**

Run: `python -m pytest skills/llm-wiki-pdf-extract-local/tests/test_extract.py -v`
Expected: PASS (3 passed).

- [ ] **Step 6: Commit**

```bash
git add skills/llm-wiki-pdf-extract-local/extract.py skills/llm-wiki-pdf-extract-local/conftest.py skills/llm-wiki-pdf-extract-local/tests/test_extract.py
git commit -m "feat(pdf-extract-local): scaffold + join_dehyphenated"
```

---

### Task 2: `find_running_lines`

**Files:**
- Modify: `skills/llm-wiki-pdf-extract-local/extract.py`
- Test: `skills/llm-wiki-pdf-extract-local/tests/test_extract.py`

**Interfaces:**
- Consumes: nothing from prior tasks.
- Produces: `find_running_lines(pages_text: list[list[str]], min_ratio: float = 0.6, max_len: int = 80) -> set[str]` — returns the set of stripped line strings that recur on at least `min_ratio` of pages (repeated headers/footers); pure-digit lines (page numbers) are always eligible regardless of length.

- [ ] **Step 1: Write the failing test**

Append to `tests/test_extract.py`:

```python
from extract import find_running_lines


def test_find_running_lines_detects_repeated_header():
    pages = [
        ["Journal of PCM", "intro text", "1"],
        ["Journal of PCM", "more text", "2"],
        ["Journal of PCM", "conclusion", "3"],
    ]
    running = find_running_lines(pages, min_ratio=0.6)
    assert "Journal of PCM" in running
    assert "1" in running and "2" in running and "3" in running
    assert "intro text" not in running


def test_find_running_lines_ignores_long_repeated_body():
    long_line = "x" * 120
    pages = [[long_line], [long_line]]
    # long, non-digit -> not treated as running furniture
    assert long_line not in find_running_lines(pages, min_ratio=0.5)
```

- [ ] **Step 2: Run test to verify it fails**

Run: `python -m pytest skills/llm-wiki-pdf-extract-local/tests/test_extract.py -k find_running -v`
Expected: FAIL — `ImportError: cannot import name 'find_running_lines'`.

- [ ] **Step 3: Write minimal implementation**

Add to `extract.py` (after `join_dehyphenated`), and add `from collections import Counter` at the top of the file:

```python
def find_running_lines(pages_text, min_ratio=0.6, max_len=80):
    """Stripped line strings recurring on >= min_ratio of pages (headers/footers)."""
    n = len(pages_text)
    if n == 0:
        return set()
    counts = Counter()
    for lines in pages_text:
        for s in {ln.strip() for ln in lines if ln.strip()}:
            counts[s] += 1
    threshold = min_ratio * n
    return {
        s
        for s, c in counts.items()
        if c >= threshold and (len(s) <= max_len or s.isdigit())
    }
```

- [ ] **Step 4: Run test to verify it passes**

Run: `python -m pytest skills/llm-wiki-pdf-extract-local/tests/test_extract.py -k find_running -v`
Expected: PASS (2 passed).

- [ ] **Step 5: Commit**

```bash
git add skills/llm-wiki-pdf-extract-local/extract.py skills/llm-wiki-pdf-extract-local/tests/test_extract.py
git commit -m "feat(pdf-extract-local): detect repeated headers/footers"
```

---

### Task 3: `is_heading` + `is_scanned`

**Files:**
- Modify: `skills/llm-wiki-pdf-extract-local/extract.py`
- Test: `skills/llm-wiki-pdf-extract-local/tests/test_extract.py`

**Interfaces:**
- Produces:
  - `is_heading(size: float, body_median: float) -> int` — returns `2` if `size >= 1.5 * body_median`, `3` if `size >= 1.2 * body_median`, else `0`.
  - `is_scanned(avg_chars_per_page: float, threshold: float = 100.0) -> bool` — `True` when text density is too low to be a real text layer.

- [ ] **Step 1: Write the failing test**

Append to `tests/test_extract.py`:

```python
from extract import is_heading, is_scanned


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
```

- [ ] **Step 2: Run test to verify it fails**

Run: `python -m pytest skills/llm-wiki-pdf-extract-local/tests/test_extract.py -k "heading or scanned" -v`
Expected: FAIL — `ImportError: cannot import name 'is_heading'`.

- [ ] **Step 3: Write minimal implementation**

Add to `extract.py`:

```python
def is_heading(size, body_median):
    """0 = body text, 2 = h2, 3 = h3, based on font size vs body median."""
    if body_median <= 0:
        return 0
    if size >= 1.5 * body_median:
        return 2
    if size >= 1.2 * body_median:
        return 3
    return 0


def is_scanned(avg_chars_per_page, threshold=100.0):
    """True when average characters per page is below the text-layer threshold."""
    return avg_chars_per_page < threshold
```

- [ ] **Step 4: Run test to verify it passes**

Run: `python -m pytest skills/llm-wiki-pdf-extract-local/tests/test_extract.py -k "heading or scanned" -v`
Expected: PASS (3 passed).

- [ ] **Step 5: Commit**

```bash
git add skills/llm-wiki-pdf-extract-local/extract.py skills/llm-wiki-pdf-extract-local/tests/test_extract.py
git commit -m "feat(pdf-extract-local): heading classification + scanned detection"
```

---

### Task 4: `build_body`

**Files:**
- Modify: `skills/llm-wiki-pdf-extract-local/extract.py`
- Test: `skills/llm-wiki-pdf-extract-local/tests/test_extract.py`

**Interfaces:**
- Consumes: `find_running_lines`, `is_heading`, `join_dehyphenated`.
- Produces: `build_body(pages: list[list[tuple[str, float]]]) -> str` — `pages` is a list of pages; each page is a list of `(line_text, font_size)`. Returns markdown: heading lines prefixed with `##`/`###`, body lines merged into dehyphenated paragraphs, running headers/footers and blank lines dropped, blocks separated by a blank line.

- [ ] **Step 1: Write the failing test**

Append to `tests/test_extract.py`:

```python
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
```

- [ ] **Step 2: Run test to verify it fails**

Run: `python -m pytest skills/llm-wiki-pdf-extract-local/tests/test_extract.py -k build_body -v`
Expected: FAIL — `ImportError: cannot import name 'build_body'`.

- [ ] **Step 3: Write minimal implementation**

Add `import statistics` at the top of `extract.py`, then add:

```python
def build_body(pages):
    """Assemble cleaned markdown from pages of (line_text, font_size) tuples."""
    pages_text = [[t for t, _ in page] for page in pages]
    running = find_running_lines(pages_text)

    sizes = [
        size
        for page in pages
        for text, size in page
        if text.strip() and text.strip() not in running
    ]
    body_median = statistics.median(sizes) if sizes else 0.0

    blocks = []          # ("h", level, text) or ("p", text)
    para = []            # buffered body lines for the current paragraph

    def flush():
        if para:
            blocks.append(("p", join_dehyphenated(para)))
            para.clear()

    for page in pages:
        for text, size in page:
            t = text.strip()
            if not t or t in running:
                flush()
                continue
            level = is_heading(size, body_median)
            if level:
                flush()
                blocks.append(("h", level, t))
            else:
                para.append(t)
        flush()

    rendered = []
    for block in blocks:
        if block[0] == "h":
            rendered.append("#" * block[1] + " " + block[2])
        else:
            rendered.append(block[1])
    return "\n\n".join(rendered)
```

- [ ] **Step 4: Run test to verify it passes**

Run: `python -m pytest skills/llm-wiki-pdf-extract-local/tests/test_extract.py -k build_body -v`
Expected: PASS (3 passed).

- [ ] **Step 5: Commit**

```bash
git add skills/llm-wiki-pdf-extract-local/extract.py skills/llm-wiki-pdf-extract-local/tests/test_extract.py
git commit -m "feat(pdf-extract-local): assemble cleaned markdown body"
```

---

### Task 5: `extract_pages` (fitz + pdftotext fallback)

**Files:**
- Modify: `skills/llm-wiki-pdf-extract-local/extract.py`
- Test: `skills/llm-wiki-pdf-extract-local/tests/test_extract.py`

**Interfaces:**
- Consumes: PyMuPDF (`fitz`) / `pdftotext`.
- Produces: `extract_pages(pdf_path: str, engine: str = "auto") -> dict` with keys:
  - `pages`: `list[list[tuple[str, float]]]` (line text + font size; size is `1.0` for the pdftotext engine).
  - `first_pages_text`: `str` — raw text of the first up to 2 pages.
  - `page_count`: `int`.
  - `avg_chars_per_page`: `float`.
  - `engine`: `str` — the engine actually used (`"fitz"` or `"pdftotext"`).
  `engine="auto"` uses `fitz` if importable, else `pdftotext`.

- [ ] **Step 1: Write the failing test**

Append to `tests/test_extract.py`:

```python
import fitz  # PyMuPDF, used only to synthesize a test PDF
from extract import extract_pages


def _make_pdf(path):
    doc = fitz.open()
    page = doc.new_page()
    page.insert_text((72, 72), "Big Heading", fontsize=20)
    page.insert_text((72, 110), "Normal body sentence here.", fontsize=11)
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
```

- [ ] **Step 2: Run test to verify it fails**

Run: `python -m pytest skills/llm-wiki-pdf-extract-local/tests/test_extract.py -k extract_pages -v`
Expected: FAIL — `ImportError: cannot import name 'extract_pages'`.

- [ ] **Step 3: Write minimal implementation**

Add `import subprocess` at the top of `extract.py`, then add:

```python
def _extract_with_fitz(pdf_path):
    import fitz

    doc = fitz.open(pdf_path)
    pages = []
    page_texts = []
    try:
        for page in doc:
            lines = []
            text_chunks = []
            data = page.get_text("dict")
            for block in data.get("blocks", []):
                for line in block.get("lines", []):
                    spans = line.get("spans", [])
                    if not spans:
                        continue
                    line_text = "".join(s.get("text", "") for s in spans)
                    max_size = max((s.get("size", 0.0) for s in spans), default=0.0)
                    if line_text.strip():
                        lines.append((line_text, max_size))
                        text_chunks.append(line_text)
            pages.append(lines)
            page_texts.append("\n".join(text_chunks))
    finally:
        doc.close()
    return pages, page_texts


def _extract_with_pdftotext(pdf_path):
    out = subprocess.run(
        ["pdftotext", "-layout", pdf_path, "-"],
        capture_output=True, text=True, check=True,
    ).stdout
    page_texts = out.split("\f")  # pdftotext separates pages with form feeds
    page_texts = [p for p in page_texts if p.strip()] or [out]
    pages = [
        [(ln, 1.0) for ln in p.splitlines() if ln.strip()]
        for p in page_texts
    ]
    return pages, page_texts


def extract_pages(pdf_path, engine="auto"):
    if engine == "auto":
        try:
            import fitz  # noqa: F401
            engine = "fitz"
        except ImportError:
            engine = "pdftotext"

    if engine == "fitz":
        pages, page_texts = _extract_with_fitz(pdf_path)
    elif engine == "pdftotext":
        pages, page_texts = _extract_with_pdftotext(pdf_path)
    else:
        raise ValueError(f"unknown engine: {engine}")

    page_count = len(page_texts)
    total_chars = sum(len(t) for t in page_texts)
    avg = (total_chars / page_count) if page_count else 0.0
    first_pages_text = "\n\n".join(page_texts[:2])
    return {
        "pages": pages,
        "first_pages_text": first_pages_text,
        "page_count": page_count,
        "avg_chars_per_page": avg,
        "engine": engine,
    }
```

- [ ] **Step 4: Run test to verify it passes**

Run: `python -m pytest skills/llm-wiki-pdf-extract-local/tests/test_extract.py -k extract_pages -v`
Expected: PASS (2 passed).

- [ ] **Step 5: Commit**

```bash
git add skills/llm-wiki-pdf-extract-local/extract.py skills/llm-wiki-pdf-extract-local/tests/test_extract.py
git commit -m "feat(pdf-extract-local): fitz extraction with pdftotext fallback"
```

---

### Task 6: CLI `main()` — single JSON to stdout

**Files:**
- Modify: `skills/llm-wiki-pdf-extract-local/extract.py`
- Test: `skills/llm-wiki-pdf-extract-local/tests/test_extract.py`

**Interfaces:**
- Consumes: `extract_pages`, `build_body`, `is_scanned`.
- Produces: CLI `python extract.py <pdf> [--engine auto|fitz|pdftotext]` printing one JSON object to stdout with keys `body`, `first_pages_text`, `page_count`, `avg_chars_per_page`, `scanned`, `engine`. This is the contract the SKILL.md (Task 7) parses.

- [ ] **Step 1: Write the failing test**

Append to `tests/test_extract.py`:

```python
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
```

- [ ] **Step 2: Run test to verify it fails**

Run: `python -m pytest skills/llm-wiki-pdf-extract-local/tests/test_extract.py -k cli -v`
Expected: FAIL — JSON parse error / nonzero exit (no `main()` / `__main__` block yet).

- [ ] **Step 3: Write minimal implementation**

Add `import argparse` and `import json` at the top of `extract.py`, then add at the end of the file:

```python
def main(argv=None):
    parser = argparse.ArgumentParser(description="Local low-token PDF text extractor.")
    parser.add_argument("pdf", help="path to the PDF file")
    parser.add_argument(
        "--engine", choices=["auto", "fitz", "pdftotext"], default="auto"
    )
    args = parser.parse_args(argv)

    data = extract_pages(args.pdf, engine=args.engine)
    out = {
        "body": build_body(data["pages"]),
        "first_pages_text": data["first_pages_text"],
        "page_count": data["page_count"],
        "avg_chars_per_page": data["avg_chars_per_page"],
        "scanned": is_scanned(data["avg_chars_per_page"]),
        "engine": data["engine"],
    }
    print(json.dumps(out, ensure_ascii=False))


if __name__ == "__main__":
    main()
```

- [ ] **Step 4: Run test to verify it passes**

Run: `python -m pytest skills/llm-wiki-pdf-extract-local/tests/test_extract.py -k cli -v`
Expected: PASS (1 passed).

- [ ] **Step 5: Run the whole suite**

Run: `python -m pytest skills/llm-wiki-pdf-extract-local/tests/test_extract.py -v`
Expected: PASS (all tests green: 14 total).

- [ ] **Step 6: Commit**

```bash
git add skills/llm-wiki-pdf-extract-local/extract.py skills/llm-wiki-pdf-extract-local/tests/test_extract.py
git commit -m "feat(pdf-extract-local): CLI emits single JSON contract"
```

---

### Task 7: `SKILL.md` orchestration

**Files:**
- Create: `skills/llm-wiki-pdf-extract-local/SKILL.md`

**Interfaces:**
- Consumes: the `extract.py` CLI JSON contract from Task 6.
- Produces: the skill document Claude Code loads to run the workflow.

- [ ] **Step 1: Write the SKILL.md**

Create `skills/llm-wiki-pdf-extract-local/SKILL.md` with exactly:

````markdown
---
name: llm-wiki-pdf-extract-local
description: Low-token, OFFLINE alternative to llm-wiki-pdf-extract. Converts PDFs in Raw/Files/ into ingest-ready <name>.pdf.md companions using deterministic local extraction (PyMuPDF/pdftotext); a cheap Haiku subagent writes only the header. Use when the user asks to extract/process/convert a PDF "locally", "offline", "cheaply", "quickly", or "without NotebookLM", or to fill missing .pdf.md companions at minimal token cost. For curated study guides, use llm-wiki-pdf-extract instead.
---

# Skill: llm-wiki-pdf-extract-local

## Purpose

Convert PDFs in `Raw/Files/` into `<name>.pdf.md` companions with **minimal token use**.
The local script does all text extraction and cleanup; the document body never enters a
model. A Haiku subagent sees only the first ~2 pages to write a short header.

This is the fast/offline alternative to `llm-wiki-pdf-extract` (NotebookLM study guides).

## When To Use

- A PDF in `Raw/Files/` has no matching `.pdf.md`, and the user wants a low-token/offline extraction.
- The user says "extract locally", "offline", "quick", "cheap", or "without NotebookLM".

## Prerequisites

- `python` available. PyMuPDF (`fitz`) preferred; `pdftotext` is the fallback.
- Script path: the `extract.py` next to this SKILL.md.

## Steps

1. Find PDFs missing a companion: for each `Raw/Files/*.pdf`, check whether
   `Raw/Files/<name>.pdf.md` exists. Process only the missing ones unless the user
   asked to refresh (then include the named ones / all).

2. For each PDF to process:

   a. Run the extractor and capture its JSON stdout:
   ```bash
   python "<skill_dir>/extract.py" "Raw/Files/<name>.pdf"
   ```
   Parse: `body`, `first_pages_text`, `page_count`, `avg_chars_per_page`, `scanned`, `engine`.

   b. If `scanned` is `true` (avg < 100 chars/page): do NOT write a companion. Record the
      PDF as "needs OCR/NotebookLM" and recommend running `llm-wiki-pdf-extract` for it.
      Continue to the next PDF.

   c. Dispatch a **Haiku subagent** to write the header from `first_pages_text` ONLY.
      Subagent prompt:
      > You are given the first pages of an academic PDF. Output ONLY a markdown header:
      > line 1 = `# <concise title>`; line 2 = blank; line 3 = a single italic source line
      > with authors / venue / year / DOI **if present in the text** (omit unknown fields,
      > never invent). No other text, no code fences, no YAML.
      >
      > First pages:
      > <first_pages_text>

   d. Assemble the companion as `<header>\n\n<body>` and write it to
      `Raw/Files/<name>.pdf.md`. Do not overwrite an existing companion unless refreshing.

   e. Verify the file is non-empty and its first line starts with `# `. If not, report the
      failure and delete the bad file (do not leave a broken companion).

3. Report a summary: written, skipped (already had a companion), and flagged-as-scanned.

## Constraints

- Never modify the original PDFs.
- **No YAML frontmatter** in the companion — `# Title`, source line, then body. Frontmatter
  is added later by `scripts/add_frontmatter.py`.
- The document body must never be sent to a model — only `first_pages_text` goes to Haiku.
- Never write a near-empty companion (it would falsely satisfy the "has companion" check).
- Default: skip PDFs that already have a `.pdf.md`. Overwrite only on explicit refresh request.
````

- [ ] **Step 2: Verify frontmatter parses**

Run: `python -c "import sys; t=open('skills/llm-wiki-pdf-extract-local/SKILL.md',encoding='utf-8').read(); assert t.startswith('---'); assert 'name: llm-wiki-pdf-extract-local' in t; print('SKILL.md OK')"`
Expected: prints `SKILL.md OK`.

- [ ] **Step 3: Commit**

```bash
git add skills/llm-wiki-pdf-extract-local/SKILL.md
git commit -m "feat(pdf-extract-local): SKILL.md orchestration"
```

---

### Task 8: End-to-end validation + install to global skills dir

**Files:**
- Install: `~/.claude/skills/llm-wiki-pdf-extract-local/extract.py`, `~/.claude/skills/llm-wiki-pdf-extract-local/SKILL.md`

**Interfaces:**
- Consumes: everything above.
- Produces: a runnable installed skill and verified companions for the 2 missing PDFs.

- [ ] **Step 1: Run the extractor on the two missing PDFs and inspect JSON**

Run (from repo root):
```bash
python "skills/llm-wiki-pdf-extract-local/extract.py" "Raw/Files/oe-18-17-18383.pdf" | python -c "import sys,json; d=json.load(sys.stdin); print('engine',d['engine'],'pages',d['page_count'],'avg',round(d['avg_chars_per_page']),'scanned',d['scanned']); print(d['body'][:300])"
python "skills/llm-wiki-pdf-extract-local/extract.py" "Raw/Files/ome-12-6-2145.pdf"   | python -c "import sys,json; d=json.load(sys.stdin); print('engine',d['engine'],'pages',d['page_count'],'avg',round(d['avg_chars_per_page']),'scanned',d['scanned']); print(d['body'][:300])"
```
Expected: `scanned False`, a positive page count, and readable body text. (If either reports `scanned True`, that PDF is image-only — leave it for the NotebookLM path and note it.)

- [ ] **Step 2: Produce the companions through the full skill flow**

Invoke the skill (`llm-wiki-pdf-extract-local`) on `Raw/Files/`. For each non-scanned missing PDF it runs the script, dispatches the Haiku header subagent, and writes `Raw/Files/<name>.pdf.md`.

Verify each new companion:
```bash
for f in "Raw/Files/oe-18-17-18383.pdf.md" "Raw/Files/ome-12-6-2145.pdf.md"; do
  test -s "$f" && head -1 "$f" | grep -q '^# ' && echo "OK: $f" || echo "MISSING/BAD: $f"
done
```
Expected: `OK:` for each companion that was written (scanned PDFs legitimately absent).

- [ ] **Step 3: Confirm skip behavior leaves existing companions untouched**

Re-invoke the skill. Expected report: the 7 pre-existing companions plus any just-written ones are all **skipped** (already present); nothing is overwritten.

- [ ] **Step 4: Install to the global skills directory**

```bash
mkdir -p ~/.claude/skills/llm-wiki-pdf-extract-local
cp skills/llm-wiki-pdf-extract-local/extract.py skills/llm-wiki-pdf-extract-local/SKILL.md ~/.claude/skills/llm-wiki-pdf-extract-local/
python "$HOME/.claude/skills/llm-wiki-pdf-extract-local/extract.py" --help >/dev/null && echo "installed OK"
```
Expected: `installed OK`. (The global copy is the runtime; the repo copy stays the source of truth.)

- [ ] **Step 5: Commit the new companions**

```bash
git add Raw/Files/*.pdf.md
git commit -m "feat(pdf-extract-local): add local companions for missing PDFs"
```

---

## Self-Review

**Spec coverage:**
- Output type (local text + cheap header) → Tasks 1–6 (extraction) + Task 7 (Haiku header). ✓
- Token control (body never to a model; only first 2 pages) → Task 5 `first_pages_text`, Task 7 subagent prompt, Global Constraints. ✓
- File contract (`Raw/Files/<name>.pdf.md`, no frontmatter, skip-existing, `--force`/refresh) → Global Constraints + Task 7 steps 1, 2d, 3. ✓
- Engine PyMuPDF + pdftotext fallback → Task 5. ✓
- Scanned detection + flag for NotebookLM → Task 3 (`is_scanned`), Task 6 (`scanned` in JSON), Task 7 step 2b. ✓
- Heading detection via font size → Task 3 (`is_heading`) + Task 4 (`build_body`). ✓
- Mechanical cleanup (dehyphenate, strip running furniture, whitespace) → Tasks 1, 2, 4. ✓
- Name/location + global install → Global Constraints + Task 7 + Task 8 step 4. ✓
- Testing (2 missing PDFs, skip, scanned, fallback) → Task 5 (fallback), Task 8 (e2e + skip). ✓
- Error handling (both engines missing, broken header, isolation) → `extract_pages` raises clearly; Task 7 step 2c/2e; per-PDF loop continues. Deterministic header fallback when Haiku is unavailable is noted as a runtime judgment in the spec; Task 7 step 2e deletes broken output rather than aborting. ✓

**Placeholder scan:** No TBD/TODO; every code step shows complete code; every command has an expected result. ✓

**Type consistency:** `extract_pages` returns the dict keys consumed by `build_body` (`pages`) and `main` (`first_pages_text`, `avg_chars_per_page`, `engine`); `pages` element shape `(text, size)` matches `build_body`'s parameter contract in Task 4; CLI JSON keys in Task 6 match what SKILL.md parses in Task 7. ✓
