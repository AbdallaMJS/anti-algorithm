from __future__ import annotations

from dataclasses import dataclass
from math import sqrt
from statistics import mean

from data import AXES, CATALOG, PREFERENCE_VECTORS


@dataclass(frozen=True)
class Recommendation:
    title: str
    score: int
    why: str
    diffs: list[dict]
    vector: list[float]


def average_vector(vectors: list[list[float]]) -> list[float]:
    if not vectors:
        raise ValueError("At least one preference vector is required.")
    return [mean(values) for values in zip(*vectors)]


def normalized_distance(a: list[float], b: list[float]) -> float:
    if len(a) != len(b):
        raise ValueError("Vectors must have equal length.")
    if not a:
        return 0.0
    raw = sqrt(sum((x - y) ** 2 for x, y in zip(a, b)))
    return raw / sqrt(len(a) * (100**2))


def novelty_score(user_vector: list[float], item_vector: list[float]) -> int:
    """Map normalized Euclidean distance to an interpretable 0-100 novelty score."""
    return round(max(0.0, min(1.0, normalized_distance(user_vector, item_vector))) * 100)


def build_profile(category: str, selected: list[str]) -> list[float]:
    vectors = PREFERENCE_VECTORS[category]
    unknown = [name for name in selected if name not in vectors]
    if unknown:
        raise ValueError(f"Unknown preferences: {', '.join(unknown)}")
    return average_vector([vectors[name] for name in selected])


def explain_differences(category: str, user_vector: list[float], item_vector: list[float]) -> list[dict]:
    rows = []
    for axis, user_value, item_value in zip(AXES[category], user_vector, item_vector):
        rows.append(
            {
                "Dimension": axis,
                "You": round(user_value),
                "Recommendation": round(item_value),
                "Gap": round(abs(user_value - item_value)),
            }
        )
    rows.sort(key=lambda row: row["Gap"], reverse=True)
    return rows


def recommend(category: str, selected: list[str], limit: int = 3) -> tuple[list[float], list[Recommendation]]:
    if not selected:
        raise ValueError("Choose at least one preference.")
    user_vector = build_profile(category, selected)
    results = []
    for item in CATALOG[category]:
        results.append(
            Recommendation(
                title=item["title"],
                score=novelty_score(user_vector, item["vector"]),
                why=item["why"],
                diffs=explain_differences(category, user_vector, item["vector"]),
                vector=item["vector"],
            )
        )
    results.sort(key=lambda rec: (-rec.score, rec.title))
    return user_vector, results[: max(1, limit)]


def pairwise_diversity(recommendations: list[Recommendation]) -> float:
    if len(recommendations) < 2:
        return 0.0
    distances = []
    for i, left in enumerate(recommendations):
        for right in recommendations[i + 1 :]:
            distances.append(normalized_distance(left.vector, right.vector))
    return round(mean(distances) * 100, 1)
