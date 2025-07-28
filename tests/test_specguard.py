from backend.core.spec_guard import grade


def test_specguard_perfect():
    msg = "> $100.00 to clean 10 windows in Perth\n> — QuoteGPT, 2025\nRationale: sample."
    res = grade(msg)
    assert res.score == 1.0
    assert not res.violations


def test_specguard_violations():
    res = grade("No markdown")
    assert res.score < 0.9
    assert any(v.startswith("missing blockquote") for v in res.violations)
