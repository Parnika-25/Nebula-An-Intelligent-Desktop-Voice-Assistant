import logging
import sys
from logging.handlers import RotatingFileHandler
from .config import LOG_DIR, LOG_FILE, APP_NAME

LOG_DIR.mkdir(parents=True, exist_ok=True)

# ─── Silence noisy third-party libraries ───────────────────────────────────
for noisy in (
    "uvicorn.access", "uvicorn.error", "uvicorn", "fastapi",
    "multipart", "httpx", "asyncio", "httpcore",
    "pyttsx3", "comtypes", "comtypes.client",
):
    logging.getLogger(noisy).setLevel(logging.CRITICAL)


class CleanFormatter(logging.Formatter):
    COLORS = {
        logging.DEBUG:    "\033[90m",
        logging.INFO:     "\033[96m",
        logging.WARNING:  "\033[93m",
        logging.ERROR:    "\033[91m",
        logging.CRITICAL: "\033[95m",
    }
    RESET = "\033[0m"

    def format(self, record):
        color = self.COLORS.get(record.levelno, "")
        msg = super().format(record)
        return f"{color}{msg}{self.RESET}"


def get_logger(name: str = APP_NAME) -> logging.Logger:
    logger = logging.getLogger(name)
    if logger.handlers:
        return logger

    logger.setLevel(logging.INFO)
    logger.propagate = False

    file_fmt    = logging.Formatter("%(asctime)s | %(levelname)s | %(name)s | %(message)s")
    console_fmt = CleanFormatter("%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
                                 datefmt="%H:%M:%S")

    fh = RotatingFileHandler(LOG_FILE, maxBytes=2_000_000, backupCount=5, encoding="utf-8")
    fh.setFormatter(file_fmt)

    ch = logging.StreamHandler(sys.stdout)
    ch.setFormatter(console_fmt)

    logger.addHandler(fh)
    logger.addHandler(ch)
    return logger