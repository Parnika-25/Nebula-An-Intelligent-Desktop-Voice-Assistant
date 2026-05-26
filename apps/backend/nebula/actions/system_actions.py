import os
import subprocess
from nebula.logger import get_logger

logger = get_logger("SystemActions")

def open_app(app_name: str):
    try:
        logger.info(f"Opening application: {app_name}")
        os.startfile(app_name)
    except Exception as e:
        logger.error(f"Failed to open app {app_name}: {e}")

def shutdown():
    logger.warning("System shutdown requested")
    subprocess.call(["shutdown", "/s", "/t", "5"])

def restart():
    logger.warning("System restart requested")
    subprocess.call(["shutdown", "/r", "/t", "5"])
