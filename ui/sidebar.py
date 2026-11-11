import streamlit as st

from ui.components import brand


PAGES = [
    "Overview", "Property Predictor", "Explore Locations", "Recommendations",
    "Market Insights", "Future Forecast", "Buy vs Wait", "Model Performance", "About EstateWise",
]

NAV_LABELS = {
    "Overview": "◫   Overview",
    "Property Predictor": "⌂   Property Valuation",
    "Explore Locations": "⌖   Explore Locations",
    "Recommendations": "✦   Recommendations",
    "Market Insights": "▥   Market Insights",
    "Future Forecast": "↗   Future Forecast",
    "Buy vs Wait": "⇄   Buy vs Wait",
    "Model Performance": "⌁   Model Performance",
    "About EstateWise": "ⓘ   About Project",
}


def render_sidebar(model_metadata=None):
    with st.sidebar:
        brand()
        st.markdown("<div class='ew-kicker' style='padding:.2rem .7rem'>WORKSPACE</div>", unsafe_allow_html=True)
        target = st.session_state.pop("_next_page", None)
        if target in PAGES:
            st.session_state["page_choice"] = target
        page = st.radio("Workspace", PAGES, format_func=NAV_LABELS.get, label_visibility="collapsed", key="page_choice")
        st.markdown("<div class='ew-divider'></div>", unsafe_allow_html=True)
        st.caption("DATA COVERAGE")
        st.markdown("**India · Residential flats**")
        st.caption("Historical listing sample · City level")
        return page
