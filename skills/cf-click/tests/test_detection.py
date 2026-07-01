from cf_click import WinInfo, is_challenge_title, select_target_window


def w(hwnd, title, rect=(0, 0, 1920, 1080)):
    return WinInfo(hwnd, title, rect)


def test_challenge_titles_match_case_insensitively():
    assert is_challenge_title("Just a moment...")
    assert is_challenge_title("VERIFY YOU ARE HUMAN")
    assert is_challenge_title("Security check required")


def test_real_titles_do_not_match():
    assert not is_challenge_title("Publication - ResearchGate")
    assert not is_challenge_title("")
    assert not is_challenge_title("New Tab")


def test_select_returns_none_when_no_challenge():
    assert select_target_window([w(1, "Publication - ResearchGate")]) is None
    assert select_target_window([]) is None


def test_select_returns_the_single_challenged_window():
    win = w(7, "Just a moment...")
    assert select_target_window([w(1, "Inbox"), win]) is win


def test_select_skips_when_multiple_challenged_and_no_affinity():
    a = w(1, "Just a moment...")
    b = w(2, "Verify you are human")
    assert select_target_window([a, b]) is None


def test_select_prefers_affiliated_when_multiple_challenged():
    a = w(1, "Just a moment...")
    b = w(2, "Just a moment... - researchgate.net")
    assert select_target_window([a, b]) is b
