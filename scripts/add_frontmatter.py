#!/usr/bin/env python3
"""Add llmwiki Raw-source frontmatter to NotebookLM web-export .md files.

Reads each export in PCM_New__export/, extracts the leading '# Title' and
'Source URL:' line, and writes a frontmatter'd copy into 'Temp sources/'.
Raw exports are never modified (AGENTS.md). Known-junk and still-blocked
pages are skipped and reported rather than wrapped.

Usage:  python scripts/add_frontmatter.py
        python scripts/add_frontmatter.py --src <dir> --out <dir>
"""
import os, re, sys, glob, argparse, datetime

try:  # Windows consoles default to cp1251 here; force UTF-8 so prints don't crash.
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

SRC = r"F:\____IL_AI\PCM\PCM_New__export"
OUT = r"F:\____IL_AI\PCM\Temp sources"
TODAY = datetime.date.today().isoformat()

# 11 known-junk exports: 9 captcha (recovered via API) + 2 navigation pages.
# Matched by case-insensitive substring of the filename.
SKIP_KNOWN = [
    "Challenges and Enhancement Strategies -",          # PMC13150642 (recovered)
    "Endurance of chalcogenide optical phase change",   # Optica (recovered)
    "Laser-induced phase transitions of Ge2Sb2Te5",     # Optica (recovered)
    "Microstructure characterization, phase transition",# PMC (recovered)
    "Multifunctional Electrospun Phase Change Material",# PMC (recovered)
    "Nanoencapsulation of phase change materials",      # PMC (recovered)
    "Phase-Change Memory from Molecular Tellurides",    # PMC (recovered)
    "Protocol for nanoscale thermal mapping",           # PMC (recovered)
    "Solution-derived Ge",                              # PMC (recovered)
    "RePEc",                                            # nav page
    "PapersFlow",                                       # nav page
]

BLOCK_MARKERS = [
    "checking your browser", "recaptcha", "requires you to enter",
    "before you can download", "verifying you are human", "just a moment",
    "enable javascript and cookies", "select all images", "select all squares",
    # publisher nav / login pages NotebookLM sometimes captures instead of content
    "your token has expired", "please log in again", "skip to article",
    "skip to sidebar", "recently viewed", "close modal",
]

# A real article body has many long paragraph lines; nav/login pages have almost
# none. Require at least this many characters living in long (>100 char) lines.
MIN_PROSE_CHARS = 600

def slug(s):
    s = re.sub(r"[^\w\s-]", "", s.lower()).strip()
    return re.sub(r"[\s_]+", "-", s)[:80].strip("-")

def content_type(url):
    u = (url or "").lower()
    if u.endswith(".pdf") or ".pdf" in u:
        return "pdf"
    return "web"

def frontmatter(title, ref, ctype):
    return (
        "---\n"
        f'Title: "{title.replace(chr(34), chr(39))}"\n'
        'Author: "Unknown"\n'
        f'Reference: "{ref}"\n'
        "ContentType:\n"
        f'  - "{ctype}"\n'
        f"Created: {TODAY}\n"
        "Processed: false\n"
        "tags:\n"
        '  - "source"\n'
        "---\n\n"
    )

def parse(text):
    lines = text.splitlines()
    title, url, body_start = None, None, 0
    for i, ln in enumerate(lines[:6]):
        s = ln.strip()
        if title is None and s.startswith("# "):
            title = s[2:].strip().rstrip(".").strip()
        m = re.match(r"Source URL:\s*(\S+)", s, re.I)
        if m:
            url = m.group(1)
            body_start = i + 1
    body = "\n".join(lines[body_start:]).strip()
    return title, url, body

def main(src, out):
    os.makedirs(out, exist_ok=True)
    files = sorted(glob.glob(os.path.join(src, "*.md")))
    conv, skip = [], []
    for path in files:
        name = os.path.basename(path)
        if any(k.lower() in name.lower() for k in SKIP_KNOWN):
            print(f"[SKIP] known junk/recovered : {name}")
            skip.append((name, "known junk/recovered"))
            continue
        with open(path, "r", encoding="utf-8") as f:
            text = f.read()
        if text.lstrip().startswith("---"):
            print(f"[SKIP] already has frontmatter: {name}")
            skip.append((name, "already has frontmatter"))
            continue
        title, url, body = parse(text)
        # NotebookLM PDF exports sometimes use the URL as the '# ' line — derive a
        # placeholder title from the filename instead, and flag it for manual fixing.
        if title and re.match(r"https?://", title):
            title = None
        flagged = title is None
        title = title or re.sub(r"\.(pdf|md)$", "", name, flags=re.I)
        title = re.sub(r"[_-]+", " ", title).strip()
        low = body.lower()
        if any(mk in low for mk in BLOCK_MARKERS):
            print(f"[SKIP] blocked/nav page       : {name}")
            skip.append((name, "blocked/nav page"))
            continue
        prose = sum(len(l) for l in body.splitlines() if len(l.strip()) > 100)
        if prose < MIN_PROSE_CHARS:
            print(f"[SKIP] little prose (prose={prose}) : {name}")
            skip.append((name, f"little prose ({prose} chars in long lines) — nav/abstract-only"))
            continue
        ref = url or name
        dest = os.path.join(out, (slug(title) or slug(os.path.splitext(name)[0])) + ".md")
        with open(dest, "w", encoding="utf-8") as f:
            f.write(frontmatter(title, ref, content_type(url)))
            f.write(body + "\n")
        flag = "  [!] title from filename — fix Title" if flagged else ""
        print(f"[CONVERT] {name}\n           -> {dest}{flag}")
        conv.append((dest, flagged))
    print(f"\nDone. Converted {len(conv)}, skipped {len(skip)}.")
    needfix = [d for d, fl in conv if fl]
    if needfix:
        print(f"Title needs manual fix ({len(needfix)}):")
        for d in needfix:
            print(f"  - {os.path.basename(d)}")
    if skip:
        print("Skipped:")
        for n, why in skip:
            print(f"  - {n} :: {why}")

if __name__ == "__main__":
    ap = argparse.ArgumentParser(description="Add Raw-source frontmatter to NotebookLM web-exports.")
    ap.add_argument("--src", default=SRC)
    ap.add_argument("--out", default=OUT)
    args = ap.parse_args()
    main(args.src, args.out)
