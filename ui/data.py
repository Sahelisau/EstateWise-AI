from pathlib import Path

import pandas as pd
import streamlit as st

from src.data_loader import ROOT


@st.cache_data(show_spinner=False)
def load_clean_data():
    path = ROOT / "data" / "processed" / "cleaned_properties.csv"
    if not path.exists():
        raise FileNotFoundError("Cleaned data is missing. Run `python -m src.eda` first.")
    return pd.read_csv(path)


@st.cache_data(show_spinner=False)
def load_csv(name):
    path = ROOT / "reports" / name
    return pd.read_csv(path) if path.exists() else pd.DataFrame()


@st.cache_data(show_spinner=False)
def load_json(name):
    import json
    path = ROOT / "reports" / name
    return json.loads(path.read_text(encoding="utf-8")) if path.exists() else {}


def load_image(name):
    path = ROOT / "reports" / "figures" / name
    return path if Path(path).exists() else None
