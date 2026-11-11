import plotly.express as px
import streamlit as st

from ui.charts import style
from ui.components import empty_state, footer, hero, inr, metric_card, section
from ui.data import load_csv, load_json


def render(metadata):
    hero("Model performance", "See how each regression model performed in validation and on the held-out test set. The test split was reserved for final evaluation.", "Model transparency")
    comparison = load_csv("model_comparison.csv")
    metrics = load_json("test_metrics.json")
    importance = load_csv("feature_importance.csv")
    predictions = load_csv("test_predictions.csv")
    if comparison.empty or not metrics:
        empty_state("Training results are unavailable", "Run `python -m src.train` to create the model comparison and evaluation results.", "warning")
        return

    model_name = metadata.get("model_name", metrics.get("model_name", "Unknown"))
    selected = comparison[comparison.model.eq(model_name)]
    cv_rmse = inr(selected.iloc[0].cv_rmse) if not selected.empty else "Unavailable"
    st.markdown(f'<div class="ew-pill">SELECTED · {model_name}</div>', unsafe_allow_html=True)
    a, b, c, d = st.columns(4)
    with a: metric_card("Test MAE", inr(metrics["mae"]), "Mean absolute error")
    with b: metric_card("Test RMSE", inr(metrics["rmse"]), "Larger misses have more weight")
    with c: metric_card("Test R²", f"{metrics['r2']:.3f}", "Held-out 20% split")
    with d: metric_card("Selected CV RMSE", cv_rmse, "Lowest validation RMSE")
    st.caption(f"Trained {metadata.get('trained_at_utc', 'date unavailable')} · Dataset fingerprint {metadata.get('dataset_sha256', 'unavailable')[:12]}…")

    section("Model comparison", "Cross-validation scores were calculated on the training split. Test results were kept separate from model selection.")
    display = comparison.copy()
    st.dataframe(display, hide_index=True, use_container_width=True, column_config={
        "cv_mae": st.column_config.NumberColumn("CV MAE · INR", format="₹%.0f"),
        "cv_rmse": st.column_config.NumberColumn("CV RMSE · INR", format="₹%.0f"),
        "cv_rmse_std": st.column_config.NumberColumn("CV RMSE spread · INR", format="₹%.0f"),
        "test_mae": st.column_config.NumberColumn("Test MAE · INR", format="₹%.0f"),
        "test_rmse": st.column_config.NumberColumn("Test RMSE · INR", format="₹%.0f"),
        "cv_r2": st.column_config.NumberColumn("CV R²", format="%.3f"),
        "test_r2": st.column_config.NumberColumn("Test R²", format="%.3f"),
    })
    chart_data = comparison.sort_values("cv_rmse").copy()
    chart_data["selection"] = chart_data.model.eq(model_name).map({True: "Selected", False: "Other models"})
    fig = px.bar(chart_data, x="cv_rmse", y="model", orientation="h", color="selection", color_discrete_map={"Selected": "#087F5B", "Other models": "#B7C8D8"}, hover_data={"cv_mae": ":,.0f", "cv_r2": ":.3f"}, labels={"cv_rmse": "Cross-validation RMSE (INR)", "model": "Model", "selection": "Selection"})
    fig.update_xaxes(tickprefix="₹", tickformat="~s")
    st.plotly_chart(style(fig, 390), use_container_width=True, config={"displayModeBar": False})

    left, right = st.columns(2, gap="large")
    if not predictions.empty:
        predictions = predictions.copy()
        predictions["residual_inr"] = predictions.actual - predictions.predicted
        with left:
            section("Actual vs predicted", "Points closer to the diagonal are more accurate.")
            sample = predictions.sample(min(4_000, len(predictions)), random_state=42)
            fig = px.scatter(sample, x="actual", y="predicted", opacity=.45, labels={"actual": "Actual asking price (INR)", "predicted": "Predicted asking price (INR)"}, color_discrete_sequence=["#087F5B"])
            fig.update_xaxes(type="log", tickprefix="₹", tickformat="~s")
            fig.update_yaxes(type="log", tickprefix="₹", tickformat="~s")
            st.plotly_chart(style(fig, 360), use_container_width=True, config={"displayModeBar": False})
        with right:
            section("Prediction residuals", "Actual minus predicted. A balanced cloud around zero is preferred.")
            sample = predictions.sample(min(4_000, len(predictions)), random_state=24)
            fig = px.scatter(sample, x="predicted", y="residual_inr", opacity=.42, labels={"predicted": "Predicted asking price (INR)", "residual_inr": "Residual (INR)"}, color_discrete_sequence=["#547BA8"])
            fig.add_hline(y=0, line_dash="dash", line_color="#98A4B0")
            fig.update_xaxes(type="log", tickprefix="₹", tickformat="~s")
            fig.update_yaxes(tickprefix="₹", tickformat="~s")
            st.plotly_chart(style(fig, 360), use_container_width=True, config={"displayModeBar": False})

    if not importance.empty:
        section("Feature importance", "Global impurity-based importance from the selected tree model; it does not show causality or explain one prediction.")
        top = importance.head(12).sort_values("importance")
        fig = px.bar(top, x="importance", y="feature", orientation="h", color_discrete_sequence=["#547BA8"], labels={"importance": "Relative importance", "feature": "Transformed feature"})
        st.plotly_chart(style(fig, max(350, len(top) * 28)), use_container_width=True, config={"displayModeBar": False})
    st.markdown('<div class="ew-insight">Random Forest was selected using the lowest cross-validation RMSE. Its held-out errors are still large, so treat each estimate as an educational reference rather than a valuation.</div>', unsafe_allow_html=True)
    footer()
