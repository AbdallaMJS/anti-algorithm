from datetime import datetime
from math import sqrt

import pandas as pd
import streamlit as st
from data import AXES, CATALOG, PREFERENCE_VECTORS

st.set_page_config(
    page_title="The Anti-Algorithm",
    page_icon="🪞",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown("""
<style>
:root{
  --bg:#070A12;
  --panel:#101625;
  --line:rgba(255,255,255,.09);
  --muted:#98A2B3;
  --violet:#8B5CF6;
  --cyan:#22D3EE;
  --pink:#F472B6;
}
.stApp{
  background:
    radial-gradient(circle at 8% 0%, rgba(139,92,246,.15), transparent 28%),
    radial-gradient(circle at 95% 8%, rgba(34,211,238,.09), transparent 24%),
    var(--bg);
}
.block-container{max-width:1220px;padding-top:1.5rem;padding-bottom:3rem;}
[data-testid="stSidebar"]{background:rgba(10,14,25,.98);border-right:1px solid var(--line);}
h1,h2,h3{letter-spacing:-.025em;}
.hero{border:1px solid var(--line);border-radius:26px;padding:1.7rem 1.8rem;background:linear-gradient(135deg,rgba(139,92,246,.16),rgba(34,211,238,.08));box-shadow:0 24px 70px rgba(0,0,0,.24);margin-bottom:1.15rem;}
.eyebrow{color:var(--cyan);font-size:.78rem;font-weight:850;letter-spacing:.15em;}
.hero h1{margin:.25rem 0 .45rem 0;font-size:3.15rem;line-height:1.02;}
.hero p{color:#CAD3DF;font-size:1.08rem;max-width:820px;margin:0;}
.sidebar-brand{padding:.45rem 0 .8rem 0;}
.sidebar-brand .mini{color:var(--cyan);font-size:.72rem;font-weight:850;letter-spacing:.14em;}
.sidebar-brand .name{font-size:1.48rem;font-weight:900;margin:.22rem 0;}
.sidebar-brand .desc{color:var(--muted);font-size:.86rem;}
.kpi{border:1px solid var(--line);border-radius:18px;padding:1rem 1.05rem;background:rgba(16,22,37,.82);min-height:118px;}
.kpi .label{color:var(--muted);font-size:.78rem;text-transform:uppercase;letter-spacing:.09em;}
.kpi .value{font-size:2.05rem;font-weight:900;margin:.32rem 0 .12rem 0;}
.kpi .sub{color:#BEC8D6;font-size:.82rem;}
.result-card{border:1px solid rgba(139,92,246,.32);border-radius:24px;padding:1.35rem 1.45rem;background:linear-gradient(145deg,rgba(139,92,246,.13),rgba(16,22,37,.88));min-height:190px;}
.result-card .label{color:#BCA7FF;font-size:.76rem;font-weight:850;letter-spacing:.12em;}
.result-card .title{font-size:2.35rem;line-height:1.08;font-weight:950;margin:.4rem 0 .5rem;}
.result-card .why{color:#D5DCE7;line-height:1.5;}
.badge{display:inline-block;margin-top:.7rem;padding:.22rem .58rem;border-radius:999px;border:1px solid rgba(139,92,246,.28);background:rgba(139,92,246,.13);color:#C4B5FD;font-size:.78rem;}
.scorebox{border:1px solid var(--line);border-radius:24px;padding:1.15rem;background:rgba(16,22,37,.82);min-height:190px;display:flex;align-items:center;justify-content:center;text-align:center;}
.scorebox .big{font-size:3.5rem;font-weight:950;color:var(--cyan);line-height:1;}
.scorebox .small{margin-top:.4rem;color:var(--muted);font-size:.77rem;letter-spacing:.1em;}
.compare{border:1px solid var(--line);border-radius:18px;padding:.95rem 1rem;background:rgba(16,22,37,.74);margin-bottom:.65rem;}
.compare-head{display:flex;justify-content:space-between;gap:12px;margin-bottom:.6rem;}
.compare-title{font-weight:850;}.compare-gap{font-weight:850;color:var(--pink);}
.track{height:9px;background:rgba(255,255,255,.07);border-radius:999px;overflow:hidden;margin:.22rem 0 .45rem;}
.you{height:100%;background:linear-gradient(90deg,#7C3AED,#A78BFA);border-radius:999px;}
.rec{height:100%;background:linear-gradient(90deg,#0891B2,#22D3EE);border-radius:999px;}
.legend{font-size:.76rem;color:var(--muted);}
.rank-card{border:1px solid var(--line);border-radius:16px;padding:.85rem 1rem;background:rgba(16,22,37,.66);margin-bottom:.55rem;}
.rank-row{display:flex;align-items:center;justify-content:space-between;gap:14px;}
.rank-name{font-weight:900;}.rank-score{font-weight:950;color:var(--cyan);}
.note{border-left:3px solid var(--cyan);border-radius:0 12px 12px 0;background:rgba(34,211,238,.07);padding:.82rem 1rem;color:#D4ECF2;}
hr{border-color:var(--line)!important;}
</style>
""", unsafe_allow_html=True)

if "history" not in st.session_state:
    st.session_state.history = []
if "last" not in st.session_state:
    st.session_state.last = None

def average_vector(vectors):
    return [sum(values) / len(values) for values in zip(*vectors)]

def normalized_distance(a, b):
    raw = sqrt(sum((x-y)**2 for x, y in zip(a, b)))
    return raw / sqrt(6 * (100 ** 2))

def anti_match_score(a, b):
    d = normalized_distance(a, b)
    return round(max(35, min(99, 38 + d * 82)))

def distance_label(score):
    if score >= 90:
        return "Extreme departure"
    if score >= 80:
        return "Very unfamiliar"
    if score >= 70:
        return "Outside your pattern"
    if score >= 60:
        return "Meaningfully different"
    return "Some overlap"

def build_results(category, user_vector):
    axes = AXES[category]
    rows = []
    for item in CATALOG[category]:
        diffs = []
        for axis, user_value, item_value in zip(axes, user_vector, item["vector"]):
            diffs.append({
                "Dimension": axis,
                "You": round(user_value),
                "Recommendation": round(item_value),
                "Gap": round(abs(user_value - item_value)),
            })
        diffs.sort(key=lambda x: x["Gap"], reverse=True)
        rows.append({
            **item,
            "score": anti_match_score(user_vector, item["vector"]),
            "diffs": diffs,
        })
    rows.sort(key=lambda x: (-x["score"], x["title"]))
    return rows

with st.sidebar:
    st.markdown("""
    <div class="sidebar-brand">
      <div class="mini">BREAK THE FEED</div>
      <div class="name">🪞 Anti-Algorithm</div>
      <div class="desc">An explainable discovery engine designed to move away from your usual taste.</div>
    </div>
    """, unsafe_allow_html=True)

    page = st.radio(
        "Navigate",
        ["Discover", "Taste Shift", "How it works"],
        label_visibility="collapsed",
    )

    if page == "Discover":
        st.divider()
        category = st.selectbox("Category", list(PREFERENCE_VECTORS.keys()))
        options = list(PREFERENCE_VECTORS[category].keys())
        selected = st.multiselect(
            "Your usual choices",
            options,
            default=options[:3],
            help="Pick the choices that best represent your normal taste.",
        )
        count = st.slider("How many opposite picks?", 1, 5, 3)

        if st.button("Generate opposites", type="primary", use_container_width=True):
            if not selected:
                st.warning("Choose at least one preference.")
            else:
                user_vector = average_vector(
                    [PREFERENCE_VECTORS[category][x] for x in selected]
                )
                st.session_state.last = {
                    "category": category,
                    "selected": selected,
                    "user_vector": user_vector,
                    "results": build_results(category, user_vector)[:count],
                }

if page == "Discover":
    st.markdown("""
    <div class="hero">
      <div class="eyebrow">ANTI-RECOMMENDATION ENGINE</div>
      <h1>Break your pattern.</h1>
      <p>Instead of predicting more of what you already like, this interface maps your taste and deliberately searches in the opposite direction.</p>
    </div>
    """, unsafe_allow_html=True)

    if st.session_state.last is None:
        st.markdown("### Start in the control panel")
        st.markdown(
            '<div class="note">Choose a category and your normal preferences in the left sidebar, then press <b>Generate opposites</b>.</div>',
            unsafe_allow_html=True,
        )
    else:
        last = st.session_state.last
        top = last["results"][0]
        profile = sorted(
            zip(AXES[last["category"]], last["user_vector"]),
            key=lambda x: x[1],
            reverse=True,
        )

        st.markdown("### Your taste signal")
        c1, c2, c3 = st.columns(3)
        for col, (axis, value) in zip([c1, c2, c3], profile[:3]):
            with col:
                st.markdown(
                    f'<div class="kpi"><div class="label">{axis}</div><div class="value">{round(value)}/100</div><div class="sub">Strong profile dimension</div></div>',
                    unsafe_allow_html=True,
                )

        st.write("")
        left, right = st.columns([1.7, .7])
        with left:
            st.markdown(
                f'<div class="result-card"><div class="label">TOP OPPOSITE PICK</div><div class="title">{top["title"]}</div><div class="why">{top["why"]}</div><div class="badge">{distance_label(top["score"])}</div></div>',
                unsafe_allow_html=True,
            )
        with right:
            st.markdown(
                f'<div class="scorebox"><div><div class="big">{top["score"]}</div><div class="small">ANTI-MATCH / 100</div></div></div>',
                unsafe_allow_html=True,
            )

        st.markdown("### Why it clashes with your normal taste")
        for d in top["diffs"][:3]:
            html = (
                '<div class="compare">'
                '<div class="compare-head">'
                f'<div class="compare-title">{d["Dimension"]}</div>'
                f'<div class="compare-gap">{d["Gap"]}-point gap</div>'
                '</div>'
                f'<div class="legend">You - {d["You"]}/100</div>'
                f'<div class="track"><div class="you" style="width:{d["You"]}%"></div></div>'
                f'<div class="legend">Recommendation - {d["Recommendation"]}/100</div>'
                f'<div class="track"><div class="rec" style="width:{d["Recommendation"]}%"></div></div>'
                '</div>'
            )
            st.markdown(html, unsafe_allow_html=True)

        st.markdown("### Other opposite directions")
        for i, item in enumerate(last["results"], 1):
            html = (
                '<div class="rank-card">'
                '<div class="rank-row">'
                f'<div class="rank-name">#{i} - {item["title"]}</div>'
                f'<div class="rank-score">{item["score"]}/100</div>'
                '</div>'
                f'<div class="badge">{distance_label(item["score"])} - Biggest contrast: {item["diffs"][0]["Dimension"]}</div>'
                '</div>'
            )
            st.markdown(html, unsafe_allow_html=True)

        st.markdown("### Would you cross the line?")
        reaction = st.radio(
            "Reaction",
            [
                "Still not for me",
                "I am curious enough to try it",
                "I tried it and liked it",
                "I tried it and still disliked it",
            ],
            horizontal=True,
            label_visibility="collapsed",
        )

        if st.button("Save reaction"):
            st.session_state.history.append({
                "time": datetime.now().strftime("%H:%M:%S"),
                "category": last["category"],
                "usual_choices": ", ".join(last["selected"]),
                "recommendation": top["title"],
                "anti_match": top["score"],
                "reaction": reaction,
            })
            st.success("Saved. Open Taste Shift from the sidebar.")

elif page == "Taste Shift":
    st.markdown("""
    <div class="hero">
      <div class="eyebrow">TASTE SHIFT TRACKER</div>
      <h1>Did the unfamiliar become interesting?</h1>
      <p>This view measures whether opposite recommendations create curiosity, rejection, or an unexpected new preference.</p>
    </div>
    """, unsafe_allow_html=True)

    if not st.session_state.history:
        st.markdown(
            '<div class="note">No reactions saved yet. Generate a result in Discover and save your reaction first.</div>',
            unsafe_allow_html=True,
        )
    else:
        df = pd.DataFrame(st.session_state.history)
        total = len(df)
        curious = df["reaction"].isin(
            ["I am curious enough to try it", "I tried it and liked it"]
        ).sum()
        liked = (df["reaction"] == "I tried it and liked it").sum()
        flexibility = round(curious / total * 100)

        c1, c2, c3 = st.columns(3)
        metrics = [
            ("Challenges", total, "Recorded taste challenges"),
            ("Openness", int(curious), "Curious or unexpectedly positive"),
            ("Unexpected likes", int(liked), "Opposite picks you liked"),
        ]
        for col, (label_text, value, sub) in zip([c1, c2, c3], metrics):
            with col:
                st.markdown(
                    f'<div class="kpi"><div class="label">{label_text}</div><div class="value">{value}</div><div class="sub">{sub}</div></div>',
                    unsafe_allow_html=True,
                )

        st.write("")
        st.markdown(
            f'<div class="result-card"><div class="label">TASTE FLEXIBILITY</div><div class="title">{flexibility}/100</div><div class="why">Share of opposite recommendations that made you curious or became an unexpected like.</div></div>',
            unsafe_allow_html=True,
        )
        if total < 3:
            suffix = "s" if total != 1 else ""
            st.caption(f"Early signal - based on only {total} recorded challenge{suffix}.")
        else:
            st.caption(f"Based on {total} recorded challenges.")

        st.markdown("### Reaction history")
        st.dataframe(df, use_container_width=True, hide_index=True)

else:
    st.markdown("""
    <div class="hero">
      <div class="eyebrow">EXPLAINABLE LOGIC</div>
      <h1>Not random. Not a black box.</h1>
      <p>The system converts preferences into visible dimensions, measures distance, then shows the largest reasons behind each opposite recommendation.</p>
    </div>
    """, unsafe_allow_html=True)

    a, b = st.columns(2)
    with a:
        st.markdown(
            '<div class="result-card"><div class="label">01 - PROFILE</div><div class="title" style="font-size:1.55rem">Map your normal taste</div><div class="why">Each selected preference contributes to six interpretable dimensions.</div></div>',
            unsafe_allow_html=True,
        )
        st.write("")
        st.markdown(
            '<div class="result-card"><div class="label">03 - EXPLAIN</div><div class="title" style="font-size:1.55rem">Show the biggest clashes</div><div class="why">The interface exposes the largest score gaps so the recommendation is understandable.</div></div>',
            unsafe_allow_html=True,
        )
    with b:
        st.markdown(
            '<div class="result-card"><div class="label">02 - DISTANCE</div><div class="title" style="font-size:1.55rem">Search away from similarity</div><div class="why">Normalized Euclidean distance compares your profile with every candidate.</div></div>',
            unsafe_allow_html=True,
        )
        st.write("")
        st.markdown(
            '<div class="result-card"><div class="label">04 - LEARN</div><div class="title" style="font-size:1.55rem">Track taste movement</div><div class="why">Saved reactions reveal whether unfamiliar choices create curiosity or unexpected likes.</div></div>',
            unsafe_allow_html=True,
        )

    st.markdown("### Prototype scope")
    st.markdown(
        '<div class="note">The current version uses a curated, transparent dataset. A production version could connect to external APIs while keeping the same explainable logic.</div>',
        unsafe_allow_html=True,
    )

st.divider()
st.caption("The Anti-Algorithm - Explainable distance-based recommendation - Python + Streamlit")
