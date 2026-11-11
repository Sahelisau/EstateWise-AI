import plotly.express as px


def style(fig, height=360):
    fig.update_layout(
        template="plotly_white",
        font={"family": "Inter, Plus Jakarta Sans, Segoe UI, sans-serif", "color": "#526071", "size": 12},
        margin={"l": 12, "r": 16, "t": 30, "b": 12},
        height=height,
        legend_title_text="",
        paper_bgcolor="rgba(255,255,255,0)",
        plot_bgcolor="rgba(255,255,255,0)",
    )
    fig.update_xaxes(showgrid=False, zeroline=False, linecolor="#E5E9ED", tickfont_color="#647184")
    fig.update_yaxes(gridcolor="#EDF0F2", zeroline=False, tickfont_color="#647184")
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
        color_discrete_sequence=["#087F5B"],
        hover_data={"median_price_inr": ":,.0f", "records": ":,", "median_area_sqft": ":,.0f"},
        labels={"city": "City", "median_price_inr": "Median asking price (INR)", "records": "Dataset records", "median_area_sqft": "Median area (sq. ft.)"},
    )
    fig.update_traces(marker_line_width=0, hovertemplate="%{y}<br>Median price: ₹%{x:,.0f}<extra></extra>")
    return style(fig, max(360, 27 * len(grouped)))
