import plotly.express as px
import streamlit as st

from ui.charts import city_medians, style
from ui.components import footer, hero, inr, metric_card, section
from ui.data import load_clean_data


def render():
    data = load_clean_data()
    hero("Market insights", "Explore the price distribution, area patterns and differences between city samples in this historical listing dataset.", "Cross-sectional analytics")
    st.info("The dataset has no listing dates. These charts compare records across places; they do not show price appreciation over time.")
    a, b, c = st.columns(3)
    with a: metric_card("Mean asking price", inr(data.price_inr.mean()), "Sensitive to high-price records")
    with b: metric_card("Median asking price", inr(data.price_inr.median()), "Retained dataset records")
    with c: metric_card("Median per sq. ft.", inr(data.price_per_sqft.median(), compact=False), "Derived rate")

    left, right = st.columns(2)
    with left:
        section("Price distribution", "Log scale keeps high-value records visible without hiding the main range.")
        fig = px.histogram(data, x="price_inr", nbins=50, color_discrete_sequence=["#36c9a5"], labels={"price_inr": "Asking price (INR)", "count": "Records"})
        fig.update_xaxes(type="log")
        st.plotly_chart(style(fig, 340), use_container_width=True, config={"displayModeBar": False})
    with right:
        section("Area and price per sq. ft.", "Price per sq. ft. is derived from asking price divided by selected area.")
        sample = data.sample(min(4_000, len(data)), random_state=7)
        fig = px.scatter(sample, x="area_sqft", y="price_per_sqft", color="area_basis", hover_data=["city", "bedrooms", "price_inr"], labels={"area_sqft": "Area (sq. ft.)", "price_per_sqft": "Derived price per sq. ft. (INR)", "area_basis": "Area basis"}, color_discrete_sequence=["#78a9ff", "#36c9a5"])
        fig.update_xaxes(type="log")
        fig.update_yaxes(type="log")
        st.plotly_chart(style(fig, 340), use_container_width=True, config={"displayModeBar": False})

    section("City median comparison", "Cities with fewer than 30 records are omitted from this chart.")
    st.plotly_chart(city_medians(data, 25), use_container_width=True, config={"displayModeBar": False})
    by_bedroom = data[data.bedrooms.notna()].groupby("bedrooms").agg(records=("price_inr", "size"), median_price=("price_inr", "median")).reset_index()
    by_bedroom = by_bedroom[by_bedroom.records >= 30]
    fig = px.bar(by_bedroom, x="bedrooms", y="median_price", color="median_price", color_continuous_scale=["#78a9ff", "#36c9a5"], hover_data={"records": ":,", "median_price": ":,.0f"}, labels={"bedrooms": "Bedrooms", "median_price": "Median asking price (INR)"})
    st.plotly_chart(style(fig, 330), use_container_width=True, config={"displayModeBar": False})
    st.caption("No sale dates, structured locality field, property-type variation, or CPI series were provided. Locality averages, historical trends, and inflation comparisons are not shown.")
    footer()
