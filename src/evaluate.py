import json
import os
from pathlib import Path

os.environ.setdefault("MPLCONFIGDIR", str(Path(__file__).resolve().parents[1] / ".mplconfig"))

import joblib
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

from src.data_loader import ROOT
from src.model_utils import FEATURES, TARGET, load_split


MODEL_PATH = ROOT / "models" / "property_price_model.pkl"
METADATA_PATH = ROOT / "models" / "model_metadata.json"
REPORTS = ROOT / "reports"


def metrics(actual, predicted):
    return {
        "mae": mean_absolute_error(actual, predicted),
        "rmse": float(np.sqrt(mean_squared_error(actual, predicted))),
        "r2": r2_score(actual, predicted),
    }


def save_evaluation(model, x_test, y_test, metadata=None):
    REPORTS.mkdir(parents=True, exist_ok=True)
    (REPORTS / "figures").mkdir(parents=True, exist_ok=True)
    predicted = model.predict(x_test)
    predicted = np.maximum(predicted, 0)
    residual = y_test.to_numpy() - predicted
    scores = metrics(y_test, predicted)

    actual_plot = pd.DataFrame({"actual": y_test.to_numpy(), "predicted": predicted})
    actual_plot.to_csv(REPORTS / "test_predictions.csv", index=False)

    fig, ax = plt.subplots(figsize=(7, 6))
    ax.scatter(y_test, predicted, alpha=0.35, s=12)
    low, high = max(1, y_test.min()), max(y_test.max(), predicted.max())
    ax.plot([low, high], [low, high], color="black", linestyle="--")
    ax.set(xscale="log", yscale="log", title="Held-out actual and predicted prices", xlabel="Actual price (INR)", ylabel="Predicted price (INR)")
    fig.tight_layout()
    fig.savefig(REPORTS / "figures" / "actual_vs_predicted.png", dpi=160)
    plt.close(fig)

    fig, ax = plt.subplots(figsize=(8, 5))
    ax.scatter(predicted, residual, alpha=0.35, s=12)
    ax.axhline(0, color="black", linestyle="--")
    ax.set(title="Held-out residuals", xlabel="Predicted price (INR)", ylabel="Actual minus predicted (INR)")
    fig.tight_layout()
    fig.savefig(REPORTS / "figures" / "residual_plot.png", dpi=160)
    plt.close(fig)

    errors = pd.DataFrame({
        "city": x_test["city"].to_numpy(),
        "actual_price_inr": y_test.to_numpy(),
        "predicted_price_inr": predicted,
        "absolute_error_inr": np.abs(residual),
    })
    errors["absolute_percentage_error"] = errors["absolute_error_inr"] / errors["actual_price_inr"].clip(lower=1)
    errors.nlargest(100, "absolute_error_inr").to_csv(REPORTS / "prediction_error_analysis.csv", index=False)
    city_rows = []
    for city, group in errors.groupby("city"):
        city_rows.append({
            "city": city,
            "records": len(group),
            "mae_inr": mean_absolute_error(group.actual_price_inr, group.predicted_price_inr),
            "rmse_inr": np.sqrt(mean_squared_error(group.actual_price_inr, group.predicted_price_inr)),
            "r2": r2_score(group.actual_price_inr, group.predicted_price_inr) if len(group) > 1 else np.nan,
        })
    pd.DataFrame(city_rows).to_csv(REPORTS / "prediction_error_by_city.csv", index=False)

    report = {"model_name": (metadata or {}).get("model_name", "loaded model"), **scores}
    (REPORTS / "test_metrics.json").write_text(json.dumps(report, indent=2), encoding="utf-8")
    return scores


def main():
    if not MODEL_PATH.exists() or not METADATA_PATH.exists():
        raise FileNotFoundError("Train the model first with `python -m src.train`.")
    metadata = json.loads(METADATA_PATH.read_text(encoding="utf-8"))
    if metadata.get("features") != FEATURES or metadata.get("target") != TARGET:
        raise ValueError("Model metadata does not match the current dataset feature schema.")
    model = joblib.load(MODEL_PATH)
    _, _, x_test, _, y_test = load_split()
    scores = save_evaluation(model, x_test, y_test, metadata)
    print("Held-out test metrics:", {key: round(value, 3) for key, value in scores.items()})
    print("Evaluation files saved under", REPORTS)


if __name__ == "__main__":
    main()
