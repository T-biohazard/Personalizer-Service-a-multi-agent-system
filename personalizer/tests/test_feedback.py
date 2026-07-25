import asyncio

from app.main import feedback


def test_feedback_records_and_updates_profile():
    class FakeProfileRow:
        def __init__(self):
            self.known_topics = []

    class FakeSession:
        def __init__(self):
            self.profile_row = FakeProfileRow()
            self.added = []
            self.commit_calls = 0

        def add(self, obj):
            self.added.append(obj)

        async def commit(self):
            self.commit_calls += 1

        async def get(self, model, user_id):
            return self.profile_row

    session = FakeSession()
    response = asyncio.run(feedback(user_id="u1", topic="python", liked=True, session=session))

    assert response["status"] == "recorded"
    assert session.commit_calls == 1
    assert session.profile_row.known_topics == ["python"]
    assert session.added[0].topic == "python"
