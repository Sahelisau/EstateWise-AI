import streamlit as st

from ui.components import footer, hero, section


def render():
    hero("About EstateWise AI", "An academic machine-learning project for real-estate price estimation and transparent city-level property analysis.", "CSE570 · Machine Learning with Python")
    left, right = st.columns(2)
    with left:
        section("What it does")
        st.markdown('<div class="ew-card"><div class="ew-muted">• Estimates asking prices with a trained Random Forest regression pipeline<br>• Compares city-level historical property profiles<br>• Shows held-out model metrics and feature importance<br>• Keeps model training separate from application startup</div></div>', unsafe_allow_html=True)
    with right:
        section("Data and scope")
        st.markdown('<div class="ew-card"><div class="ew-muted">The primary dataset contains flat listings across 81 India location categories, without listing dates or a structured locality field. Estimates reflect historical asking-price data and should not be treated as current listings or official valuations.</div></div>', unsafe_allow_html=True)
    section("Technology")
    st.markdown('<div class="ew-card"><div class="ew-muted">Python · Pandas · Scikit-learn · Streamlit · Plotly<br><br>Project documentation and data attribution are maintained in the repository README files.</div></div>', unsafe_allow_html=True)
    footer()
