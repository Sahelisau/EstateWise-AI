import plotly.express as px
import streamlit as st

from ui.charts import city_medians, style
from ui.components import footer, hero, inr, metric_card, section
from ui.data import load_clean_data


def render():
    data = load_clean_data()
    hero("Market insights", "A cross-sectional view of historical asking prices, property sizes and city samples. This dataset has no dates, so it cannot show price movement over time.", "Research and analytics")

    a, b, c = st.columns(3)
    with a: metric_card("Mean asking price", inr(data.price_inr.mean()), "Pulled upward by high-value records")
    with b: metric_card("Median asking price", inr(data.price_inr.median()), "Typical midpoint of the sample")
    with c: metric_card("Median per sq. ft.", inr(data.price_per_sqft.median(), compact=False), "Derived from asking price and area")

    st.markdown('<div class="ew-insight">The city comparison is statistically significant in the available sample (Kruskal–Wallis H = 18,106.751, p &lt; 0.001 across 76 cities with 30+ records). This compares distributions; property mix and source sampling can explain part of the difference.</div>', unsafe_allow_html=True)

    left, right = st.columns([1.15, 1], gap="large")
    with left:
        section("Asking price distribution", "Prices are right-skewed; the log scale keeps the common range readable.")
        fig = px.histogram(data, x="price_inr", nbins=52, color_discrete_sequence=["#087F5B"], labels={"price_inr": "Asking price (INR)", "count": "Records"})
        fig.update_xaxes(type="log", tickprefix="₹", tickformat="~s")
        st.plotly_chart(style(fig, 355), use_container_width=True, config={"displayModeBar": False})
    with right:
        section("Area and derived rate", "The per-square-foot measure is for analysis and is not a model input.")
        sample = data.sample(min(3_500, len(data)), random_state=7)
        fig = px.scatter(sample, x="area_sqft", y="price_per_sqft", color="area_basis", hover_data=["city", "bedrooms", "price_inr"], labels={"area_sqft": "Area (sq. ft.)", "price_per_sqft": "Derived price per sq. ft. (INR)", "area_basis": "Area basis"}, color_discrete_sequence=["#547BA8", "#087F5B"])
        fig.update_xaxes(type="log")
        fig.update_yaxes(type="log", tickprefix="₹", tickformat="~s")
        st.plotly_chart(style(fig, 355), use_container_width=True, config={"displayModeBar": False})

    section("How listing profiles differ", "Descriptive comparisons do not isolate the effect of any one property feature.")
    left, right = st.columns([1.4, 1], gap="large")
    with left:
        st.plotly_chart(city_medians(data, 24), use_container_width=True, config={"displayModeBar": False})
    with right:
        bedrooms = data.dropna(subset=["bedrooms"]).groupby("bedrooms").agg(records=("price_inr", "size"), median_price=("price_inr", "median")).query("records >= 30").reset_index()
        fig = px.bar(bedrooms, x="bedrooms", y="median_price", color_discrete_sequence=["#547BA8"], hover_data={"records": ":,", "median_price": ":,.0f"}, labels={"bedrooms": "Bedrooms", "median_price": "Median asking price (INR)", "records": "Records"})
        fig.update_yaxes(tickprefix="₹", tickformat="~s")
        st.plotly_chart(style(fig, 390), use_container_width=True, config={"displayModeBar": False})
    st.caption("The data contains asking prices rather than verified sale prices. It has no listing dates, standardized localities, property-type variation, or CPI series.")
    footer()
