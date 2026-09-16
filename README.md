# 🪞 The Anti-Algorithm

An explainable recommendation-system prototype that deliberately suggests options **outside** a user's usual preferences instead of optimizing for more of the same.

## Why this project
Most recommendation systems are designed to maximize similarity, engagement, or predicted preference. This project explores the opposite design question: **what if a recommender intentionally helps a user discover unfamiliar choices, while clearly explaining why each suggestion is different?**

## How it works
1. Each category (music, movies, games, food, books, websites) is represented with six interpretable dimensions scored from 0–100.
2. A user's preference profile is calculated by averaging the vectors of their selected usual choices.
3. Every candidate recommendation is compared with that profile using normalized Euclidean distance.
4. Larger distance becomes a higher **novelty score**.
5. The system explains the recommendation by ranking the dimensions with the largest absolute gaps.
6. A pairwise-diversity metric shows whether the returned recommendations are meaningfully different from one another.
7. User reactions can be recorded and exported to CSV to observe whether unfamiliar recommendations become interesting over time.

## Important honesty note
This is an **algorithmic recommender, not a trained machine-learning model**. The preference and catalog vectors are hand-authored for a portfolio prototype. The goal is to demonstrate interpretable recommendation logic, vector-based reasoning, evaluation, and responsible communication—not to misrepresent rule-based scoring as ML.

## Project structure
```text
app.py                         Streamlit interface
anti_algorithm/recommender.py Core ranking, novelty, diversity, explanations
data.py                        Interpretable preference/catalog vectors
evaluate.py                    Reproducible aggregate evaluation
tests/test_recommender.py      Mathematical and ranking tests
requirements.txt               Runtime/test dependencies
```

## Run locally
```bash
pip install -r requirements.txt
streamlit run app.py
```

## Evaluation
Run the recommender across every single-preference profile:

```bash
python evaluate.py
```

The script reports:
- mean novelty of the top recommendation,
- mean novelty across the top three,
- mean pairwise diversity of the top three,
- and sample evaluation rows.

The evaluation is a **behavioral sanity check**, not evidence of predictive accuracy, because the project has no ground-truth labels or trained model.

## Testing
```bash
pytest -q
```

Tests check:
- vector averaging,
- distance symmetry,
- bounded novelty scores,
- ranking order,
- rejection of empty profiles,
- and non-negative recommendation diversity.

## Responsible interpretation
The system does not infer personality, psychological traits, or objective quality. Scores only describe distance inside the project's manually designed feature space. Different feature definitions or vector values would change the results.

## Future work
A research-oriented extension could replace the hand-authored vectors with embeddings learned from real user-item interaction data, compare novelty against relevance, evaluate serendipity with held-out feedback, and study whether explanations improve exploration. That would require a genuine dataset and experimental protocol rather than simply adding an ML library.

## Portfolio takeaway
This project demonstrates recommendation-system design, vector mathematics, explainability, metric design, testing, data presentation, and responsible distinction between algorithmic logic and machine learning.
