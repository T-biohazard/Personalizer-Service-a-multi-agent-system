from datetime import datetime
from typing import Literal

from pydantic import BaseModel, Field


class HealthResponse(BaseModel):
    message: str


class UserProfile(BaseModel):
    user_id: str
    known_topics: list[str] = Field(default_factory=list)
    skill_level: Literal["beginner", "intermediate", "advanced"] = "beginner"
    interests: list[str] = Field(default_factory=list)


class Interaction(BaseModel):
    user_id: str
    query: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)


class Recommendation(BaseModel):
    title: str
    reason: str
    confidence: float


class RecommendationRequest(BaseModel):
    user_id: str
    topic: str
