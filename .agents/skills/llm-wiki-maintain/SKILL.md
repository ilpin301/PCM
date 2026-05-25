# Skill: llm-wiki-maintain

## Purpose

Keep the Wiki healthy: rebuild indexes, update the manifest, and run all gates.

## When To Use

- After any batch of edits or ingests
- When the user asks to "maintain", "rebuild", or "refresh" the Wiki
- As a routine check before a commit

## Steps

1. Rebuild all generated artifacts:
   ```bash
   python3 scripts/wiki_tool.py build
   ```
2. Validate compiled Wiki notes:
   ```bash
   python3 scripts/wiki_tool.py lint
   ```
3. Update the source manifest:
   ```bash
   python3 scripts/wiki_tool.py source-scan --update --accept-covered
   ```
4. Validate source coverage:
   ```bash
   python3 scripts/wiki_tool.py source-lint
   ```
5. Check for secrets or local paths:
   ```bash
   python3 scripts/audit_public.py
   ```
6. Run doctor for a summary:
   ```bash
   python3 scripts/wiki_tool.py doctor
   ```

## What Gets Regenerated

- `Wiki/catalog.jsonl` — machine-readable index of all compiled Wiki notes
- `Wiki/index.md` — human-readable master index
- `Wiki/Topics/index.md`, `Wiki/Concepts/index.md`, etc. — per-folder indexes
- `Schema/source-manifest.jsonl` — coverage map of Raw sources

## Constraints

- Do not manually edit `catalog.jsonl`, `index.md`, or `source-manifest.jsonl` — always regenerate them with `wiki_tool.py build` and `source-scan --update`.
