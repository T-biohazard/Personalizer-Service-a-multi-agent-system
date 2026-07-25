from __future__ import annotations

from typing import Any

from app.agents.critique_agent import critique_node
from app.agents.graph_memory_agent import graph_memory_node
from app.agents.recommender_agent import recommender_node
from app.agents.retrieval_agent import retrieval_node
from app.agents.vision_agent import vision_node
from app.graph_state import GraphState
from langgraph.graph import END, StateGraph


def route_after_critique(state: GraphState) -> str:
    attempts = state.get("attempts", 0)
    approved = state.get("approved", False)
    if approved or attempts >= 3:
        return END
    return "recommender"


def build_graph() -> Any:
    graph = StateGraph(GraphState)

    graph.add_node("retrieval", retrieval_node)
    graph.add_node("vision", vision_node)
    graph.add_node("graph_memory", graph_memory_node)
    graph.add_node("recommender", recommender_node)
    graph.add_node("critique", critique_node)

    graph.set_entry_point("retrieval")
    graph.add_edge("retrieval", "vision")
    graph.add_edge("vision", "graph_memory")
    graph.add_edge("graph_memory", "recommender")
    graph.add_edge("recommender", "critique")
    graph.add_conditional_edges("critique", route_after_critique, {"recommender": "recommender", END: END})

    return graph.compile()


async def get_compiled_graph() -> Any:
    graph = build_graph()

    try:
        from app.db import DATABASE_URL
        from langgraph.checkpoint.postgres.aio import AsyncPostgresSaver
    except Exception:
        return graph

    if not DATABASE_URL:
        return graph

    try:
        checkpointer = AsyncPostgresSaver.from_conn_string(DATABASE_URL)
        await checkpointer.setup()
        return graph.compile(checkpointer=checkpointer)
    except Exception:
        return graph
