__author__ = 'Chris'
from sqlalchemy_declarative import *
import math


class Index():
    def __init__(self):
        return

    def setGoodness(self):
        # self.idx = dict()
        for summoner in session.query(Summoner).all():
            # self.idx[summoner.summonerId] = dict()
            for champion in session.query(Champion).all():
                if len(session.query(SummonerToChampion).filter(SummonerToChampion.summonerId == summoner.id, SummonerToChampion.championId == champion.id).all()) > 0:
                    s2c = session.query(SummonerToChampion).filter(SummonerToChampion.summonerId == summoner.id, SummonerToChampion.championId == champion.id).all()[0]
                    print("Summoner %d: K= %d D= %d A= %d  Win: %d" % (s2c.summonerId, s2c.kills, s2c.deaths, s2c.assists, s2c.wins))
                    if s2c.deaths > 0:
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
                    # self.idx[summoner.summonerId][champion.championId] = s2c.goodness


    # def summonerSimilarity(self, s1, s2):



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