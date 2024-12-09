import dash
from dash import html, dcc
from dotenv import load_dotenv
import os
import plotly.express as px

# Load environment variables from a .env file
load_dotenv()

# Retrieve the Mapbox token from the environment variable
mapbox_token = os.getenv("MAPBOX_TOKEN")

px.set_mapbox_access_token(mapbox_token)

# Sample data
df = px.data.carshare()

# Create a Mapbox figure. You can customize the data and layout as needed.
fig = px.scatter_mapbox(
    df,
    lat="centroid_lat",
    lon="centroid_lon",
    size="car_hours",
    color="peak_hour",
    color_continuous_scale=px.colors.cyclical.IceFire,
    size_max=15,
    zoom=10,
    title="Sample Mapbox Visualization"
)

# Set the Mapbox style and remove extra margins for a cleaner full-screen view
fig.update_layout(
    mapbox_style="streets",
    margin={"r": 0, "t": 0, "l": 0, "b": 0}
)

# Initialize Dash
app = dash.Dash(__name__)

# Full-screen styling applied to the outer div
app.layout = html.Div(
    style={
        "width": "100vw",
        "height": "100vh",
        "margin": "0",
        "padding": "0",
        "overflow": "hidden"
    },
    children=[
        dcc.Graph(
            figure=fig,
            style={"width": "100%", "height": "100%"}
        )
    ]
)

if __name__ == "__main__":
    app.run_server(debug=True)
