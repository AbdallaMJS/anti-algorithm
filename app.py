from __future__ import annotations

from datetime import datetime

import pandas as pd
import streamlit as st

from anti_algorithm.recommender import pairwise_diversity, recommend
from data import AXES, PREFERENCE_VECTORS


st.set_page_config(page_title="The Anti-Algorithm", page_icon="🪞", layout="wide")
st.title("🪞 The Anti-Algorithm")
st.caption("An explainable anti-recommendation engine that deliberately explores choices outside a user's usual preference profile.")

if "history" not in st.session_state:
    st.session_state.history = []
if "last" not in st.session_state:
    st.session_state.last = None

page = st.sidebar.radio("Navigate", ["Discover", "Taste Shift", "Methodology"])

if page == "Discover":
    category = st.sidebar.selectbox("Category", list(PREFERENCE_VECTORS.keys()))
    options = list(PREFERENCE_VECTORS[category].keys())
    selected = st.sidebar.multiselect("Your usual choices", options, default=options[:3])
    count = st.sidebar.slider("How many opposite picks?", 1, 5, 3)

    if st.sidebar.button("Generate opposites", type="primary"):
        try:
            user_vector, results = recommend(category, selected, limit=count)
            st.session_state.last = {
                "category": category,
                "selected": selected,
                "user_vector": user_vector,
                "results": results,
            }
        except ValueError as exc:
            st.sidebar.warning(str(exc))

    if st.session_state.last is None:
        st.info("Choose your normal preferences in the sidebar, then generate deliberately unfamiliar recommendations.")
    else:
        last = st.session_state.last
        results = last["results"]
        top = results[0]

        c1, c2, c3 = st.columns(3)
        c1.metric("Top novelty", f"{top.score}/100")
        c2.metric("Recommendation diversity", f"{pairwise_diversity(results)}%")
        c3.metric("Profile dimensions", len(AXES[last["category"]]))

        st.markdown(f"## {top.title}")
        st.write(top.why)
        st.progress(top.score / 100, text=f"Novelty score: {top.score}/100")

        st.subheader("Why this is different")
        df = pd.DataFrame(top.diffs)
        st.dataframe(df, use_container_width=True, hide_index=True)

        st.subheader("Other opposite directions")
        for i, item in enumerate(results, 1):
            with st.expander(f"#{i} {item.title} — novelty {item.score}/100"):
                st.write(item.why)
                st.dataframe(pd.DataFrame(item.diffs[:3]), use_container_width=True, hide_index=True)

        reaction = st.radio(
            "Would you cross the line?",
            [
                "Still not for me",
                "I am curious enough to try it",
                "I tried it and liked it",
                "I tried it and still disliked it",
            ],
            horizontal=True,
        )
        if st.button("Save reaction"):
            st.session_state.history.append(
                {
                    "time": datetime.now().isoformat(timespec="seconds"),
                    "category": last["category"],
                    "usual_choices": ", ".join(last["selected"]),
                    "recommendation": top.title,
                    "novelty": top.score,
                    "reaction": reaction,
                }
            )
            st.success("Reaction saved. Open Taste Shift to inspect the history.")

elif page == "Taste Shift":
    st.subheader("Taste-shift tracker")
    if not st.session_state.history:
        st.info("No reactions saved yet.")
    else:
        df = pd.DataFrame(st.session_state.history)
        total = len(df)
        curious = df["reaction"].isin(["I am curious enough to try it", "I tried it and liked it"]).sum()
        liked = (df["reaction"] == "I tried it and liked it").sum()
        c1, c2, c3 = st.columns(3)
        c1.metric("Challenges", total)
        c2.metric("Curious/positive", int(curious))
        c3.metric("Unexpected likes", int(liked))
        st.dataframe(df, use_container_width=True, hide_index=True)
        st.download_button(
            "Download reaction history (CSV)",
            data=df.to_csv(index=False).encode("utf-8"),
            file_name="anti_algorithm_history.csv",
            mime="text/csv",
        )

else:
    st.subheader("Methodology and responsible interpretation")
    st.markdown(
        """
**1. Preference representation.** Each category uses six interpretable 0–100 dimensions. A user's profile is the mean of the vectors associated with their selected usual choices.

**2. Novelty calculation.** Candidate items are ranked by normalized Euclidean distance from the user profile. Larger distance means the item is more unlike the user's normal pattern.

**3. Explainability.** The interface shows the dimensions with the largest absolute gaps, so every recommendation has an explicit mathematical reason.

**4. Diversity.** The app reports pairwise distance among returned recommendations to distinguish a varied result set from several nearly identical alternatives.

**5. Evaluation.** `python evaluate.py` runs the recommender across every single-preference profile and reports aggregate novelty and diversity. `pytest -q` checks mathematical invariants and ranking behavior.
        """
    )
    st.warning(
        "This is an explainable algorithmic recommender, not a trained machine-learning model. "
        "The vectors are hand-authored for a portfolio prototype, so scores should not be treated as psychological measurements or objective judgments of taste."
    )
