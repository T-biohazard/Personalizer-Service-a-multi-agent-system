import json

from app.graph_state import GraphState
from app.llm_client import ask_llm
from app.schemas import Recommendation, UserProfile

SYSTEM_PROMPT = """You are the Recommender Agent in a learning-personalization system.
You will receive a learner's profile, their query, CANDIDATE topics retrieved from the real catalog,
and GRAPH_SUGGESTIONS (topics that logically follow what they already know from a prerequisite graph).
You must choose ONE candidate only — do not invent a topic that isn't in the candidate list.
Prefer a candidate that also appears in graph_suggestions when possible; otherwise pick the best candidate alone.
Prefer candidates matching their skill level; avoid ones already in known_topics.

Reason briefly first, then output strict JSON:
REASONING: <1-2 sentences>
ANSWER: {"title": "...", "reason": "...", "confidence": 0.0-1.0}
Nothing else. No markdown formatting.
"""


async def recommend(query: str, profile: UserProfile, candidates: list[dict], graph_suggestions: list[str] | None = None) -> Recommendation:
    if not candidates:
        raise ValueError("At least one candidate is required")

    prompt = f"""Learner profile: skill_level={profile.skill_level}, known_topics={profile.known_topics}
Query: {query}
Candidates: {candidates}
Graph suggestions (logical next topics): {graph_suggestions or []}"""

    try:
        raw = await ask_llm(prompt=prompt, system=SYSTEM_PROMPT)
    except Exception:
        top = candidates[0]
        return Recommendation(
            title=top["title"],
            reason=f"Selected the closest catalog match for '{query}'.",
            confidence=0.75,
        )

    _, _, answer_part = raw.partition("ANSWER:")
    data = json.loads(answer_part.strip())
    return Recommendation(**data)


async def recommender_node(state: GraphState) -> dict:
    profile = state.get("profile")
    query = state.get("query", "")
    candidates = state.get("candidates", [])
    if profile is None:
        raise ValueError("Profile is required for recommender node")

    recommendation = await recommend(query, profile, candidates, state.get("graph_suggestions", []))
    return {
        "recommendation": recommendation,
        "attempts": state.get("attempts", 0) + 1,
    }
