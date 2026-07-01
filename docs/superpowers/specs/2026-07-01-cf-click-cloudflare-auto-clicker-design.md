# Design: `cf-click` — OS-level Cloudflare auto-clicker

- **Date:** 2026-07-01
- **Status:** Approved (Variant A) — pending spec review
- **Scope:** ResearchGate harvests via the existing `researchgate-harvester` subagent; designed to generalize to other Cloudflare-protected sites later.

## 1. Problem

The `researchgate-harvester` subagent (`.claude/agents/researchgate-harvester.md`, Sonnet) drives a real Chrome window through **Playwright MCP**. ResearchGate sits behind Cloudflare Turnstile, so on first load and roughly every ~2 navigations the page shows *"Just a moment…" / "Verify you are human."* The agent **cannot** clear it: its own instructions say *"Do NOT try to auto-click it — coordinate/mouse clicks are detected and the challenge just re-issues (new Ray ID)."* That warning refers to **CDP/Playwright coordinate clicks**, which are detectable. So today the agent polls the page title for up to ~3 minutes and a **human** must click the checkbox in the visible window.

**Goal:** remove the human from that loop in the common case.

**Success bar (chosen):** *Reduce the clicking.* Best-effort auto-click; if it occasionally fails, the human clicks (the harvester's existing poll + manual fallback stays intact as graceful degradation). **Not** a guaranteed bypass.

## 2. Key idea

Use **OS-level mouse input** (real Win32 `SendInput` events via `pyautogui`, with humanized movement), not Playwright/CDP coordinate clicks. OS-level events go through the real Windows input stack, so at the browser level they are indistinguishable from a human — the harvester's "clicks get detected" warning does **not** apply to them. The clicker runs as a separate process and acts on the **same visible Chrome window** the harvester already opens.

## 3. Architecture

**Form: a skill** (`cf-click`), not a subagent. A clicker must run *concurrently* with the harvester for minutes; a subagent dispatches and returns. The skill ships a deterministic Python watcher (`cf_click.py`) plus `SKILL.md` documenting the protocol. Vision localization is offloaded to a cheap model (Haiku), matching the "run autonomously, offload to cheaper models" preference.

**Zero changes to the harvester.** The harvester keeps doing exactly what it does today. Lifecycle is owned by the **main agent**, which wraps the delegation:

```
User: "rg harvest …"
  │
  ▼
Main agent:
  1. python skills/cf-click/cf_click.py start      ← launches detached watcher
  2. delegate to researchgate-harvester             ← blocks for the whole harvest
  3. python skills/cf-click/cf_click.py stop         ← kills watcher, prints summary
```

The harvester never knows the watcher exists. The watcher is purely additive: when it works it saves clicks; when it fails the harvester's own ~3-min title-poll + human fallback still works.

**Integration trigger (auto-wrap — decided):** `cf-click` is a user-invocable skill with explicit `start`/`stop`/`status` commands, **and** ResearchGate harvests auto-wrap. This is wired through a one-line nudge in the project `CLAUDE.md` (the orchestration layer — the harvester agent file itself stays untouched) instructing the main agent to run `cf_click.py start` before delegating to `researchgate-harvester` and `cf_click.py stop` after it returns. The `SKILL.md` documents the same protocol so the skill is also usable standalone.

## 4. Components (`skills/cf-click/cf_click.py`)

One file, four logical units, each independently testable:

1. **CLI / lifecycle** — `start | stop | status | watch | self-test` (see §8).
2. **Detector** — finds the right Chrome window and decides if a challenge is showing (§5).
3. **Locator** — finds the checkbox on screen (§6).
4. **Clicker** — humanized OS-level click (§7).

A small state machine drives the loop (§5): `IDLE → CHALLENGE → VERIFY → IDLE | GIVE_UP`.

## 5. Detection (Win32 window-title polling)

- Enumerate top-level windows via `win32gui.EnumWindows`; keep windows of class `Chrome_WidgetWin_1`.
- Match `GetWindowText` against **configurable title patterns**:
  - challenge-active: `just a moment`, `verify you are human`, `security check required`
  - site-affinity (RG): `researchgate`, `researchgate.net`
- A challenge is "active" when a Chrome window's title matches a challenge pattern. **Window selection (v1):** among Chrome windows matching a challenge pattern, prefer one that also matches an RG-affinity pattern; if exactly one challenged window exists, act on it; if several challenged windows exist and none is RG-affiliated, do nothing this tick (avoid clicking in unrelated tabs). The watcher targets the selected window's `GetWindowRect`.
- **State machine:** every loop tick (~2–5 s, randomized):
  - `IDLE`: no challenge title → sleep.
  - `CHALLENGE`: challenge title present → screenshot window → locate → click → go to `VERIFY`.
  - `VERIFY`: re-check title for ~15 s. Cleared (real RG title / no challenge pattern) → `IDLE`, log success. Still challenged → retry from `CHALLENGE` up to **3 attempts**, randomized delays. After 3 failed attempts → `GIVE_UP`, log, leave for the human (do **not** loop forever).
- If the challenge is the **non-interactive/passive** kind (no checkbox, just "Just a moment…" auto-resolving), the Locator returns "no clickable checkbox" → the watcher does **not** click, just waits for the title to clear.

## 6. Localization (screenshot + cheap vision)

- Screenshot the target window's rect (`pyautogui.screenshot(region=...)`), save to a temp PNG.
- Ask a **Haiku vision model via the `claude` CLI in print mode** to return the checkbox center as JSON screen coordinates, e.g. `claude -p --model claude-haiku-4-5 "<prompt>"` with the image path. The prompt maps image pixels to absolute screen coords using the window rect and instructs: return `{"click": true, "x": <int>, "y": <int>}` only if an interactive Cloudflare checkbox is present, else `{"click": false}`. Validate the returned point falls **inside** the window rect; clamp/reject otherwise.
- **Inner fallback (Variant C):** if the vision call errors, times out, or returns `click:false` while a challenge title is still present, optionally try one click at the canonical centered region of the challenge widget, then re-verify. If that also fails, `GIVE_UP`.
- `claude` CLI is chosen so the watcher reuses the session's auth (no separate API key). If invoking `claude` from a detached process proves unreliable, fall back to the `anthropic` SDK + `ANTHROPIC_API_KEY` — flagged as an implementation verification step (§13).

## 7. Click (humanized, OS-level, guarded)

- `win32gui.SetForegroundWindow(hwnd)` on the target window so the click lands, then:
- `pyautogui.moveTo(x, y, duration=random(0.25–0.6 s), tween=easeOutQuad)`, small random terminal jitter (±a few px), random pre-click dwell (80–250 ms), then `click()`.
- This produces non-deterministic, human-like `SendInput` events — not detectable as automation at the browser level.
- **The clicker only ever left-clicks a single located point.** It never types, never presses keys, never fills forms, never touches credentials.

## 8. CLI contract

```
python skills/cf-click/cf_click.py start      # detach watcher (pythonw + DETACHED_PROCESS), write PID + log
python skills/cf-click/cf_click.py stop        # read PID, terminate, print summary
python skills/cf-click/cf_click.py status      # running? challenges handled, gave-up count, last event
python skills/cf-click/cf_click.py watch       # foreground loop (used by `start`; also runnable directly)
python skills/cf-click/cf_click.py self-test   # run Locator on a fixture screenshot, print coords, NO click
```

- Runtime artifacts (PID, log) live in a gitignored `.cf-click/` at project root (fallback: `%TEMP%\cf-click\`). Logs contain **only** timestamps, actions, coords, and window titles — never page content or secrets (auditable by `scripts/audit_public.py`).

## 9. Dependencies & install

- `pywin32` (win32gui — window enum/rect/foreground), `pyautogui` (mouse + screenshot; pulls Pillow).
- No `anthropic` SDK required if the `claude` CLI path works.
- Install on this machine must bypass the SOCKS system proxy:
  ` $env:NO_PROXY='*'; python -m pip install pywin32 pyautogui`

## 10. Safety & guardrails

- **Act only on a detected Cloudflare checkbox** inside the target window. Reject out-of-bounds coords. Never click anywhere vision didn't identify (centered-region fallback is bounded to the widget area).
- **Bounded:** max 3 attempts per challenge; min ~3 s between clicks; **circuit breaker** — stop after e.g. 30 total clicks per run to prevent runaway.
- **Additive/graceful:** any exception, missing window, or failed vision call → log and continue/sleep. The harvest is never harmed; worst case it degrades to today's manual flow.
- **No secrets, no raw exports, no page content** in artifacts.

## 11. Testing strategy

- **Fixture-based Locator test (`self-test`):** feed saved Cloudflare-challenge screenshots (light/dark, checked/unchecked) through the Locator and assert it returns sane in-window coords. Deterministic, no live browser, no live Cloudflare. This is the primary automated test.
- **State-machine unit tests:** stub the Detector (window/title) and Clicker (no-op) to drive `IDLE→CHALLENGE→VERIFY→IDLE/GIVE_UP` transitions and the retry/circuit-breaker logic.
- **Manual smoke (not automatable in CI):** run a real RG harvest with watcher on → confirm it clears challenges; compare to watcher-off (current behavior). Live Cloudflare cannot be reliably tested headless, so this stays manual.
- No fabricated pass-rates: report actual handled/gave-up counts from the log, never present a tiny run as proof of reliability.

## 12. Known constraints

- Chrome window must stay **visible and the screen unlocked** during the run (OS-level input can't reach a minimized/covered/locked window). No worse than today; now you can ignore the window instead of watching it.
- Best-effort, not guaranteed — matches the chosen "reduce the clicking" bar.
- Targets ResearchGate by default; title patterns are config so it generalizes later.

## 13. Open items / implementation verification

1. **Skill discovery:** confirm `skills/cf-click/SKILL.md` is auto-discovered like the other `skills/*` skills (the project's existing `llm-wiki-pdf-extract-*` skills are). If project skills are discovered from a different path, place/ symlink accordingly.
2. **Vision call transport:** verify the `claude -p --model claude-haiku-4-5 …` invocation works from a detached process and returns parseable JSON coords; otherwise switch to the `anthropic` SDK + key.
3. **Windows detachment:** confirm `pythonw` + `DETACHED_PROCESS` (or equivalent) reliably backgrounds the watcher and survives the main agent's delegation window.
