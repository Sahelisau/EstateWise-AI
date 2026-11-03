import plotly.express as px
import streamlit as st

from ui.charts import style
from ui.components import footer, hero, inr, metric_card, section
from ui.data import load_clean_data


def render():
    data = load_clean_data()
    hero("Explore locations", "Compare city-level price profiles in the historical flat-listing sample. Search the city selector by typing a location name.", "City intelligence")
    cities = sorted(data.city.dropna().unique())
    selected = st.selectbox("Search and select a city", cities)
    city_data = data[data.city.eq(selected)]
    summary = [
        ("Median asking price", inr(city_data.price_inr.median()), "Historical records"),
        ("Median per sq. ft.", inr(city_data.price_per_sqft.median(), compact=False), "Derived from price and area"),
        ("Median area", f"{city_data.area_sqft.median():,.0f} sq. ft.", "Selected carpet or super area"),
        ("Records", f"{len(city_data):,}", "Cleaned city sample"),
    ]
    cols = st.columns(4)
    for col, (label, value, note) in zip(cols, summary):
        with col:
            metric_card(label, value, note)

    left, right = st.columns([1.15, 1], gap="large")
    with left:
        section(f"Asking prices in {selected.replace('-', ' ').title()}", "Log scale helps show both typical and high-value records.")
        fig = px.histogram(city_data, x="price_inr", nbins=36, color_discrete_sequence=["#087F5B"], labels={"price_inr": "Asking price (INR)", "count": "Records"})
        fig.update_xaxes(type="log", tickprefix="₹", tickformat="~s")
        st.plotly_chart(style(fig, 360), use_container_width=True, config={"displayModeBar": False})
    with right:
        section("Price by furnishing", "Median asking price for furnishing categories in the selected city.")
        furnishing = city_data.groupby("furnishing", dropna=False).agg(records=("price_inr", "size"), median_price=("price_inr", "median")).reset_index()
        furnishing["furnishing"] = furnishing.furnishing.fillna("Not recorded")
        furnishing = furnishing.query("records >= 10").sort_values("median_price")
        fig = px.bar(furnishing, x="median_price", y="furnishing", orientation="h", color_discrete_sequence=["#547BA8"], hover_data={"records": ":,", "median_price": ":,.0f"}, labels={"median_price": "Median asking price (INR)", "furnishing": "Furnishing", "records": "Records"})
        fig.update_xaxes(tickprefix="₹", tickformat="~s")
        st.plotly_chart(style(fig, 360), use_container_width=True, config={"displayModeBar": False})

    section("Compare city profiles", "Only cities with at least 30 records are included. A larger bubble indicates a larger sample.")
    comparison = data.groupby("city").agg(records=("price_inr", "size"), median_price=("price_inr", "median"), median_rate=("price_per_sqft", "median"), median_area=("area_sqft", "median")).query("records >= 30").reset_index()
    fig = px.scatter(comparison, x="median_price", y="median_rate", size="records", color="median_area", hover_name="city", hover_data={"records": ":,", "median_price": ":,.0f", "median_rate": ":,.0f", "median_area": ":,.0f"}, color_continuous_scale=["#D7E8E0", "#087F5B"], labels={"median_price": "Median asking price (INR)", "median_rate": "Median per sq. ft. (INR)", "median_area": "Median area (sq. ft.)", "records": "Records"})
    fig.update_xaxes(type="log", tickprefix="₹", tickformat="~s")
    fig.update_yaxes(type="log", tickprefix="₹", tickformat="~s")
    st.plotly_chart(style(fig, 420), use_container_width=True, config={"displayModeBar": False})
    st.caption("City medians reflect each sample’s property mix. They are not current market quotes or live availability counts.")
    footer()
