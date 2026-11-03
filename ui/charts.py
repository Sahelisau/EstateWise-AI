import plotly.express as px


def style(fig, height=360):
    fig.update_layout(
        template="plotly_dark",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font={"family": "Inter, Segoe UI, sans-serif", "color": "#dce6f4", "size": 12},
        margin={"l": 8, "r": 8, "t": 42, "b": 8},
        height=height,
        legend_title_text="",
    )
    fig.update_xaxes(showgrid=False, zeroline=False, linecolor="rgba(151,174,204,.14)")
    fig.update_yaxes(gridcolor="rgba(151,174,204,.10)", zeroline=False)
    return fig


def city_medians(data, limit=20):
    grouped = data.groupby("city").agg(
        median_price_inr=("price_inr", "median"),
        records=("price_inr", "size"),
        median_area_sqft=("area_sqft", "median"),
    ).query("records >= 30").sort_values("median_price_inr").tail(limit).reset_index()
    fig = px.bar(
        grouped,
        x="median_price_inr",
        y="city",
        orientation="h",
        color="median_price_inr",
        color_continuous_scale=["#78a9ff", "#36c9a5"],
        hover_data={"median_price_inr": ":,.0f", "records": ":,", "median_area_sqft": ":,.0f"},
        labels={"city": "City", "median_price_inr": "Median asking price (INR)", "records": "Dataset records", "median_area_sqft": "Median area (sq. ft.)"},
    )
    return style(fig, max(360, 25 * len(grouped)))
