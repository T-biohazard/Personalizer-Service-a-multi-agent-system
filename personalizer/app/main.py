from fastapi import Depends, FastAPI
from sqlalchemy.ext.asyncio import AsyncSession

from app.celery_app import celery_app
from app.db import get_session
from app.models import FeedbackRow, ProfileRow
from app.tasks import run_personalizer_graph

app = FastAPI(title="Personalizer Service")


@app.post("/ask")
async def ask(user_id: str, query: str):
    task = run_personalizer_graph.delay(user_id, query)
    return {"job_id": task.id, "status": "pending"}


@app.get("/jobs/{job_id}")
async def get_job(job_id: str):
    result = celery_app.AsyncResult(job_id)
    if result.state == "PENDING":
        return {"status": "pending"}
    if result.state == "FAILURE":
        return {"status": "failed", "error": str(result.result)}
    return {"status": "done", "result": result.result}


@app.post("/feedback")
async def feedback(user_id: str, topic: str, liked: bool, session: AsyncSession = Depends(get_session)):
    session.add(FeedbackRow(user_id=user_id, topic=topic, liked=liked))
    profile_row = await session.get(ProfileRow, user_id)
    if profile_row is not None and liked and topic not in profile_row.known_topics:
        profile_row.known_topics = profile_row.known_topics + [topic]
    await session.commit()
    return {"status": "recorded"}