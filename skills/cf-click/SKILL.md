---
name: cf-click
description: Best-effort auto-clicker for Cloudflare "Verify you are human" / "Just a moment" challenges in the visible Chrome window. Use when running a ResearchGate harvest (researchgate-harvester / "rg harvest") or any Cloudflare-protected browsing task where you want to stop manually clicking the checkbox. Clears the challenge with humanized OS-level mouse input (not Playwright/CDP, which gets detected). Triggers: "cf click", "cloudflare click", "auto-click cloudflare", "start cf-click".
---

# cf-click

A detached Python watcher that watches the visible Chrome window and clicks
the Cloudflare checkbox for you while another agent (e.g. researchgate-harvester)
browses a Cloudflare-protected site.

## Commands

- `python skills/cf-click/cf_click.py start` — launch the watcher (detached)
- `python skills/cf-click/cf_click.py stop` — stop it, print summary
- `python skills/cf-click/cf_click.py status` — running? + click/clear/give-up counts
- `python skills/cf-click/cf_click.py self-test <image.png>` — locate the checkbox in a saved screenshot without clicking (verification)

## Protocol for a ResearchGate harvest

The main agent wraps the harvest (this is also wired in `CLAUDE.md`):

1. `python skills/cf-click/cf_click.py start`
2. delegate to `researchgate-harvester`
3. `python skills/cf-click/cf_click.py stop`

## Constraints

- Keep the Chrome window **visible** and the screen **unlocked** during the run.
- **Best-effort.** If it gives up (3 failed attempts, or 30 clicks/run circuit
  breaker), click the box manually — the harvester's own ~3-min title poll stays
  as the safety net.
- It only ever left-clicks a located checkbox. It never types, fills forms, or
  touches credentials.
