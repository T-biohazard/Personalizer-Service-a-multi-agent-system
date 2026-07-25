import networkx as nx

TOPIC_GRAPH_EDGES = [
    ("python-basics", "python-oop"),
    ("python-basics", "python-concurrency"),
    ("python-oop", "backend-apis"),
    ("backend-apis", "agentic-ai"),
    ("agentic-ai", "rag"),
    ("rag", "agent-memory"),
    ("agentic-ai", "mcp"),
    ("backend-apis", "devops"),
]


def build_topic_graph() -> nx.DiGraph:
    graph = nx.DiGraph()
    graph.add_edges_from(TOPIC_GRAPH_EDGES, relation="prerequisite_of")
    return graph


_topic_graph = build_topic_graph()


def get_next_topics(known_topics: list[str]) -> list[str]:
    """Given topics the user already knows, find graph-neighbors they don't know yet."""
    candidates = set()
    for topic in known_topics:
        if topic in _topic_graph:
            candidates.update(_topic_graph.successors(topic))
    return list(candidates - set(known_topics))
