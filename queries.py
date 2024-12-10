import pandas as pd
from model import Club, Groupe, Training, Championnat


def carto_data(session, season, phase):
    """
    Load clubs, trainings, and groupes filtered by season and phase.
    Returns a DataFrame with the necessary columns.
    """
    # SQLAlchemy query to get all the needed info
    # c = clubs (Club), t = trainings (Training), g = groupes (Groupe), ch = championnats (Championnat)
    query = (
        session.query(
            Club.club_name,
            Club.latitude,
            Club.longitude,
            Training.jour_entrainement.label("Jour d'entraînement"),
            Training.debut_entrainement.label("Début d'entraînement"),
            Training.fin_entrainement.label("Fin d'entraînement"),
            Groupe.groupe.label("Groupe"),
            Club.commentaires.label("Commentaires"),
            Club.marker_size,
            Club.created,
            Club.updated,
            Club.deleted,
        )
        .join(Groupe, Club.id == Groupe.club_id)
        .join(Championnat, Groupe.championnat_id == Championnat.id)
        .join(Training, Club.id == Training.club_id)
        .filter(Championnat.season == season, Championnat.phase == phase)
    )

    results = query.all()
    df = pd.DataFrame(
        results,
        columns=[
            "Club",
            "training_lat_coord",
            "training_lon_coord",
            "Jour d'entraînement",
            "Début d'entraînement",
            "Fin d'entraînement",
            "Groupe",
            "Commentaires",
            "marker_size",
            "created",
            "updated",
            "deleted",
        ],
    )
    return df
