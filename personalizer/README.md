# Personalizer

A FastAPI-based learning personalization service that recommends next learning topics using a LangGraph workflow, asynchronous job processing, graph-memory reasoning, and optional local voice input/output.

## Overview

This repo is built as a working end-to-end recommendation pipeline:

1. User sends a query via `/ask`.
2. The service enqueues the request in Celery/Redis.
3. A worker executes a LangGraph workflow that retrieves candidate topics, reasons over prerequisite graphs, generates a recommendation, and performs a critique pass.
4. The user polls `/jobs/{job_id}` for status and then receives the final recommendation.
5. Optional `/feedback` updates the stored profile so future recommendations improve.

## End-to-end pipeline

```mermaid
flowchart LR
    A[User client] -->|POST /ask| B[FastAPI API gateway]
    B -->|Celery task enqueue| C[Redis broker]
    C -->|Task dispatch| D[Celery worker]
    D --> E[LangGraph workflow]
    E --> F[Retrieval agent]
    E --> G[Graph memory agent]
    E --> H[Recommendation agent]
    E --> I[Critique agent]
    D -->|Store result| J[Celery backend / result store]
    K[User client] -->|GET /jobs/{job_id}| J
    D -->|Profile/feedback| L[Neon/Postgres]
    F --> M[Chroma vector retrieval]
    H --> N[Groq API]
    O[Optional voice client] -->|mic audio| P[app/voice_io.py]
    P -->|transcribed query| A
    O <--|speech output| Q[Piper TTS]
```

## Architecture

- **API**: `app/main.py` exposes `/ask`, `/jobs/{job_id}`, and `/feedback`.
- **Workflow**: `app/graph.py` defines a LangGraph state graph with retrieval, vision, graph memory, recommendation, and critique nodes.
- **Async processing**: `app/tasks.py` submits requests to Celery and runs the graph in the background.
- **Data**: `app/db.py` configures Neon/Postgres via SQLAlchemy async sessions.
- **Search**: `app/vector_store.py` builds and queries a Chroma collection.
- **LLM**: `app/llm_client.py` calls Groq for text and vision reasoning.
- **Voice**: `app/voice_io.py` captures local audio and transcribes it with `faster-whisper`.

## Tech stack

| Layer | Stack |
| --- | --- |
| API | FastAPI, Uvicorn |
| Orchestration | LangGraph |
| Background jobs | Celery, Redis |
| Data | PostgreSQL (Neon), SQLAlchemy async |
| Vector search | Chroma, sentence-transformers |
| LLM | Groq API |
| Vision | Groq vision API |
| Voice | faster-whisper, Piper TTS |

## Deployment modes

### Local development

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
# edit .env for GROQ_API_KEY and DATABASE_URL
python -m app.create_tables
uvicorn app.main:app --reload
celery -A app.celery_app worker --loglevel=info
```

### Docker compose (prepared, not run)

```bash
docker compose up --build
```

This starts:
- `redis` on port `6379`
- `chroma` on port `8001`
- `api` on port `8000`
- `worker` as a Celery process

## Usage

### Submit a query

```bash
curl "http://localhost:8000/ask?user_id=u1&query=python"
```

### Poll job status

```bash
curl "http://localhost:8000/jobs/<job_id>"
```

### Send feedback

```bash
curl "http://localhost:8000/feedback?user_id=u1&topic=python&liked=true"
```

### Voice demo

```bash
python voice_main.py
```

The script records microphone input, transcribes it locally, sends the transcribed text to `/ask`, and prints the returned job details.

## Testing

```bash
pytest -q
```

## Notes

- The app uses Neon/Postgres for profile and feedback persistence. There is no local Mongo container.
- The LLM layer is built for Groq API usage, not Ollama.
- Dockerization is targeted at Redis, Chroma, the API, and the Celery worker.
- The voice layer is optional and runs fully locally with `faster-whisper`.

## Milestones

- M0-M9: Graph-based recommendation, critique-driven retry, graph memory, multimodal state, async queue.
- M10: local voice STT/TTS demo.
- M11: Docker-compose-ready setup for Redis, Chroma, API, worker.
- M12: feedback loop and structured logging.

