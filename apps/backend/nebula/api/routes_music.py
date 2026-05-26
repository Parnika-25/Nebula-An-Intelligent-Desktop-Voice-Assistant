from fastapi import APIRouter
from pydantic import BaseModel
from nebula.actions import music_actions

router = APIRouter(prefix="/music")

class MusicRequest(BaseModel):
    action: str  # play, next, prev, volup, voldown, mute

@router.post("/control")
def music_control(req: MusicRequest):
    action = req.action.lower()

    if action == "play":
        music_actions.play_pause()
    elif action == "next":
        music_actions.next_track()
    elif action == "prev":
        music_actions.previous_track()
    elif action == "volup":
        music_actions.volume_up()
    elif action == "voldown":
        music_actions.volume_down()
    elif action == "mute":
        music_actions.mute()
    else:
        return {"status": "error", "message": "Unknown action"}

    return {"status": "ok", "action": action}
