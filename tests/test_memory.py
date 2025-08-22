from utils.memory import Memory

def test_memory_roundtrip(tmp_path, monkeypatch):
    m = Memory()
    m.append('user', 'hi')
    m.append('assistant', 'hello')
    hist = m.load_history()
    assert len(hist) >= 2
