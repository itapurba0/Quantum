# New Dash app to visualize Pink Morsel sales by date
# ...existing code...
from dash import Dash, dcc, html, Input, Output
import plotly.express as px
import pandas as pd

DATA_PATH = "pink_morsel_sales.csv"
PRICE_INCREASE_DATE = "2021-01-15"

app = Dash(__name__)

# Load data
try:
    df = pd.read_csv(DATA_PATH, parse_dates=["Date"])
except Exception:
    df = pd.DataFrame(columns=["Sales", "Date", "Region"])

# Prepare region options
regions = sorted(df["Region"].dropna().unique().tolist()) if not df.empty else []
region_options = [{"label": r.title(), "value": r} for r in regions]

app.layout = html.Div([
    html.H1("Pink Morsel Sales — Before vs After Price Increase"),
    html.P("Interactive visualiser showing total daily sales for Pink Morsels. Select a region to filter."),
    dcc.Dropdown(id="region-filter", options=region_options, placeholder="All regions", clearable=True),
    dcc.Graph(id="sales-line"),
    html.Div(id="summary")
])


@app.callback(
    Output("sales-line", "figure"),
    Output("summary", "children"),
    Input("region-filter", "value")
)
def update_chart(region):
    if df.empty:
        return px.line(title="No data available"), "No data"
    dff = df.copy()
    if region:
        dff = dff[dff["Region"] == region]
    # Aggregate sales by date
    dff["Date"] = pd.to_datetime(dff["Date"])
    agg = dff.groupby("Date", as_index=False)["Sales"].sum().sort_values("Date")

    fig = px.line(agg, x="Date", y="Sales", title="Daily Sales (Pink Morsel)", labels={"Sales":"Total Sales ($)", "Date":"Date"})
    # Add vertical line for price increase date
    try:
        fig.add_vline(x=pd.to_datetime(PRICE_INCREASE_DATE), line_dash="dash", line_color="red", annotation_text="Price increase", annotation_position="top left")
    except Exception:
        pass

    # Simple before/after comparison
    inc_date = pd.to_datetime(PRICE_INCREASE_DATE)
    before = agg[agg["Date"] < inc_date]["Sales"].sum()
    after = agg[agg["Date"] >= inc_date]["Sales"].sum()
    more = "after" if after > before else "before" if before > after else "about the same"
    summary = f"Total sales before {PRICE_INCREASE_DATE}: ${before:,.2f} — after: ${after:,.2f}. Higher {more}."

    return fig, summary


if __name__ == "__main__":
    app.run(debug=True)
