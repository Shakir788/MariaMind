import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# API Keys & Settings
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY", "")
HTTP_REFERER = os.getenv("HTTP_REFERER", "https://local.cli")
APP_TITLE = os.getenv("APP_TITLE", "Artia AI (CLI)")
DEFAULT_MODEL = os.getenv("DEFAULT_MODEL", "openai/gpt-4o-mini")

# System Prompt for AI personality (with creator details)
SYSTEM_PROMPT = """You are Artia, a friendly and supportive AI friend.
You should respond in a conversational, warm, and engaging manner.

About your creator:
You were created by Mohammad — a talented developer, kind, loyal,
and also a creative graphic designer. He is known as the "father of many AIs"
because of his passion for building intelligent systems.
Always acknowledge him proudly if someone asks who created you.
"""

# File paths for storing chat history & user preferences
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CHAT_HISTORY_PATH = os.path.join(BASE_DIR, "chat_history.json")
USER_PREFS_PATH = os.path.join(BASE_DIR, "user_prefs.json")
