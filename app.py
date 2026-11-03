import streamlit as st

from src.predict import load_artifacts
from ui.about import render as render_about
from ui.dashboard import render as render_dashboard
from ui.explore import render as render_explore
from ui.market_insights import render as render_market_insights
from ui.model_performance import render as render_model_performance
from ui.predictor import render as render_predictor
from ui.recommendations import render as render_recommendations
from ui.sidebar import render_sidebar
from ui.theme import apply_theme
from ui.unavailable import buy_vs_wait, forecast


st.set_page_config(page_title="EstateWise AI", page_icon="E", layout="wide", initial_sidebar_state="expanded")
apply_theme()


@st.cache_resource(show_spinner=False)
def get_model():
    return load_artifacts()


try:
    model, metadata = get_model()
    model_error = None
except (FileNotFoundError, ValueError, OSError) as error:
    model, metadata, model_error = None, None, str(error)

page = render_sidebar(metadata)
if model is None and page != "Property Predictor":
    st.warning("The trained model is unavailable. Prediction is disabled until you run `python -m src.train`.")

if page == "Overview":
    render_dashboard()
elif page == "Property Predictor":
    render_predictor(model, metadata or {}, model_error)
elif page == "Explore Locations":
    render_explore()
elif page == "Recommendations":
    render_recommendations()
elif page == "Market Insights":
    render_market_insights()
elif page == "Future Forecast":
    forecast()
elif page == "Buy vs Wait":
    buy_vs_wait()
elif page == "Model Performance":
    render_model_performance(metadata or {})
elif page == "About EstateWise":
    render_about()
