from pathlib import Path
import os

ROOT = Path(__file__).resolve().parents[1]
os.environ.setdefault("MPLCONFIGDIR", str(ROOT / ".mplconfig"))
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from scipy.stats import kruskal

from src.data_loader import DEFAULT_DATA, load_properties
from src.preprocessing import clean_properties


FIGURES = ROOT / "reports" / "figures"
PROCESSED = ROOT / "data" / "processed"
REPORTS = ROOT / "reports"


def save_figures(data, summary):
    FIGURES.mkdir(parents=True, exist_ok=True)
    sns.set_theme(style="whitegrid", palette="deep")

    plots = [
        ("price_distribution.png", "price_inr", "Property price (INR)", True),
        ("area_distribution.png", "area_sqft", "Area (square feet)", True),
        ("bedroom_distribution.png", "bedrooms", "Bedrooms", False),
        ("bathroom_distribution.png", "bathrooms", "Bathrooms", False),
        ("price_per_sqft_distribution.png", "price_per_sqft", "Price per square foot (INR)", True),
    ]
    for filename, column, label, log_scale in plots:
        values = data[column].dropna()
        fig, ax = plt.subplots(figsize=(9, 5))
        sns.histplot(values, bins=50, ax=ax)
        if log_scale:
            ax.set_xscale("log")
        ax.set(title=label + " distribution", xlabel=label, ylabel="Records")
        fig.tight_layout()
        fig.savefig(FIGURES / filename, dpi=160)
        plt.close(fig)

    pd.Series({"Raw rows": summary["raw_rows"], "After exact deduplication": summary["unique_rows"], "Clean sale rows": summary["clean_rows"]}).plot.bar(figsize=(8, 5), color="#277da1")
    plt.title("Rows retained through cleaning")
    plt.ylabel("Rows")
    plt.xticks(rotation=15, ha="right")
    plt.tight_layout()
    plt.savefig(FIGURES / "cleaning_steps.png", dpi=160)
    plt.close()

    data["city"].value_counts().head(20).sort_values().plot.barh(figsize=(9, 7), color="#277da1")
    plt.title("20 cities with the most retained records")
    plt.xlabel("Records")
    plt.tight_layout()
    plt.savefig(FIGURES / "city_frequency.png", dpi=160)
    plt.close()

    sample = data.sample(min(8_000, len(data)), random_state=42)
    fig, ax = plt.subplots(figsize=(9, 6))
    sns.scatterplot(data=sample, x="area_sqft", y="price_inr", hue="area_basis", alpha=0.45, s=20, ax=ax)
    ax.set(xscale="log", yscale="log", title="Area and asking price", xlabel="Area (square feet)", ylabel="Price (INR)")
    fig.tight_layout()
    fig.savefig(FIGURES / "area_vs_price.png", dpi=160)
    plt.close(fig)

    top_city_names = data["city"].value_counts().head(6).index
    city_sample = data[data["city"].isin(top_city_names)].sample(
        min(6_000, len(data[data["city"].isin(top_city_names)])), random_state=42
    )
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.scatterplot(data=city_sample, x="area_sqft", y="price_inr", hue="city", alpha=0.5, s=20, ax=ax)
    ax.set(xscale="log", yscale="log", title="Area and price across the six largest city samples", xlabel="Area (square feet)", ylabel="Price (INR)")
    fig.tight_layout()
    fig.savefig(FIGURES / "area_location_price.png", dpi=160)
    plt.close(fig)

    top_cities = data["city"].value_counts().head(15).index
    fig, ax = plt.subplots(figsize=(12, 6))
    sns.boxplot(data=data[data["city"].isin(top_cities)], x="city", y="price_inr", showfliers=False, ax=ax)
    ax.set_yscale("log")
    ax.tick_params(axis="x", rotation=45)
    ax.set(title="Asking price by city (15 largest samples)", xlabel="City", ylabel="Price (INR, log scale)")
    fig.tight_layout()
    fig.savefig(FIGURES / "price_by_city.png", dpi=160)
    plt.close(fig)

    by_bedroom = data[data["bedrooms"].between(1, 8)]
    fig, ax = plt.subplots(figsize=(9, 5))
    sns.boxplot(data=by_bedroom, x="bedrooms", y="price_inr", showfliers=False, ax=ax)
    ax.set_yscale("log")
    ax.set(title="Asking price by bedroom count", xlabel="Bedrooms", ylabel="Price (INR, log scale)")
    fig.tight_layout()
    fig.savefig(FIGURES / "price_by_bedrooms.png", dpi=160)
    plt.close(fig)

    fig, ax = plt.subplots(figsize=(8, 5))
    sns.boxplot(data=data, x="furnishing", y="price_inr", showfliers=False, ax=ax)
    ax.set_yscale("log")
    ax.set(title="Asking price by furnishing", xlabel="Furnishing", ylabel="Price (INR, log scale)")
    ax.tick_params(axis="x", rotation=15)
    fig.tight_layout()
    fig.savefig(FIGURES / "price_by_furnishing.png", dpi=160)
    plt.close(fig)

    outlook = data["overlooking"].value_counts().head(10).index
    fig, ax = plt.subplots(figsize=(12, 6))
    sns.boxplot(data=data[data["overlooking"].isin(outlook)], x="overlooking", y="price_inr", showfliers=False, ax=ax)
    ax.set_yscale("log")
    ax.tick_params(axis="x", rotation=35)
    ax.set(title="Asking price by reported outlook", xlabel="Outlook text", ylabel="Price (INR, log scale)")
    fig.tight_layout()
    fig.savefig(FIGURES / "price_by_outlook.png", dpi=160)
    plt.close(fig)

    numeric = data[["price_inr", "area_sqft", "bedrooms", "bathrooms", "balconies", "price_per_sqft"]].corr(numeric_only=True)
    fig, ax = plt.subplots(figsize=(8, 6))
    sns.heatmap(numeric, annot=True, fmt=".2f", cmap="vlag", center=0, ax=ax)
    ax.set_title("Numeric feature correlations")
    fig.tight_layout()
    fig.savefig(FIGURES / "correlation_heatmap.png", dpi=160)
    plt.close(fig)


def statistical_analysis(data):
    groups = [group["price_inr"].to_numpy() for _, group in data.groupby("city") if len(group) >= 30]
    result = kruskal(*groups)
    city_summary = data.groupby("city")["price_inr"].agg(records="size", median_price_inr="median", mean_price_inr="mean")
    city_summary.sort_values("median_price_inr").to_csv(REPORTS / "city_price_summary.csv")
    return len(groups), result, city_summary


def save_missingness_plot(missingness):
    top = missingness.sort_values("missing_count", ascending=False).head(12).sort_values("missing_percent")
    top["missing_percent"].plot.barh(figsize=(9, 6), color="#f9844a")
    plt.title("Raw dataset fields with the most missing values")
    plt.xlabel("Missing values (%)")
    plt.tight_layout()
    plt.savefig(FIGURES / "raw_missingness.png", dpi=160)
    plt.close()


def run_eda(path=DEFAULT_DATA):
    REPORTS.mkdir(parents=True, exist_ok=True)
    PROCESSED.mkdir(parents=True, exist_ok=True)
    raw = load_properties(path)
    cleaned, summary = clean_properties(raw)
    cleaned.to_csv(PROCESSED / "cleaned_properties.csv", index=False)
    pd.DataFrame([summary]).to_csv(REPORTS / "data_quality_summary.csv", index=False)
    missingness = pd.DataFrame({"missing_count": raw.isna().sum(), "missing_percent": raw.isna().mean().mul(100)})
    missingness.sort_values("missing_count", ascending=False).to_csv(REPORTS / "raw_missingness.csv")
    save_figures(cleaned, summary)
    save_missingness_plot(missingness)
    city_count, result, city_summary = statistical_analysis(cleaned)
    price = cleaned["price_inr"]
    area = cleaned["area_sqft"]
    price_sqft = cleaned["price_per_sqft"]
    bedroom_medians = cleaned.groupby("bedrooms")["price_inr"].median().dropna()
    area_price_rank = cleaned[["area_sqft", "price_inr"]].corr(method="spearman").iloc[0, 1]
    largest_city = city_summary.sort_values("records", ascending=False).iloc[0]
    smallest_city = city_summary.sort_values("records").iloc[0]
    low_city = city_summary.sort_values("median_price_inr").iloc[0]
    high_city = city_summary.sort_values("median_price_inr").iloc[-1]
    furnishing_summary = cleaned.groupby("furnishing", dropna=True)["price_inr"].median().sort_values()

    q99 = price.quantile(0.99)
    area_q01 = area.quantile(0.01)
    area_q99 = area.quantile(0.99)
    price_sqft_q99 = price_sqft.quantile(0.99)
    extremes = cleaned[
        price.gt(q99) | area.gt(area_q99) | area.lt(area_q01) | price_sqft.gt(price_sqft_q99)
    ][["source_index", "city", "area_sqft", "area_basis", "price_inr", "price_per_sqft"]]
    extremes.to_csv(REPORTS / "outlier_review.csv", index=False)
    p_text = f"{result.pvalue:.3g}" if result.pvalue >= 0.001 else "< 0.001"

    summary_text = f"""# Exploratory analysis notes

## Cleaning snapshot

- Raw rows: {summary['raw_rows']:,}
- Exact repeated rows removed after excluding the generated `Index` field: {summary['exact_duplicates_removed_excluding_index']:,}
- Unique rows after deduplication: {summary['unique_rows']:,}
- Rows after sale transaction filter: {summary['rows_after_sale_filter']:,}
- Rows after valid price filter: {summary['rows_after_valid_price_filter']:,}
- Rows excluded by area sanity bounds (100 to 20,000 sq ft): {summary['rows_outside_area_sanity_bounds']:,}
- Sale rows with valid price but no usable area: {summary['rows_without_area_after_sale_and_price_filters']:,}
- Rows excluded by derived rate sanity bounds (₹100 to ₹1,000,000 per sq ft): {summary['rows_outside_price_per_sqft_sanity_bounds']:,}
- Rows retained for sale-price analysis: {summary['clean_rows']:,}
- Cities represented after cleaning: {summary['cities_retained']}
- Rows without a numeric asking price: {summary['rows_without_numeric_price']:,}
- Rows without a usable area: {summary['rows_with_unusable_area']:,}

Exact row repeats were removed because every substantive column matched; the row-number field alone differed. Unsupported regional area units were left unusable rather than converted with uncertain local definitions. Records with areas below 100 or above 20,000 sq ft were excluded as implausible for a flat listing. We also excluded derived rates below ₹100 or above ₹1,000,000 per sq ft; manual review found malformed 1–20 sq ft areas and several multi-crore-per-square-foot records. Other high values are retained and listed for review rather than trimmed by percentile.

## What the figures show

- `price_distribution.png`: prices are strongly right-skewed. The median is ₹{price.median():,.0f}, while the mean is ₹{price.mean():,.0f}; a small number of very expensive records pull the mean upward.
- `area_distribution.png`: the median selected area is {area.median():,.0f} sq ft and the 99th percentile is {area.quantile(.99):,.0f} sq ft. Values beyond that percentile need source-level review.
- `bedroom_distribution.png` and `bathroom_distribution.png`: the typical listing has {cleaned['bedrooms'].median():.0f} bedrooms and {cleaned['bathrooms'].median():.0f} bathrooms. Some values are missing because the bedroom count was parsed from the title and unresolved count strings were left blank.
- `city_frequency.png`: {largest_city.name} has the most retained records ({int(largest_city['records']):,}); {smallest_city.name} has the fewest ({int(smallest_city['records']):,}). City sample sizes are not equal.
- `price_per_sqft_distribution.png`: the median derived rate is ₹{price_sqft.median():,.0f}/sq ft. This is calculated from the cleaned target and area, so it is for analysis only and must not be used as a model input.
- `area_vs_price.png`: area and price have a Spearman rank correlation of {area_price_rank:.2f}, indicating a positive monotonic association in these listings. This is not a causal effect.
- `area_location_price.png`: shows how the area-price pattern varies across the six cities with the largest cleaned samples.
- `price_by_city.png`: among cities with at least 30 records, median prices range from ₹{low_city['median_price_inr']:,.0f} in {low_city.name} to ₹{high_city['median_price_inr']:,.0f} in {high_city.name}. Differences may reflect property mix as well as location.
- `price_by_bedrooms.png`: group medians generally provide a simple comparison of listing prices by bedroom count; the chart suppresses extreme points so the common range remains readable.
- `price_by_furnishing.png`: compares median asking-price distributions across furnished categories; this is descriptive and does not control for city or property size. The observed median ranges from {('₹' + f'{furnishing_summary.iloc[0]:,.0f}') if len(furnishing_summary) else 'not available'} to {('₹' + f'{furnishing_summary.iloc[-1]:,.0f}') if len(furnishing_summary) else 'not available'} across categories.
- `price_by_outlook.png`: compares the most common reported outlook descriptions. These are free-text combinations, not standardized amenity labels.
- `correlation_heatmap.png`: numeric correlations summarize linear relationships. Correlation does not establish cause, and derived price per square foot is target-dependent.
- `cleaning_steps.png`: shows how exact duplicate removal and required price/area filters reduce the raw row count.
- `raw_missingness.png`: shows that `Plot Area` and `Dimensions` are entirely empty, so they cannot be used.

The raw missing-value counts and percentages are in `reports/raw_missingness.csv`. Optional model features with missing values remain missing in the cleaned file; their imputers will be fitted on training data later. The source has no property-age field or dedicated amenities field. `location` is city-level; locality appears only in free text. The original `Price (in rupees)` field was not used as a predictor because its meaning is unclear and it has zero and extreme values. `source_index` is retained only to trace a cleaned row back to the raw archive and must be excluded from model features.

## Statistical comparison

Kruskal-Wallis test comparing asking-price distributions across {city_count} cities with at least 30 retained records: H = {result.statistic:.3f}, p {p_text}.

Null hypothesis: the cities have the same asking-price distribution. Alternative: at least one city has a different distribution. At the 0.05 level, the result is {'statistically significant, so the null hypothesis is rejected' if result.pvalue < 0.05 else 'not statistically significant, so the null hypothesis is not rejected'}. Kruskal-Wallis does not require normally distributed prices, but it assumes independent observations; the interpretation as a median comparison also assumes similarly shaped group distributions. The test compares distributions, not causal city effects. Listings may not be independent if the source contains multiple records for the same property, and differences in property mix can affect the result.

## Interpretation limits

The dataset is a cross-sectional listing snapshot with no listing date. Asking prices are not confirmed sale prices. Locality is embedded in free text rather than supplied as a clean field. Price per square foot is derived from the asking price and selected area, so it is an analysis measure and must not be used as a predictor of that same price.

Figures are saved in `reports/figures/`. The full city summary is in `reports/city_price_summary.csv`; potentially unusual records are listed in `reports/outlier_review.csv` for review, not automatic deletion.
"""
    (REPORTS / "eda_findings.md").write_text(summary_text, encoding="utf-8")
    print("Cleaned rows:", len(cleaned))
    print("Cities:", cleaned["city"].nunique())
    print("Kruskal-Wallis p-value:", f"{result.pvalue:.3g}" if result.pvalue >= 0.001 else "< 0.001")
    print("Saved cleaned data to", PROCESSED / "cleaned_properties.csv")
    print("Saved figures to", FIGURES)


if __name__ == "__main__":
    run_eda()
