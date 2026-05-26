import re
from nebula.logger import get_logger

logger = get_logger("LangDetector")

# Telugu Unicode block
TELUGU_REGEX = re.compile(r"[\u0C00-\u0C7F]")

def detect_language(text: str) -> str:
    """
    Returns:
        'te' for Telugu
        'en' for English (default)
    """
    if not text:
        return "en"

    if TELUGU_REGEX.search(text):
        logger.info("Language detected: Telugu")
        return "te"

    logger.info("Language detected: English")
    return "en"
