from fastapi import APIRouter
from pydantic import BaseModel
from nebula.nlp.lang_detector import detect_language
from nebula.nlp.intent_parser import parse_intent

router = APIRouter(prefix="/intent")

class IntentRequest(BaseModel):
    text: str

@router.post("/process")
def process_intent(req: IntentRequest):
    lang = detect_language(req.text)
    intent_data = parse_intent(req.text, lang)
    return {
        "status": "ok",
        "intent": intent_data
    }
