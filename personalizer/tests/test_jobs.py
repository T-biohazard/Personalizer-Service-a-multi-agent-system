import asyncio

from app.main import ask, get_job
from app.tasks import run_personalizer_graph


def test_ask_returns_job_id(monkeypatch):
    class DummyTask:
        id = "job-123"

    def fake_delay(user_id, query, image_data=None):
        return DummyTask()

    monkeypatch.setattr(run_personalizer_graph, "delay", fake_delay)

    response = asyncio.run(ask(user_id="u1", query="hello"))

    assert response["status"] == "pending"
    assert response["job_id"] == "job-123"


def test_get_job_reports_pending_without_result(monkeypatch):
    class DummyResult:
        state = "PENDING"
        result = None

    monkeypatch.setattr("app.main.celery_app.AsyncResult", lambda job_id: DummyResult())

    response = asyncio.run(get_job("job-123"))

    assert response["status"] == "pending"
