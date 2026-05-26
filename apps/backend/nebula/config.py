import os
from pathlib import Path

# Base paths
BASE_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = BASE_DIR.parent.parent.parent

# App info
APP_NAME = "Nebula AI"
APP_ENV = os.getenv("NEBULA_ENV", "development")

# Server
HOST = os.getenv("NEBULA_HOST", "127.0.0.1")
PORT = int(os.getenv("NEBULA_PORT", "5055"))

# Languages
SUPPORTED_LANGUAGES = ["en", "te"]
DEFAULT_LANGUAGE = "en"

# Wake system (used later)
WAKE_PHRASE = "nebula wakeup"
WAKE_REPLY = "whatsup boss"

# Logs
LOG_DIR = PROJECT_ROOT / "logs"
LOG_FILE = LOG_DIR / "nebula.log"

# Feature flags (future-proof)
ENABLE_VISION = True
ENABLE_MUSIC = True
ENABLE_BACKGROUND_MODE = True