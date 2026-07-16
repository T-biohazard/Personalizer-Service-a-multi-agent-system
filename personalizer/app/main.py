from fastapi import FastAPI, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas import Interaction, Recommendation
from app.agents.recommender_agent import recommend
from app.agents.profile_agent import get_or_create_profile, log_interaction
from app.db import get_session

app = FastAPI(title="Personalizer Service")

# @app.post("/ask", response_model=Recommendation)
# async def ask(interaction: Interaction, session: AsyncSession = Depends(get_session)):
#     profile = await get_or_create_profile(session, interaction.user_id)
#     await log_interaction(session, interaction.user_id, interaction.query)
#     return await recommend(interaction.query, profile)

from app.agents.retrieval_agent import retrieve

@app.post("/ask", response_model=Recommendation)
async def ask(interaction: Interaction, session: AsyncSession = Depends(get_session)):
    profile = await get_or_create_profile(session, interaction.user_id)
    await log_interaction(session, interaction.user_id, interaction.query)
    candidates = await retrieve(interaction.query)
    return await recommend(interaction.query, profile, candidates)