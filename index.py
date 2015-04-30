__author__ = 'Chris'
from sqlalchemy_declarative import *
import math


class Index():
    def __init__(self):
        return

    def setGoodness(self):
        self.idx = dict()
        self.s2s = dict()
        self.c2c = dict()
        i = 0
        for summoner in session.query(Summoner).all():
            if i > 600:
                break
            i += 1
            self.idx[summoner.summonerId] = dict()
            for champion in session.query(Champion).all():
                if len(session.query(SummonerToChampion).filter(SummonerToChampion.summonerId == summoner.id, SummonerToChampion.championId == champion.id).all()) > 0:
                    s2c = session.query(SummonerToChampion).filter(SummonerToChampion.summonerId == summoner.id, SummonerToChampion.championId == champion.id).all()[0]
                    print("Summoner %d: K= %d D= %d A= %d  Win: %d" % (s2c.summonerId, s2c.kills, s2c.deaths, s2c.assists, s2c.wins))
                    if s2c.deaths > 0:
                        #normalize = goodness/sum of goodness
                        goodness = (((s2c.kills + .75 * s2c.assists) / s2c.deaths) + .1*s2c.wins)/s2c.games
                        if(goodness > 0):
                            s2c.goodness = math.log10(goodness)
                        else:
                            s2c.goodness = 0
                    else:
                        goodness = (((s2c.kills + .75 * s2c.assists) / 1) + .1*s2c.wins)/s2c.games
                        if(goodness > 0):
                            s2c.goodness = math.log10(goodness)
                        else:
                            s2c.goodness = 0

                    session.commit()
                    self.idx[summoner.summonerId][champion.championId] = s2c.goodness
            self.s2s[summoner.summonerId] = dict()
        # Summoner to Summoner similarity
        for s1 in self.s2s.keys():
            for s2 in self.s2s.keys():
                s1[s2] = 0
                total = 0
                for champion in session.query(Champion).all():
                    total += self.idx[s1][champion.championId] * self.idx[s2][champion.championId]
                self.s2s[s1][s2] = total

        # Champion to Champion similarity
        for c1 in session.query(Champion).all():
            for c2 in session.query(Champion).all():
                total = 0
                for summoner in self.s2s.keys():
                    total += self.idx[summoner][c1.championId] * self.idx[summoner][c2.championId]

    # def summonerSimilarity(self, s1, s2):

    # def champSuggestion(self):


def main():
    index = Index()
    index.setGoodness()


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