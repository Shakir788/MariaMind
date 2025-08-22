import os
import requests
from config import OPENROUTER_API_KEY, HTTP_REFERER

class OpenRouterClient:
    def __init__(self):
        self.api_key = OPENROUTER_API_KEY
        self.base_url = "https://openrouter.ai/api/v1/chat/completions"

    def chat(self, messages, model="openai/gpt-4o-mini"):
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "HTTP-Referer": HTTP_REFERER,
            "X-Title": "Artia AI CLI"
        }

        payload = {
            "model": model,
            "messages": messages,
            "temperature": 0.7   # 🔥 FIXED
        }

        response = requests.post(self.base_url, headers=headers, json=payload)

        if response.status_code != 200:
            raise Exception(f"OpenRouter error {response.status_code}: {response.text}")

        data = response.json()
        return data["choices"][0]["message"]["content"]
