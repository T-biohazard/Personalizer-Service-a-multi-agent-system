# Personalizer

A starter FastAPI project skeleton for the Personalizer application.

## Structure

- app/main.py: FastAPI entrypoint
- app/schemas.py: Pydantic models
- app/llm_client.py: LLM client wrapper
- app/agents/: agent implementations for profile, retrieval, recommender, critique, and graph memory
- app/graph.py: LangGraph workflow definition
- app/graph_memory.py: prerequisite graph for graph-memory suggestions
- mcp_server.py: MCP tool server exposing catalog search and graph-memory tools
- data/catalog/: course/article metadata storage
