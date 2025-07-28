from backend.agents.quote_agent import QuoteAgent
from backend.agents.memory_agent import MemoryAgent


def test_memory_roundtrip():
    # generate & store two quotes
    QuoteAgent().run("Clean 4 windows in Suburbia")
    QuoteAgent().run("Clean 2 windows in Riverside")

    res = MemoryAgent.run("windows in Riverside")
    assert res  # not empty
    # top result should mention Riverside quote
    assert any("Riverside" in m["snippet"] for m in res)
