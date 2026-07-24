from app.graph_state import GraphState


async def retrieve(query: str, top_k: int = 3) -> list[dict]:
    from app.vector_store import search

    return search(query, top_k=top_k)


async def retrieval_node(state: GraphState) -> dict:
    query = state.get("query", "")
    return {"candidates": await retrieve(query)}