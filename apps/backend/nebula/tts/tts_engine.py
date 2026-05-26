import pyttsx3
import threading
from nebula.logger import get_logger

logger = get_logger("TTS")
_lock = threading.Lock()


def speak(text: str):
    if not text or not text.strip():
        return

    with _lock:
        try:
            logger.info(f"TTS → {text}")

            engine = pyttsx3.init()
            engine.setProperty("rate", 170)
            engine.setProperty("volume", 1.0)

            engine.say(text)
            engine.runAndWait()
            engine.stop()

        except Exception as e:
            logger.error(f"TTS Error: {e}")