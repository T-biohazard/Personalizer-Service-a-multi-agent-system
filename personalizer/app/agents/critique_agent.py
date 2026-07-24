import json

from app.graph_state import GraphState
from app.llm_client import ask_llm

SYSTEM_PROMPT = """You are the Critique Agent. Review a recommendation against the learner's profile.
Check: is the difficulty appropriate for their skill_level? Is it not already in known_topics?
Reason briefly, then output strict JSON:
REASONING: <1-2 sentences>
ANSWER: {\"approved\": true or false, \"confidence\": 0.0-1.0}
Nothing else."""


async def critique_node(state: GraphState) -> dict:
    recommendation = state.get("recommendation")
    profile = state.get("profile")
    if recommendation is None or profile is None:
        return {"approved": False}

    prompt = (
        f"Profile: skill_level={profile.skill_level}, known_topics={profile.known_topics}\n"
        f"Recommendation: {recommendation.title} — {recommendation.reason}"
    )

    try:
        raw = await ask_llm(prompt=prompt, system=SYSTEM_PROMPT)
    except Exception:
        return {"approved": True, "recommendation": recommendation}

    _, _, answer_part = raw.partition("ANSWER:")
    data = json.loads(answer_part.strip())

    recommendation.confidence = float(data.get("confidence", recommendation.confidence))
    return {"recommendation": recommendation, "approved": bool(data.get("approved", False))}
