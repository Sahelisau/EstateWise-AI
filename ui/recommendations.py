from html import escape

import streamlit as st

from ui.components import empty_state, footer, hero, inr, section
from ui.data import load_clean_data


def find_profiles(data, city, budget, min_area, bedrooms):
    matches = data[
        data["price_inr"].le(budget)
        & data["area_sqft"].ge(min_area)
        & data["bedrooms"].eq(bedrooms)
    ]
    if city != "All cities":
        matches = matches[matches["city"].eq(city)]
    return matches.groupby("city").agg(
        records=("price_inr", "size"),
        median_price_inr=("price_inr", "median"),
        median_price_per_sqft=("price_per_sqft", "median"),
        median_area_sqft=("area_sqft", "median"),
    ).reset_index()


def render():
    data = load_clean_data()
    hero("Find a city profile that fits", "Compare historical property records by budget, area and bedroom count. Results are dataset matches, not properties currently listed for sale.", "Transparent recommendations")
    section("Set your requirements", "The source supports apartment / flat records only.")
    with st.form("recommendation_filters"):
        a, b = st.columns(2)
        city = a.selectbox("Preferred city", ["All cities"] + sorted(data.city.unique()))
        budget = b.number_input("Maximum budget · INR", min_value=100_000, value=10_000_000, step=500_000)
        c, d = st.columns(2)
        min_area = c.number_input("Minimum area · sq. ft.", min_value=100, value=900, step=50)
        bedrooms = d.selectbox("Bedrooms", list(range(1, 11)), index=2)
        st.selectbox("Property type", ["Apartment / flat · only type in dataset"])
        sort_by = st.selectbox("Sort results", ["Lowest median price", "Lowest price per sq. ft.", "Most matching records"])
        submitted = st.form_submit_button("Find matching profiles", type="primary", use_container_width=True)

    if submitted:
        profiles = find_profiles(data, city, budget, min_area, bedrooms)
        if profiles.empty:
            empty_state("No matching profiles found", "Try increasing your budget, lowering the area requirement, or selecting All cities.")
        else:
            sort_column = {
                "Lowest median price": "median_price_inr",
                "Lowest price per sq. ft.": "median_price_per_sqft",
                "Most matching records": "records",
            }[sort_by]
            profiles = profiles.sort_values(sort_column, ascending=sort_by != "Most matching records").head(12)
            section("Matching city profiles", f"{len(profiles)} city profiles match the selected filters.")
            for start in range(0, len(profiles), 3):
                cols = st.columns(3)
                for column, row in zip(cols, profiles.iloc[start:start + 3].itertuples(index=False)):
                    with column:
                        st.markdown(
                            f'<div class="ew-card"><div class="ew-kicker">CITY PROFILE</div>'
                            f'<div class="ew-section-title">{escape(row.city.replace("-", " ").title())}</div>'
                            f'<div class="ew-metric-value">{inr(row.median_price_inr)}</div>'
                            f'<div class="ew-muted">Median asking price · {row.records:,} matching records</div>'
                            f'<div class="ew-divider"></div><div class="ew-muted">{inr(row.median_price_per_sqft, compact=False)} / sq. ft. median<br>'
                            f'{row.median_area_sqft:,.0f} sq. ft. median area<br>Meets the selected budget and bedroom count.</div></div>',
                            unsafe_allow_html=True,
                        )
            st.caption("Ranking uses historical record medians and matching record counts. It does not indicate live supply, availability, or investment appreciation.")
    footer()
