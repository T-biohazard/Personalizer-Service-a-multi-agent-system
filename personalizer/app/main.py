from typing import Annotated

from fastapi import Depends, FastAPI, File, Form, UploadFile
from sqlalchemy.ext.asyncio import AsyncSession

from app.agents.profile_agent import get_or_create_profile, log_interaction
from app.db import get_session
from app.graph import get_compiled_graph
from app.schemas import Recommendation

app = FastAPI(title="Personalizer Service")


@app.post("/ask", response_model=Recommendation)
async def ask(
    user_id: Annotated[str, Form()],
    query: Annotated[str, Form()],
    image: Annotated[UploadFile | None, File()] = None,
    session: AsyncSession = Depends(get_session),
):
    profile = await get_or_create_profile(session, user_id)
    await log_interaction(session, user_id, query)

    image_bytes = await image.read() if image else None

    graph = await get_compiled_graph()
    result = await graph.ainvoke(
        {
            "user_id": user_id,
            "query": query,
            "profile": profile,
            "candidates": [],
            "recommendation": None,
            "approved": False,
            "attempts": 0,
            "image_bytes": image_bytes,
            "image_signal": None,
        },
        config={"configurable": {"thread_id": user_id}},
    )

    return result["recommendation"]