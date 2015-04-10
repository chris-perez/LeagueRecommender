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
    summonerId = Column(Integer)
    name = Column(String(20), nullable=False)#not sure how if you want to use summonerID or name
    matchId = Column(Integer)
    championId = Column(Integer)
    previousRank = Column(String(20))
    summonerSpell1 = Column(Integer)
    summonerSpell2 = Column(Integer)
    kills = Column(Integer)
    deaths = Column(Integer)
    assists = Column(Integer)
    champLevel = Column(Integer)
    firstBloodKill = Column(String(5))
    goldEarned = Column(Integer)
    towerKills = Column(Integer)
    winner = (String(5))

class SummonerToChampion(Base):
    __tablename__ = 'summoner_to_champion'
    id = Column(Integer, primary_key=True)
    summonerId = Column(Integer)
    name = Column(String(20), nullable=False)
    championId = Column(Integer)
    kills = Column(Integer)
    deaths = Column(Integer)
    assists = Column(Integer)
    wins = Column(Integer)
    games = Column(Integer)


# Create an engine that stores data in the local directory's
# sqlalchemy_example.db file.
engine = create_engine('sqlite:///data.db')

# Create all tables in the engine. This is equivalent to "Create Table"
# statements in raw SQL.
Base.metadata.create_all(engine)
