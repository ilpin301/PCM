#!/usr/bin/env python3
"""Low-token local PDF -> markdown extractor for llm-wiki-pdf-extract-local."""

import argparse
import json
import re
import statistics
import subprocess
import sys
from collections import Counter


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


_TRAILING_PAGENUM = re.compile(r"[\s.,;:/–—-]*\d+\s*$")


def _furniture_key(line):
    """Normalize a line for furniture detection: drop a trailing page number and
    collapse internal whitespace. Returns '' for lines that are only a number."""
    s = line.strip()
    s = _TRAILING_PAGENUM.sub("", s)
    s = re.sub(r"\s+", " ", s).strip()
    return s


def _is_page_number(line):
    """True for a bare, page-number-like line (1-4 digits only)."""
    return re.fullmatch(r"\d{1,4}", line.strip()) is not None


def find_running_lines(pages_text, min_ratio=0.6):
    """Normalized line-forms that recur on >= min_ratio of pages (headers/footers).

    Lines are normalized with `_furniture_key` so footers that differ only by a
    trailing page number collapse to one key. Pure-number lines normalize to '' and
    are excluded here (bare page numbers are handled by `_is_page_number` in
    `build_body`). Long lines are no longer exempt: recurrence across most pages is
    the furniture signal.
    """
    n = len(pages_text)
    if n == 0:
        return set()
    counts = Counter()
    for lines in pages_text:
        keys = {
            _furniture_key(ln)
            for ln in lines
            if ln.strip() and _furniture_key(ln)
        }
        for k in keys:
            counts[k] += 1
    threshold = min_ratio * n
    return {k for k, c in counts.items() if c >= threshold}


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


def build_body(pages):
    """Assemble cleaned markdown from pages of (line_text, font_size) tuples."""
    pages_text = [[t for t, _ in page] for page in pages]
    running = find_running_lines(
        pages_text, min_ratio=2.0 if len(pages_text) == 1 else 0.6
    )

    def is_furniture(text):
        t = text.strip()
        if not t:
            return False
        if _is_page_number(t):
            return True
        return _furniture_key(t) in running

    sizes = [
        size
        for page in pages
        for text, size in page
        if text.strip() and not is_furniture(text)
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
            if not t or is_furniture(text):
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


def main(argv=None):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except (AttributeError, ValueError):
        pass

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
