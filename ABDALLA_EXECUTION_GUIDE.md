# Abdalla Execution Guide — The Anti-Algorithm

This file is a **student execution guide**, not evidence that the work has already been completed. The branch was prepared with AI-assisted development support. Abdalla should personally run the steps, inspect the behavior, make final decisions, and complete `PROJECT_JOURNAL.md` in his own words.

## Goal
Reproduce the recommender, verify its ranking/explanation logic, and evaluate how the anti-recommendation behavior differs from similarity-oriented and random baselines.

## 1. Work on the execution branch
```bash
git clone https://github.com/AbdallaMJS/anti-algorithm.git
cd anti-algorithm
git checkout abdalla-execution
```

## 2. Create a clean environment and install
macOS/Linux:
```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
```

Windows PowerShell:
```powershell
py -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
```

## 3. Run tests and the current evaluation
```bash
pytest -q
python evaluate.py
```
Save the real output. If a test or evaluation fails, record the failure before fixing it.

## 4. Launch the application
```bash
streamlit run app.py
```
Try several different preference profiles. For at least three profiles, record:
- the top anti-recommendation;
- novelty score;
- the two strongest explanation dimensions;
- whether the recommendation appears genuinely different from the input profile.

## 5. Compare against two baselines
For the same profiles, compare the anti-recommender with:
- a **similarity baseline** that ranks the nearest items first;
- a **random baseline** using a fixed random seed for reproducibility.

Recommended outputs:
- mean top-1 novelty;
- mean top-3 novelty;
- mean pairwise diversity of the top three;
- a short qualitative comparison.

Do not describe the system as more accurate: there are no ground-truth relevance labels in the current design.

## 6. Run a sensitivity check
Perturb selected vector dimensions by approximately 5% and 10%, rerun the rankings, and note whether the top recommendation changes. Record examples where ranking is stable and where it is sensitive.

Suggested evidence file: `results/baseline_and_sensitivity.md`.

## 7. Review the data design
Abdalla should be able to explain:
- who/what authored the vectors in the prototype;
- what each dimension represents;
- why the distance is normalized;
- why changing the dimensions/vectors can change the recommendations;
- what real interaction data would be needed for a learned recommender.

Suggested student-written file: `DATA_DESIGN.md` or a concise section in the journal.

## 8. Final student-owned evidence
After the real run, Abdalla should personally add or approve:
- completed `PROJECT_JOURNAL.md`;
- genuine baseline/sensitivity observations;
- any plots or tables generated from the real run;
- a correction or improvement he decided to make after inspecting results.

Suggested final student commit:
```text
Document Anti-Algorithm baselines and sensitivity findings
```

## Interview check
Abdalla should be able to answer without reading notes:
1. How is the user profile vector calculated?
2. Why does Euclidean distance make sense here, and what are its limitations?
3. What is the difference between novelty and relevance?
4. Why is this not machine learning?
5. What would be required to turn it into a data-driven recommender?
