import pytest

from anti_algorithm.recommender import (
    average_vector,
    normalized_distance,
    novelty_score,
    pairwise_diversity,
    recommend,
)


def test_average_vector():
    assert average_vector([[0, 100], [100, 0]]) == [50, 50]


def test_distance_is_zero_for_identical_vectors():
    assert normalized_distance([10, 20], [10, 20]) == 0.0


def test_distance_is_symmetric():
    a = [0, 50, 100]
    b = [100, 50, 0]
    assert normalized_distance(a, b) == normalized_distance(b, a)


def test_novelty_is_bounded():
    score = novelty_score([0, 0], [100, 100])
    assert 0 <= score <= 100


def test_recommend_returns_ranked_results():
    _, results = recommend("Music", ["pop"], limit=3)
    assert len(results) == 3
    assert results[0].score >= results[1].score >= results[2].score
    assert results[0].diffs[0]["Gap"] >= results[0].diffs[-1]["Gap"]


def test_empty_preferences_rejected():
    with pytest.raises(ValueError):
        recommend("Music", [], limit=3)


def test_pairwise_diversity_is_nonnegative():
    _, results = recommend("Movies", ["action"], limit=3)
    assert pairwise_diversity(results) >= 0
