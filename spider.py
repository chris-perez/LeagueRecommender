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

        if len(session.query(Summoner).filter(Summoner.summonerId == summonerId).all()) <= 0:
            session.add(summoner)
        else:
            summoner = session.query(Summoner).filter(Summoner.summonerId == summonerId).all()[0]

        if len(session.query(Match).filter(Match.matchId == m.matchId).all()) <= 0:
            session.add(m)
        else:
            m = session.query(Match).filter(Match.matchId == m.matchId).all()[0]

        s2m = SummonerToMatch(win=win, kills=kills, deaths=deaths, assists=assists, championId=championId)
        s2m.match = m
        if len(session.query(SummonerToMatch).filter(SummonerToMatch.summonerId == summoner.id, SummonerToMatch.matchId == m.id).all()) <= 0:
            summoner.matches.append(s2m)
            session.add(s2m)

            if len(session.query(SummonerToChampion).filter(SummonerToChampion.summonerId == summoner.id, SummonerToChampion.championId == championId).all()) <= 0:
                s2c = SummonerToChampion(summonerId=summonerId, championId=championId, kills=kills, deaths=deaths, assists=assists, games=1)
                if win:
                    s2c.wins = 1
                else:
                    s2c.wins = 0
                summoner.champions.append(s2c)
                session.add(s2c)
            else:
                s2c = session.query(SummonerToChampion).filter(SummonerToChampion.summonerId == summoner.id, SummonerToChampion.championId == championId).all()[0]
                s2c.kills += kills
                s2c.deaths += deaths
                s2c.assists += assists
                s2c.games += 1
                if win:
                    s2c.wins += 1

        for p in match["fellowPlayers"]:
            if p["summonerId"] != summonerId:
                self.summonersToSearch.append(p["summonerId"])

        session.commit()

    def parseChampions(self):
        champions = self.riot.getChampionInfo()
        for champ in champions["data"]:
            c = champions["data"][champ]
            name = champ
            championId = c["id"]
            armor = c["stats"]["armor"]
            armorperlevel = c["stats"]["armorperlevel"]
            attackdamage = c["stats"]["attackdamage"]
            attackdamageperlevel = c["stats"]["attackdamageperlevel"]
            attackrange = c["stats"]["attackrange"]
            attackspeedoffset = c["stats"]["attackspeedoffset"]
            attackspeedperlevel = c["stats"]["attackspeedperlevel"]
            crit = c["stats"]["crit"]
            critperlevel = c["stats"]["critperlevel"]
            hp = c["stats"]["hp"]
            hpperlevel = c["stats"]["hpperlevel"]
            hpregen = c["stats"]["hpregen"]
            hpregenperlevel = c["stats"]["hpregenperlevel"]
            movespeed = c["stats"]["movespeed"]
            mp = c["stats"]["mp"]
            mpperlevel = c["stats"]["mpperlevel"]
            mpregen = c["stats"]["mpregen"]
            mpregenperlevel = c["stats"]["mpregenperlevel"]
            spellblock = c["stats"]["spellblock"]
            spellblockperlevel = c["stats"]["spellblockperlevel"]

            defense = c["info"]["defense"]
            magic = c["info"]["magic"]
            difficulty = c["info"]["difficulty"]
            attack = c["info"]["attack"]

            # tags = champ["tags"]
            if len(session.query(Champion).filter(Champion.championId == championId).all()) <= 0:
                c = Champion(championId=championId, armor=armor, armorperlevel=armorperlevel, attackdamage=attackdamage,
                             attackdamageperlevel=attackdamageperlevel, attackrange=attackrange, attackspeedoffset=attackspeedoffset,
                             attackspeedperlevel=attackspeedperlevel, crit=crit, critperlevel=critperlevel, hp=hp,
                             hpperlevel=hpperlevel, hpregen=hpregen, hpregenperlevel=hpregenperlevel, movespeed=movespeed, mp=mp,
                             mpperlevel=mpperlevel, mpregen=mpregen, mpregenperlevel=mpregenperlevel, spellblock=spellblock,
                             spellblockperlevel=spellblockperlevel, defense=defense, magic=magic, difficulty=difficulty, attack=attack,
                             name=name)
                session.add(c)
                session.commit()

    def makeSummonerToChampTable(self):
        for summoner in session.query(Summoner).all():
            print("Summoner Id: " + str(summoner.id))
            for match in session.query(SummonerToMatch).filter(SummonerToMatch.summonerId == summoner.id).all():
                if len(session.query(SummonerToChampion).filter(SummonerToChampion.summonerId == match.summonerId, SummonerToChampion.championId == match.championId).all()) <= 0:
                    s2c = SummonerToChampion(summonerId=match.summonerId, championId=match.championId, kills=match.kills, deaths=match.deaths, assists=match.assists, games=1)
                    if int(match.win) > 0:
                        s2c.wins = 1
                    else:
                        s2c.wins = 0
                    summoner.champions.append(s2c)
                    session.add(s2c)
                    session.commit()
                else:
                    s2c = session.query(SummonerToChampion).filter(SummonerToChampion.summonerId == summoner.id, SummonerToChampion.championId == match.championId).all()[0]
                    s2c.kills += match.kills
                    s2c.deaths += match.deaths
                    s2c.assists += match.assists
                    s2c.games += 1
                    if int(match.win) > 0:
                        s2c.wins += 1
        return

    def parseSummoner(self, summoner):
        id = summoner['summonerId']
        name = summoner['summonerName']
        s = Summoner(summonerId=id, name=name)
        return s


    def run(self):
        # my ID =  28866449
        names = ["chrispychips5", "frozenbastion", "begginstrips", "jumbone", "milkbone", "pupperoni", "spriteknight",
                 "catmanavan", "demonecorvo", "happilymourning", "kirbstomper", "mystletaynn",
                 "nignagpoliwag", "siegemaximo", "thisiscaptain", "wham", "cannedsheep",
                 "sintar", "gluck", "baskseven", "laughingdead", "jabujabu"]
        for name in names:
            summoner = self.riot.getSummonerByName(name)
            print(summoner)
            summonerId = summoner[name]["id"]
            self.summonersToSearch.append(summonerId)

        while len(self.summonersToSearch) > 0:
            summonerId = self.summonersToSearch.pop(0)
            print(summonerId)
            matchHistory = self.riot.getMatchHistory(summonerId)["games"]
            print(matchHistory)

            for match in matchHistory:
                if match["gameType"] == "MATCHED_GAME":
                    if(match["subType"] == "NORMAL" or match["subType"] == "NORMAL_3x3" or
                        match["subType"] == "RANKED_SOLO_5x5" or match["subType"] == "RANKED_PREMADE_5x5" or
                            match["subType"] == "RANKED_TEAM_5x5" or match["subType"] == "RANKED_TEAM_3x3"):
                                self.parseMatch(match, summonerId)



# def math():
#     kills=0
#     assists=0
#     towerKills=0
#     deaths=1
#     win = 1
#     goodness = log((kills + .75*assists + .5*towerKills)/deaths) + .1*win

def main():
    spider = Spider()
    # spider.parseChampions()
    # spider.run()
    spider.makeSummonerToChampTable()
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