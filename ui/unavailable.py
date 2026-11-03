import streamlit as st

from ui.components import footer, hero, navigate_button, section


def forecast():
    hero("Future forecast", "A reliable forecast requires dated market observations. The listing dataset is a single cross-sectional snapshot, so EstateWise does not project future prices.", "Research module · not available")
    left, right = st.columns([1.15, 1], gap="large")
    with left:
        section("What is needed", "A forecast can be added once suitable time-series data is inspected.")
        st.markdown('<div class="ew-card"><div class="ew-section-title">Forecast inputs</div><div class="ew-divider"></div><div class="ew-muted">Regular dated city or locality price observations<br><br>Enough periods for chronological validation<br><br>Uncertainty ranges that are evaluated out of sample</div></div>', unsafe_allow_html=True)
    with right:
        section("What EstateWise has today", "The current model answers a different question.")
        st.markdown('<div class="ew-card"><div class="ew-section-title">Available data</div><div class="ew-divider"></div><div class="ew-muted">Historical asking-price records without listing dates<br><br>City-level labels without a structured locality field<br><br>A cross-sectional regression model for property profiles</div></div>', unsafe_allow_html=True)
    st.markdown('<div class="ew-insight">An index forecast would describe a broad market series, not predict the price of an individual property. No future values or growth rates are fabricated here.</div>', unsafe_allow_html=True)
    st.caption("The RBI House Price Index may support a separate city-level trend study after its dated data is sourced, checked, and validated.")
    footer()


def buy_vs_wait():
    hero("Buy today or wait?", "Compare scenarios only when there is enough evidence to estimate future prices and financing costs. Those inputs are not available in this project dataset.", "Scenario analysis · not available")
    section("Why the comparison is unavailable", "A current listing estimate and a future-market forecast are different model outputs.")
    left, right = st.columns(2, gap="large")
    with left:
        st.markdown('<div class="ew-card"><div class="ew-kicker">BUY TODAY</div><div class="ew-section-title">Current profile estimate</div><div class="ew-divider"></div><div class="ew-muted">Use Property Valuation for an estimate based on historical asking-price records. It is not an offer, official valuation, or financing quote.</div></div>', unsafe_allow_html=True)
        navigate_button("Open property valuation", "Property Predictor", "buy_now_predict")
    with right:
        st.markdown('<div class="ew-card"><div class="ew-kicker">WAIT</div><div class="ew-section-title">Future price unavailable</div><div class="ew-divider"></div><div class="ew-muted">No dated housing-price series, calibrated forecast interval, mortgage rate, transaction cost, or investment-return assumption is included.</div></div>', unsafe_allow_html=True)
    section("Interpretation", "This educational project does not make a buy-or-wait recommendation. A complete comparison would require market, financing, and personal budget assumptions.")
    footer()
