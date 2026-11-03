import streamlit as st

from ui.components import brand


PAGES = [
    "Overview",
    "Property Predictor",
    "Explore Locations",
    "Recommendations",
    "Market Insights",
    "Future Forecast",
    "Buy vs Wait",
    "Model Performance",
    "About EstateWise",
]


def render_sidebar(model_metadata=None):
    with st.sidebar:
        brand()
        target = st.session_state.pop("_next_page", None)
        if target in PAGES:
            st.session_state["page_choice"] = target
        page = st.radio("Workspace", PAGES, label_visibility="collapsed", key="page_choice")
        st.markdown("<div class='ew-divider'></div>", unsafe_allow_html=True)
        st.caption("MODEL STATUS")
        if model_metadata:
            st.markdown(f"**{model_metadata['model_name']}**")
            st.caption(f"Loaded · {model_metadata['trained_at_utc'][:10]}")
        else:
            st.warning("Model artifact unavailable")
        st.markdown("<div class='ew-divider'></div>", unsafe_allow_html=True)
        st.caption("INDIA · RESIDENTIAL FLATS")
    return page
