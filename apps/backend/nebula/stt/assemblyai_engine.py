import os
import time
import requests
import sounddevice as sd
import numpy as np
from scipy.io.wavfile import write
from tempfile import NamedTemporaryFile
from nebula.logger import get_logger

logger = get_logger("AssemblyAI")

MIC_DEVICE_INDEX    = 1
ASSEMBLYAI_API_KEY  = "70444a4d0df9474091061f4aa3594d9c"
_UPLOAD_URL         = "https://api.assemblyai.com/v2/upload"
_TRANSCRIPT_URL     = "https://api.assemblyai.com/v2/transcript"
_HEADERS            = {"authorization": ASSEMBLYAI_API_KEY, "content-type": "application/json"}


class AssemblyAIEngine:

    def __init__(self, sample_rate: int = 16000):
        self.sample_rate = sample_rate

    def record_audio(self) -> np.ndarray:
        logger.info("Listening...")
        threshold, silence_limit, max_duration, chunk = 500, 1.2, 20, 1024
        silence_counter = 0.0
        recording_started = False
        frames = []

        try:
            with sd.InputStream(samplerate=self.sample_rate, channels=1,
                                dtype="int16", device=MIC_DEVICE_INDEX) as stream:
                start = time.time()
                while True:
                    data, _ = stream.read(chunk)
                    flat = data.flatten()
                    volume = float(np.abs(flat).mean())

                    if volume > threshold:
                        if not recording_started:
                            logger.info("Speech detected")
                            recording_started = True
                        silence_counter = 0.0
                        frames.append(flat)
                    else:
                        if recording_started:
                            silence_counter += chunk / self.sample_rate
                            frames.append(flat)
                            if silence_counter > silence_limit:
                                logger.info("Silence — stopping")
                                break

                    if time.time() - start > max_duration:
                        break
        except Exception as e:
            logger.error(f"Microphone error: {e}")
            return np.zeros(self.sample_rate // 2, dtype=np.int16)

        if not frames:
            return np.zeros(self.sample_rate // 2, dtype=np.int16)
        return np.concatenate(frames).astype(np.int16)

    def transcribe(self) -> str:
        audio = self.record_audio()
        tmp_path = None
        try:
            with NamedTemporaryFile(suffix=".wav", delete=False) as f:
                tmp_path = f.name
                write(f.name, self.sample_rate, audio)

            with open(tmp_path, "rb") as af:
                up = requests.post(_UPLOAD_URL,
                                   headers={"authorization": ASSEMBLYAI_API_KEY},
                                   data=af, timeout=30)
                up.raise_for_status()
                upload_url = up.json()["upload_url"]

            tr = requests.post(_TRANSCRIPT_URL, headers=_HEADERS,
                               json={"audio_url": upload_url,
                                     "punctuate": True, "format_text": True},
                               timeout=15)
            tr.raise_for_status()
            tid = tr.json()["id"]

            deadline = time.time() + 30
            while time.time() < deadline:
                poll = requests.get(f"{_TRANSCRIPT_URL}/{tid}",
                                    headers=_HEADERS, timeout=10).json()
                if poll["status"] == "completed":
                    text = poll.get("text") or ""
                    logger.info(f"Heard: {text}")
                    return text
                if poll["status"] == "error":
                    logger.error(f"AssemblyAI error: {poll.get('error')}")
                    return ""
                time.sleep(0.8)

            logger.warning("Transcription timed out")
            return ""

        except requests.RequestException as e:
            logger.error(f"Network error: {e}")
            return ""
        except Exception as e:
            logger.error(f"Transcription failed: {e}")
            return ""
        finally:
            if tmp_path:
                try: os.unlink(tmp_path)
                except Exception: pass