from cf_click import WinInfo, _parse_vision_json, locate_checkbox


def win(rect=(100, 200, 1100, 900), hwnd=42):
    return WinInfo(hwnd, "Just a moment...", rect)


def test_parse_accepts_in_bounds_click():
    res = _parse_vision_json('{"click": true, "x": 150, "y": 300}', win())
    assert res == {"click": True, "x": 150, "y": 300}


def test_parse_rejects_out_of_bounds_x():
    res = _parse_vision_json('{"click": true, "x": 5000, "y": 300}', win())
    assert res["click"] is False


def test_parse_handles_click_false():
    assert _parse_vision_json('{"click": false}', win())["click"] is False


def test_parse_strips_code_fence():
    txt = '```json\n{"click": true, "x": 200, "y": 250}\n```'
    res = _parse_vision_json(txt, win())
    assert res == {"click": True, "x": 200, "y": 250}


def test_parse_malformed_returns_click_false():
    assert _parse_vision_json("the checkbox is at...", win())["click"] is False


def test_locate_uses_injected_vision_and_returns_coords(monkeypatch):
    monkeypatch.setattr("cf_click.screenshot_window", lambda win, dest: dest)
    fake_vision = lambda image_path, win: {"click": True, "x": 500, "y": 700}
    coords = locate_checkbox(win(), vision_fn=fake_vision, image_path="x.png")
    assert coords == (500, 700)


def test_locate_returns_none_when_no_checkbox(monkeypatch):
    monkeypatch.setattr("cf_click.screenshot_window", lambda win, dest: dest)
    fake_vision = lambda image_path, win: {"click": False}
    assert locate_checkbox(win(), vision_fn=fake_vision, image_path="x.png") is None
