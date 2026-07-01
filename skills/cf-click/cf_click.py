"""cf-click: best-effort OS-level Cloudflare auto-clicker watcher.

Detects a Cloudflare challenge in the visible Chrome window (Win32 title
polling), locates the checkbox (cheap vision call), and clears it with
humanized OS-level mouse input. Purely additive: if it fails, the existing
human-in-the-loop poll in researchgate-harvester still works.
"""
from __future__ import annotations

import json
import os
import random
import re
import subprocess
import sys
import tempfile
import time
from dataclasses import dataclass
from pathlib import Path

CHALLENGE_PATTERNS = ("just a moment", "verify you are human", "security check required")
AFFINITY_PATTERNS = ("researchgate", "researchgate.net")
MAX_ATTEMPTS = 3
MAX_TOTAL_CLICKS = 30
LOOP_MIN = 2.0
LOOP_MAX = 5.0
VISION_MODEL = "haiku"

RUNDIR = Path(os.environ.get("CF_CLICK_RUNDIR", ".cf-click"))
PIDFILE = RUNDIR / "watcher.pid"
LOGFILE = RUNDIR / "watcher.log"


@dataclass
class WinInfo:
    hwnd: int
    title: str
    rect: tuple  # (left, top, right, bottom) in screen pixels


def is_challenge_title(title: str, patterns: tuple = CHALLENGE_PATTERNS) -> bool:
    t = (title or "").lower()
    return any(p in t for p in patterns)


def select_target_window(
    windows,
    challenge_patterns: tuple = CHALLENGE_PATTERNS,
    affinity_patterns: tuple = AFFINITY_PATTERNS,
):
    challenged = [w for w in windows if is_challenge_title(w.title, challenge_patterns)]
    if not challenged:
        return None
    if len(challenged) == 1:
        return challenged[0]
    affiliated = [
        w for w in challenged
        if any(p in (w.title or "").lower() for p in affinity_patterns)
    ]
    if len(affiliated) == 1:
        return affiliated[0]
    return None  # ambiguous -> do nothing (don't click in unrelated tabs)


def list_chrome_windows():
    """Live Win32 enumeration of visible Chrome top-level windows."""
    import win32gui

    found = []

    def _cb(hwnd, _):
        if not win32gui.IsWindowVisible(hwnd):
            return
        if win32gui.GetClassName(hwnd) != "Chrome_WidgetWin_1":
            return
        title = win32gui.GetWindowText(hwnd)
        if not title:
            return
        found.append(WinInfo(hwnd, title, win32gui.GetWindowRect(hwnd)))

    win32gui.EnumWindows(_cb, None)
    return found


def screenshot_window(win: WinInfo, dest):
    """Screenshot the window's screen rect to `dest` (path-like)."""
    import pyautogui

    left, top, right, bottom = win.rect
    region = (left, top, max(1, right - left), max(1, bottom - top))
    pyautogui.screenshot(region=region).save(str(dest))
    return Path(dest)


def _parse_vision_json(text: str, win: WinInfo) -> dict:
    m = re.search(r"\{.*\}", text or "", re.S)
    if not m:
        return {"click": False}
    try:
        obj = json.loads(m.group(0))
    except json.JSONDecodeError:
        return {"click": False}
    if not obj.get("click"):
        return {"click": False}
    try:
        x, y = int(obj["x"]), int(obj["y"])
    except (KeyError, TypeError, ValueError):
        return {"click": False}
    left, top, right, bottom = win.rect
    if not (left <= x <= right and top <= y <= bottom):
        return {"click": False}
    return {"click": True, "x": x, "y": y}


def vision_locate_via_cli(image_path, win: WinInfo) -> dict:
    """Ask Haiku (via `claude -p`) where the Cloudflare checkbox is.

    Reuses the session's auth — no separate API key. If `claude` is missing
    or the `@path` image mechanism from Step 1 does not work, swap this body
    for an `anthropic` SDK call with a base64 image block + ANTHROPIC_API_KEY;
    the signature stays the same.
    """
    left, top, _r, _b = win.rect
    prompt = (
        f"You locate a UI element in a screenshot. The screenshot's top-left is "
        f"at absolute screen pixel ({left}, {top}). If the image contains an "
        f"interactive Cloudflare checkbox ('Verify you are human' / "
        f"'I'm not a robot'), reply ONLY JSON: {{\"click\": true, \"x\": <int>, "
        f"\"y\": <int>}} where x,y are ABSOLUTE screen coordinates of the checkbox "
        f"center. If there is no clickable checkbox (passive 'Just a moment', or "
        f"the real page already loaded), reply ONLY {{\"click\": false}}. "
        f"@{image_path}"
    )
    try:
        proc = subprocess.run(
            ["claude", "-p", "--model", VISION_MODEL, prompt],
            capture_output=True, text=True, timeout=60,
        )
    except (FileNotFoundError, subprocess.TimeoutExpired):
        return {"click": False}
    return _parse_vision_json(proc.stdout, win)


def locate_checkbox(win: WinInfo, vision_fn=vision_locate_via_cli, image_path=None):
    """Return (x, y) screen coords of the checkbox, or None if none found.

    `vision_fn` is injectable so tests don't need a live model or browser.
    """
    image_path = image_path or Path(tempfile.gettempdir()) / f"cf_click_{win.hwnd}.png"
    try:
        screenshot_window(win, image_path)
    except Exception:
        return None
    res = vision_fn(image_path, win)
    if res.get("click"):
        return (res["x"], res["y"])
    return None
