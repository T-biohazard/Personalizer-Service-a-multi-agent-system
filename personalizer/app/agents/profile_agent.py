from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import InteractionRow, ProfileRow
from app.schemas import UserProfile


async def get_or_create_profile(session: AsyncSession, user_id: str) -> UserProfile:
    row = await session.get(ProfileRow, user_id)
    if row is None:
        row = ProfileRow(user_id=user_id)
        session.add(row)
        await session.commit()

    return UserProfile(
        user_id=row.user_id,
        skill_level=row.skill_level,
        known_topics=row.known_topics,
        interests=row.interests,
    )


async def log_interaction(session: AsyncSession, user_id: str, query: str) -> None:
    session.add(InteractionRow(user_id=user_id, query=query))
    await session.commit()
