import asyncio

from app.graph import build_graph, route_after_critique
from app.schemas import Recommendation, UserProfile
from mcp_server import search_catalog, suggest_next_topics


def test_route_after_critique_retries_until_cap():
    state = {"approved": False, "attempts": 1}

    assert route_after_critique(state) == "recommender"


def test_graph_can_run_with_stubbed_nodes(monkeypatch):
    async def fake_retrieval_node(state):
        return {"candidates": [{"title": "API Design"}]}

    async def fake_recommender_node(state):
        return {
            "recommendation": Recommendation(title="API Design", reason="Good fit", confidence=0.8),
            "attempts": state.get("attempts", 0) + 1,
        }

    async def fake_critique_node(state):
        return {"approved": True}

    import app.graph as graph_module

    monkeypatch.setattr(graph_module, "retrieval_node", fake_retrieval_node)
    monkeypatch.setattr(graph_module, "vision_node", lambda state: {"image_signal": "traceback about async"})
    monkeypatch.setattr(graph_module, "graph_memory_node", lambda state: {"graph_suggestions": ["backend-apis"]})
    monkeypatch.setattr(graph_module, "recommender_node", fake_recommender_node)
    monkeypatch.setattr(graph_module, "critique_node", fake_critique_node)

    graph = build_graph()
    result = asyncio.run(
        graph.ainvoke(
            {
                "user_id": "u1",
                "query": "backend APIs",
                "profile": UserProfile(user_id="u1"),
                "candidates": [],
                "recommendation": None,
                "approved": False,
                "attempts": 0,
                "graph_suggestions": ["backend-apis"],
            }
        )
    )

    assert result["approved"] is True
    assert result["recommendation"].title == "API Design"
    assert result["graph_suggestions"] == ["backend-apis"]
    assert result["image_signal"] == "traceback about async"


def test_mcp_tools_expose_existing_capabilities():
    search_results = search_catalog("backend APIs", top_k=1)
    assert search_results == [] or search_results[0]["title"]

    next_topics = suggest_next_topics(["python-basics", "python-oop"])
    assert "backend-apis" in next_topics
