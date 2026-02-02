from dash import Dash, dcc, html, Input, Output
import plotly.express as px
import pandas as pd

DATA_PATH = "pink_morsel_sales.csv"
PRICE_INCREASE_DATE = "2021-01-15"
REGION_OPTIONS = [
    {"label": "All regions", "value": "all"},
    {"label": "North", "value": "north"},
    {"label": "East", "value": "east"},
    {"label": "South", "value": "south"},
    {"label": "West", "value": "west"},
]

app = Dash(__name__)
server = app.server

try:
    df = pd.read_csv(DATA_PATH, parse_dates=["Date"])
except Exception:
    df = pd.DataFrame(columns=["Sales", "Date", "Region"])


def filter_sales(region_value: str) -> pd.DataFrame:
    if df.empty:
        return df
    if region_value and region_value != "all":
        return df[df["Region"] == region_value]
    return df


def summarize_periods(agg: pd.DataFrame) -> str:
    inc_date = pd.to_datetime(PRICE_INCREASE_DATE)
    before = agg[agg["Date"] < inc_date]["Sales"].sum()
    after = agg[agg["Date"] >= inc_date]["Sales"].sum()
    trend = "after" if after > before else "before" if before > after else "about the same"
    return f"Total sales before {PRICE_INCREASE_DATE}: ${before:,.2f} — after: ${after:,.2f}. Higher {trend}."


def create_figure(agg: pd.DataFrame) -> px.line:
    fig = px.line(
        agg,
        x="Date",
        y="Sales",
        title="Daily Sales (Pink Morsel)",
        labels={"Sales": "Total Sales ($)", "Date": "Date"},
    )
    try:
        fig.add_vline(
            x=pd.to_datetime(PRICE_INCREASE_DATE),
            line_dash="dash",
            line_color="#ff6f61",
            annotation_text="Price increase",
            annotation_position="top left",
        )
    except Exception:
        pass
    fig.update_layout(hovermode="x unified", margin=dict(t=60, b=40))
    return fig


app.layout = html.Div(
    className="page",
    children=[
        html.Header(
            className="header-card",
            children=[
                html.H1("Pink Morsel Sales — Before vs After Price Increase"),
                html.P(
                    "Tune into region-specific sales and watch how demand reacted to the January 15 price change."
                ),
            ],
        ),
        html.Div(
            className="controls",
            children=[
                html.Label("Filter by region", className="controls-label"),
                dcc.RadioItems(
                    id="region-filter",
                    options=REGION_OPTIONS,
                    value="all",
                    inline=True,
                    className="region-radio",
                ),
            ],
        ),
        html.Div(
            className="chart-card",
            children=[
                dcc.Graph(id="sales-line", config={"displayModeBar": False}),
                html.Div(id="summary", className="summary"),
            ],
        ),
    ],
)


@app.callback(Output("sales-line", "figure"), Output("summary", "children"), Input("region-filter", "value"))
def update_chart(region_value: str):
    filtered = filter_sales(region_value)
    if filtered.empty:
        return px.line(title="No data available"), "No sales data to display yet."

    filtered["Date"] = pd.to_datetime(filtered["Date"])
    agg = filtered.groupby("Date", as_index=False)["Sales"].sum().sort_values("Date")
    fig = create_figure(agg)
    summary = summarize_periods(agg)
    return fig, summary


if __name__ == "__main__":
    app.run(debug=True)
