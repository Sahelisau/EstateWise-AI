from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_DATA = ROOT / "data" / "raw" / "india_property_listings_81_cities.zip"


def load_properties(path=DEFAULT_DATA):
    path = Path(path)
    if path.suffix.lower() == ".zip":
        return pd.read_csv(path, compression="zip", low_memory=False)
    if path.suffix.lower() in {".xlsx", ".xls"}:
        return pd.read_excel(path)
    return pd.read_csv(path, low_memory=False)
