from langgraph.graph import END

from app.graph import route_after_critique


def test_critique_routes_to_end_when_approved():
    state = {"approved": True, "attempts": 1}

    assert route_after_critique(state) == END


def test_critique_retries_when_rejected_and_attempts_remain():
    state = {"approved": False, "attempts": 1}

    assert route_after_critique(state) == "recommender"


def test_critique_stops_after_max_attempts_even_if_rejected():
    state = {"approved": False, "attempts": 3}

    assert route_after_critique(state) == END
