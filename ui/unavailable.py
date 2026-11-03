import streamlit as st

from ui.components import footer, hero, section


def forecast():
    hero("Future forecast", "A forecast needs a dated sequence of market observations. The property dataset is a single listing snapshot, so EstateWise does not generate future values from it.", "Forecasting unavailable")
    section("What is missing", "No fabricated forecasts or appreciation rates are shown.")
    a, b = st.columns(2)
    with a:
        st.markdown('<div class="ew-card"><div class="ew-section-title">Needed for a defensible forecast</div><div class="ew-divider"></div><div class="ew-muted">• Dated city or locality price observations<br>• Enough regular periods for chronological validation<br>• A separate inflation series for real-price comparisons, if needed</div></div>', unsafe_allow_html=True)
    with b:
        st.markdown('<div class="ew-card"><div class="ew-section-title">Available today</div><div class="ew-divider"></div><div class="ew-muted">• Historical asking-price records without listing dates<br>• City-level categories, but no structured locality<br>• A cross-sectional regression model for current-profile estimates</div></div>', unsafe_allow_html=True)
    st.caption("The RBI House Price Index can support a separate city-level trend study once its dated data is added and inspected. An index forecast would not be a prediction for an individual property.")
    footer()


def buy_vs_wait():
    hero("Buy today or wait?", "EstateWise cannot compare these scenarios responsibly until a supported future price forecast and financing assumptions are available.", "Scenario analysis unavailable")
    section("Why no comparison is shown", "A current model estimate and a future forecast answer different questions.")
    left, right = st.columns(2)
    with left:
        st.markdown('<div class="ew-card"><div class="ew-kicker">BUY TODAY</div><div class="ew-section-title">Property estimate available</div><div class="ew-divider"></div><div class="ew-muted">Use Property Predictor for a model estimate based on historical asking-price records. It is not an offer or official valuation.</div></div>', unsafe_allow_html=True)
    with right:
        st.markdown('<div class="ew-card"><div class="ew-kicker">BUY LATER</div><div class="ew-section-title">Future value unavailable</div><div class="ew-divider"></div><div class="ew-muted">There is no dated housing-price series, calibrated forecast interval, mortgage rate, transaction cost, or investment-return assumption in the project data.</div></div>', unsafe_allow_html=True)
    section("How to interpret this", "A future price scenario would depend on market behavior and financing choices that this dataset does not measure. No investment recommendation is implied.")
    footer()
