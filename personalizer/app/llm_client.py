import base64
import os
from pathlib import Path

from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / ".env")

try:
    from groq import Groq
except ImportError:  # pragma: no cover - optional dependency in local dev
    Groq = None

api_key = os.getenv("GROQ_API_KEY")
client = None
if Groq and api_key:
    try:
        client = Groq(api_key=api_key)
    except Exception:  # pragma: no cover - fallback for environments with incomplete optional deps
        client = None


async def ask_llm(prompt: str, system: str = "", model: str = "llama-3.1-8b-instant") -> str:
    if client is None:
        raise RuntimeError("Groq client is not available; set GROQ_API_KEY to enable LLM recommendations")

    messages = []
    if system:
        messages.append({"role": "system", "content": system})
    messages.append({"role": "user", "content": prompt})

    resp = client.chat.completions.create(model=model, messages=messages)
    return resp.choices[0].message.content


async def ask_vision(image_bytes: bytes, prompt: str, model: str = "llama-3.2-11b-vision-preview") -> str:
    if client is None:
        raise RuntimeError("Groq client is not available; set GROQ_API_KEY to enable vision analysis")

    encoded = base64.b64encode(image_bytes).decode("utf-8")
    resp = client.chat.completions.create(
        model=model,
        messages=[
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": prompt},
                    {"type": "image_url", "image_url": {"url": f"data:image/png;base64,{encoded}"}},
                ],
            }
        ],
    )
    return resp.choices[0].message.content