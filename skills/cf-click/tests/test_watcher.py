from cf_click import Watcher, WinInfo


def make_watcher(detect, locate, click, **kw):
    return Watcher(detect=detect, locate=locate, click=click, log=lambda **k: None, **kw)


def test_idle_when_no_window():
    w = make_watcher(detect=lambda: None, locate=lambda win: None, click=lambda p, win: None)
    for _ in range(5):
        assert w.tick() == "IDLE"
    assert w.total_clicks == 0


def test_clicks_then_clears_counts_handled():
    seq = iter([WinInfo(1, "Just a moment...", (0, 0, 1000, 800)),
                WinInfo(1, "Just a moment...", (0, 0, 1000, 800)),
                None])
    clicked = []
    w = make_watcher(detect=lambda: next(seq), locate=lambda win: (50, 60),
                     click=lambda p, win: clicked.append(p))
    assert w.tick() == "CLICKED"
    assert w.tick() == "CLICKED"
    assert w.tick() == "IDLE"          # cleared
    assert clicked == [(50, 60), (50, 60)]
    assert w.total_clicks == 2 and w.handled == 1


def test_give_up_after_max_attempts_then_abandoned():
    clicked = []
    w = make_watcher(detect=lambda: WinInfo(1, "Verify you are human", (0, 0, 1000, 800)),
                     locate=lambda win: (50, 60),
                     click=lambda p, win: clicked.append(p))
    assert w.tick() == "CLICKED"       # attempt 1
    assert w.tick() == "CLICKED"       # attempt 2
    assert w.tick() == "CLICKED"       # attempt 3
    assert w.tick() == "GIVE_UP"       # 3 clicks already -> give up
    assert w.tick() == "ABANDONED"     # same hwnd -> skip
    assert w.tick() == "ABANDONED"
    assert len(clicked) == 3 and w.gave_up == 1


def test_passive_challenge_never_clicks():
    clicked = []
    w = make_watcher(detect=lambda: WinInfo(1, "Just a moment...", (0, 0, 1000, 800)),
                     locate=lambda win: None, click=lambda p, win: clicked.append(p))
    for _ in range(4):
        assert w.tick() == "NO_CHECKBOX"
    assert clicked == []


def test_circuit_breaker_stops():
    w = make_watcher(detect=lambda: WinInfo(1, "Just a moment...", (0, 0, 1000, 800)),
                     locate=lambda win: (1, 1), click=lambda p, win: None,
                     max_total_clicks=2)
    assert w.tick() == "CLICKED"
    assert w.tick() == "CLICKED"
    assert w.tick() == "STOP"


def test_reset_after_clear_engages_new_challenge():
    states = [None, WinInfo(1, "Just a moment...", (0, 0, 1000, 800))]
    seq = iter(states + [None])
    attempts = {"n": 0}
    def locate(win):
        attempts["n"] += 1
        return (5, 5)
    w = make_watcher(detect=lambda: next(seq), locate=locate, click=lambda p, win: None)
    w.tick()  # IDLE
    w.tick()  # CLICKED (attempt 1)
    w.tick()  # IDLE (cleared) -> handled=1, attempts reset
    assert w.handled == 1 and w.click_attempts == 0


def test_run_stops_on_circuit_breaker():
    w = make_watcher(detect=lambda: WinInfo(1, "Just a moment...", (0, 0, 1000, 800)),
                     locate=lambda win: (1, 1), click=lambda p, win: None,
                     max_total_clicks=2)
    w.run(sleep=lambda: None)
    assert w.total_clicks == 2
