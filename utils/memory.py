import os
import json
from config import CHAT_HISTORY_PATH, USER_PREFS_PATH

class Memory:
    def __init__(self):
        self.chat_history = {"messages": []}
        self.user_prefs = {}
        self._ensure_files_exist()

    def _ensure_files_exist(self):
        # Ensure chat history file exists
        if not os.path.exists(CHAT_HISTORY_PATH):
            with open(CHAT_HISTORY_PATH, "w", encoding="utf-8") as f:
                json.dump({"messages": []}, f)

        # Ensure user prefs file exists
        if not os.path.exists(USER_PREFS_PATH):
            with open(USER_PREFS_PATH, "w", encoding="utf-8") as f:
                json.dump({}, f)

    # ---------- CHAT HISTORY ----------
    def add_message(self, role, content):
        self.chat_history["messages"].append({"role": role, "content": content})
        self._save_chat_history()

    def get_chat_history(self):
        return self.chat_history.get("messages", [])

    def load_history(self):
        try:
            with open(CHAT_HISTORY_PATH, "r", encoding="utf-8") as f:
                self.chat_history = json.load(f)
        except:
            self.chat_history = {"messages": []}
        return self.get_chat_history()

    def _save_chat_history(self):
        with open(CHAT_HISTORY_PATH, "w", encoding="utf-8") as f:
            json.dump(self.chat_history, f, indent=2)

    def clear_history(self):
        self.chat_history = {"messages": []}
        self._save_chat_history()

    # ---------- USER PREFS ----------
    def save_prefs(self, prefs):
        self.user_prefs = prefs
        with open(USER_PREFS_PATH, "w", encoding="utf-8") as f:
            json.dump(prefs, f, indent=2)

    def load_prefs(self):
        try:
            with open(USER_PREFS_PATH, "r", encoding="utf-8") as f:
                self.user_prefs = json.load(f)
        except:
            self.user_prefs = {}
        return self.user_prefs

    # ---------- SUMMARY ----------
    def summarize_long_term(self):
        """
        Returns a simple summary of the chat history
        (You can make this smarter later)
        """
        messages = self.get_chat_history()
        if not messages:
            return "No prior conversation."
        last_messages = [msg["content"] for msg in messages[-5:]]
        return "Summary of recent chats: " + " | ".join(last_messages)
