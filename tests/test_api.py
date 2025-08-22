import pytest
from models.openrouter import OpenRouterClient

@pytest.mark.skip(reason="integration test — requires real API key")
def test_openrouter_chat():
    cl = OpenRouterClient()
    out = cl.chat([{"role":"user","content":"Say hello in 3 words"}], temperature=0)
    assert isinstance(out, str) and len(out) > 0
