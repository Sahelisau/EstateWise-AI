import plotly.express as px
import streamlit as st

from ui.charts import city_medians, style
from ui.components import empty_state, footer, hero, inr, metric_card, navigate_button, section
from ui.data import load_clean_data


def render():
    data = load_clean_data()
    hero("A clearer view of the Indian housing market.", "Explore historical flat listings, compare city-level profiles, and get a machine-learning estimate grounded in the data EstateWise actually has.", "Property intelligence · India")

    _, action = st.columns([3.2, 1])
    with action:
        navigate_button("Start a valuation  →", "Property Predictor", "go_predict")

    stats = [
        ("Average asking price", inr(data.price_inr.mean()), "Mean of cleaned records"),
        ("Median asking price", inr(data.price_inr.median()), "Less affected by high outliers"),
        ("Average per sq. ft.", inr(data.price_per_sqft.mean(), compact=False), "Derived from asking price and area"),
        ("Supported locations", f"{data.city.nunique():,}", f"Across {len(data):,} historical flat records"),
    ]
    cols = st.columns([1.15, 1.15, 1.15, .95], gap="medium")
    for col, (label, value, note) in zip(cols, stats):
        with col:
            metric_card(label, value, note)
    st.caption("Coverage: city-level historical asking-price records. No listing dates, structured localities, or live availability feed.")

    left, right = st.columns([1.65, 1], gap="large")
    with left:
        section("What homes cost across cities", "Median asking price among cities with at least 30 records. Use this to compare samples, not current quotes.")
        st.plotly_chart(city_medians(data, 16), use_container_width=True, config={"displayModeBar": False})
    with right:
        section("Furnishing profile", "Share of records by the furnishing field supplied with each listing.")
        furnishing = data.furnishing.fillna("Not recorded").value_counts().rename_axis("furnishing").reset_index(name="records")
        fig = px.pie(furnishing, names="furnishing", values="records", hole=.64, color_discrete_sequence=["#087F5B", "#8CBFA9", "#A9BDD4", "#DDE5E8", "#D8B77D"])
        fig.update_traces(textposition="inside", textinfo="percent", hovertemplate="%{label}<br>%{value:,} records · %{percent}<extra></extra>")
        st.plotly_chart(style(fig, 340), use_container_width=True, config={"displayModeBar": False})

    section("A quick read on the sample", "These summaries describe the dataset snapshot, not a change over time.")
    low, high = data.price_inr.quantile([.25, .75])
    c1, c2 = st.columns([1, 1.5])
    with c1:
        metric_card("Middle half of asking prices", f"{inr(low)} – {inr(high)}", "25th to 75th percentile")
    with c2:
        st.markdown('<div class="ew-insight">EstateWise uses a trained Random Forest pipeline for estimates. The source is cross-sectional, so this dashboard does not show appreciation trends or current property availability.</div>', unsafe_allow_html=True)

    section("Explore the platform", "Choose the next step based on your question.")
    a, b, c = st.columns(3)
    with a:
        st.markdown('<div class="ew-card"><div class="ew-kicker">01 · ESTIMATE</div><div class="ew-section-title">Value a property</div><div class="ew-muted">Enter details supported by the trained model and review its estimate.</div></div>', unsafe_allow_html=True)
        navigate_button("Open valuation", "Property Predictor", "go_predict_2")
    with b:
        st.markdown('<div class="ew-card"><div class="ew-kicker">02 · COMPARE</div><div class="ew-section-title">Explore city profiles</div><div class="ew-muted">Compare price, area and record counts across supported locations.</div></div>', unsafe_allow_html=True)
        navigate_button("Explore locations", "Explore Locations", "go_explore")
    with c:
        st.markdown('<div class="ew-card"><div class="ew-kicker">03 · VALIDATE</div><div class="ew-section-title">Review model quality</div><div class="ew-muted">Inspect validation results, held-out errors and feature importance.</div></div>', unsafe_allow_html=True)
        navigate_button("View model results", "Model Performance", "go_model")
    footer()
