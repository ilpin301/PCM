from extract import join_dehyphenated, find_running_lines, is_heading, is_scanned


def test_is_heading_levels():
    assert is_heading(20.0, 10.0) == 2   # 2.0x -> h2
    assert is_heading(12.5, 10.0) == 3   # 1.25x -> h3
    assert is_heading(10.5, 10.0) == 0   # ~body -> not a heading


def test_is_heading_zero_body_median_is_safe():
    assert is_heading(12.0, 0.0) == 0


def test_is_scanned_threshold():
    assert is_scanned(20.0) is True
    assert is_scanned(5000.0) is False
    assert is_scanned(100.0) is False    # boundary is exclusive


def test_join_dehyphenated_merges_hyphenated_break():
    lines = ["This is an exam-", "ple of wrapped text."]
    assert join_dehyphenated(lines) == "This is an example of wrapped text."


def test_join_dehyphenated_joins_plain_lines_with_space():
    lines = ["first line", "second line"]
    assert join_dehyphenated(lines) == "first line second line"


def test_join_dehyphenated_single_line():
    assert join_dehyphenated(["just one"]) == "just one"


def test_find_running_lines_detects_repeated_header():
    pages = [
        ["Journal of PCM", "intro text", "1"],
        ["Journal of PCM", "more text", "2"],
        ["Journal of PCM", "conclusion", "3"],
    ]
    running = find_running_lines(pages, min_ratio=0.6)
    assert "Journal of PCM" in running
    assert "1" in running and "2" in running and "3" in running
    assert "intro text" not in running


def test_find_running_lines_ignores_long_repeated_body():
    long_line = "x" * 120
    pages = [[long_line], [long_line]]
    # long, non-digit -> not treated as running furniture
    assert long_line not in find_running_lines(pages, min_ratio=0.5)


from extract import build_body


def test_build_body_emits_headings_and_paragraphs():
    pages = [
        [
            ("Introduction", 20.0),
            ("This sentence is", 10.0),
            ("on two lines.", 10.0),
        ],
    ]
    out = build_body(pages)
    assert "## Introduction" in out
    assert "This sentence is on two lines." in out


def test_build_body_drops_running_furniture():
    pages = [
        [("Journal X", 10.0), ("real body one", 10.0)],
        [("Journal X", 10.0), ("real body two", 10.0)],
    ]
    out = build_body(pages)
    assert "Journal X" not in out
    assert "real body one" in out
    assert "real body two" in out


def test_build_body_dehyphenates_across_lines():
    pages = [[("hyphen-", 10.0), ("ation works", 10.0)]]
    assert "hyphenation works" in build_body(pages)
