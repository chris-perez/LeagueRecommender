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
        self.summonersToSearch = []

    def parseMatch(self, match, summonerId):
        id = match['gameId']
        mapId = match['mapId']
        creation = match['createDate']
        mode = match['gameMode']
        type = match['subType']

        m = Match(id=id, mapId=mapId, creation=creation, mode=mode, type=type)

        stats = match["stats"]
        win = stats["win"]
        champion = match["championId"]
        kills = stats["championsKilled"]
        deaths = stats["numDeaths"]
        assists = stats["assists"]
        summoner = Summoner(id=summonerId)
        s2m = SummonerToMatch(win=win, kills=kills, deaths=deaths, assists=assists)
        s2m.match = match
        summoner.matches.append(s2m)
        session.add(s2m)

        for p in match["fellowPlayers"]:
            self.summonersToSearch.append(p["summonerId"])

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
        # my ID =  28866449
        summonerId = summoner["chrispychips5"]["id"]
        self.summonersToSearch.append(summonerId)
        while len(self.summonersToSearch) > 0:
            summonerId = self.summonersToSearch.pop(0)
            matchHistory = self.riot.getMatchHistory(summonerId)["games"]
            for match in matchHistory:
                if match["gameType"] == "MATCHED_GAME":
                    if(match["subType"] == "NORMAL" or match["subType"] == "NORMAL_3x3" or
                        match["subType"] == "RANKED_SOLO_5x5" or match["subType"] == "RANKED_PREMADE_5x5" or
                            match["subType"] == "RANKED_TEAM_5x5" or match["subType"] == "RANKED_TEAM_3x3"):
                                self.parseMatch(match, summonerId)

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