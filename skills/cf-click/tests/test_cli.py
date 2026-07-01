import json
from pathlib import Path

import cf_click


def test_parse_summary_counts_events(tmp_path, monkeypatch):
    log = tmp_path / "watcher.log"
    log.write_text("\n".join([
        json.dumps({"ts": "t1", "event": "CLICKED", "x": 1, "y": 2}),
        json.dumps({"ts": "t2", "event": "CLICKED"}),
        json.dumps({"ts": "t3", "event": "CLEARED"}),
        json.dumps({"ts": "t4", "event": "GIVE_UP"}),
        "not json",
    ]) + "\n", encoding="utf-8")
    monkeypatch.setattr(cf_click, "LOGFILE", log)
    assert cf_click._summary() == "clicks=2 cleared=1 gave_up=1 last=t4"


def test_start_writes_pid_and_detaches(tmp_path, monkeypatch):
    rundir = tmp_path / "run"
    monkeypatch.setattr(cf_click, "RUNDIR", rundir)
    monkeypatch.setattr(cf_click, "PIDFILE", rundir / "watcher.pid")
    monkeypatch.setattr(cf_click, "LOGFILE", rundir / "watcher.log")

    class FakeProc:
        pid = 4242
    captured = {}

    def fake_popen(cmd, **kw):
        captured["cmd"] = cmd
        captured["creationflags"] = kw.get("creationflags")
        return FakeProc()
    monkeypatch.setattr(cf_click.subprocess, "Popen", fake_popen)

    cf_click.cmd_start()
    assert (rundir / "watcher.pid").read_text() == "4242"
    assert "watch" in captured["cmd"]
    assert captured["creationflags"] & 0x00000008  # DETACHED_PROCESS bit set


def test_start_refuses_if_already_running(tmp_path, monkeypatch):
    rundir = tmp_path / "run"
    rundir.mkdir()
    (rundir / "watcher.pid").write_text("999")
    monkeypatch.setattr(cf_click, "RUNDIR", rundir)
    monkeypatch.setattr(cf_click, "PIDFILE", rundir / "watcher.pid")
    monkeypatch.setattr(cf_click, "_pid_alive", lambda pid: True)
    monkeypatch.setattr(cf_click.subprocess, "Popen", lambda *a, **k: None)  # must not be called
    cf_click.cmd_start()  # should return without spawning
    assert (rundir / "watcher.pid").read_text() == "999"


def test_stop_kills_and_removes_pidfile(tmp_path, monkeypatch):
    rundir = tmp_path / "run"
    rundir.mkdir()
    (rundir / "watcher.pid").write_text("12345")
    monkeypatch.setattr(cf_click, "RUNDIR", rundir)
    monkeypatch.setattr(cf_click, "PIDFILE", rundir / "watcher.pid")
    killed = {}
    monkeypatch.setattr(cf_click.subprocess, "run",
                        lambda cmd, **k: killed.setdefault("cmd", cmd) or type("R", (), {"stdout": ""})())
    cf_click.cmd_stop()
    assert not (rundir / "watcher.pid").exists()
    assert "12345" in killed["cmd"]


def test_self_test_does_not_click_and_reports(monkeypatch, capsys, tmp_path):
    monkeypatch.setattr(cf_click, "screenshot_window", lambda win, dest: dest)
    monkeypatch.setattr(cf_click, "humanized_click",
                        lambda p, win: (_ for _ in ()).throw(AssertionError("must not click")))
    fake_vision = lambda image_path, win: {"click": True, "x": 10, "y": 20}
    monkeypatch.setattr(cf_click, "locate_checkbox",
                        lambda win, vision_fn=fake_vision, image_path=None: (10, 20))
    cf_click.cmd_self_test(str(tmp_path / "shot.png"))
    out = capsys.readouterr().out
    assert "(10, 20)" in out
