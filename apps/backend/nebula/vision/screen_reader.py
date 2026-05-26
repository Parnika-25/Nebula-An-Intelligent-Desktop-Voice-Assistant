import pytesseract
from PIL import Image, ImageFilter, ImageOps
import numpy as np
import re

from nebula.logger import get_logger

logger = get_logger("ScreenReader")

pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"


# ======================================================
# IMAGE PREPROCESSING
# ======================================================

def _preprocess(image: Image.Image) -> Image.Image:
    image = image.convert("L")
    image = ImageOps.autocontrast(image)
    image = image.filter(ImageFilter.SHARPEN)
    return image


# ======================================================
# DETECT MAIN TEXT REGION USING OCR BOX DATA
# ======================================================

def _detect_text_region(image: Image.Image):

    data = pytesseract.image_to_data(
        image,
        output_type=pytesseract.Output.DICT,
        config="--oem 3 --psm 6"
    )

    boxes = []

    for i in range(len(data["text"])):
        text = data["text"][i].strip()
        if len(text) > 3:  # ignore small UI junk
            x = data["left"][i]
            y = data["top"][i]
            w = data["width"][i]
            h = data["height"][i]
            boxes.append((x, y, x + w, y + h))

    if not boxes:
        return image  # fallback

    xs = [b[0] for b in boxes]
    ys = [b[1] for b in boxes]
    x2s = [b[2] for b in boxes]
    y2s = [b[3] for b in boxes]

    min_x = max(min(xs) - 20, 0)
    min_y = max(min(ys) - 20, 0)
    max_x = min(max(x2s) + 20, image.width)
    max_y = min(max(y2s) + 20, image.height)

    cropped = image.crop((min_x, min_y, max_x, max_y))

    return cropped


# ======================================================
# CLEAN TEXT
# ======================================================

def _clean_text(text: str) -> str:
    text = re.sub(r"\s+", " ", text)
    text = re.sub(r"\b[a-zA-Z]{1,2}\b", "", text)
    return text.strip()


# ======================================================
# MAIN FUNCTION
# ======================================================

def read_text_from_image(image_path: str) -> str:

    try:
        image = Image.open(image_path)

        # preprocess
        image = _preprocess(image)

        # detect main text region
        content_region = _detect_text_region(image)

        # run OCR again only on content
        final_text = pytesseract.image_to_string(
            content_region,
            config="--oem 3 --psm 6"
        )

        cleaned = _clean_text(final_text)

        logger.info("Structured text extracted from screen")
        return cleaned

    except Exception as e:
        logger.error(f"OCR failed: {e}")
        return ""
