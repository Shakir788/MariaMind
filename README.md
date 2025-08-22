# Artia AI (Python CLI)

## Quick Start
```bash
python -m venv .venv
# Windows:
.venv\Scripts\activate
# Mac/Linux:
. .venv/bin/activate

pip install -r requirements.txt
cp .env.example .env
# paste your OpenRouter key in .env
python main.py
```

**CLI commands**: `voice` (toggle), `prefs name=YourName tone=gentle`, `quit`

### Notes
- Windows PyAudio tip:
  ```bash
  pip install pipwin
  pipwin install pyaudio
  ```
- Change model via `.env` -> `DEFAULT_MODEL` (e.g., `anthropic/claude-3.5-sonnet`, `meta-llama/llama-3.1-8b-instruct`).
- Voice languages for TTS: change `voice.speak(..., lang="en")` to `"hi"` (Hindi), `"tl"` (Tagalog), etc.
