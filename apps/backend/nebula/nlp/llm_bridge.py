import requests
from nebula.logger import get_logger

logger = get_logger("LLMBridge")

GEMINI_API_KEY = "AIzaSyC6eCfmyX6GDJUyjHHuI3bntuQWFW5ZisI"

GEMINI_URL = (
    "https://generativelanguage.googleapis.com/v1beta/models/"
    "gemini-2.0-flash:generateContent?key=" + GEMINI_API_KEY
)

HEADERS = {"Content-Type": "application/json"}


def _call_gemini(prompt: str) -> str:
    """Send a prompt to Gemini and return the response text."""
    try:
        body = {
            "contents": [
                {
                    "parts": [{"text": prompt}]
                }
            ],
            "generationConfig": {
                "maxOutputTokens": 150,
                "temperature": 0.7
            }
        }

        response = requests.post(GEMINI_URL, headers=HEADERS, json=body, timeout=10)

        if response.status_code == 429:
            logger.error("Gemini quota exceeded — try again in a minute")
            return ""

        if response.status_code != 200:
            logger.error(f"Gemini API error: {response.status_code} {response.text}")
            return ""

        data = response.json()
        text = data["candidates"][0]["content"]["parts"][0]["text"]
        return text.strip()

    except Exception as e:
        logger.error(f"Gemini error: {e}")
        return ""


def process_with_llm(payload: dict) -> dict:
    """Handles screen summary, screen QA and chitchat."""

    task = payload.get("task")

    # ================= SCREEN SUMMARY =================
    if task == "summarize_screen":
        prompt = (
            "Summarize this screen text in simple words in 3 short lines. "
            "Be concise and clear:\n\n"
            f"{payload['content'][:800]}"
        )
        response = _call_gemini(prompt)
        return {"response": response}

    # ================= SCREEN QA =================
    elif task == "screen_qa":
        prompt = (
            f"Based only on this screen text:\n\n"
            f"{payload['content'][:800]}\n\n"
            f"Answer this question in 1-2 sentences:\n{payload['question']}"
        )
        response = _call_gemini(prompt)
        return {"response": response}

    # ================= CHITCHAT =================
    elif task == "chitchat":
        prompt = (
            "You are Nebula, a smart and friendly AI voice assistant. "
            "Reply in 1-2 short sentences only. Be helpful, friendly and natural. "
            "Do not use bullet points or markdown. Just speak naturally.\n\n"
            f"User: {payload['text']}\nNebula:"
        )
        response = _call_gemini(prompt)
        return {"response": response}

    return {"response": ""}