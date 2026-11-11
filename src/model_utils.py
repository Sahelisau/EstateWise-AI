from pathlib import Path

import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.model_selection import train_test_split

from src.data_loader import ROOT


DATA_PATH = ROOT / "data" / "processed" / "cleaned_properties.csv"
TARGET = "price_inr"
NUMERIC = ["area_sqft", "bedrooms", "bathrooms", "balconies"]
CATEGORICAL = ["city", "area_basis", "furnishing", "facing", "overlooking", "ownership", "transaction"]
FEATURES = NUMERIC + CATEGORICAL
RANDOM_STATE = 42


def load_split(data_path=DATA_PATH):
    path = Path(data_path)
    if not path.exists():
        raise FileNotFoundError("Cleaned data is missing. Run `python -m src.eda` first.")
    data = pd.read_csv(path)
    missing = set(FEATURES + [TARGET]) - set(data.columns)
    if missing:
        raise ValueError(f"Cleaned dataset is missing required columns: {sorted(missing)}")
    x_train, x_test, y_train, y_test = train_test_split(
        data[FEATURES], data[TARGET], test_size=0.2, random_state=RANDOM_STATE
    )
    return data, x_train, x_test, y_train, y_test


def make_preprocessor():
    numeric = Pipeline([
        ("fill", SimpleImputer(strategy="median", add_indicator=True)),
        ("scale", StandardScaler(with_mean=False)),
    ])
    categorical = Pipeline([
        ("fill", SimpleImputer(strategy="most_frequent")),
        ("encode", OneHotEncoder(handle_unknown="ignore", min_frequency=10)),
    ])
    return ColumnTransformer([
        ("numeric", numeric, NUMERIC),
        ("category", categorical, CATEGORICAL),
    ])
