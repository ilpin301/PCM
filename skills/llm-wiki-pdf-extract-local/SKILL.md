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
