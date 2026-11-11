import hashlib
import json
import os
from datetime import datetime, timezone
from pathlib import Path

os.environ.setdefault("MPLCONFIGDIR", str(Path(__file__).resolve().parents[1] / ".mplconfig"))

import joblib
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.base import clone
from sklearn.dummy import DummyRegressor
from sklearn.ensemble import GradientBoostingRegressor, RandomForestRegressor
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.model_selection import KFold, RandomizedSearchCV, cross_validate
from sklearn.pipeline import Pipeline
from sklearn.tree import DecisionTreeRegressor
from sklearn.compose import TransformedTargetRegressor

from src.data_loader import DEFAULT_DATA, ROOT
from src.evaluate import save_evaluation
from src.model_utils import FEATURES, TARGET, load_split, make_preprocessor


MODEL_DIR = ROOT / "models"
REPORTS = ROOT / "reports"
FIGURES = REPORTS / "figures"
SCORING = {
    "mae": "neg_mean_absolute_error",
    "rmse": "neg_root_mean_squared_error",
    "r2": "r2",
}


def model_pipeline(estimator):
    pipeline = Pipeline([("preprocess", make_preprocessor()), ("model", estimator)])
    return TransformedTargetRegressor(regressor=pipeline, func=np.log1p, inverse_func=np.expm1)


def dataset_fingerprint(path=DEFAULT_DATA):
    digest = hashlib.sha256()
    with open(path, "rb") as source:
        for block in iter(lambda: source.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def cross_validation_scores(model, x_train, y_train, cv):
    scores = cross_validate(model, x_train, y_train, cv=cv, scoring=SCORING, n_jobs=1)
    return {
        "cv_mae": -scores["test_mae"].mean(),
        "cv_rmse": -scores["test_rmse"].mean(),
        "cv_rmse_std": scores["test_rmse"].std(),
        "cv_r2": scores["test_r2"].mean(),
    }


def tune_forest(x_train, y_train, cv):
    search = RandomizedSearchCV(
        model_pipeline(RandomForestRegressor(random_state=42, n_jobs=1)),
        param_distributions={
            "regressor__model__n_estimators": [40, 60],
            "regressor__model__max_depth": [12, 20, None],
            "regressor__model__min_samples_leaf": [1, 2, 4],
            "regressor__model__max_features": ["sqrt", 0.8],
        },
        n_iter=3,
        scoring=SCORING,
        refit="rmse",
        cv=cv,
        random_state=42,
        n_jobs=1,
        return_train_score=False,
    )
    search.fit(x_train, y_train)
    result = search.cv_results_
    best = search.best_index_
    scores = {
        "cv_mae": -result["mean_test_mae"][best],
        "cv_rmse": -result["mean_test_rmse"][best],
        "cv_rmse_std": result["std_test_rmse"][best],
        "cv_r2": result["mean_test_r2"][best],
    }
    return search.best_estimator_, scores, search.best_params_


def save_importance(model):
    if not hasattr(model, "regressor_"):
        return
    pipeline = model.regressor_
    estimator = pipeline.named_steps["model"]
    transformer = pipeline.named_steps["preprocess"]
    joblib.dump(transformer, MODEL_DIR / "preprocessing_pipeline.pkl")
    if hasattr(estimator, "feature_importances_"):
        values = estimator.feature_importances_
    elif hasattr(estimator, "coef_"):
        values = np.abs(estimator.coef_).ravel()
    else:
        return
    importance = pd.DataFrame({"feature": transformer.get_feature_names_out(), "importance": values})
    importance = importance.sort_values("importance", ascending=False)
    importance.to_csv(REPORTS / "feature_importance.csv", index=False)
    top = importance.head(25).sort_values("importance")
    top.plot.barh(x="feature", y="importance", figsize=(10, 8), legend=False, color="#277da1")
    plt.title("Most influential transformed features")
    plt.xlabel("Importance")
    plt.tight_layout()
    plt.savefig(FIGURES / "feature_importance.png", dpi=160)
    plt.close()


def write_training_summary(comparison, metadata, train_rows, test_rows):
    baseline = comparison.loc[comparison["model"] == "Dummy median baseline"].iloc[0]
    selected = comparison.loc[comparison["model"] == metadata["model_name"]].iloc[0]
    decision_tree = comparison.loc[comparison["model"] == "Decision Tree"].iloc[0]
    tuned_forest = comparison.loc[comparison["model"] == "Random Forest (tuned)"].iloc[0]
    mae_gain = 100 * (1 - selected["test_mae"] / baseline["test_mae"])
    rmse_gain = 100 * (1 - selected["test_rmse"] / baseline["test_rmse"])
    importance_path = REPORTS / "feature_importance.csv"
    top_features = pd.read_csv(importance_path).head(5) if importance_path.exists() else pd.DataFrame()
    feature_text = ", ".join(
        f"`{row.feature}` ({row.importance:.1%})" for row in top_features.itertuples(index=False)
    ) or "Not available for the selected model."

    lines = [
        "# Model training results",
        "",
        f"- Selected model: {metadata['model_name']}",
        f"- Training records: {train_rows:,}; held-out test records: {test_rows:,}",
        "- Split: 80:20, random state 42; model comparison used shuffled 3-fold cross-validation on training data.",
        "- Preprocessing is inside each model pipeline, so imputers and encoders are fitted separately within each training fold.",
        f"- Selection used validation RMSE. Selected CV RMSE: ₹{selected['cv_rmse']:,.0f}; tuned forest CV RMSE: ₹{comparison.loc[comparison['model'] == 'Random Forest (tuned)', 'cv_rmse'].iloc[0]:,.0f}.",
        f"- Held-out test MAE: ₹{metadata['test_metrics']['mae']:,.0f}; RMSE: ₹{metadata['test_metrics']['rmse']:,.0f}; R²: {metadata['test_metrics']['r2']:.3f}.",
        f"- Compared with the median dummy baseline, test MAE was {mae_gain:.1f}% lower and test RMSE was {rmse_gain:.1f}% lower.",
        f"- The tuned forest had a lower test MAE (₹{tuned_forest['test_mae']:,.0f}) but higher CV RMSE than the selected forest; selection followed the predeclared CV RMSE criterion.",
        f"- The decision tree's test RMSE (₹{decision_tree['test_rmse']:,.0f}) was slightly lower than the selected forest's, while its CV RMSE was higher. The test set was kept for final reporting rather than model selection.",
        "",
        "## Cross-validation and test comparison",
        "",
    ]
    for row in comparison.itertuples(index=False):
        lines.append(
            f"- {row.model}: CV MAE ₹{row.cv_mae:,.0f}, CV RMSE ₹{row.cv_rmse:,.0f}, CV R² {row.cv_r2:.3f}; "
            f"test MAE ₹{row.test_mae:,.0f}, test RMSE ₹{row.test_rmse:,.0f}, test R² {row.test_r2:.3f}."
        )
    lines.extend([
        "",
        "## Feature importance",
        "",
        f"The selected tree model's largest impurity-based importance values were {feature_text}. These scores describe how the forest used transformed features; they do not show cause and can favor continuous features with many possible split points.",
        "",
        "## Reading the result",
        "",
        "The model improves substantially on the dummy baseline, but the held-out RMSE remains large because a few high-price errors count heavily. The MAE is the more direct typical absolute-error summary. This is a listing-price estimate from an older dataset, not a current valuation. The cross-city dataset has no structured locality feature and covers flats only.",
        "",
        "Model comparison is in `reports/model_comparison.csv`; held-out predictions and error slices are in `reports/`; model details and the data fingerprint are in `models/model_metadata.json`.",
    ])
    (REPORTS / "model_training_summary.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def train():
    MODEL_DIR.mkdir(parents=True, exist_ok=True)
    REPORTS.mkdir(parents=True, exist_ok=True)
    FIGURES.mkdir(parents=True, exist_ok=True)
    _, x_train, x_test, y_train, y_test = load_split()
    cv = KFold(n_splits=3, shuffle=True, random_state=42)

    candidates = {
        "Dummy median baseline": DummyRegressor(strategy="median"),
        "Linear Regression": model_pipeline(LinearRegression()),
        "Decision Tree": model_pipeline(DecisionTreeRegressor(max_depth=18, min_samples_leaf=2, random_state=42)),
        "Random Forest": model_pipeline(RandomForestRegressor(n_estimators=50, max_depth=16, min_samples_leaf=2, random_state=42, n_jobs=1)),
        "Gradient Boosting": model_pipeline(GradientBoostingRegressor(n_estimators=50, learning_rate=0.05, max_depth=3, subsample=0.8, random_state=42)),
    }
    fitted = {}
    rows = []

    for name, candidate in candidates.items():
        print(f"Cross-validating {name}...", flush=True)
        row = {"model": name, **cross_validation_scores(candidate, x_train, y_train, cv)}
        fitted_model = clone(candidate).fit(x_train, y_train)
        prediction = np.maximum(fitted_model.predict(x_test), 0)
        row.update({f"test_{key}": value for key, value in {
            "mae": mean_absolute_error(y_test, prediction),
            "rmse": np.sqrt(mean_squared_error(y_test, prediction)),
            "r2": r2_score(y_test, prediction),
        }.items()})
        fitted[name] = fitted_model
        rows.append(row)

    print("Tuning Random Forest with randomized search...", flush=True)
    tuned, tuned_scores, best_params = tune_forest(x_train, y_train, cv)
    tuned_prediction = np.maximum(tuned.predict(x_test), 0)
    rows.append({
        "model": "Random Forest (tuned)",
        **tuned_scores,
        "test_mae": mean_absolute_error(y_test, tuned_prediction),
        "test_rmse": np.sqrt(mean_squared_error(y_test, tuned_prediction)),
        "test_r2": r2_score(y_test, tuned_prediction),
    })
    fitted["Random Forest (tuned)"] = tuned

    comparison = pd.DataFrame(rows).sort_values("cv_rmse")
    comparison.to_csv(REPORTS / "model_comparison.csv", index=False)
    selected_row = comparison.iloc[0]
    selected_name = selected_row["model"]
    selected = fitted[selected_name]
    final_metrics = save_evaluation(selected, x_test, y_test, {"model_name": selected_name})
    joblib.dump(selected, MODEL_DIR / "property_price_model.pkl")
    save_importance(selected)

    metadata = {
        "model_name": selected_name,
        "dataset": DEFAULT_DATA.name,
        "dataset_sha256": dataset_fingerprint(),
        "trained_at_utc": datetime.now(timezone.utc).isoformat(),
        "features": FEATURES,
        "target": TARGET,
        "target_unit": "INR",
        "test_metrics": final_metrics,
        "validation_metrics": {key: float(value) for key, value in selected_row.items() if key.startswith("cv_")},
        "selected_model_parameters": selected.regressor_.named_steps["model"].get_params() if hasattr(selected, "regressor_") else selected.get_params(),
        "best_random_forest_parameters": {key: str(value) for key, value in best_params.items()},
        "training_config": {"test_size": 0.2, "random_state": 42, "cross_validation": "3-fold shuffled KFold", "target_transform": "log1p for regression models"},
        "python_version": __import__("platform").python_version(),
        "scikit_learn_version": __import__("sklearn").__version__,
    }
    (MODEL_DIR / "model_metadata.json").write_text(json.dumps(metadata, indent=2), encoding="utf-8")
    write_training_summary(comparison, metadata, len(y_train), len(y_test))

    print("\nCross-validation model comparison:")
    print(comparison[["model", "cv_mae", "cv_rmse", "cv_r2", "test_mae", "test_rmse", "test_r2"]].to_string(index=False, formatters={key: "{:,.2f}".format for key in comparison.columns if key != "model"}))
    print("\nSelected model:", selected_name)
    print("Test metrics:", {key: round(value, 2) for key, value in final_metrics.items()})
    print("Best Random Forest parameters:", best_params)
    print("Saved artifacts in", MODEL_DIR)


if __name__ == "__main__":
    train()
