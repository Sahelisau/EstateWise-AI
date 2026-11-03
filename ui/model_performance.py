import plotly.express as px
import streamlit as st

from ui.charts import style
from ui.components import empty_state, footer, hero, inr, metric_card, section
from ui.data import load_csv, load_json


def render(metadata):
    hero("Model performance", "Validation and held-out test results from the saved training run.", "Model transparency")
    comparison = load_csv("model_comparison.csv")
    metrics = load_json("test_metrics.json")
    importance = load_csv("feature_importance.csv")
    predictions = load_csv("test_predictions.csv")
    if comparison.empty or not metrics:
        empty_state("Training results are unavailable", "Run `python -m src.train` to create the model comparison and evaluation results.", "warning")
        return

    model_name = metadata.get("model_name", metrics.get("model_name", "Unknown"))
    cv = comparison.loc[comparison.model.eq(model_name)].iloc[0]
    a, b, c, d = st.columns(4)
    with a: metric_card("Selected model", model_name, "Chosen by cross-validation RMSE")
    with b: metric_card("Test MAE", inr(metrics["mae"]), "Mean absolute error")
    with c: metric_card("Test RMSE", inr(metrics["rmse"]), "Penalizes large errors more")
    with d: metric_card("Test R²", f"{metrics['r2']:.3f}", "Held-out 20% split")
    st.caption(f"Trained {metadata.get('trained_at_utc', 'date unavailable')} · Dataset SHA-256 {metadata.get('dataset_sha256', 'unavailable')[:12]}…")

    section("Model comparison", "Metrics are calculated in INR; CV scores use three shuffled folds from the training split.")
    st.dataframe(comparison, hide_index=True, use_container_width=True, column_config={
        "cv_mae": st.column_config.NumberColumn("CV MAE · INR", format="₹%.0f"),
        "cv_rmse": st.column_config.NumberColumn("CV RMSE · INR", format="₹%.0f"),
        "cv_rmse_std": st.column_config.NumberColumn("CV RMSE spread · INR", format="₹%.0f"),
        "test_mae": st.column_config.NumberColumn("Test MAE · INR", format="₹%.0f"),
        "test_rmse": st.column_config.NumberColumn("Test RMSE · INR", format="₹%.0f"),
        "cv_r2": st.column_config.NumberColumn("CV R²", format="%.3f"),
        "test_r2": st.column_config.NumberColumn("Test R²", format="%.3f"),
    })
    fig = px.bar(comparison.sort_values("cv_rmse"), x="cv_rmse", y="model", orientation="h", color="cv_rmse", color_continuous_scale=["#36c9a5", "#78a9ff"], hover_data={"cv_mae": ":,.0f", "cv_r2": ":.3f"}, labels={"cv_rmse": "Cross-validation RMSE (INR)", "model": "Model"})
    st.plotly_chart(style(fig, 360), use_container_width=True, config={"displayModeBar": False})

    left, right = st.columns(2)
    if not predictions.empty:
        predictions["residual_inr"] = predictions["actual"] - predictions["predicted"]
        with left:
            section("Actual vs predicted", "Each point is a held-out test record.")
            fig = px.scatter(predictions.sample(min(4_000, len(predictions)), random_state=42), x="actual", y="predicted", opacity=.55, labels={"actual": "Actual price (INR)", "predicted": "Predicted price (INR)"}, color_discrete_sequence=["#36c9a5"])
            fig.update_xaxes(type="log")
            fig.update_yaxes(type="log")
            st.plotly_chart(style(fig, 360), use_container_width=True, config={"displayModeBar": False})
        with right:
            section("Residuals", "Actual minus predicted price; zero is the reference line.")
            fig = px.scatter(predictions.sample(min(4_000, len(predictions)), random_state=24), x="predicted", y="residual_inr", opacity=.5, labels={"predicted": "Predicted price (INR)", "residual_inr": "Residual (INR)"}, color_discrete_sequence=["#78a9ff"])
            fig.add_hline(y=0, line_dash="dash", line_color="#9aaac0")
            fig.update_xaxes(type="log")
            st.plotly_chart(style(fig, 360), use_container_width=True, config={"displayModeBar": False})

    if not importance.empty:
        section("Feature importance", "Impurity-based importance from the selected Random Forest; not a causal explanation.")
        top = importance.head(15).sort_values("importance")
        fig = px.bar(top, x="importance", y="feature", orientation="h", color="importance", color_continuous_scale=["#78a9ff", "#36c9a5"], labels={"importance": "Relative importance", "feature": "Transformed feature"})
        st.plotly_chart(style(fig, 440), use_container_width=True, config={"displayModeBar": False})
    st.caption("The selected model improves on the dummy baseline, but test errors remain substantial. See `reports/model_training_summary.md` for the full comparison and limits.")
    footer()
