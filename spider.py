__author__ = 'Chris'

from sqlalchemy import *
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy import create_engine
from sqlalchemy_declarative import *
from riot import *
import time


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

        m = Match(matchId=id, mapId=mapId, creation=creation, mode=mode, type=type)

        stats = match["stats"]
        win = stats["win"]
        championId = match["championId"]
        if "championsKilled" in stats:
            kills = stats["championsKilled"]
        else:
            kills = 0
        if "numDeaths" in stats:
            deaths = stats["numDeaths"]
        else:
            deaths = 0
        if "assists" in stats:
            assists = stats["assists"]
        else:
            assists = 0
        summoner = Summoner(summonerId=summonerId)
        s2m = SummonerToMatch(win=win, kills=kills, deaths=deaths, assists=assists, championId=championId)
        s2m.match = m
        if len(session.query(SummonerToMatch).filter(SummonerToMatch.summonerId == summoner.id, SummonerToMatch.matchId == m.id).all()) <= 0:
            summoner.matches.append(s2m)
            session.add(s2m)

        if len(session.query(SummonerToChampion).filter(SummonerToChampion.summonerId == summonerId, SummonerToChampion.championId == championId).all()) <= 0:
            s2c = SummonerToChampion(summonerId=summonerId, championId=championId, kills=kills, deaths=deaths, assists=assists, games=1)
            if win:
                s2c.wins = 1
            summoner.champions.append(s2c)
            session.add(s2c)
        else:
            s2c = session.query(Summoner).filter(SummonerToChampion.summonerId == summonerId, SummonerToChampion.championId == championId).all()[0]
            s2c.kills += kills
            s2c.deaths += deaths
            s2c.assists += assists
            s2c.games += 1
            if win:
                s2c.wins += 1

        for p in match["fellowPlayers"]:
            if p["summonerId"] != summonerId:
                self.summonersToSearch.append(p["summonerId"])

        if len(session.query(Summoner).filter(Summoner.summonerId == summonerId).all()) <= 0:
            session.add(summoner)
        if len(session.query(Match).filter(Match.matchId == m.matchId).all()) <= 0:
            session.add(m)
        session.commit()

    def parseSummoner(self, summoner):
        id = summoner['summonerId']
        name = summoner['summonerName']
        s = Summoner(summonerId=id, name=name)
        return s


    def run(self):
        summoner = self.riot.getSummonerByName("chrispychips5")
        time.sleep(1.2)
        print(summoner)
        # my ID =  28866449
        summonerId = summoner["chrispychips5"]["id"]
        self.summonersToSearch.append(summonerId)
        while len(self.summonersToSearch) > 0:
            summonerId = self.summonersToSearch.pop(0)
            print(summonerId)
            matchHistory = self.riot.getMatchHistory(summonerId)["games"]
            time.sleep(1.2)
            print(matchHistory)

            for match in matchHistory:
                if match["gameType"] == "MATCHED_GAME":
                    if(match["subType"] == "NORMAL" or match["subType"] == "NORMAL_3x3" or
                        match["subType"] == "RANKED_SOLO_5x5" or match["subType"] == "RANKED_PREMADE_5x5" or
                            match["subType"] == "RANKED_TEAM_5x5" or match["subType"] == "RANKED_TEAM_3x3"):
                                self.parseMatch(match, summonerId)


def main():
    spider = Spider()
    spider.run()

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

main()