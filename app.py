import dash
from dash import html, dcc, Input, Output
from dotenv import load_dotenv
import os
import plotly.express as px
from model import Base, Championnat
from queries import carto_data
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Create engine and session factory
engine = create_engine("sqlite:///database.db", echo=False)
SessionLocal = sessionmaker(bind=engine)

# Ensure tables are created if they don't exist
Base.metadata.create_all(bind=engine)

# Load environment variables from a .env file
load_dotenv()
mapbox_token = os.getenv("MAPBOX_TOKEN")
px.set_mapbox_access_token(mapbox_token)

# Create a session
session = SessionLocal()

# Query distinct seasons and phases from championnats table for dropdowns
seasons = session.query(Championnat.season).distinct().all()
seasons = [s[0] for s in seasons]

# For phases, we can load them dynamically once a season is selected.
# For now, let's load phases for the first season as initial.
if seasons:
    initial_season = seasons[0]
    phases = (
        session.query(Championnat.phase)
        .filter(Championnat.season == initial_season)
        .distinct()
        .all()
    )
    phases = [p[0] for p in phases]
else:
    initial_season = None
    phases = []
    # If no data in database, handle gracefully

initial_phase = phases[0] if phases else None


# Load initial data
carto_df = carto_data(session, initial_season, initial_phase)

fig = px.scatter_mapbox(
    carto_df,
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

fig.update_layout(
    mapbox_style="streets",
    margin=dict(l=0, r=0, t=0, b=0),
    legend=dict(
        x=0,
        y=1,
        xanchor="left",
        yanchor="top",
        bgcolor="rgba(255,255,255,0.5)",
    ),
)

app = dash.Dash(__name__)

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
        "display": "flex",
        "flexDirection": "column",
        "height": "100vh",
        "width": "100vw",
        "margin": "0",
        "padding": "0",
        "overflow": "hidden",
    },
    children=[
        # Navbar with Season and Phase dropdowns
        html.Div(
            style={
                "height": "50px",
                "backgroundColor": "#333",
                "display": "flex",
                "alignItems": "center",
                "paddingLeft": "15px",
                "color": "#fff",
                "gap": "20px",
            },
            children=[
                html.Div("Champ'35 Loisir", style={"fontWeight": "bold"}),
                dcc.Dropdown(
                    id="season-dropdown",
                    options=[{"label": s, "value": s} for s in seasons],
                    value=initial_season,
                    placeholder="Select a season",
                    style={"width": "200px"},
                ),
                dcc.Dropdown(
                    id="phase-dropdown",
                    placeholder="Select a phase",
                    # The options will be updated dynamically based on season selection
                    options=[{"label": p, "value": p} for p in phases],
                    value=initial_phase,
                    style={"width": "200px"},
                ),
            ],
        ),
        # Map Container
        html.Div(
            style={"flex": "1", "overflow": "hidden"},
            children=[
                dcc.Graph(
                    id="map-graph",
                    figure=fig,
                    config={"scrollZoom": True},
                    style={"width": "100%", "height": "100%"},
                )
            ],
        ),
    ],
)


@app.callback(
    Output("phase-dropdown", "options"),
    Output("phase-dropdown", "value"),
    Input("season-dropdown", "value"),
)
def update_phase_options(selected_season):
    if selected_season is None:
        return [], None

    # Query phases for the selected season
    new_phases = (
        session.query(Championnat.phase)
        .filter(Championnat.season == selected_season)
        .distinct()
        .all()
    )
    new_phases = [p[0] for p in new_phases]
    return [{"label": p, "value": p} for p in new_phases], (
        new_phases[0] if new_phases else None
    )


@app.callback(
    Output("map-graph", "figure"),
    Input("season-dropdown", "value"),
    Input("phase-dropdown", "value"),
)
def update_figure(selected_season, selected_phase):
    if not selected_season or not selected_phase:
        # If dropdowns not selected, return empty map or some default
        return px.scatter_mapbox(lat=[], lon=[])

    updated_df = carto_data(session, selected_season, selected_phase)
    if updated_df.empty:
        # If no data, show empty map or some default layout
        empty_fig = px.scatter_mapbox(lat=[], lon=[])
        empty_fig.update_layout(mapbox_style="streets", margin=dict(l=0, r=0, t=0, b=0))
        return empty_fig

    updated_fig = px.scatter_mapbox(
        updated_df,
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
    updated_fig.update_layout(
        mapbox_style="streets",
        margin=dict(l=0, r=0, t=0, b=0),
        legend=dict(
            x=0,
            y=1,
            xanchor="left",
            yanchor="top",
            bgcolor="rgba(255,255,255,0.5)",
        ),
    )
    return updated_fig


if __name__ == "__main__":
    app.run_server(debug=False)
