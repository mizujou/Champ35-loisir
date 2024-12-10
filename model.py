from sqlalchemy import Column, Integer, Text, ForeignKey, Float
from sqlalchemy.orm import relationship, declarative_base

# Define a base class for declarative models
Base = declarative_base()


class Club(Base):
    __tablename__ = "clubs"

    id = Column(Integer, primary_key=True)
    club_name = Column(Text)
    latitude = Column(Float)
    longitude = Column(Float)
    commentaires = Column(Text)
    marker_size = Column(Integer)
    created = Column(Text)
    updated = Column(Text)
    deleted = Column(Text)

    trainings = relationship("Training", back_populates="club")
    groupes = relationship("Groupe", back_populates="club")


class Training(Base):
    __tablename__ = "trainings"

    id = Column(Integer, primary_key=True)
    club_id = Column(Integer, ForeignKey("clubs.id"))
    jour_entrainement = Column(Text)
    debut_entrainement = Column(Text)
    fin_entrainement = Column(Text)
    commentaires = Column(Text)
    created = Column(Text)
    updated = Column(Text)
    deleted = Column(Text)

    club = relationship("Club", back_populates="trainings")


class Championnat(Base):
    __tablename__ = "championnats"

    id = Column(Integer, primary_key=True)
    season = Column(Text)
    phase = Column(Text)
    commentaires = Column(Text)
    created = Column(Text)
    updated = Column(Text)
    deleted = Column(Text)

    groupes = relationship("Groupe", back_populates="championnat")


class Groupe(Base):
    __tablename__ = "groupes"

    id = Column(Integer, primary_key=True)
    club_id = Column(Integer, ForeignKey("clubs.id"))
    championnat_id = Column(Integer, ForeignKey("championnats.id"))
    groupe = Column(Text)
    commentaires = Column(Text)
    created = Column(Text)
    updated = Column(Text)
    deleted = Column(Text)

    club = relationship("Club", back_populates="groupes")
    championnat = relationship("Championnat", back_populates="groupes")
