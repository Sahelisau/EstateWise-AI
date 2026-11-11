import plotly.express as px
import streamlit as st

from ui.charts import style
from ui.components import empty_state, footer, hero, section
from ui.data import load_clean_data


def find_profiles(data, city, budget, min_area, bedrooms):
    matches = data[data.price_inr.le(budget) & data.area_sqft.ge(min_area) & data.bedrooms.eq(bedrooms)]
    if city != "All cities":
        matches = matches[matches.city.eq(city)]
    return matches.groupby("city").agg(
        records=("price_inr", "size"), median_price_inr=("price_inr", "median"),
        median_price_per_sqft=("price_per_sqft", "median"), median_area_sqft=("area_sqft", "median"),
    ).reset_index()


def render():
    data = load_clean_data()
    hero("Find a city profile that fits", "Filter historical records by budget and property needs. Results describe matching city samples, not homes currently for sale.", "Transparent recommendations")
    with st.container(border=True):
        section("Set your requirements", "The dataset includes residential flats only.")
        with st.form("recommendation_filters"):
            a, b = st.columns(2)
            city = a.selectbox("Preferred city", ["All cities"] + sorted(data.city.unique()))
            budget = b.number_input("Maximum asking price · INR", min_value=100_000, value=10_000_000, step=500_000)
            c, d = st.columns(2)
            min_area = c.number_input("Minimum area · sq. ft.", min_value=100, value=900, step=50)
            bedrooms = d.selectbox("Bedrooms", list(range(1, 11)), index=2)
            st.caption("Property type: apartment / flat · only supported type")
            sort_by = st.selectbox("Rank city profiles by", ["Lowest median price", "Lowest price per sq. ft.", "Most matching records"])
            submitted = st.form_submit_button("Find matching profiles", type="primary", use_container_width=True)

    if submitted:
        profiles = find_profiles(data, city, budget, min_area, bedrooms)
        if profiles.empty:
            empty_state("No matching profiles", "Raise the budget, reduce the area requirement, or compare all cities.")
        else:
            sort_column = {"Lowest median price": "median_price_inr", "Lowest price per sq. ft.": "median_price_per_sqft", "Most matching records": "records"}[sort_by]
            profiles = profiles.sort_values(sort_column, ascending=sort_by != "Most matching records").head(12)
            profiles["city"] = profiles.city.str.replace("-", " ").str.title()
            section("Ranked city profiles", f"{len(profiles)} city samples meet the selected filters. Each result is based on records under budget with the requested bedroom count and area.")
            left, right = st.columns([1.2, 1], gap="large")
            with left:
                chart = px.bar(profiles.sort_values("median_price_inr"), x="median_price_inr", y="city", orientation="h", color_discrete_sequence=["#087F5B"], hover_data={"records": ":,", "median_price_per_sqft": ":,.0f", "median_area_sqft": ":,.0f"}, labels={"median_price_inr": "Median asking price (INR)", "city": "City", "records": "Matching records", "median_price_per_sqft": "Median per sq. ft. (INR)", "median_area_sqft": "Median area (sq. ft.)"})
                chart.update_xaxes(tickprefix="₹", tickformat="~s")
                st.plotly_chart(style(chart, max(360, len(profiles) * 34)), use_container_width=True, config={"displayModeBar": False})
            with right:
                st.dataframe(profiles.rename(columns={"city": "City", "records": "Matching records", "median_price_inr": "Median asking price · INR", "median_price_per_sqft": "Median per sq. ft. · INR", "median_area_sqft": "Median area · sq. ft."}), hide_index=True, use_container_width=True, column_config={"Median asking price · INR": st.column_config.NumberColumn(format="₹%.0f"), "Median per sq. ft. · INR": st.column_config.NumberColumn(format="₹%.0f")})
                st.markdown('<div class="ew-insight">Profiles are ranked on historical asking prices and record counts. No individual property recommendations, live availability, or appreciation scores are generated.</div>', unsafe_allow_html=True)
    footer()
