from datetime import datetime
from math import sqrt
import pandas as pd
import streamlit as st
from data import AXES, CATALOG, PREFERENCE_VECTORS

st.set_page_config(page_title="The Anti-Algorithm", page_icon="🪞", layout="wide")

st.markdown("""
<style>
.block-container {max-width: 1180px; padding-top: 1.7rem;}
.hero {padding: 1.35rem 1.5rem; border: 1px solid rgba(128,128,128,.25); border-radius: 18px;
background: linear-gradient(135deg, rgba(112,82,230,.14), rgba(30,190,170,.09)); margin-bottom: 1rem;}
.hero h1 {margin: 0 0 .35rem 0; font-size: 2.35rem;}
.hero p {margin: 0; opacity: .84; font-size: 1.05rem;}
.card {padding: 1rem 1.15rem; border: 1px solid rgba(128,128,128,.24); border-radius: 16px; margin: .65rem 0;}
.top-title {font-size: 2.45rem; font-weight: 800; margin: .15rem 0 .45rem 0;}
.kicker {font-size: .82rem; opacity: .68; font-weight: 700; letter-spacing: .04em;}
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="hero">
<h1>🪞 The Anti-Algorithm</h1>
<p><b>Most recommendation systems predict what you will like.</b><br>
This one deliberately finds what sits furthest outside your usual pattern — and explains exactly why.</p>
</div>
""", unsafe_allow_html=True)

if "history" not in st.session_state:
    st.session_state.history = []

def avg(vectors):
    return [sum(x)/len(x) for x in zip(*vectors)]

def normalized_distance(a, b):
    raw = sqrt(sum((x-y)**2 for x,y in zip(a,b)))
    return raw / sqrt(6 * 100**2)

def anti_score(a, b):
    d = normalized_distance(a,b)
    return round(max(35, min(99, 38 + d*82)))

def label(score):
    if score >= 90: return "Extreme departure"
    if score >= 80: return "Very unfamiliar"
    if score >= 70: return "Outside your pattern"
    if score >= 60: return "Meaningfully different"
    return "Some overlap"

def build_results(category, user_vector):
    axes = AXES[category]
    out = []
    for item in CATALOG[category]:
        diffs = []
        for axis,u,v in zip(axes,user_vector,item["vector"]):
            diffs.append({"Dimension":axis,"You":round(u),"Recommendation":round(v),"Gap":round(abs(u-v))})
        diffs.sort(key=lambda r:r["Gap"], reverse=True)
        out.append({**item,"score":anti_score(user_vector,item["vector"]),"diffs":diffs})
    out.sort(key=lambda r:(-r["score"], r["title"]))
    return out

discover, shift, explain = st.tabs(["🧭 Discover", "📈 Taste Shift", "🧠 How It Works"])

with discover:
    st.subheader("Step 1 — Build your normal pattern")
    category = st.selectbox("Category", list(PREFERENCE_VECTORS.keys()))
    choices = list(PREFERENCE_VECTORS[category].keys())
    selected = st.multiselect(
        "What do you normally choose?",
        choices,
        default=choices[:3],
        help="Choose 1–5 items that genuinely represent your usual taste."
    )

    if not selected:
        st.warning("Choose at least one preference.")
    else:
        user_vector = avg([PREFERENCE_VECTORS[category][x] for x in selected])

        st.markdown("### Your taste profile")
        profile = sorted(zip(AXES[category], user_vector), key=lambda x:x[1], reverse=True)
        c1,c2,c3 = st.columns(3)
        for col,(axis,value) in zip([c1,c2,c3], profile[:3]):
            col.metric(axis, f"{round(value)}/100")

        with st.expander("See full profile"):
            st.dataframe(pd.DataFrame({
                "Dimension": AXES[category],
                "Your score": [round(v) for v in user_vector]
            }), use_container_width=True, hide_index=True)

        st.divider()
        st.subheader("Step 2 — Find what is furthest from you")
        count = st.slider("Number of anti-recommendations", 1, 5, 3)

        if st.button("🪞 Generate my Anti-Algorithm results", type="primary", use_container_width=True):
            st.session_state.last = {
                "category": category,
                "selected": selected,
                "user_vector": user_vector,
                "results": build_results(category,user_vector)[:count]
            }

    if "last" in st.session_state:
        last = st.session_state.last
        top = last["results"][0]

        st.divider()
        st.subheader("Your result")
        a,b,c = st.columns(3)
        a.metric("Anti-match score", f"{top['score']}/100")
        b.metric("Distance level", label(top["score"]))
        c.metric("Based on", f"{len(last['selected'])} preferences")
        st.progress(top["score"]/100)

        st.markdown(f"""
        <div class="card">
          <div class="kicker">TOP ANTI-RECOMMENDATION</div>
          <div class="top-title">{top["title"]}</div>
          <b>Why it is unusual for you:</b><br>{top["why"]}
        </div>
        """, unsafe_allow_html=True)

        st.markdown("### Why this result is different from your taste")
        st.dataframe(pd.DataFrame(top["diffs"][:3]), use_container_width=True, hide_index=True)

        strongest = top["diffs"][0]
        st.success(
            f"Biggest contrast: **{strongest['Dimension']}** — you are {strongest['You']}/100, "
            f"while **{top['title']}** is {strongest['Recommendation']}/100."
        )

        st.markdown("### Ranked anti-recommendations")
        ranking = []
        for i,item in enumerate(last["results"],1):
            ranking.append({
                "Rank":i,
                "Recommendation":item["title"],
                "Anti-match score":item["score"],
                "Distance":label(item["score"]),
                "Biggest contrast":item["diffs"][0]["Dimension"]
            })
        st.dataframe(pd.DataFrame(ranking), use_container_width=True, hide_index=True)

        st.caption("Higher Anti-match score = farther from your average preference profile.")

        st.divider()
        st.subheader("Step 3 — Did it change your mind?")
        reaction = st.radio("Your reaction", [
            "I would still never choose it",
            "I am curious enough to try it",
            "I tried it and liked it",
            "I tried it and still disliked it",
        ])
        if st.button("Save reaction"):
            st.session_state.history.append({
                "time":datetime.now().strftime("%H:%M:%S"),
                "category":last["category"],
                "usual_choices":", ".join(last["selected"]),
                "recommendation":top["title"],
                "anti_match":top["score"],
                "reaction":reaction
            })
            st.success("Saved. Open Taste Shift to see the trend.")

with shift:
    st.subheader("Taste Shift Tracker")
    st.write("Track whether unfamiliar recommendations start becoming interesting.")
    if not st.session_state.history:
        st.info("No reactions saved yet.")
    else:
        df = pd.DataFrame(st.session_state.history)
        total = len(df)
        curious = df["reaction"].isin(["I am curious enough to try it","I tried it and liked it"]).sum()
        liked = (df["reaction"]=="I tried it and liked it").sum()
        c1,c2,c3 = st.columns(3)
        c1.metric("Challenges recorded", total)
        c2.metric("Curiosity / openness", int(curious))
        c3.metric("Unexpected likes", int(liked))
        flexibility = round(curious/total*100)
        st.markdown("### Taste flexibility score")
        st.progress(flexibility/100)
        st.write(f"**{flexibility}/100**")
        st.dataframe(df,use_container_width=True,hide_index=True)

with explain:
    st.subheader("How the Anti-Algorithm works")
    st.markdown("""
**1. Build a profile** — your normal choices are converted into six visible dimensions.  
**2. Measure distance** — the app compares your profile with every candidate.  
**3. Rank the opposite** — the most distant options appear first.  
**4. Explain the result** — the biggest dimension gaps are shown clearly.  
**5. Track taste change** — your reactions measure curiosity and unexpected likes.
""")
    st.markdown("### Why this version is stronger")
    st.markdown("""
- Different recommendations receive **different scores**
- Every score comes from **visible dimensions**
- The result includes a **comparison table**
- The app shows the **biggest contrast**
- The interface is divided into clear steps
- Taste changes are tracked over time
""")
    st.info("Portfolio prototype: the dataset is curated and the scoring is transparent and explainable.")

st.divider()
st.caption("Portfolio prototype • Python • Streamlit • Explainable distance-based recommendation")
