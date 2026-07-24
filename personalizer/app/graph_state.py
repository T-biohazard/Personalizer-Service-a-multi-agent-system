from typing import TypedDict

from app.schemas import Recommendation, UserProfile


class GraphState(TypedDict, total=False):
    user_id: str
    query: str
    profile: UserProfile
    candidates: list[dict]
    recommendation: Recommendation | None
    approved: bool
    attempts: int
