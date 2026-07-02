from cf_click import WinInfo, ensure_window_visible


class FakeApi:
    """Minimal win32gui stand-in with call recording."""

    def __init__(self, iconic=False, foreground_hwnd=0, rect=(10, 20, 810, 620),
                 set_foreground_raises=False):
        self.iconic = iconic
        self.foreground_hwnd = foreground_hwnd
        self.rect = rect
        self.set_foreground_raises = set_foreground_raises
        self.calls = []

    def IsIconic(self, hwnd):
        self.calls.append(("IsIconic", hwnd))
        return self.iconic

    def ShowWindow(self, hwnd, flag):
        self.calls.append(("ShowWindow", hwnd, flag))
        self.iconic = False

    def GetForegroundWindow(self):
        self.calls.append(("GetForegroundWindow",))
        return self.foreground_hwnd

    def SetForegroundWindow(self, hwnd):
        self.calls.append(("SetForegroundWindow", hwnd))
        if self.set_foreground_raises:
            raise OSError("foreground lock")
        self.foreground_hwnd = hwnd

    def BringWindowToTop(self, hwnd):
        self.calls.append(("BringWindowToTop", hwnd))

    def GetWindowRect(self, hwnd):
        self.calls.append(("GetWindowRect", hwnd))
        return self.rect


def names(api):
    return [c[0] for c in api.calls]


def test_minimized_window_restored_with_fresh_rect():
    win = WinInfo(42, "Just a moment...", (-32000, -32000, -31840, -31900))
    api = FakeApi(iconic=True, foreground_hwnd=0, rect=(10, 20, 810, 620))
    slept = []
    out = ensure_window_visible(win, api=api, sleep=slept.append)
    assert ("ShowWindow", 42, 9) in api.calls          # SW_RESTORE
    assert ("SetForegroundWindow", 42) in api.calls
    assert out.rect == (10, 20, 810, 620)               # fresh, not bogus
    assert out.hwnd == 42 and out.title == win.title
    assert slept                                        # settled after change


def test_already_foreground_no_activation_no_sleep():
    win = WinInfo(42, "Just a moment...", (0, 0, 800, 600))
    api = FakeApi(iconic=False, foreground_hwnd=42, rect=(0, 0, 800, 600))
    slept = []
    out = ensure_window_visible(win, api=api, sleep=slept.append)
    assert "ShowWindow" not in names(api)
    assert "SetForegroundWindow" not in names(api)
    assert slept == []                                  # nothing changed
    assert out.rect == (0, 0, 800, 600)


def test_background_window_brought_to_foreground():
    win = WinInfo(42, "Just a moment...", (0, 0, 800, 600))
    api = FakeApi(iconic=False, foreground_hwnd=7, rect=(0, 0, 800, 600))
    out = ensure_window_visible(win, api=api, sleep=lambda s: None)
    assert ("SetForegroundWindow", 42) in api.calls
    assert out.hwnd == 42


def test_foreground_lock_falls_back_to_bring_to_top():
    win = WinInfo(42, "Just a moment...", (0, 0, 800, 600))
    api = FakeApi(iconic=False, foreground_hwnd=7, set_foreground_raises=True)
    out = ensure_window_visible(win, api=api, sleep=lambda s: None)
    assert ("BringWindowToTop", 42) in api.calls
    assert out.rect == api.rect                         # still returns fresh rect


def test_api_failure_returns_original_win():
    class BrokenApi:
        def IsIconic(self, hwnd):
            raise OSError("boom")

    win = WinInfo(42, "Just a moment...", (1, 2, 3, 4))
    out = ensure_window_visible(win, api=BrokenApi(), sleep=lambda s: None)
    assert out is win
