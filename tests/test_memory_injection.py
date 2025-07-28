"""Verify `vector_used=True` when a prior similar quote exists."""

from backend.agents.quote_agent import QuoteAgent


def test_vector_used_flag():
    # first call stores a quote about 'Bayview'
    QuoteAgent().run("Clean 6 windows in Bayview")

    # second call with similar wording should retrieve memory
    res = QuoteAgent().run("Need a quote to clean 6 windows in Bayview again")

    assert res["vector_used"] is True
