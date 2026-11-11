import re

import numpy as np
import pandas as pd


AREA_FACTORS = {"sqft": 1.0, "sqft.": 1.0, "sq.ft.": 1.0, "sqyd": 9.0, "sqyards": 9.0, "sqm": 10.7639}


def parse_price(values):
    parts = values.astype("string").str.strip().str.extract(r"(?i)^([\d,.]+)\s*(lac|lakh|cr|crore)$")
    amount = pd.to_numeric(parts[0].str.replace(",", "", regex=False), errors="coerce")
    factor = parts[1].str.lower().map({"lac": 100_000, "lakh": 100_000, "cr": 10_000_000, "crore": 10_000_000})
    return amount * factor


def parse_area(values):
    parts = values.astype("string").str.strip().str.lower().str.extract(r"^([\d,.]+)\s*([a-z.²]+)$")
    amount = pd.to_numeric(parts[0].str.replace(",", "", regex=False), errors="coerce")
    return amount * parts[1].map(AREA_FACTORS)


def _count(values):
    numbers = values.astype("string").str.strip().str.extract(r"^(\d+(?:\.\d+)?)$")[0]
    return pd.to_numeric(numbers, errors="coerce")


def clean_properties(raw):
    source = raw.drop(columns=["Index"], errors="ignore")
    unique_rows = ~source.duplicated()
    deduped = raw.loc[unique_rows].copy()

    price = parse_price(deduped["Amount(in rupees)"])
    carpet = parse_area(deduped["Carpet Area"])
    super_area = parse_area(deduped["Super Area"])
    area = carpet.combine_first(super_area)
    basis = pd.Series(np.where(carpet.notna(), "Carpet Area", "Super Area"), index=deduped.index)

    transaction = deduped["Transaction"].astype("string").str.strip()
    sale = transaction.isin(["Resale", "New Property"])
    rate = price.div(area)
    valid_area = area.between(100, 20_000)
    valid_rate = rate.between(100, 1_000_000)
    keep = sale & price.gt(0) & valid_area & valid_rate
    cleaned = pd.DataFrame({
        "source_index": deduped.loc[keep, "Index"],
        "city": deduped.loc[keep, "location"].astype("string").str.strip().str.lower(),
        "area_sqft": area.loc[keep],
        "area_basis": basis.loc[keep],
        "bedrooms": pd.to_numeric(deduped.loc[keep, "Title"].str.extract(r"(?i)(\d+(?:\.\d+)?)\s*BHK")[0], errors="coerce"),
        "bathrooms": _count(deduped.loc[keep, "Bathroom"]),
        "balconies": _count(deduped.loc[keep, "Balcony"]),
        "furnishing": deduped.loc[keep, "Furnishing"],
        "facing": deduped.loc[keep, "facing"],
        "overlooking": deduped.loc[keep, "overlooking"],
        "ownership": deduped.loc[keep, "Ownership"],
        "transaction": transaction.loc[keep],
        "price_inr": price.loc[keep],
    }).reset_index(drop=True)
    cleaned["price_per_sqft"] = cleaned["price_inr"] / cleaned["area_sqft"]

    summary = {
        "raw_rows": len(raw),
        "exact_duplicates_removed_excluding_index": int((~unique_rows).sum()),
        "unique_rows": len(deduped),
        "rows_without_numeric_price": int(price.isna().sum()),
        "rows_with_unusable_area": int(area.isna().sum()),
        "non_sale_or_unknown_transaction_rows": int((~sale).sum()),
        "rows_after_sale_filter": int(sale.sum()),
        "rows_after_valid_price_filter": int((sale & price.gt(0)).sum()),
        "rows_outside_area_sanity_bounds": int((sale & price.gt(0) & area.notna() & ~valid_area).sum()),
        "rows_without_area_after_sale_and_price_filters": int((sale & price.gt(0) & area.isna()).sum()),
        "rows_outside_price_per_sqft_sanity_bounds": int((sale & price.gt(0) & valid_area & ~valid_rate).sum()),
        "clean_rows": len(cleaned),
        "cities_retained": int(cleaned["city"].nunique()),
    }
    return cleaned, summary
