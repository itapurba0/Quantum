from dash import Dash, html
import pandas as pd

# Minimal Dash app used to validate the environment and demonstrate dash + pandas

def create_sample_df():
    return pd.DataFrame({'x': [1, 2, 3], 'y': [1, 4, 9]})

app = Dash(__name__)
df = create_sample_df()

app.layout = html.Div([
    html.H1("Quantium starter — Dash setup check"),
    html.Div(f"Data preview (first rows): {df.head().to_dict()}")
])

if __name__ == '__main__':
    # Running the server requires the `dash` package to be installed in the active venv.
    app.run_server(debug=True)

