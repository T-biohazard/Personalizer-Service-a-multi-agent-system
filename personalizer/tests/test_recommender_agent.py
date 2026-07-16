import pytest

from app.agents.recommender_agent import recommend
from app.schemas import UserProfile


@pytest.mark.asyncio
async def test_recommend_falls_back_to_catalog_title(monkeypatch):
    async def fake_ask_llm(*args, **kwargs):
        raise RuntimeError("llm unavailable")

    monkeypatch.setattr("app.agents.recommender_agent.ask_llm", fake_ask_llm)

    profile = UserProfile(user_id="u1")
    candidates = [{"title": "API Setup & Integration", "topic": "backend-apis", "level": "intermediate"}]

    result = await recommend("I want to get better at backend APIs", profile, candidates)

    assert result.title == "API Setup & Integration"
    assert result.confidence >= 0.5
