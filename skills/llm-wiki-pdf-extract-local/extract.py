#!/usr/bin/env python3
"""Low-token local PDF -> markdown extractor for llm-wiki-pdf-extract-local."""

import statistics
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


def build_body(pages):
    """Assemble cleaned markdown from pages of (line_text, font_size) tuples."""
    pages_text = [[t for t, _ in page] for page in pages]
    running = find_running_lines(pages_text, min_ratio=2.0 if len(pages_text) == 1 else 0.6)

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
