from backend.quote_pricing import WindowJob


def test_volume_discount():
    assert WindowJob(5).price() == 50.0
    assert WindowJob(16).price() == 16 * 9.0
