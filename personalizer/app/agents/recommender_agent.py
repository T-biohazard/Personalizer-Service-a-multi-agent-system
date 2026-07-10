from app.llm_client import ask_llm
from app.schemas import Recommendation
import json

SYSTEM_PROMPT = """You are the Recommender Agent in a learning-personalization system.
Your only job: given a learner's query, suggest ONE next learning topic.

You must reason briefly first, then output a final answer as strict JSON.
Follow this exact structure:

REASONING: <1-2 sentences of your thinking>
ANSWER: {"title": "...", "reason": "...", "confidence": 0.0-1.0}

Do not include anything else. Do not add markdown formatting around the JSON.
"""

async def recommend(query: str) -> Recommendation:
    raw = await ask_llm(prompt=query, system=SYSTEM_PROMPT)

    # split reasoning from answer
    _, _, answer_part = raw.partition("ANSWER:")
    answer_part = answer_part.strip()

    data = json.loads(answer_part)
    return Recommendation(**data)