import os, subprocess, ctypes, time, psutil, json, threading
from pathlib import Path
import win32gui, win32process, pythoncom, wmi
from nebula.logger import get_logger
logger = get_logger("AppActions")

APP_INDEX: dict[str, str] = {}
_index_ready = threading.Event()

APP_ALIASES = {
    "vs code": "code", "vscode": "code", "visual studio code": "code",
    "files": "explorer", "file explorer": "explorer",
}

def _build_app_index():
    for d in [
        Path(os.environ.get("APPDATA","")) / "Microsoft/Windows/Start Menu/Programs",
        Path(os.environ.get("PROGRAMDATA","")) / "Microsoft/Windows/Start Menu/Programs",
    ]:
        if d.exists():
            for lnk in d.rglob("*.lnk"):
                APP_INDEX[lnk.stem.lower()] = str(lnk)

    try:
        r = subprocess.run(["powershell","-Command","Get-StartApps | ConvertTo-Json"],
                           capture_output=True, text=True, shell=True, timeout=10)
        if r.stdout:
            for app in json.loads(r.stdout):
                APP_INDEX[app["Name"].lower()] = f"uwp:{app['AppID']}"
    except Exception: pass

    APP_INDEX.update({"explorer":"explorer.exe","chrome":"chrome","code":"code"})
    _index_ready.set()
    logger.info(f"App index ready — {len(APP_INDEX)} entries")

threading.Thread(target=_build_app_index, daemon=True, name="AppIndexBuilder").start()

def _resolve_alias(app): return APP_ALIASES.get(app.lower(), app.lower())

def _focus_existing(app):
    found = False
    def handler(hwnd, _):
        nonlocal found
        if not win32gui.IsWindowVisible(hwnd): return True
        _, pid = win32process.GetWindowThreadProcessId(hwnd)
        for p in psutil.process_iter(["pid","name"]):
            if p.info["pid"]==pid and app in (p.info["name"] or "").lower():
                win32gui.ShowWindow(hwnd,9)
                try: win32gui.SetForegroundWindow(hwnd)
                except Exception: pass
                found = True; return False
        return True
    try: win32gui.EnumWindows(handler, None)
    except Exception: pass
    return found

def _launch(target, new=False, background=False):
    try:
        if target.startswith("uwp:"):
            subprocess.run(["explorer.exe",f"shell:AppsFolder\\{target[4:]}"],shell=True)
            return True
        if target == "chrome":
            subprocess.Popen(["chrome"]+( ["--new-window"] if new else []),
                             creationflags=0x08000000 if background else 0); return True
        if target == "code":
            subprocess.Popen(["code","-n"] if new else ["code"],
                             creationflags=0x08000000 if background else 0); return True
        if target.endswith((".exe",".lnk")):
            os.startfile(target); return True
    except Exception as e: logger.error(f"Launch failed: {e}")
    return False

def open_app(app, new=False, background=False):
    app = _resolve_alias(app)
    if not _index_ready.is_set(): _index_ready.wait(timeout=6)
    if not new and _focus_existing(app): return True
    for name, target in APP_INDEX.items():
        if app == name or app in name: return _launch(target, new, background)
    logger.warning(f"App not found: {app}"); return False

def close_app(app):
    app = _resolve_alias(app)
    for p in psutil.process_iter(["name"]):
        if p.info["name"] and app in p.info["name"].lower(): p.terminate()
    return True

def close_all_apps():
    PROTECTED = {
        "explorer.exe","svchost.exe","system","registry","smss.exe","csrss.exe",
        "wininit.exe","services.exe","lsass.exe","winlogon.exe","dwm.exe","taskmgr.exe",
        "spoolsv.exe","audiodg.exe","fontdrvhost.exe","sihost.exe","ctfmon.exe",
        "rundll32.exe","searchindexer.exe","runtimebroker.exe","shellexperiencehost.exe",
        "startmenuexperiencehost.exe","textinputhost.exe","securityhealthsystray.exe",
        "searchhost.exe","widgets.exe","msmpeng.exe","nissrv.exe",
        # Terminals — NEVER kill the console Nebula lives in
        "cmd.exe","conhost.exe","powershell.exe","pwsh.exe","windowsterminal.exe","wt.exe",
        # Nebula itself
        "nebula.exe","python.exe","pythonw.exe",
    }
    current_pid = os.getpid()
    logger.info("Closing all user apps...")
    for p in psutil.process_iter(["name","pid"]):
        try:
            name = (p.info["name"] or "").lower()
            if p.info["pid"] == current_pid: continue
            if name not in PROTECTED:
                p.terminate(); logger.info(f"Closed: {name}")
        except (psutil.NoSuchProcess, psutil.AccessDenied): pass
        except Exception as e: logger.error(f"Error closing {name}: {e}")

def minimize_all():
    ctypes.windll.user32.keybd_event(0x5B,0,0,0)
    ctypes.windll.user32.keybd_event(0x44,0,0,0)
    ctypes.windll.user32.keybd_event(0x44,0,2,0)
    ctypes.windll.user32.keybd_event(0x5B,0,2,0)

def minimize_app(app):
    app = _resolve_alias(app)
    def handler(hwnd,_):
        _,pid = win32process.GetWindowThreadProcessId(hwnd)
        for p in psutil.process_iter(["pid","name"]):
            if p.info["pid"]==pid and app in (p.info["name"] or "").lower():
                win32gui.ShowWindow(hwnd,6); return False
        return True
    try: win32gui.EnumWindows(handler, None)
    except Exception: pass
    return True

VK_VOLUME_UP=0xAF; VK_VOLUME_DOWN=0xAE; VK_VOLUME_MUTE=0xAD

def _press(k,n=1):
    for _ in range(n):
        ctypes.windll.user32.keybd_event(k,0,0,0)
        ctypes.windll.user32.keybd_event(k,0,2,0)
        time.sleep(0.05)

def volume_up():   _press(VK_VOLUME_UP,5)
def volume_down(): _press(VK_VOLUME_DOWN,5)
def mute_volume(): _press(VK_VOLUME_MUTE,1)

def _safe_wmi():
    try: pythoncom.CoInitialize(); return wmi.WMI(namespace="wmi")
    except Exception: return None

def brightness_up():
    c=_safe_wmi()
    if not c: return
    try: v=c.WmiMonitorBrightness()[0].CurrentBrightness; c.WmiMonitorBrightnessMethods()[0].WmiSetBrightness(0,min(100,v+10))
    except Exception: pass

def brightness_down():
    c=_safe_wmi()
    if not c: return
    try: v=c.WmiMonitorBrightness()[0].CurrentBrightness; c.WmiMonitorBrightnessMethods()[0].WmiSetBrightness(0,max(0,v-10))
    except Exception: pass

def brightness_max():
    c=_safe_wmi()
    if not c: return
    try: c.WmiMonitorBrightnessMethods()[0].WmiSetBrightness(0,100)
    except Exception: pass

def brightness_low():
    c=_safe_wmi()
    if not c: return
    try: c.WmiMonitorBrightnessMethods()[0].WmiSetBrightness(0,20)
    except Exception: pass

def shutdown_system(): os.system("shutdown /s /t 5")
def restart_system():  os.system("shutdown /r /t 5")