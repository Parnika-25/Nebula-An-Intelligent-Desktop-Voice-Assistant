#automation
import pyautogui
from nebula.logger import get_logger

logger = get_logger("Automation")

def click(x: int, y: int):
    logger.info(f"Mouse click at ({x},{y})")
    pyautogui.click(x, y)

def type_text(text: str):
    logger.info(f"Typing text: {text}")
    pyautogui.write(text, interval=0.05)
