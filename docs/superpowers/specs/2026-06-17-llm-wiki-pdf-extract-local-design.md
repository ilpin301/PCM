# Design: `llm-wiki-pdf-extract-local`

Date: 2026-06-17
Status: Approved (design); pending implementation plan
Brainstorm capture: `QA/2026-06-17-pdf-extract-lowtoken-skill.md`

## Purpose

A low-token, offline alternative to the existing `llm-wiki-pdf-extract` skill. It converts PDFs in `Raw/Files/` into ingest-ready `<name>.pdf.md` companion files using a **deterministic local extractor**, with a **single cheap-model touch only for the header**. No NotebookLM, no network access for the document body.

`llm-wiki-pdf-extract` (NotebookLM) remains the default/curated path that produces an interpretive study guide. This skill is the fast, faithful, near-free path for filling gaps.

## Goals & non-goals

**Goals**
- Produce faithful, readable markdown of a PDF's text content at near-fixed, minimal token cost regardless of page count.
- Be zero-dependency-by-default and fully offline for the document body.
- Coexist with the existing companions without clobbering them.

**Non-goals**
- Not a study guide / summary / Q&A generator (that is `llm-wiki-pdf-extract`).
- No OCR of scanned/image-only PDFs (detected and flagged instead).
- No table/equation reconstruction beyond best-effort plain text; complex math/tables are extracted as-is.

## Identity & placement

- **Name**: `llm-wiki-pdf-extract-local`
- **Location**: global `~/.claude/skills/llm-wiki-pdf-extract-local/` (sibling to `llm-wiki-pdf-extract`).
- **Trigger phrasing**: "extract this PDF **locally** / offline / low-token / quick / cheaply"; "process PDFs without NotebookLM". The description must make clear it is the *local, low-token* variant so it does not steal the default trigger from `llm-wiki-pdf-extract`.

## Components

### 1. `extract.py` (the only heavy lifter)

Engine: **PyMuPDF (`fitz`)** — chosen because it exposes per-span font size, which the heading heuristic needs and which `pdftotext` cannot provide. Fallback: **`pdftotext`** (poppler) when `fitz` is unavailable (body only, no font-based headings).

Responsibilities:
- Extract text block-by-block, sorting blocks by position to handle multi-column layouts reasonably.
- **Mechanical cleanup** (deterministic, no model):
  - De-hyphenate words broken across line wraps (`exam-\nple` → `example`).
  - Strip repeated running headers/footers: lines that recur on most pages (e.g. journal name, page numbers).
  - Collapse redundant whitespace/blank runs.
- **Heading detection** via font size: spans whose size is meaningfully above the body-text median become `##` / `###` (two tiers). Conservative — when in doubt, leave as body text.
- **Outputs**:
  - `body.md` (or stdout): the cleaned markdown body.
  - A small **JSON sidecar** containing: the text of the **first ~2 pages** (for the header step), `page_count`, and `avg_chars_per_page`.

CLI shape (final flags settled in the implementation plan):
- Input: a single PDF path.
- Output: writes/streams body markdown + the JSON sidecar to a temp/known location.

### 2. Header step (Haiku subagent)

- The skill (main agent) dispatches a **Haiku subagent** with **only the first ~2 pages** of extracted text (from the JSON sidecar).
- The subagent returns a short header:
  - `# <Title>` (inferred from the first page).
  - A one- or two-line source line: authors / venue / year / DOI when visible on the first pages.
- **No YAML frontmatter.** This mirrors the existing companions' light style. Frontmatter is added downstream by `scripts/add_frontmatter.py` at ingest time; `_templates/source-note.md` is the eventual Wiki note shape.
- The document body **never** enters any model's context — this is the core token-control mechanism.

### 3. `SKILL.md` (orchestration)

Steps:
1. Enumerate `Raw/Files/*.pdf`. For each, check whether `Raw/Files/<name>.pdf.md` exists.
   - Default: process only PDFs **without** a companion.
   - `--force` (or explicit user request): re-process and overwrite.
2. For each PDF to process:
   a. Run `extract.py` → body markdown + JSON sidecar.
   b. **Scanned/no-text check**: if `avg_chars_per_page` < ~100, write **nothing**, record the PDF as "needs NotebookLM/OCR", and continue. Recommend the `llm-wiki-pdf-extract` fallback for it.
   c. Dispatch the Haiku subagent with the first ~2 pages → header.
   d. Assemble `header + "\n\n" + body` and write `Raw/Files/<name>.pdf.md`.
   e. **Verify**: file is non-empty and starts with a `#` heading.
3. Report a summary: which PDFs were written, which were skipped (already had a companion), which were flagged as scanned.

## Data flow (per PDF)

```
PDF
 └─ extract.py ──► { body.md, sidecar.json(first 2 pages, page_count, avg_chars_per_page) }
                      │
        avg_chars_per_page < ~100 ? ──yes──► skip + flag for NotebookLM/OCR
                      │ no
                      ▼
        Haiku subagent(first 2 pages) ──► header (# Title + source line)
                      │
                      ▼
        header + body ──► Raw/Files/<name>.pdf.md ──► verify (non-empty, starts with #)
```

## File contract

- Output path: `Raw/Files/<original-name>.pdf.md`.
- Content shape: `# <Title>`, a short source/authors line, then the cleaned markdown body. **No YAML frontmatter.**
- One companion per PDF. Never overwrite an existing companion unless `--force`.

## Error handling

- `fitz` missing → fall back to `pdftotext`. Both missing → report clearly; do not write empty files.
- Extraction yields near-empty text (scanned) → skip + flag; never write a near-empty companion (which would falsely satisfy the "has companion" check and block a later proper extraction).
- Subagent fails to return a usable header → fall back to a deterministic header (filename-derived title + any PDF metadata) rather than aborting the whole file; note this in the run summary.
- Any per-PDF failure is isolated: report it and continue with the remaining PDFs.

## Token budget

- Document body: **0 model tokens** (deterministic extraction + cleanup).
- Per-PDF model cost ≈ first ~2 pages → Haiku, roughly fixed regardless of total page count.

## Testing

- **Happy path**: run on the 2 currently-missing PDFs (`oe-18-17-18383.pdf`, `ome-12-6-2145.pdf`). Confirm each produces a non-empty `.pdf.md` with a sensible `# Title`, a source line, and detected headings in the body.
- **Skip behavior**: re-run; confirm the 7 PDFs that already have companions are skipped and untouched.
- **Force**: `--force` on one existing PDF re-extracts and overwrites.
- **Scanned detection**: feed an image-only PDF (or simulate near-empty extraction); confirm no companion is written and it is flagged for the NotebookLM path.
- **Fallback**: with `fitz` unavailable, confirm `pdftotext` path still produces a usable (headingless) body.

## Open questions / deferred to implementation plan

- Exact `extract.py` CLI flags and sidecar file location/format.
- Precise heading-size threshold and running-header detection ratio (tune against the test PDFs).
- Whether the deterministic header fallback also runs when Haiku is unavailable in the environment.
