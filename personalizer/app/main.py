from fastapi import FastAPI

from .llm_client import ask_llm
from .schemas import Interaction, Recommendation
from app.agents.recommender_agent import recommend

app = FastAPI(title="Personalizer Service")

@app.post("/ask", response_model=Recommendation)
async def ask(interaction: Interaction):
     return await recommend(interaction.query)
#     prompt = f"""A learner asked: "{interaction.query}"
# Suggest ONE learning topic to explore next and a one-sentence reason.
# Respond as: TITLE | REASON"""
#     raw = await ask_llm(prompt)
#     title, _, reason = raw.partition("|")
#     return Recommendation(title=title.strip(), reason=reason.strip(), confidence=0.5)