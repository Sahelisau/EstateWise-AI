from html import escape

import streamlit as st

from src.predict import known_categories, predict_price
from ui.components import empty_state, footer, hero, inr, section
from ui.data import load_clean_data, load_csv


def render(model, metadata, model_error):
    hero("Property valuation", "Build a profile from the fields represented in the training data, then review the trained model’s asking-price estimate.", "Machine-learning estimate")
    if model is None:
        st.error(model_error or "The trained model could not be loaded.")
        st.code("python -m src.train\nstreamlit run app.py", language="powershell")
        return

    categories = known_categories(model)
    data = load_clean_data()
    importance = load_csv("feature_importance.csv")
    default_area = float(data.area_sqft.median())
    default_beds = int(round(data.bedrooms.median()))
    result_key = "estatewise_last_prediction"

    with st.form("predictor_form"):
        section("01 · Location", "Choose a supported city from the training data.")
        city = st.selectbox("City", sorted(categories["city"]))

        section("02 · Property configuration", "These details match the available flat-listing fields.")
        beds, baths, balconies = st.columns(3)
        bedrooms = beds.number_input("Bedrooms", min_value=1, max_value=10, value=max(1, min(default_beds, 10)), step=1)
        bathrooms = baths.number_input("Bathrooms", min_value=1.0, max_value=10.0, value=2.0, step=.5)
        balcony = balconies.number_input("Balconies", min_value=0, max_value=10, value=1, step=1)

        section("03 · Area and dimensions", "The model accepts square feet and the area basis recorded in the source.")
        area_col, basis_col = st.columns([1.3, 1])
        area_sqft = area_col.number_input("Property area · sq. ft.", min_value=100.0, max_value=20_000.0, value=max(100.0, min(default_area, 20_000.0)), step=50.0)
        area_basis = basis_col.selectbox("Area basis", categories["area_basis"])

        section("04 · Listing features", "Select the closest supported listing values.")
        furnishing, facing = st.columns(2)
        furnished = furnishing.selectbox("Furnishing", categories["furnishing"])
        direction = facing.selectbox("Facing", categories["facing"])
        outlook = st.selectbox("Overlooking", categories["overlooking"])
        owner, transaction = st.columns(2)
        ownership = owner.selectbox("Ownership", categories["ownership"])
        sale_type = transaction.selectbox("Transaction", categories["transaction"])
        submitted = st.form_submit_button("Generate valuation", type="primary", use_container_width=True)

    if submitted:
        values = {
            "city": city, "area_sqft": area_sqft, "area_basis": area_basis, "bedrooms": bedrooms,
            "bathrooms": bathrooms, "balconies": balcony, "furnishing": furnished, "facing": direction,
            "overlooking": outlook, "ownership": ownership, "transaction": sale_type,
        }
        try:
            with st.spinner("Running the saved EstateWise model…"):
                estimate = predict_price(model, values)
            st.session_state[result_key] = {"estimate": estimate, "area": area_sqft, "values": values}
        except ValueError as error:
            st.error(str(error))

    result = st.session_state.get(result_key)
    if result:
        details = result["values"]
        section("Valuation summary", "Estimate generated from the saved Random Forest pipeline.")
        left, right = st.columns([1.2, 1], gap="large")
        with left:
            st.markdown(
                f'<div class="ew-result"><div class="ew-kicker">ESTIMATED ASKING PRICE</div>'
                f'<div class="ew-result-value">{inr(result["estimate"], compact=False)}</div>'
                f'<div class="ew-muted">{escape(details["city"].replace("-", " ").title())} · {result["area"]:,.0f} sq. ft. · {details["bedrooms"]} bedrooms</div></div>',
                unsafe_allow_html=True,
            )
            st.metric("Estimated asking price per sq. ft.", inr(result["estimate"] / result["area"], compact=False))
        with right:
            section("Property profile")
            profile = f"**{details['city'].replace('-', ' ').title()}**  ·  {details['bedrooms']} bed / {details['bathrooms']:g} bath\n\n{result['area']:,.0f} sq. ft. · {details['area_basis']}\n\n{details['furnishing']} · {details['facing']} facing"
            st.markdown(profile)
            st.caption(f"Model: {metadata['model_name']} · trained {metadata['trained_at_utc'][:10]}")
        st.warning("This is an estimate from historical asking-price listings, not a live quote or official valuation. The model does not provide a calibrated price range.")
        if not importance.empty:
            section("What the model learned", "Global Random Forest feature importance. These are not individualized or causal explanations.")
            st.dataframe(importance.head(5), hide_index=True, use_container_width=True)
    else:
        empty_state("Your valuation will appear here", "Complete the property profile above and choose Generate valuation.")

    st.caption("The source contains flats only. It has no structured locality, property age, or dedicated amenity features, so those fields are not used.")
    footer()
