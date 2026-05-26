from nebula.logger import get_logger
from nebula.utils.constants import INTENT_SYSTEM, INTENT_CHAT
import re

logger = get_logger("IntentParser")

# ================= APP / SYSTEM KEYWORDS =================

SCREENSHOT_WORDS = [
    "take a screenshot", "take screenshot",
    "capture screen", "capture the screen",
    "screenshot", "screen capture"
]

SHUTDOWN_WORDS = ["shutdown", "shut down", "turn off", "power off"]
RESTART_WORDS = ["restart", "reboot", "restart system"]
SLEEP_WORDS = ["sleep mode", "hibernate", "suspend", "go to sleep", "sleep system"]

OPEN_WORDS = ["open", "launch", "start"]
CLOSE_ALL_WORDS = ["close all", "close everything", "close all apps", "quit all", "exit all"]
CLOSE_WORDS = ["close", "exit", "quit", "stop"]

BACKGROUND_WORDS = ["background", "in background", "in the background"]
NEW_WORDS = ["new", "another"]

SEPARATORS = [" and ", ",", " & "]

MINIMIZE_ALL = ["minimize all", "show desktop", "take me home"]
MINIMIZE_APP = ["minimize", "hide"]

VOLUME_UP = ["volume up", "increase volume"]
VOLUME_DOWN = ["volume down", "decrease volume"]
MUTE = ["mute", "silent"]

BRIGHT_UP = ["brightness up"]
BRIGHT_DOWN = ["brightness down"]
BRIGHT_MAX = ["brightness max", "full brightness"]
BRIGHT_LOW = ["brightness low", "dim"]

# ================= FILE COMMANDS =================

FILE_SEARCH_WORDS = ["search file", "find file"]
FOLDER_SEARCH_WORDS = ["search folder", "find folder"]
OPEN_FILE_WORDS = ["open file"]
DELETE_WORDS = ["delete", "remove"]

# ================= BROWSER =================

SEARCH_WORDS = ["search", "find"]
YOUTUBE_WORDS = ["youtube"]
BROWSER_WORDS = ["chrome", "edge"]

# ================= TIME =================

TIME_WORDS = ["what time", "current time", "tell me the time", "what is the time"]
DATE_WORDS = ["date", "today", "what date"]

# Extended timer trigger words — covers natural speech
TIMER_WORDS = [
    "set timer", "start timer", "put the timer",
    "timer for", "set a timer", "start a timer",
    "put a timer", "create a timer"
]

# Extended alarm trigger words
ALARM_WORDS = [
    "set alarm", "set an alarm", "put alarm",
    "wake me up", "alarm for", "create alarm"
]

# Word to number mapping for spoken numbers
WORD_NUMBERS = {
    "one": 1, "two": 2, "three": 3, "four": 4, "five": 5,
    "six": 6, "seven": 7, "eight": 8, "nine": 9, "ten": 10,
    "eleven": 11, "twelve": 12, "thirteen": 13, "fourteen": 14,
    "fifteen": 15, "twenty": 20, "thirty": 30, "forty": 40,
    "forty five": 45, "sixty": 60
}

# ================= FOLDERS =================

KNOWN_FOLDERS = [
    "desktop", "downloads", "documents",
    "pictures", "photos", "videos", "music"
]

# ================= SCREEN =================

SCREEN_SUMMARY = [
    "summarize this page",
    "summarize the page",
    "summarize screen",
    "explain this page",
    "explain screen"
]

SCREEN_QA_TRIGGERS = [
    "what does this say",
    "what is written",
    "what is on screen",
    "what's on screen"
]

EXTRACT_TEXT_WORDS = [
    "extract text",
    "extract the text",
    "extract the words",
    "read the page",
    "read screen text"
]


# ================= HELPERS =================

def _strip_words(text, words):
    for w in words:
        text = text.replace(w, "")
    return " ".join(text.split())

def _extract_apps(text, keywords):
    t = _strip_words(text.lower(), keywords + NEW_WORDS + BACKGROUND_WORDS)
    parts = [t]
    for s in SEPARATORS:
        parts = sum([p.split(s) for p in parts], [])
    return [p.strip() for p in parts if p.strip()]

def _extract_single(text, keywords):
    return _strip_words(text.lower(), keywords + NEW_WORDS + BACKGROUND_WORDS)

def _extract_browser(text):
    for b in BROWSER_WORDS:
        if b in text:
            return b
    return None

def _clean_search_query(text):
    t = text.lower()
    for w in SEARCH_WORDS:
        t = t.replace(w, "")
    for w in YOUTUBE_WORDS + BROWSER_WORDS:
        t = t.replace(w, "")
    t = re.sub(r"\b(in|on)\b", "", t)
    return " ".join(t.split()).strip()

def _extract_number(text):
    # First try digits
    m = re.search(r"\d+", text)
    if m:
        return int(m.group())

    # Then try spoken words like "five", "thirty"
    text_lower = text.lower()
    for word, num in sorted(WORD_NUMBERS.items(), key=lambda x: -len(x[0])):
        if word in text_lower:
            return num

    return None

def _extract_alarm_time(text):
    m = re.search(r"(\d{1,2})(?::(\d{2}))?\s*(am|pm)?", text)
    if not m:
        return None
    h = int(m.group(1))
    mnt = int(m.group(2)) if m.group(2) else 0
    ap = m.group(3)
    if ap == "pm" and h != 12:
        h += 12
    if ap == "am" and h == 12:
        h = 0
    return h, mnt

# ================= PARSER =================

def parse_intent(text: str, lang: str) -> dict:
    t = text.lower().strip()
    logger.info(f"Parsing intent: {t}")

    # ---------- SHUTDOWN ----------
    if any(w in t for w in SHUTDOWN_WORDS):
        return {"intent": INTENT_SYSTEM, "action": "shutdown"}

    # ---------- RESTART ----------
    if any(w in t for w in RESTART_WORDS):
        return {"intent": INTENT_SYSTEM, "action": "restart"}

    # ---------- SLEEP ----------
    if any(w in t for w in SLEEP_WORDS):
        return {"intent": INTENT_SYSTEM, "action": "sleep"}

    # ---------- SCREENSHOT ----------
    if any(w in t for w in SCREENSHOT_WORDS):
        return {"intent": INTENT_SYSTEM, "action": "screenshot"}
    # ---------- SCREEN SUMMARY ----------
    if any(w in t for w in SCREEN_SUMMARY):
        return {"intent": INTENT_SYSTEM, "action": "screen_summary"}

    # ---------- SCREEN QA ----------
    if any(w in t for w in SCREEN_QA_TRIGGERS):
        return {
            "intent": INTENT_SYSTEM,
            "action": "screen_qa",
            "question": text
        }

    # ---------- EXTRACT SCREEN TEXT ----------
    if any(w in t for w in EXTRACT_TEXT_WORDS):
        return {
            "intent": INTENT_SYSTEM,
            "action": "extract_screen_text"
        }

    # ---------- FILE SEARCH ----------
    if any(w in t for w in FILE_SEARCH_WORDS):
        name = _strip_words(t, FILE_SEARCH_WORDS)
        return {"intent": INTENT_SYSTEM, "action": "explorer_search", "query": name}

    if any(w in t for w in FOLDER_SEARCH_WORDS):
        name = _strip_words(t, FOLDER_SEARCH_WORDS)
        return {"intent": INTENT_SYSTEM, "action": "explorer_search", "query": name}

    # ---------- OPEN FOLDER ----------
    if any(w in t for w in OPEN_WORDS):
        for folder in KNOWN_FOLDERS:
            if folder in t:
                return {"intent": INTENT_SYSTEM, "action": "open_folder", "folder": folder}

    # ---------- OPEN FILE ----------
    if any(w in t for w in OPEN_FILE_WORDS) or (
        any(w in t for w in OPEN_WORDS) and re.search(r"\.\w{2,4}\b", t)
    ):
        name = _strip_words(t, OPEN_FILE_WORDS + OPEN_WORDS)
        return {"intent": INTENT_SYSTEM, "action": "open_file", "name": name}

    # ---------- DELETE ----------
    if any(w in t for w in DELETE_WORDS):
        if "folder" in t:
            name = _strip_words(t, DELETE_WORDS + ["folder"])
            return {"intent": INTENT_SYSTEM, "action": "delete_folder", "name": name}
        else:
            name = _strip_words(t, DELETE_WORDS + ["file"])
            return {"intent": INTENT_SYSTEM, "action": "delete_file", "name": name}

    # ---------- TIMER — must be before TIME check ----------
    if any(w in t for w in TIMER_WORDS):
        n = _extract_number(t)
        if n:
            if "minute" in t or "min" in t:
                return {"intent": INTENT_SYSTEM, "action": "set_timer", "seconds": n * 60}
            if "hour" in t:
                return {"intent": INTENT_SYSTEM, "action": "set_timer", "seconds": n * 3600}
            # default to seconds
            return {"intent": INTENT_SYSTEM, "action": "set_timer", "seconds": n}

    # ---------- ALARM — must be before TIME check ----------
    if any(w in t for w in ALARM_WORDS):
        at = _extract_alarm_time(t)
        if at:
            return {"intent": INTENT_SYSTEM, "action": "set_alarm", "hour": at[0], "minute": at[1]}

    # ---------- TIME / DATE — comes AFTER timer/alarm ----------
    if any(w in t for w in TIME_WORDS):
        return {"intent": INTENT_SYSTEM, "action": "get_time"}

    if any(w in t for w in DATE_WORDS):
        return {"intent": INTENT_SYSTEM, "action": "get_date"}

    # ---------- SEARCH ----------
    if any(w in t for w in SEARCH_WORDS) and not any(f in t for f in KNOWN_FOLDERS):
        q = _clean_search_query(t)
        if "youtube" in t:
            return {"intent": INTENT_SYSTEM, "action": "youtube_search", "query": q}
        return {"intent": INTENT_SYSTEM, "action": "google_search", "query": q}

    # ---------- OPEN APP ----------
    for w in OPEN_WORDS:
        if w in t:
            return {
                "intent": INTENT_SYSTEM,
                "action": "open",
                "apps": _extract_apps(t, OPEN_WORDS),
                "new": any(n in t for n in NEW_WORDS),
                "background": any(b in t for b in BACKGROUND_WORDS),
                "browser": _extract_browser(t)
            }

    # ---------- CLOSE ALL — must be before CLOSE check ----------
    if any(w in t for w in CLOSE_ALL_WORDS):
        return {"intent": INTENT_SYSTEM, "action": "close_all"}

    # ---------- CLOSE ----------
    for w in CLOSE_WORDS:
        if w in t:
            return {"intent": INTENT_SYSTEM, "action": "close", "app": _extract_single(t, CLOSE_WORDS)}

    # ---------- MINIMIZE ----------
    if any(m in t for m in MINIMIZE_ALL):
        return {"intent": INTENT_SYSTEM, "action": "minimize_all"}

    if any(m in t for m in MINIMIZE_APP):
        return {"intent": INTENT_SYSTEM, "action": "minimize_app", "app": _extract_single(t, MINIMIZE_APP)}

    # ---------- VOLUME ----------
    if any(v in t for v in VOLUME_UP):
        return {"intent": INTENT_SYSTEM, "action": "volume_up"}

    if any(v in t for v in VOLUME_DOWN):
        return {"intent": INTENT_SYSTEM, "action": "volume_down"}

    if any(v in t for v in MUTE):
        return {"intent": INTENT_SYSTEM, "action": "mute"}

    # ---------- BRIGHTNESS ----------
    if any(b in t for b in BRIGHT_MAX):
        return {"intent": INTENT_SYSTEM, "action": "brightness_max"}

    if any(b in t for b in BRIGHT_UP):
        return {"intent": INTENT_SYSTEM, "action": "brightness_up"}

    if any(b in t for b in BRIGHT_DOWN):
        return {"intent": INTENT_SYSTEM, "action": "brightness_down"}

    if any(b in t for b in BRIGHT_LOW):
        return {"intent": INTENT_SYSTEM, "action": "brightness_low"}

    return {"intent": INTENT_CHAT, "text": text}