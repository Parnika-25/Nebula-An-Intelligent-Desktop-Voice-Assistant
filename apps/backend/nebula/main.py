# nebula/main.py
import sys
import os
import logging
import winreg
import threading

# ── Silence everything BEFORE any imports ──────────────────────────────────
logging.getLogger("uvicorn").setLevel(logging.CRITICAL)
logging.getLogger("uvicorn.access").setLevel(logging.CRITICAL)
logging.getLogger("uvicorn.error").setLevel(logging.CRITICAL)
logging.getLogger("fastapi").setLevel(logging.CRITICAL)
logging.getLogger("multipart").setLevel(logging.CRITICAL)
logging.getLogger("pyttsx3").setLevel(logging.CRITICAL)
logging.getLogger("comtypes").setLevel(logging.CRITICAL)

import uvicorn
from fastapi import FastAPI
from contextlib import asynccontextmanager

from nebula.config import APP_NAME, HOST, PORT
from nebula.logger import get_logger
from nebula.wake.wake_listener import WakeListener

from nebula.api import (
    routes_misc,
    routes_music,
    routes_system,
    routes_screen,
    routes_intent,
)

logger = get_logger()
wake_listener = WakeListener()


# ───────────────────────────────────────────────────────────────────────────
# STARTUP REGISTRATION
# ───────────────────────────────────────────────────────────────────────────

def add_to_startup():
    """Register Nebula to auto-start with Windows (EXE only)."""
    try:
        if not getattr(sys, "frozen", False):
            return

        exe_path = sys.executable

        try:
            key = winreg.OpenKey(
                winreg.HKEY_LOCAL_MACHINE,
                r"Software\Microsoft\Windows\CurrentVersion\Run",
                0,
                winreg.KEY_SET_VALUE,
            )
        except PermissionError:
            key = winreg.OpenKey(
                winreg.HKEY_CURRENT_USER,
                r"Software\Microsoft\Windows\CurrentVersion\Run",
                0,
                winreg.KEY_SET_VALUE,
            )

        winreg.SetValueEx(key, "Nebula", 0, winreg.REG_SZ, exe_path)
        winreg.CloseKey(key)
        logger.info("Nebula registered for auto-startup")

    except Exception as e:
        logger.warning(f"Startup registration skipped: {e}")


add_to_startup()


# ───────────────────────────────────────────────────────────────────────────
# BANNER
# ───────────────────────────────────────────────────────────────────────────

BANNER = r"""
  _   _      _           _
 | \ | | ___| |__  _   _| | __ _
 |  \| |/ _ \ '_ \| | | | |/ _` |
 | |\  |  __/ |_) | |_| | | (_| |
 |_| \_|\___|_.__/ \__,_|_|\__,_|

  AI Voice Assistant  |  http://{}:{}
  Say "Nebula wakeup" to begin
  Press Ctrl+C to stop
""".format(HOST, PORT)


# ───────────────────────────────────────────────────────────────────────────
# FASTAPI APP
# ───────────────────────────────────────────────────────────────────────────

@asynccontextmanager
async def lifespan(app: FastAPI):
    print(BANNER)
    logger.info("Nebula backend starting...")
    wake_listener.start()
    yield
    logger.info("Nebula backend shutting down...")
    wake_listener.stop()


app = FastAPI(title=APP_NAME, lifespan=lifespan)

app.include_router(routes_misc.router)
app.include_router(routes_music.router)
app.include_router(routes_system.router)
app.include_router(routes_screen.router)
app.include_router(routes_intent.router)


if __name__ == "__main__":
    uvicorn.run(
        app,
        host=HOST,
        port=PORT,
        reload=False,
        log_level="critical",
        access_log=False,
    )