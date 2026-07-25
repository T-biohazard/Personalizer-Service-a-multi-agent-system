from mcp.server.fastmcp import FastMCP

from app.graph_memory import get_next_topics
from app.vector_store import search

mcp = FastMCP("personalizer")


@mcp.tool()
def search_catalog(query: str, top_k: int = 3) -> list[dict]:
    """Search the catalog for relevant course topics."""
    return search(query, top_k=top_k)


@mcp.tool()
def suggest_next_topics(known_topics: list[str]) -> list[str]:
    """Return graph-based next topics from the prerequisite graph."""
    return get_next_topics(known_topics)


if __name__ == "__main__":
    mcp.run()
