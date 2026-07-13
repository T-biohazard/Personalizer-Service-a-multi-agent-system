from app.llm_client import ask_llm
from app.schemas import Recommendation, UserProfile
import json

SYSTEM_PROMPT = """You are the Recommender Agent in a learning-personalization system.
You will receive a learner's profile (skill level, known topics) and their query.
Suggest ONE next learning topic appropriate for their skill level, and don't repeat topics they already know.

Reason briefly first, then output strict JSON:
REASONING: <1-2 sentences>
ANSWER: {"title": "...", "reason": "...", "confidence": 0.0-1.0}
Nothing else. No markdown formatting.
"""

async def recommend(query: str, profile: UserProfile) -> Recommendation:
    prompt = f"""Learner profile: skill_level={profile.skill_level}, known_topics={profile.known_topics}
Query: {query}"""
    raw = await ask_llm(prompt=prompt, system=SYSTEM_PROMPT)
    _, _, answer_part = raw.partition("ANSWER:")
    data = json.loads(answer_part.strip())
    return Recommendation(**data)