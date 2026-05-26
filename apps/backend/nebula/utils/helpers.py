from datetime import datetime

def current_timestamp() -> str:
    return datetime.utcnow().isoformat()

def safe_lower(text: str) -> str:
    if not isinstance(text, str):
        return ""
    return text.strip().lower()
