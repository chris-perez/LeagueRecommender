__author__ = 'Chris'
from riot import *
from sqlalchemy_declarative import *
import math
import operator


class Index():
    def __init__(self):
        self.riot = Riot()
        self.idx = dict()
        self.s2s = dict()
        self.c2c = dict()
        i = 0
        for summoner in session.query(Summoner).all():
            # number of test champions
            if i > 30:
                break
            i += 1
            self.idx[summoner.summonerId] = dict()
            for champion in session.query(Champion).all():
                if len(session.query(SummonerToChampion).filter(SummonerToChampion.summonerId == summoner.id, SummonerToChampion.championId == champion.championId).all()) > 0:
                    s2c = session.query(SummonerToChampion).filter(SummonerToChampion.summonerId == summoner.id, SummonerToChampion.championId == champion.championId).all()[0]
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
                else:
                    self.idx[summoner.summonerId][champion.championId] = 0
            self.s2s[summoner.summonerId] = dict()
        # Summoner to Summoner similarity
        for s1 in self.s2s.keys():
            for s2 in self.s2s.keys():
                # s1[s2] = 0
                total = 0
                for champion in session.query(Champion).all():
                    total += self.idx[s1][champion.championId] * self.idx[s2][champion.championId]
                self.s2s[s1][s2] = total

        # Champion to Champion similarity
        for c1 in session.query(Champion).all():
            self.c2c[c1.championId] = dict()
            for c2 in session.query(Champion).all():
                total = 0
                for summoner in self.s2s.keys():
                    total += self.idx[summoner][c1.championId] * self.idx[summoner][c2.championId]
                self.c2c[c1.championId][c2.championId] = total

    # def summonerSimilarity(self, s1, s2):

    def champSuggestionByChampion(self, summonerId):
        print(self.idx[summonerId])
        temp = sorted(self.idx[summonerId].items(), key=operator.itemgetter(1))
        top3_champs = []
        print("Your Top 3 Champions: ")
        for i in range(0, 3):
            if i > len(self.idx[summonerId]) or self.idx[summonerId][temp[i][0]] == 0:
                break
            top3_champs.append(temp[i][0])
            print("\tName: " + session.query(Champion).filter(Champion.championId == top3_champs[i]).all()[0].name)
            print("\t\tChampion id: " + str(top3_champs[i]))

        top3_recommendations = []
        print("Your Top 3 Recommendations: ")
        for champ in top3_champs:
            temp = sorted(self.c2c[champ].items(), key=operator.itemgetter(1), reverse=True)
            # print(temp)
            for i in range(0, len(temp)):
                if self.idx[summonerId][temp[i][0]] == 0:
                    top3_recommendations.append(temp[0][0])
                    print("\tName: " + session.query(Champion).filter(Champion.championId == temp[i][0]).all()[0].name)
                    print("\t\tChampion id: " + str(temp[i][0]))
                    print("\t\tScore: " + str(temp[i][1]))
                    break



        # for summoner in self.s2s[summonerId].keys():
        #     if self.s2s[summonerId][summoner] > self.s2s[summonerId][mostSimilarSummoner]:
        #         mostSimilarSummoner = summoner


    def champSuggestionBySummoner(self, summonerId):
        mostSimilarSummoner = self.s2s[summonerId].keys()[0]
        for summoner in self.s2s[summonerId].keys():
            if self.s2s[summonerId][summoner] > self.s2s[summonerId][mostSimilarSummoner]:
                mostSimilarSummoner = summoner


def main():
    index = Index()
    while (True):
        name = input("Enter a summoner name: ")
        summonerId = index.riot.getSummonerByName(name)[name]["id"]
        # My ID: 28866449
        index.champSuggestionByChampion(summonerId)
    # index.setGoodness()


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