import asyncio

from app.agents.profile_agent import get_or_create_profile, log_interaction
from app.celery_app import celery_app
from app.db import SessionLocal
from app.graph import get_compiled_graph
from app.logging_utils import log_agent_step


@celery_app.task(name="run_personalizer_graph")
def run_personalizer_graph(user_id: str, query: str):
    return asyncio.run(_run(user_id, query))


async def _run(user_id: str, query: str):
    async with SessionLocal() as session:
        profile = await get_or_create_profile(session, user_id)
        await log_interaction(session, user_id, query)

    graph = await get_compiled_graph()
    config = {"configurable": {"thread_id": user_id}}
    state_in = {
        "user_id": user_id,
        "query": query,
        "profile": profile,
        "candidates": [],
        "recommendation": None,
        "approved": False,
        "attempts": 0,
        "image_bytes": None,
        "image_signal": None,
    }
    result = await graph.ainvoke(state_in, config=config)
    log_agent_step("graph_complete", state_in, result)

    recommendation = result["recommendation"]
    return {
        "title": recommendation.title,
        "reason": recommendation.reason,
        "confidence": recommendation.confidence,
    }
