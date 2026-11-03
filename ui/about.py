import streamlit as st

from ui.components import footer, hero, metric_card, section
from ui.data import load_clean_data


def render():
    hero("About EstateWise AI", "An academic machine-learning project for asking-price estimation and transparent city-level property analysis.", "CSE570 · Machine Learning with Python")
    data = load_clean_data()
    a, b, c = st.columns(3)
    with a: metric_card("Cleaned records", f"{len(data):,}", "Retained for analysis and modeling")
    with b: metric_card("Location labels", f"{data.city.nunique():,}", "City-level categories")
    with c: metric_card("Supported property", "Residential flats", "The only type in the source dataset")

    section("What the platform does", "EstateWise is an end-to-end supervised regression project, not a live property marketplace.")
    left, right = st.columns([1.15, 1], gap="large")
    with left:
        st.markdown('<div class="ew-card"><div class="ew-section-title">From listing data to an estimate</div><div class="ew-divider"></div><div class="ew-muted"><b>01 · Prepare</b> — clean asking prices and property details while preserving the raw source.<br><br><b>02 · Explore</b> — inspect distributions, city samples, and relationships.<br><br><b>03 · Train</b> — compare regression models with preprocessing inside each pipeline.<br><br><b>04 · Evaluate</b> — select by cross-validation and report results on held-out data.<br><br><b>05 · Apply</b> — load the saved model in this Streamlit interface.</div></div>', unsafe_allow_html=True)
    with right:
        st.markdown('<div class="ew-card"><div class="ew-section-title">Data scope and limitations</div><div class="ew-divider"></div><div class="ew-muted">The primary dataset is a historical cross-sectional sample of flat asking prices. It has no listing dates, verified sale prices, structured localities, property age, dedicated amenity fields, or current inventory feed.<br><br>Results describe the supplied sample. They are not current market quotes, official valuations, or investment advice.</div></div>', unsafe_allow_html=True)
    section("Technology")
    st.markdown('<div class="ew-card"><div class="ew-muted">Python <span style="padding:0 8px">·</span> Pandas <span style="padding:0 8px">·</span> Scikit-learn <span style="padding:0 8px">·</span> Streamlit <span style="padding:0 8px">·</span> Plotly</div></div>', unsafe_allow_html=True)
    st.caption("Dataset source, attribution, reproducibility steps and model results are documented in the repository README and reports folder.")
    footer()
