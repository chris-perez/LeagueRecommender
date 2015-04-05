__author__ = 'Chris'
import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy import create_engine

Base = declarative_base()

class Summoner(Base):
    __tablename__ = 'summoner'

    id = Column(Integer, primary_key=True)
    name = Column(String(20), nullable=False)
    profileIconId = Column(Integer)
    revisionDate = Column(Integer)
    summonerLevel = Column(Integer)
    winRate = Column(Integer)

class Match(Base):
    __tablename__ = 'match'
    id = Column(Integer, primary_key=True)

class SummonerToMatch(Base):
    __tablename__ = 'summoner_to_match'
    id = Column(Integer, primary_key=True)

class SummonerToChampion(Base):
    __tablename__ = 'summoner_to_champion'
    id = Column(Integer, primary_key=True)


# Create an engine that stores data in the local directory's
# sqlalchemy_example.db file.
engine = create_engine('sqlite:///data.db')

# Create all tables in the engine. This is equivalent to "Create Table"
# statements in raw SQL.
Base.metadata.create_all(engine)
