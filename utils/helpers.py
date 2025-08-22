from datetime import datetime
from typing import List, Dict

ISO = "%Y-%m-%dT%H:%M:%S"

def now_iso() -> str:
    return datetime.utcnow().strftime(ISO)

def clamp_history(history: List[Dict], max_turns: int = 20) -> List[Dict]:
    return history[-max_turns:]
