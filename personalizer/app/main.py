from fastapi import Depends, FastAPI
from sqlalchemy.ext.asyncio import AsyncSession

from app.agents.profile_agent import get_or_create_profile, log_interaction
from app.db import get_session
from app.graph import get_compiled_graph
from app.schemas import Interaction, Recommendation

app = FastAPI(title="Personalizer Service")


@app.post("/ask", response_model=Recommendation)
async def ask(interaction: Interaction, session: AsyncSession = Depends(get_session)):
    profile = await get_or_create_profile(session, interaction.user_id)
    await log_interaction(session, interaction.user_id, interaction.query)

    graph = await get_compiled_graph()
    result = await graph.ainvoke(
        {
            "user_id": interaction.user_id,
            "query": interaction.query,
            "profile": profile,
            "candidates": [],
            "recommendation": None,
            "approved": False,
            "attempts": 0,
        },
        config={"configurable": {"thread_id": interaction.user_id}},
    )

    return result["recommendation"]