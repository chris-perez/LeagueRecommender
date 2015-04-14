__author__ = 'Chris'

from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy import create_engine
from sqlalchemy_declarative import *


class Spider():

    def parseMatch(self, match):
        id = match['matchId']
        mapId = match['mapId']
        creation = match['matchCreation']
        duration = match['matchDuration']
        mode = match['matchMode']
        type = match['matchType']
        version = match['matchVersion']
        platformId = match['platformId']
        queueType = match['queueType']
        region = match['region']
        season = match['season']

        for p in match['participantIdentities']:
            self.parseSummoner(p['player']['summonerId'])

        m = Match(id=id, mapId=mapId, creation=creation, duration=duration, mode=mode, type=type, version=version, platformId=platformId, queueType=queueType, region=region, season=season)
        session.add(m)
        session.commit()

    def parseSummoner(self, summoner):
        id = summoner['summonerId']
        name = summoner['summonerName']
        s = Summoner(id=id, name=name)
        session.add(s)
        session.commit()


    # Create an engine that stores data in the local directory's
    # sqlalchemy_example.db file.
engine = create_engine("sqlite:///data.db")

# A DBSession() instance establishes all conversations with the database
# and represents a "staging zone" for all the objects loaded into the
# database session object. Any change made against the objects in the
# session won't be persisted into the database until you call
# session.commit(). If you're not happy about the changes, you can
# revert all of them back to the last commit by calling
# session.rollback()
DBSession = sessionmaker(bind=engine)
session = DBSession()