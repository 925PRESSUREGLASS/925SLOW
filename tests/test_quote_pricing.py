from backend.quote_pricing import WindowJob


def test_basic_price():
    assert WindowJob(5).price() == 50.0


def test_discount_applied():
    assert WindowJob(16).price() == 16 * 9.0
