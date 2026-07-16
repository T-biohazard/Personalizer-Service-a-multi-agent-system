from app.vector_store import search

async def retrieve(query: str, top_k: int = 3) -> list[dict]:
    return search(query, top_k=top_k)