import os
from pathlib import Path

from dotenv import load_dotenv
from groq import Groq

BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / ".env")

client = Groq(api_key=os.environ["GROQ_API_KEY"])


async def ask_llm(prompt: str, system: str = "", model: str = "llama-3.1-8b-instant") -> str:
    messages = []
    if system:
        messages.append({"role": "system", "content": system})
    messages.append({"role": "user", "content": prompt})

    resp = client.chat.completions.create(model=model, messages=messages)
    return resp.choices[0].message.content