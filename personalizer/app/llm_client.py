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
client = Groq(api_key=api_key) if Groq and api_key else None


async def ask_llm(prompt: str, system: str = "", model: str = "llama-3.1-8b-instant") -> str:
    if client is None:
        raise RuntimeError("Groq client is not available; set GROQ_API_KEY to enable LLM recommendations")

    messages = []
    if system:
        messages.append({"role": "system", "content": system})
    messages.append({"role": "user", "content": prompt})

    resp = client.chat.completions.create(model=model, messages=messages)
    return resp.choices[0].message.content