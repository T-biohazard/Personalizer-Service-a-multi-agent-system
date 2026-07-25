# Personalizer

A FastAPI-based learning personalizer that recommends the next topic using a LangGraph workflow, a catalog vector store, and optional background job processing.

## Architecture

- FastAPI routes expose the experience through `/ask`, `/jobs/{job_id}`, and `/feedback`.
- A LangGraph workflow coordinates retrieval, graph-memory reasoning, recommendation, and critique.
- Celery + Redis handle asynchronous long-running requests.
- Neon/Postgres stores profile and interaction data; Chroma provides vector retrieval.

## Tech stack

| Layer | Stack |
| --- | --- |
| API | FastAPI, Uvicorn |
| Orchestration | LangGraph |
| Background jobs | Celery, Redis |
| Data | PostgreSQL (Neon), SQLAlchemy |
| Search | Chroma, sentence-transformers |
| LLM | Groq API |
| Voice | faster-whisper, Piper TTS |

## Setup

1. Create a virtual environment and install dependencies:
   ```bash
   python -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt
   ```
2. Copy .env.example to `.env` and fill in your secrets.
3. Create the database tables:
   ```bash
   python -m app.create_tables
   ```
4. Run the API and worker:
   ```bash
   uvicorn app.main:app --reload
   celery -A app.celery_app worker --loglevel=info
   ```

## Example requests

```bash
curl "http://localhost:8000/ask?user_id=u1&query=python"
curl "http://localhost:8000/feedback?user_id=u1&topic=python&liked=true"
```

## Milestones

- M0-M9: graph orchestration, critique, graph memory, MCP exposure, multimodal input, and async job queue.
- M10: optional voice input/output via local Whisper and Piper.
- M11: Docker compose setup for Redis, Chroma, the API, and the worker.
- M12: feedback loop and structured logging.

