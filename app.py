import dash
from dash import html, dcc
from dotenv import load_dotenv
import os
import plotly.express as px
import pandas as pd

# Load environment variables from a .env file
load_dotenv()

# Retrieve the Mapbox token from the environment variable
mapbox_token = os.getenv("MAPBOX_TOKEN")

px.set_mapbox_access_token(mapbox_token)

df = pd.read_csv("data.csv")

fig = px.scatter_mapbox(
    df,
    lat="training_lat_coord",
    lon="training_lon_coord",
    size="marker_size",
    color="Groupe",
    zoom=9,
    hover_name="Club",
    hover_data={
        "Jour d'entraînement": True,
        "Début d'entraînement": True,
        "Commentaires": True,
        "training_lat_coord": False,
        "training_lon_coord": False,
        "marker_size": False,
    },
)

# Remove all margins in the figure layout
fig.update_layout(
    mapbox_style="streets",
    margin=dict(l=0, r=0, t=0, b=0),
)

app = dash.Dash(__name__)

# We apply a full-screen style to html and body in an external_stylesheets or by adding a <style> block.
# For simplicity, we can inline a style block in the layout:
app.index_string = """
    <!DOCTYPE html>
    <html>
        <head>
            <style>
                html, body {
                    margin: 0;
                    padding: 0;
                    height: 100%;
                    width: 100%;
                }
            </style>
        </head>
        <body>
            {%app_entry%}
            {%config%}
            {%scripts%}
            {%renderer%}
        </body>
    </html>
"""

app.layout = html.Div(
    style={
        "width": "100vw",
        "height": "100vh",
        "margin": "0",
        "padding": "0",
        "overflow": "hidden",
    },
    children=[
        dcc.Graph(
            figure=fig,
            style={"width": "100%", "height": "100%"},
            config={"scrollZoom": True},
        )
    ],
)

if __name__ == "__main__":
    app.run_server(debug=False)
