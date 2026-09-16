# The Anti-Algorithm — Project Journal

> **Authenticity note:** This journal template was prepared with AI assistance. Abdalla should complete each dated entry only after personally performing the work described. Do not backdate entries or report results that were not reproduced.

## How to use this journal
For every session, record the real date, commands run, outputs checked, design decisions, unexpected behavior, and what was learned. Link evidence and commits when available.

---

## Session 1 — Environment, tests, and current recommender behavior

**Date:**

**Commands I personally ran:**
```text

```

**What I verified:**
- [ ] Dependencies installed
- [ ] `pytest -q` passed
- [ ] `python evaluate.py` ran successfully
- [ ] Streamlit application launched
- [ ] I inspected recommendations for several different profiles
- [ ] I checked that explanations correspond to the largest feature gaps

**Observed evaluation output:**

**A recommendation I found surprising and why:**

**Evidence links:**

**What I learned in my own words:**

**Related commit / issue comment:**

---

## Session 2 — Baselines and sensitivity

**Date:**

**What I compared:**
- [ ] anti-recommender ranking
- [ ] similarity-oriented ranking
- [ ] random ranking with a fixed seed

**Metrics / observations:**

**Sensitivity check:**
I changed or perturbed selected feature values by a small amount and recorded whether the top recommendations stayed stable.

**What changed and what stayed stable:**

**Evidence links:**

**What I learned in my own words:**

**Related commit:**

---

## Session 3 — Data-design review and final reproducibility

**Date:**

**What I reviewed:**
- [ ] how the six dimensions are defined
- [ ] how catalog/preference vectors were authored
- [ ] how normalized Euclidean distance becomes a novelty score
- [ ] why the system is algorithmic rather than trained ML
- [ ] limitations of hand-authored vectors
- [ ] Streamlit demo and CSV export

**What the project actually demonstrates:**

**Main limitation(s):**

**What a future data-driven version would require:**

**Evidence links:**

**Final commit:**

---

## Reproducibility sign-off
- [ ] I can install and run the project from the repository instructions.
- [ ] I can explain normalized Euclidean distance.
- [ ] I can explain how the user profile vector is built.
- [ ] I can explain the novelty score and pairwise diversity metric.
- [ ] I can explain why this is not a trained ML model.
- [ ] I can explain what the baseline and sensitivity experiments reveal.
- [ ] I can describe at least two limitations without reading a script.

**Abdalla initials:**

**Date:**
