#!/usr/bin/env python3
"""Low-token local PDF -> markdown extractor for llm-wiki-pdf-extract-local."""

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
        if (c >= threshold and len(s) <= max_len) or s.isdigit()
    }


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
