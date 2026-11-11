# Exploratory analysis notes

## Cleaning snapshot

- Raw rows: 187,531
- Exact repeated rows removed after excluding the generated `Index` field: 119,339
- Unique rows after deduplication: 68,192
- Rows after sale transaction filter: 68,052
- Rows after valid price filter: 65,136
- Rows excluded by area sanity bounds (100 to 20,000 sq ft): 132
- Sale rows with valid price but no usable area: 1,889
- Rows excluded by derived rate sanity bounds (₹100 to ₹1,000,000 per sq ft): 7
- Rows retained for sale-price analysis: 63,108
- Cities represented after cleaning: 81
- Rows without a numeric asking price: 2,937
- Rows without a usable area: 2,062

Exact row repeats were removed because every substantive column matched; the row-number field alone differed. Unsupported regional area units were left unusable rather than converted with uncertain local definitions. Records with areas below 100 or above 20,000 sq ft were excluded as implausible for a flat listing. We also excluded derived rates below ₹100 or above ₹1,000,000 per sq ft; manual review found malformed 1–20 sq ft areas and several multi-crore-per-square-foot records. Other high values are retained and listed for review rather than trimmed by percentile.

## What the figures show

- `price_distribution.png`: prices are strongly right-skewed. The median is ₹6,500,000, while the mean is ₹10,161,246; a small number of very expensive records pull the mean upward.
- `area_distribution.png`: the median selected area is 1,150 sq ft and the 99th percentile is 4,100 sq ft. Values beyond that percentile need source-level review.
- `bedroom_distribution.png` and `bathroom_distribution.png`: the typical listing has 3 bedrooms and 2 bathrooms. Some values are missing because the bedroom count was parsed from the title and unresolved count strings were left blank.
- `city_frequency.png`: bangalore has the most retained records (2,917); madurai has the fewest (26). City sample sizes are not equal.
- `price_per_sqft_distribution.png`: the median derived rate is ₹5,674/sq ft. This is calculated from the cleaned target and area, so it is for analysis only and must not be used as a model input.
- `area_vs_price.png`: area and price have a Spearman rank correlation of 0.71, indicating a positive monotonic association in these listings. This is not a causal effect.
- `area_location_price.png`: shows how the area-price pattern varies across the six cities with the largest cleaned samples.
- `price_by_city.png`: among cities with at least 30 records, median prices range from ₹2,220,000 in vapi to ₹21,000,000 in mumbai. Differences may reflect property mix as well as location.
- `price_by_bedrooms.png`: group medians generally provide a simple comparison of listing prices by bedroom count; the chart suppresses extreme points so the common range remains readable.
- `price_by_furnishing.png`: compares median asking-price distributions across furnished categories; this is descriptive and does not control for city or property size. The observed median ranges from ₹5,980,000 to ₹7,000,000 across categories.
- `price_by_outlook.png`: compares the most common reported outlook descriptions. These are free-text combinations, not standardized amenity labels.
- `correlation_heatmap.png`: numeric correlations summarize linear relationships. Correlation does not establish cause, and derived price per square foot is target-dependent.
- `cleaning_steps.png`: shows how exact duplicate removal and required price/area filters reduce the raw row count.
- `raw_missingness.png`: shows that `Plot Area` and `Dimensions` are entirely empty, so they cannot be used.

The raw missing-value counts and percentages are in `reports/raw_missingness.csv`. Optional model features with missing values remain missing in the cleaned file; their imputers will be fitted on training data later. The source has no property-age field or dedicated amenities field. `location` is city-level; locality appears only in free text. The original `Price (in rupees)` field was not used as a predictor because its meaning is unclear and it has zero and extreme values. `source_index` is retained only to trace a cleaned row back to the raw archive and must be excluded from model features.

## Statistical comparison

Kruskal-Wallis test comparing asking-price distributions across 76 cities with at least 30 retained records: H = 18106.751, p < 0.001.

Null hypothesis: the cities have the same asking-price distribution. Alternative: at least one city has a different distribution. At the 0.05 level, the result is statistically significant, so the null hypothesis is rejected. Kruskal-Wallis does not require normally distributed prices, but it assumes independent observations; the interpretation as a median comparison also assumes similarly shaped group distributions. The test compares distributions, not causal city effects. Listings may not be independent if the source contains multiple records for the same property, and differences in property mix can affect the result.

## Interpretation limits

The dataset is a cross-sectional listing snapshot with no listing date. Asking prices are not confirmed sale prices. Locality is embedded in free text rather than supplied as a clean field. Price per square foot is derived from the asking price and selected area, so it is an analysis measure and must not be used as a predictor of that same price.

Figures are saved in `reports/figures/`. The full city summary is in `reports/city_price_summary.csv`; potentially unusual records are listed in `reports/outlier_review.csv` for review, not automatic deletion.
