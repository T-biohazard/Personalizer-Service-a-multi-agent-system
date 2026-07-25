import os
from pathlib import Path

import sounddevice as sd
import soundfile as sf
from faster_whisper import WhisperModel

MODEL_NAME = os.getenv("WHISPER_MODEL", "small")
STT_MODEL = WhisperModel(MODEL_NAME, device="cpu", compute_type="int8")


def record_audio(seconds: int = 5, path: str = "input.wav") -> str:
    audio = sd.rec(int(seconds * 16000), samplerate=16000, channels=1)
    sd.wait()
    sf.write(path, audio, 16000)
    return path


def transcribe(path: str = "input.wav") -> str:
    segments, _ = STT_MODEL.transcribe(path)
    return " ".join(seg.text for seg in segments)
