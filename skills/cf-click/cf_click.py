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


@dataclass
class Watcher:
    detect: object            # callable() -> WinInfo | None
    locate: object            # callable(WinInfo) -> tuple | None
    click: object             # callable(point, WinInfo) -> None
    log: object = lambda **k: None
    max_attempts: int = MAX_ATTEMPTS
    max_total_clicks: int = MAX_TOTAL_CLICKS
    state: str = "IDLE"
    click_attempts: int = 0
    total_clicks: int = 0
    handled: int = 0
    gave_up: int = 0
    abandoned_hwnd: object = None  # hwnd we gave up on; skip until it clears

    def tick(self) -> str:
        if self.total_clicks >= self.max_total_clicks:
            return "STOP"
        win = self.detect()
        if win is None:
            if self.state in ("CHALLENGE", "VERIFY") and self.abandoned_hwnd is None:
                self.handled += 1
                self.log(event="CLEARED")
            self.state = "IDLE"
            self.click_attempts = 0
            self.abandoned_hwnd = None
            return "IDLE"
        if self.abandoned_hwnd == win.hwnd:
            return "ABANDONED"
        coords = self.locate(win)
        if coords is None:
            self.state = "VERIFY"
            return "NO_CHECKBOX"
        if self.click_attempts >= self.max_attempts:
            self.abandoned_hwnd = win.hwnd
            self.gave_up += 1
            self.state = "IDLE"
            self.log(event="GIVE_UP", hwnd=win.hwnd)
            return "GIVE_UP"
        self.click(coords, win)
        self.total_clicks += 1
        self.click_attempts += 1
        self.state = "CHALLENGE"
        self.log(event="CLICKED", hwnd=win.hwnd, x=coords[0], y=coords[1])
        return "CLICKED"

    def run(self, sleep=None):
        if sleep is None:
            sleep = lambda: time.sleep(random.uniform(LOOP_MIN, LOOP_MAX))
        while True:
            result = self.tick()
            if result == "STOP":
                break
            sleep()


def humanized_click(point, win: WinInfo):
    """Bring the window forward and click `point` with humanized movement."""
    import pyautogui
    import win32gui

    try:
        win32gui.ShowWindow(win.hwnd, 9)            # SW_RESTORE
        win32gui.SetForegroundWindow(win.hwnd)
    except Exception:
        pass
    x, y = point
    pyautogui.moveTo(x, y, duration=random.uniform(0.25, 0.6),
                     tween=pyautogui.easeOutQuad)
    time.sleep(random.uniform(0.08, 0.25))
    pyautogui.click(x, y)


# ---- logging + lifecycle ----

def log_event(**fields):
    RUNDIR.mkdir(parents=True, exist_ok=True)
    fields.setdefault("ts", time.strftime("%Y-%m-%dT%H:%M:%S"))
    with open(LOGFILE, "a", encoding="utf-8") as f:
        f.write(json.dumps(fields, ensure_ascii=False) + "\n")


def _pid_alive(pid) -> bool:
    if not pid:
        return False
    try:
        out = subprocess.run(
            ["tasklist", "/FI", f"PID eq {pid}", "/NH"],
            capture_output=True, text=True, timeout=10,
        ).stdout
        return str(pid) in out
    except Exception:
        return False


def _summary() -> str:
    clicks = gave_up = cleared = 0
    last = ""
    if Path(LOGFILE).exists():
        for line in Path(LOGFILE).read_text(encoding="utf-8").splitlines():
            try:
                o = json.loads(line)
            except json.JSONDecodeError:
                continue
            if o.get("event") == "CLICKED":
                clicks += 1
            elif o.get("event") == "CLEARED":
                cleared += 1
            elif o.get("event") == "GIVE_UP":
                gave_up += 1
            if o.get("ts"):
                last = o["ts"]
    return f"clicks={clicks} cleared={cleared} gave_up={gave_up} last={last}"


def cmd_start():
    RUNDIR.mkdir(parents=True, exist_ok=True)
    if PIDFILE.exists() and _pid_alive(PIDFILE.read_text().strip()):
        print(f"already running (pid {PIDFILE.read_text().strip()})")
        return
    flags = 0x00000008 | 0x00000200  # DETACHED_PROCESS | CREATE_NEW_PROCESS_GROUP
    with open(LOGFILE, "a", encoding="utf-8") as out:
        proc = subprocess.Popen(
            [sys.executable, str(Path(__file__).resolve()), "watch"],
            stdout=out, stderr=subprocess.STDOUT, stdin=subprocess.DEVNULL,
            creationflags=flags, close_fds=True,
        )
    PIDFILE.write_text(str(proc.pid))
    print(f"started watcher pid {proc.pid}; log {LOGFILE}")


def cmd_stop():
    if not PIDFILE.exists():
        print("not running")
        return
    pid = PIDFILE.read_text().strip()
    subprocess.run(["taskkill", "/PID", pid, "/F", "/T"], capture_output=True)
    PIDFILE.unlink(missing_ok=True)
    print(_summary())


def cmd_status():
    running = PIDFILE.exists() and _pid_alive(PIDFILE.read_text().strip())
    print(f"running: {running}")
    print(_summary())


def _make_real_watcher():
    return Watcher(
        detect=lambda: select_target_window(list_chrome_windows()),
        locate=lambda win: locate_checkbox(win),
        click=humanized_click,
        log=log_event,
    )


def cmd_watch():
    RUNDIR.mkdir(parents=True, exist_ok=True)
    log_event(event="START")
    w = _make_real_watcher()
    w.run()
    log_event(event="STOP", total_clicks=w.total_clicks,
              handled=w.handled, gave_up=w.gave_up)


def cmd_self_test(image=None):
    win = WinInfo(0, "self-test", (0, 0, 1920, 1080))
    coords = locate_checkbox(win, image_path=Path(image)) if image else None
    print(f"locate -> {coords}")


def main(argv=None):
    argv = list(sys.argv[1:] if argv is None else argv)
    cmd = argv[0] if argv else "status"
    if cmd == "start":
        cmd_start()
    elif cmd == "stop":
        cmd_stop()
    elif cmd == "status":
        cmd_status()
    elif cmd == "watch":
        cmd_watch()
    elif cmd == "self-test":
        cmd_self_test(argv[1] if len(argv) > 1 else None)
    else:
        print("usage: cf_click.py [start|stop|status|watch|self-test [image]]")
        sys.exit(2)


if __name__ == "__main__":
    main()
