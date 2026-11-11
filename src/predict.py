import json
import math
from pathlib import Path

import joblib
import pandas as pd

from src.data_loader import ROOT
from src.model_utils import CATEGORICAL, FEATURES, TARGET


MODEL_PATH = ROOT / "models" / "property_price_model.pkl"
METADATA_PATH = ROOT / "models" / "model_metadata.json"


def load_artifacts():
    if not MODEL_PATH.exists() or not METADATA_PATH.exists():
        raise FileNotFoundError("Trained model is missing. Run `python -m src.train`, then restart the app.")
    metadata = json.loads(METADATA_PATH.read_text(encoding="utf-8"))
    if metadata.get("features") != FEATURES or metadata.get("target") != TARGET:
        raise ValueError("Model metadata does not match the current prediction feature schema.")
    model = joblib.load(MODEL_PATH)
    if not hasattr(model, "predict"):
        raise ValueError("The saved model artifact is invalid. Run `python -m src.train` again.")
    return model, metadata


def known_categories(model):
    preprocessor = model.regressor_.named_steps["preprocess"]
    encoder = preprocessor.named_transformers_["category"].named_steps["encode"]
    return {name: list(values) for name, values in zip(CATEGORICAL, encoder.categories_)}


def predict_price(model, values):
    missing = set(FEATURES) - set(values)
    if missing:
        raise ValueError(f"Enter all required property details: {', '.join(sorted(missing))}.")
    numeric = ["area_sqft", "bedrooms", "bathrooms", "balconies"]
    try:
        numbers = {name: float(values[name]) for name in numeric}
    except (TypeError, ValueError):
        raise ValueError("Area, bedrooms, bathrooms, and balconies must be numeric.") from None
    if not all(math.isfinite(value) for value in numbers.values()):
        raise ValueError("Area, bedrooms, bathrooms, and balconies must be finite numbers.")
    for name in numeric:
        if numbers[name] < 0:
            raise ValueError(f"{name.replace('_', ' ').capitalize()} cannot be negative.")
    if numbers["area_sqft"] <= 0:
        raise ValueError("Area must be greater than zero.")

    categories = known_categories(model)
    for name in CATEGORICAL:
        if values[name] not in categories[name]:
            raise ValueError(f"'{values[name]}' is not a category supported by this model for {name}.")

    row = pd.DataFrame([{name: values[name] for name in FEATURES}], columns=FEATURES)
    return max(0.0, float(model.predict(row)[0]))
