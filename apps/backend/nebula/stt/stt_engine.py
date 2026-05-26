import json
import queue
from pathlib import Path

import numpy as np
import sounddevice as sd
from vosk import Model, KaldiRecognizer

from nebula.logger import get_logger

logger = get_logger("VoskSTT")


class STTEngine:
    def __init__(self):
        # -------------------------------------------------
        # Model path (UPDATED FOR vosk-model-en-us-0.22)
        # -------------------------------------------------
        model_path = Path(__file__).parent / "models" / "vosk-model-en-us-0.22"

        if not model_path.exists():
            raise RuntimeError(
                f"Vosk model not found at: {model_path}\n"
                "Make sure the folder contains am/, conf/, graph/, ivector/"
            )

        logger.info(f"Loading Vosk model from: {model_path}")
        self.model = Model(str(model_path))

        # -------------------------------------------------
        # Audio configuration
        # -------------------------------------------------
        self.sample_rate = 16000
        self.block_size = 16000  # 1 second of audio (better accuracy)

        self.recognizer = KaldiRecognizer(self.model, self.sample_rate)
        self.recognizer.SetWords(True)

        self.audio_queue = queue.Queue()

    # -------------------------------------------------
    # Audio callback (sounddevice)
    # -------------------------------------------------
    def _callback(self, indata, frames, time, status):
        if status:
            logger.warning(status)

        # Convert audio to bytes
        self.audio_queue.put(bytes(indata))

    # -------------------------------------------------
    # Start listening
    # -------------------------------------------------
    def listen(self, on_text):
        logger.info("Microphone stream started (Vosk)")

        with sd.RawInputStream(
            samplerate=self.sample_rate,
            blocksize=self.block_size,
            dtype="int16",
            channels=1,
            callback=self._callback,
        ):
            while True:
                data = self.audio_queue.get()

                if self.recognizer.AcceptWaveform(data):
                    result = json.loads(self.recognizer.Result())
                    text = result.get("text", "").strip()

                    if text:
                        logger.info(f"Recognized → {text}")
                        on_text(text)
