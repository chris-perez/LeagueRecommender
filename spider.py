__author__ = 'Chris'

from sqlalchemy import *
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy import create_engine
from sqlalchemy_declarative import *
from riot import *


class Spider():

    def __init__(self):
        self.riot = Riot()

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

        m = Match(id=id, mapId=mapId, creation=creation, duration=duration, mode=mode, type=type, version=version, platformId=platformId, queueType=queueType, region=region, season=season)
        for p in match['participantIdentities']:
            summoner = self.parseSummoner(p['player']['summonerId'])
            s2m = SummonerToMatch()
            s2m.match = match
            summoner.matches.append(s2m)
            session.add(s2m)
            if summoner not in session.query(Summoner).filter(Summoner.id.in_([summoner.id])).all():
                session.add(summoner)
        if session.query(Match).filter(Match.id.in_([m.id])).all()[0] is None:
            session.add(m)
        session.commit()

    def parseSummoner(self, summoner):
        id = summoner['summonerId']
        name = summoner['summonerName']
        s = Summoner(id=id, name=name)
        return s


    def run(self):
        summoner = self.riot.getSummonerByName("chrispychips5")
        summonerId = summoner["id"]
        matchHistory = self.riot.getMatchHistory(summonerId)
        for match in matchHistory:
            self.parseMatch(match)



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