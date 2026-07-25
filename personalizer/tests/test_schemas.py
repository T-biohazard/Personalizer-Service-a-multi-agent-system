from app.schemas import Recommendation, UserProfile


def test_user_profile_defaults():
    profile = UserProfile(user_id="test_user")

    assert profile.skill_level == "beginner"
    assert profile.known_topics == []


def test_recommendation_confidence_is_bounded():
    recommendation = Recommendation(title="Test Topic", reason="Good fit", confidence=0.8)

    assert 0.0 <= recommendation.confidence <= 1.0
