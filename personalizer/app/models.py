from sqlalchemy import String, Float, ForeignKey, DateTime, JSON
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime
from app.db import Base

class ProfileRow(Base):
    __tablename__ = "profiles"

    user_id: Mapped[str] = mapped_column(String, primary_key=True)
    skill_level: Mapped[str] = mapped_column(String, default="beginner")
    known_topics: Mapped[list] = mapped_column(JSON, default=list)
    interests: Mapped[list] = mapped_column(JSON, default=list)

class InteractionRow(Base):
    __tablename__ = "interactions"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user_id: Mapped[str] = mapped_column(ForeignKey("profiles.user_id"))
    query: Mapped[str] = mapped_column(String)
    timestamp: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)