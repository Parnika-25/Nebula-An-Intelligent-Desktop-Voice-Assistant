import os
import threading
import time
import subprocess
from datetime import datetime
from nebula.tts.tts_engine import speak
from nebula.logger import get_logger

logger = get_logger("TimeActions")

# ---------------- TIME / DATE ----------------

def get_time():
    return datetime.now().strftime("%I:%M %p")

def get_date():
    return datetime.now().strftime("%A, %d %B %Y")

# ---------------- TIMER ----------------

def start_timer(seconds: int):
    def timer_thread():
        logger.info(f"Timer started: {seconds}s")
        time.sleep(seconds)

        # Speak the alert
        speak("Hey boss, your timer is done!")

        # Show popup
        try:
            script = (
                f"Add-Type -AssemblyName System.Windows.Forms; "
                f"[System.Windows.Forms.MessageBox]::Show("
                f"'Timer done!', 'Nebula Timer', 'OK', 'Information')"
            )
            subprocess.Popen(
                ["powershell", "-WindowStyle", "Hidden", "-Command", script]
            )
        except Exception as e:
            logger.error(f"Timer popup failed: {e}")

    threading.Thread(target=timer_thread, daemon=True).start()


# ---------------- ALARM ----------------

def set_alarm(hour: int, minute: int):
    time_str = f"{hour:02d}:{minute:02d}"
    logger.info(f"Setting alarm for {time_str}")

    try:
        # Delete old Nebula alarm if exists
        subprocess.run(
            ["schtasks", "/delete", "/tn", "NebulaAlarm", "/f"],
            capture_output=True
        )

        # PowerShell script for the alarm popup
        popup_script = (
            "Add-Type -AssemblyName System.Windows.Forms; "
            f"[System.Windows.Forms.MessageBox]::Show("
            f"'Good morning boss! Alarm time: {time_str}', "
            f"'Nebula Alarm', 'OK', 'Information')"
        )

        # Create a temp ps1 script file to avoid quoting issues
        script_path = os.path.join(os.environ.get("TEMP", "C:\\Temp"), "nebula_alarm.ps1")
        with open(script_path, "w") as f:
            f.write(popup_script)

        # Schedule the task using the ps1 file
        result = subprocess.run([
            "schtasks", "/create", "/f",
            "/tn", "NebulaAlarm",
            "/tr", f"powershell -WindowStyle Hidden -ExecutionPolicy Bypass -File \"{script_path}\"",
            "/sc", "once",
            "/st", time_str
        ], capture_output=True, text=True)

        if result.returncode == 0:
            logger.info(f"Alarm scheduled via Task Scheduler for {time_str}")
        else:
            logger.error(f"Task Scheduler failed: {result.stderr}")
            _thread_alarm(hour, minute)

    except Exception as e:
        logger.error(f"Alarm scheduling failed: {e}")
        _thread_alarm(hour, minute)


def _thread_alarm(hour: int, minute: int):
    """Fallback alarm using a thread if Task Scheduler fails."""
    def alarm_thread():
        logger.info(f"Thread alarm set for {hour}:{minute:02d}")
        while True:
            now = datetime.now()
            if now.hour == hour and now.minute == minute:
                speak(f"Good morning boss! It is {hour}:{minute:02d}")
                try:
                    script = (
                        "Add-Type -AssemblyName System.Windows.Forms; "
                        "[System.Windows.Forms.MessageBox]::Show("
                        f"'Alarm! Time is {hour}:{minute:02d}', "
                        "'Nebula Alarm', 'OK', 'Information')"
                    )
                    subprocess.Popen(
                        ["powershell", "-WindowStyle", "Hidden", "-Command", script]
                    )
                except Exception:
                    pass
                break
            time.sleep(15)

    threading.Thread(target=alarm_thread, daemon=True).start()