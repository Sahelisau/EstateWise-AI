from html import escape

import streamlit as st

from src.predict import known_categories, predict_price
from ui.components import empty_state, footer, hero, inr, metric_card, section
from ui.data import load_csv


def render(model, metadata, model_error):
    hero("Property price predictor", "Estimate an asking price from the trained EstateWise model and the property details supported by its data.", "Machine learning estimate")
    if model is None:
        st.error(model_error or "The trained model could not be loaded.")
        st.code("python -m src.train\nstreamlit run app.py", language="powershell")
        return

    categories = known_categories(model)
    importance = load_csv("feature_importance.csv")
    left, right = st.columns([1.12, .88], gap="large")
    with left:
        section("Property profile", "All fields are based on columns represented in the training data.")
        with st.form("predictor_form"):
            city = st.selectbox("City", sorted(categories["city"]))
            area, basis = st.columns([1.2, 1])
            area_sqft = area.number_input("Area · sq. ft.", min_value=100.0, max_value=20_000.0, value=1_000.0, step=50.0)
            area_basis = basis.selectbox("Area measure", categories["area_basis"])
            beds, baths, balconies = st.columns(3)
            bedrooms = beds.number_input("Bedrooms", min_value=1, max_value=10, value=2, step=1)
            bathrooms = baths.number_input("Bathrooms", min_value=1.0, max_value=10.0, value=2.0, step=.5)
            balcony = balconies.number_input("Balconies", min_value=1, max_value=10, value=1, step=1)
            furnishing, facing = st.columns(2)
            furnished = furnishing.selectbox("Furnishing", categories["furnishing"])
            direction = facing.selectbox("Facing", categories["facing"])
            outlook = st.selectbox("Overlooking", categories["overlooking"])
            ownership, transaction = st.columns(2)
            owner = ownership.selectbox("Ownership", categories["ownership"])
            sale_type = transaction.selectbox("Transaction", categories["transaction"])
            submit = st.form_submit_button("Estimate property value", type="primary", use_container_width=True)

    with right:
        section("Estimate preview", "Your result stays in this browser session.")
        result_key = "estatewise_last_prediction"
        if submit:
            values = {
                "city": city,
                "area_sqft": area_sqft,
                "area_basis": area_basis,
                "bedrooms": bedrooms,
                "bathrooms": bathrooms,
                "balconies": balcony,
                "furnishing": furnished,
                "facing": direction,
                "overlooking": outlook,
                "ownership": owner,
                "transaction": sale_type,
            }
            try:
                with st.spinner("Estimating from the trained model..."):
                    estimate = predict_price(model, values)
                st.session_state[result_key] = {"estimate": estimate, "area": area_sqft, "values": values}
            except ValueError as error:
                st.error(str(error))

        result = st.session_state.get(result_key)
        if result:
            st.markdown(
                f'<div class="ew-result"><div class="ew-metric-label">Estimated property value</div>'
                f'<div class="ew-result-value">{inr(result["estimate"])}</div>'
                f'<div class="ew-muted">{escape(city.replace("-", " ").title())} · {result["area"]:,.0f} sq. ft. · {bedrooms} bedrooms</div></div>',
                unsafe_allow_html=True,
            )
            st.markdown("<div style='height:12px'></div>", unsafe_allow_html=True)
            metric_card("Estimated price per sq. ft.", inr(result["estimate"] / result["area"], compact=False), "Estimate divided by entered area")
            st.caption(f"Model: {metadata['model_name']} · trained {metadata['trained_at_utc'][:10]}")
            st.warning("This is a model estimate based on historical asking prices, not an official valuation or current offer. No calibrated prediction range is available.")
            if not importance.empty:
                section("Model signals", "Global feature importance; these are not personalized causal explanations.")
                st.dataframe(importance.head(5), hide_index=True, use_container_width=True)
        else:
            empty_state("Your estimate will appear here", "Enter a supported property profile and select Estimate property value.")

    st.info("The dataset contains flats only. It has no structured locality, property-age, or dedicated amenity fields, so those inputs are not shown.")
    footer()
