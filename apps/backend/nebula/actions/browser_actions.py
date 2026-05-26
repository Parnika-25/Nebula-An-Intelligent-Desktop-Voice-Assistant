#browser actions
import subprocess
import webbrowser
from urllib.parse import quote_plus
from nebula.logger import get_logger

logger = get_logger("BrowserActions")

BROWSERS = {
    "chrome": r"C:\Program Files\Google\Chrome\Application\chrome.exe",
    "edge": r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
}

# ================= CORE =================

def open_site(url, browser=None, background=False, new_window=False):
    url = url.strip()
    if not url.startswith(("http://", "https://")):
        url = "https://" + url

    logger.info(f"Open site: {url} browser={browser}")

    try:
        if browser in BROWSERS:
            cmd = [BROWSERS[browser]]

            # Important: reuse window, not new
            if new_window:
                cmd.append("--new-window")

            cmd.append(url)

            subprocess.Popen(
                cmd,
                creationflags=0x08000000 if background else 0
            )
        else:
            webbrowser.open(url, new=2, autoraise=not background)

        return True
    except Exception as e:
        logger.error(f"Browser error: {e}")
        return False


# ================= SEARCH =================

def google_search(query):
    q = quote_plus(query)
    return open_site(f"https://www.google.com/search?q={q}")

def youtube_search(query):
    q = quote_plus(query)
    return open_site(f"https://www.youtube.com/results?search_query={q}")
