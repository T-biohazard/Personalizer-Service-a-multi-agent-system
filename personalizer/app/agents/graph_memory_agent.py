from app.graph_memory import get_next_topics
from app.graph_state import GraphState


async def graph_memory_node(state: GraphState) -> dict:
    known_topics = state.get("profile", None)
    if known_topics is None:
        return {"graph_suggestions": []}

    profile = state.get("profile")
    known = profile.known_topics if profile is not None else []
    suggested_topics = get_next_topics(known)
    return {"graph_suggestions": suggested_topics}
