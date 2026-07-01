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
