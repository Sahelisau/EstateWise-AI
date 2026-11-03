import plotly.express as px
import streamlit as st

from ui.charts import style
from ui.components import footer, hero, inr, metric_card, section
from ui.data import load_clean_data


def render():
    data = load_clean_data()
    hero("Explore locations", "Review city-level asking-price profiles from the cleaned dataset. Localities are not separately structured in the source.", "City intelligence")
    cities = sorted(data["city"].unique())
    selected = st.selectbox("Choose a city", cities)
    city_data = data[data["city"].eq(selected)]
    a, b, c, d = st.columns(4)
    with a: metric_card("Median asking price", inr(city_data.price_inr.median()), "Historical records")
    with b: metric_card("Median per sq. ft.", inr(city_data.price_per_sqft.median(), compact=False), "Derived from asking price and area")
    with c: metric_card("Median area", f"{city_data.area_sqft.median():,.0f} sq. ft.", "Selected carpet or super area")
    with d: metric_card("Records", f"{len(city_data):,}", "Cleaned city sample")

    section("Distribution within the selected city", "The chart shows variation across records; it is not a time series.")
    fig = px.histogram(city_data, x="price_inr", nbins=35, color_discrete_sequence=["#78a9ff"], labels={"price_inr": "Asking price (INR)", "count": "Records"})
    fig.update_xaxes(type="log")
    st.plotly_chart(style(fig, 350), use_container_width=True, config={"displayModeBar": False})

    section("Compare cities", "Only cities with at least 30 records are included in the comparison.")
    comparison = data.groupby("city").agg(records=("price_inr", "size"), median_price=("price_inr", "median"), median_rate=("price_per_sqft", "median"), median_area=("area_sqft", "median")).query("records >= 30").sort_values("median_price").reset_index()
    fig = px.scatter(comparison, x="median_price", y="median_rate", size="records", color="median_area", hover_name="city", hover_data={"records": ":,", "median_price": ":,.0f", "median_rate": ":,.0f", "median_area": ":,.0f"}, color_continuous_scale=["#78a9ff", "#36c9a5"], labels={"median_price": "Median asking price (INR)", "median_rate": "Median price per sq. ft. (INR)", "median_area": "Median area (sq. ft.)", "records": "Records"})
    fig.update_xaxes(type="log")
    fig.update_yaxes(type="log")
    st.plotly_chart(style(fig, 390), use_container_width=True, config={"displayModeBar": False})
    st.caption("City medians are influenced by the property mix in each sample and do not represent current market quotes.")
    footer()
