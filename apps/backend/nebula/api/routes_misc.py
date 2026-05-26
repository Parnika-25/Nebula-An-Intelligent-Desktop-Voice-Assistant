from fastapi import APIRouter
from pydantic import BaseModel
from nebula.config import APP_NAME
from nebula.tts.tts_engine import speak

router = APIRouter()

class SpeakRequest(BaseModel):
    text: str

@router.get("/status")
def status():
    return {
        "status": "ok",
        "app": APP_NAME
    }

@router.post("/speak")
def speak_text(req: SpeakRequest):
    speak(req.text)
    return {"status": "spoken"}
