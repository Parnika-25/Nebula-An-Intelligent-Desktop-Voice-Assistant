from fastapi import APIRouter
from nebula.vision.screenshot import capture_screen
from nebula.vision.screen_reader import read_text_from_image
from nebula.vision.vision_ai import describe_screen

router = APIRouter(prefix="/screen")

@router.get("/capture")
def capture():
    path = capture_screen()
    return {"status": "ok", "path": path}

@router.get("/describe")
def describe():
    path = capture_screen()
    text = read_text_from_image(path)
    description = describe_screen(text)
    return {
        "status": "ok",
        "description": description
    }
