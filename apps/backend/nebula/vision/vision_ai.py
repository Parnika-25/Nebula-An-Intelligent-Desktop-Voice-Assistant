import re
import pyperclip

from nebula.logger import get_logger
from nebula.nlp.llm_bridge import process_with_llm

logger = get_logger("VisionAI")


# ===============================
# TEXT CLEANING
# ===============================
def describe_screen(text: str):
    return summarize_ai(text)


def clean_text(text: str) -> str:
    text = re.sub(r"\s+", " ", text)
    return text.strip()


# ===============================
# LOCAL SUMMARY (FAST FALLBACK)
# ===============================

def summarize_local(text: str, max_sentences: int = 4):

    if not text:
        return "I cannot detect readable content."

    text = clean_text(text)
    sentences = re.split(r'(?<=[.!?]) +', text)

    summary = " ".join(sentences[:max_sentences])

    if len(summary) > 1000:
        summary = summary[:1000]

    return summary


# ===============================
# AI SUMMARY (OLLAMA)
# ===============================

def summarize_ai(text: str):

    if not text:
        return "I cannot see readable content."

    payload = {
        "task": "summarize_screen",
        "content": text[:4000]
    }

    response = process_with_llm(payload)

    ai_text = response.get("response")

    if not ai_text:
        return summarize_local(text)

    return ai_text


# ===============================
# SCREEN QA (OLLAMA)
# ===============================

def answer_question(text: str, question: str):

    if not text:
        return "I cannot see readable content."

    payload = {
        "task": "screen_qa",
        "content": text[:4000],
        "question": question
    }

    response = process_with_llm(payload)

    return response.get("response", "I cannot answer that.")


# ===============================
# CLIPBOARD COPY
# ===============================

def copy_to_clipboard(text: str):
    try:
        pyperclip.copy(text)
        return True
    except Exception:
        return False
