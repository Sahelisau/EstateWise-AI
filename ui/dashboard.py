import plotly.express as px
import streamlit as st

from ui.charts import city_medians, style
from ui.components import empty_state, footer, hero, inr, metric_card, navigate_button, section
from ui.data import load_clean_data


def render():
    data = load_clean_data()
    hero(
        "Your next property decision starts here.",
        "Estimate asking prices, compare city-level property profiles and understand how the EstateWise model performs.",
        "Discover smarter · Invest better · Live better",
    )

    avg_price = data["price_inr"].mean()
    avg_rate = data["price_per_sqft"].mean()
    median_price = data["price_inr"].median()
    median_city = data.groupby("city")["price_inr"].agg(["median", "size"]).query("size >= 30")["median"].idxmin()
    median_city_price = data.groupby("city")["price_inr"].median().loc[median_city]

    section("Market snapshot", "Computed from cleaned historical asking-price records; not a live inventory feed.")
    cols = st.columns(4)
    with cols[0]: metric_card("Average asking price", inr(avg_price), "Mean of retained records")
    with cols[1]: metric_card("Average per sq. ft.", inr(avg_rate), "Derived from price and selected area")
    with cols[2]: metric_card("Dataset records", f"{len(data):,}", "Historical flat profiles")
    with cols[3]: metric_card("Lowest median city", inr(median_city_price), median_city.replace("-", " ").title())

    section("Find a city profile", "Filter the dataset by your budget and property needs. Results are historical records, not current listings.")
    cities = sorted(data["city"].dropna().unique())
    with st.form("overview_search"):
        a, b, c, d = st.columns([1.1, 1, 1, .8])
        city = a.selectbox("City", cities)
        budget = b.number_input("Maximum budget (INR)", min_value=100_000, value=10_000_000, step=500_000)
        min_area = c.number_input("Minimum area (sq. ft.)", min_value=100, value=900, step=50)
        bedrooms = d.selectbox("Bedrooms", list(range(1, 11)), index=2)
        submitted = st.form_submit_button("Search dataset", type="primary", use_container_width=True)
    st.caption("Locality isn’t available as a structured column in this dataset; the search is city-level.")
    if submitted:
        matches = data[
            data["city"].eq(city)
            & data["price_inr"].le(budget)
            & data["area_sqft"].ge(min_area)
            & data["bedrooms"].eq(bedrooms)
        ]
        if matches.empty:
            empty_state("No matching records", "Try a higher budget, smaller area, or a different bedroom count.")
        else:
            x, y = st.columns(2)
            with x: metric_card("Matching historical records", f"{len(matches):,}", f"{city.replace('-', ' ').title()} · {bedrooms} bedrooms")
            with y: metric_card("Median asking price", inr(matches["price_inr"].median()), "Historical records meeting these filters")

    section("City comparison", "Median asking prices for locations with at least 30 cleaned records.")
    st.plotly_chart(city_medians(data, 18), use_container_width=True, config={"displayModeBar": False})

    left, right = st.columns(2)
    with left:
        section("Price distribution", "Skewed values are shown on a log scale.")
        fig = px.histogram(data, x="price_inr", nbins=45, labels={"price_inr": "Asking price (INR)", "count": "Records"}, color_discrete_sequence=["#36c9a5"])
        fig.update_xaxes(type="log")
        st.plotly_chart(style(fig, 310), use_container_width=True, config={"displayModeBar": False})
    with right:
        section("Area and asking price", "Each point is a cleaned historical record.")
        sample = data.sample(min(2_500, len(data)), random_state=42)
        fig = px.scatter(sample, x="area_sqft", y="price_inr", color="area_basis", hover_data=["city", "bedrooms"], labels={"area_sqft": "Area (sq. ft.)", "price_inr": "Asking price (INR)", "area_basis": "Area basis"}, color_discrete_sequence=["#78a9ff", "#36c9a5"])
        fig.update_xaxes(type="log")
        fig.update_yaxes(type="log")
        st.plotly_chart(style(fig, 310), use_container_width=True, config={"displayModeBar": False})
    section("Continue exploring", "Open a focused workspace for your next step.")
    action_a, action_b, action_c = st.columns(3)
    with action_a: navigate_button("Estimate a property", "Property Predictor", "go_predict")
    with action_b: navigate_button("Explore city profiles", "Explore Locations", "go_explore")
    with action_c: navigate_button("View model results", "Model Performance", "go_model")
    footer()
