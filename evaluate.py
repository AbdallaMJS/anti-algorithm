from __future__ import annotations

from statistics import mean

from anti_algorithm.recommender import pairwise_diversity, recommend
from data import PREFERENCE_VECTORS


def main() -> None:
    rows = []
    for category, preferences in PREFERENCE_VECTORS.items():
        for preference in preferences:
            _, recs = recommend(category, [preference], limit=3)
            rows.append(
                {
                    "category": category,
                    "preference": preference,
                    "top_novelty": recs[0].score,
                    "top3_mean_novelty": round(mean(r.score for r in recs), 1),
                    "top3_diversity": pairwise_diversity(recs),
                }
            )

    print(f"Evaluated {len(rows)} single-preference profiles across {len(PREFERENCE_VECTORS)} categories.")
    print(f"Mean top recommendation novelty: {mean(r['top_novelty'] for r in rows):.1f}/100")
    print(f"Mean top-3 novelty: {mean(r['top3_mean_novelty'] for r in rows):.1f}/100")
    print(f"Mean top-3 pairwise diversity: {mean(r['top3_diversity'] for r in rows):.1f}/100")
    print("\nSample rows:")
    for row in rows[:8]:
        print(row)


if __name__ == "__main__":
    main()
