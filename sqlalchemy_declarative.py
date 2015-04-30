__author__ = 'Chris'
import os
import sys
from sqlalchemy import *
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker

Base = declarative_base()

class Summoner(Base):
    __tablename__ = 'summoner'

    id = Column(Integer, primary_key=True)
    summonerId = Column(Integer, nullable=False)
    name = Column(String(20))
    profileIconId = Column(Integer)
    revisionDate = Column(Integer)
    summonerLevel = Column(Integer)
    winRate = Column(Integer)
    matches = relationship("SummonerToMatch", backref="summoner")
    champions = relationship("SummonerToChampion", backref="summoner")

class Match(Base):
    __tablename__ = 'match'

    id = Column(Integer, primary_key=True)
    matchId = Column(Integer, nullable=False)
    mapId = Column(Integer)
    creation = Column(Integer)
    duration = Column(Integer)
    mode = Column(String(250))
    type = Column(String(250))
    version = Column(String(250))
    platformId = Column(String(250))
    queueType = Column(String(250))
    region = Column(String(250))
    season = Column(String(250))


class SummonerToMatch(Base):
    __tablename__ = 'summoner_to_match'
    id = Column(Integer, primary_key=True)
    summonerId = Column(Integer, ForeignKey('summoner.id'))
    matchId = Column(Integer, ForeignKey('match.id'))
    match = relationship("Match", backref="summoner_assocs")
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
    win = Column(String(5))
    goodness = Column(Integer)

class Champion(Base):
    __tablename__ = 'champion'
    id = Column(Integer, primary_key=True)
    name = Column(String(250))
    championId = Column(Integer, nullable=False)
    armor = Column(Float)
    armorperlevel = Column(Float)
    attackdamage = Column(Float)
    attackdamageperlevel = Column(Float)
    attackrange = Column(Float)
    attackspeedoffset = Column(Float)
    attackspeedperlevel = Column(Float)
    crit = Column(Float)
    critperlevel = Column(Float)
    hp = Column(Float)
    hpperlevel = Column(Float)
    hpregen = Column(Float)
    hpregenperlevel = Column(Float)
    movespeed = Column(Float)
    mp = Column(Float)
    mpperlevel = Column(Float)
    mpregen = Column(Float)
    mpregenperlevel = Column(Float)
    spellblock = Column(Float)
    spellblockperlevel = Column(Float)

    defense = Column(Integer)
    magic = Column(Integer)
    difficulty = Column(Integer)
    attack = Column(Integer)

    avggoodness = Column(Integer)

    # tags = Column(Float)
class SummonerToChampion(Base):
    __tablename__ = 'summoner_to_champion'
    id = Column(Integer, primary_key=True)
    summonerId = Column(Integer, ForeignKey('summoner.id'))
    championId = Column(Integer, ForeignKey('champion.id'))
    champion = relationship("Champion", backref="summoner_assocs")
    kills = Column(Integer)
    deaths = Column(Integer)
    assists = Column(Integer)
    wins = Column(Integer)
    games = Column(Integer)
    goodness = Column(Integer)



# Create an engine that stores data in the local directory's
# sqlalchemy_example.db file.
engine = create_engine('sqlite:///data.db')

# Create all tables in the engine. This is equivalent to "Create Table"
# statements in raw SQL.
Base.metadata.create_all(engine)
