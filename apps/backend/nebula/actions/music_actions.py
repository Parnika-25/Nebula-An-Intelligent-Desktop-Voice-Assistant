from pynput.keyboard import Controller, Key
from nebula.logger import get_logger

logger = get_logger("MusicActions")
keyboard = Controller()

def play_pause():   
    logger.info("Music: Play/Pause")
    keyboard.press(Key.media_play_pause)
    keyboard.release(Key.media_play_pause)

def next_track():
    logger.info("Music: Next track")
    keyboard.press(Key.media_next)
    keyboard.release(Key.media_next)

def previous_track():
    logger.info("Music: Previous track")
    keyboard.press(Key.media_previous)
    keyboard.release(Key.media_previous)

def volume_up():
    logger.info("Volume up")
    keyboard.press(Key.media_volume_up)
    keyboard.release(Key.media_volume_up)

def volume_down():
    logger.info("Volume down")
    keyboard.press(Key.media_volume_down)
    keyboard.release(Key.media_volume_down)

def mute():
    logger.info("Volume mute")
    keyboard.press(Key.media_volume_mute)
    keyboard.release(Key.media_volume_mute)
