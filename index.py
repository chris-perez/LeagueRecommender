__author__ = 'Chris'
from riot import *
from sqlalchemy_declarative import *
import math
import operator
import pickle
import os


class Index():
    def __init__(self, normalize=False, champByStats=False):
        self.riot = Riot()
        self.idx = dict()
        self.s2s = dict()
        self.c2c = dict()
        i = 0
        if normalize and os.path.exists("indexN.p"):
            self.idx = pickle.load(open("indexN.p", "rb"))
        elif (not normalize) and os.path.exists("index.p"):
            self.idx = pickle.load(open("index.p", "rb"))
        else:
            print("Loading Index . . .")
            for summoner in session.query(Summoner).all():
                totalScore = 0
                # number of test champions
                if i > 600:
                    break
                i += 1
                self.idx[summoner.summonerId] = dict()
                for champion in session.query(Champion).all():
                    if len(session.query(SummonerToChampion).filter(SummonerToChampion.summonerId == summoner.id, SummonerToChampion.championId == champion.championId).all()) > 0:
                        s2c = session.query(SummonerToChampion).filter(SummonerToChampion.summonerId == summoner.id, SummonerToChampion.championId == champion.championId).all()[0]
                        print("\tSummoner %d: K= %d D= %d A= %d  Win: %d" % (s2c.summonerId, s2c.kills, s2c.deaths, s2c.assists, s2c.wins))
                        if s2c.deaths > 0:
                            #normalize = goodness/sum of goodness
                            goodness = (((s2c.kills + .75 * s2c.assists) / s2c.deaths) + .1*s2c.wins)/s2c.games
                            if goodness > 0:
                                if goodness > 1:
                                    s2c.goodness = math.log10(goodness)
                                else:
                                    s2c.goodness = goodness

                            else:
                                s2c.goodness = 0
                        else:
                            goodness = (((s2c.kills + .75 * s2c.assists) / 1) + .1*s2c.wins)/s2c.games
                            if goodness > 0:
                                if goodness > 1:
                                    s2c.goodness = math.log10(goodness)
                                else:
                                    s2c.goodness = goodness
                            else:
                                s2c.goodness = 0

                        session.commit()
                        self.idx[summoner.summonerId][champion.championId] = s2c.goodness
                    else:
                        self.idx[summoner.summonerId][champion.championId] = 0
                    totalScore += self.idx[summoner.summonerId][champion.championId]
                if normalize:
                    for score in self.idx[summoner.summonerId]:
                        score /= totalScore

            if normalize:
                pickle.dump(self.idx, open("indexN.p", "wb"))
            else:
                pickle.dump(self.idx, open("index.p", "wb"))

        # Summoner to Summoner similarity
        if normalize and os.path.exists("s2sN.p"):
            self.s2s = pickle.load(open("s2sN.p", "rb"))
        elif (not normalize) and os.path.exists("s2s.p"):
            self.s2s = pickle.load(open("s2s.p", "rb"))
        else:
            print("Loading Summoner Similarity Table . . .")
            for s1 in self.idx.keys():
                self.s2s[s1] = dict()
                print("\tSummoner ID: " + str(s1))
                for s2 in self.idx.keys():
                    # s1[s2] = 0
                    total = 0
                    for champion in session.query(Champion).all():
                        total += self.idx[s1][champion.championId] * self.idx[s2][champion.championId]
                    self.s2s[s1][s2] = total
            if normalize:
                pickle.dump(self.s2s, open("s2sN.p", "wb"))
            else:
                pickle.dump(self.s2s, open("s2s.p", "wb"))

        # Champion to Champion similarity
        if normalize and os.path.exists("c2cN.p"):
            self.c2c = pickle.load(open("c2cN.p", "rb"))
        elif (not normalize) and os.path.exists("c2c.p"):
            self.c2c = pickle.load(open("c2c.p", "rb"))
        else:
            print("Loading Champion Similarity Table . . .")
            for c1 in session.query(Champion).all():
                print("\tChampion ID: " + str(c1.championId))
                self.c2c[c1.championId] = dict()
                for c2 in session.query(Champion).all():
                    total = 0
                    for summoner in self.idx.keys():
                        total += self.idx[summoner][c1.championId] * self.idx[summoner][c2.championId]
                    self.c2c[c1.championId][c2.championId] = total
            if normalize:
                pickle.dump(self.c2c, open("c2cN.p", "wb"))
            else:
                pickle.dump(self.c2c, open("c2c.p", "wb"))
        if champByStats:
            print("Loading Champion Similarity Table . . .")
            for c1 in session.query(Champion).all():
                for c2 in session.query(Champion).all():
                    if normalize:
                        total1 = c1.defense + c1.magic + c1.attack
                        total2 = c2.defense + c2.magic + c2.attack
                        total = (c1.defense/total1)*(c2.defense/total2) + (c1.magic/total1)*(c2.magic/total2) + (c1.attack/total1)*(c2.attack/total2)
                    else:
                        total = c1.defense*c2.defense + c1.magic*c2.magic + c1.attack*c2.attack
                    self.c2c[c1.championId][c2.championId] += total

    def champSuggestionByChampion(self, summonerId):
        if summonerId not in self.idx:
            print("Can't find summoner in table.")
            return -1
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
                    top3_recommendations.append(temp[i][0])
                    print("\tName: " + session.query(Champion).filter(Champion.championId == temp[i][0]).all()[0].name)
                    print("\t\tChampion id: " + str(temp[i][0]))
                    print("\t\tScore: " + str(temp[i][1]))
                    break
        return top3_recommendations



    def champSuggestionBySummoner(self, summonerId):
        if summonerId not in self.idx:
            print("Can't find summoner in table.")
            return
        print(self.idx[summonerId])
        temp = sorted(self.s2s[summonerId].items(), key=operator.itemgetter(1))
        top3_summoners = []
        print("Your Top 3 Summoners: ")
        for i in range(0, 3):
            if i > len(self.s2s[summonerId]) or self.s2s[summonerId][temp[i][0]] == 0:
                break
            top3_summoners.append(temp[i][0])
            print("\tSummoner id: " + str(top3_summoners[i]))

        top3_recommendations = []
        print("Your Top 3 Recommendations: ")
        for summoner in top3_summoners:
            temp = sorted(self.idx[summoner].items(), key=operator.itemgetter(1), reverse=True)
            # print(temp)
            for i in range(0, len(temp)):
                if self.idx[summonerId][temp[i][0]] == 0:
                    top3_recommendations.append(temp[i][0])
                    print("\tName: " + session.query(Champion).filter(Champion.championId == temp[i][0]).all()[0].name)
                    print("\t\tChampion id: " + str(temp[i][0]))
                    print("\t\tScore: " + str(temp[i][1]))
                    break
        return top3_recommendations


def main():
    index = Index(False, False)
    while (True):
        name = input("Enter a summoner name: ")
        summoner = index.riot.getSummonerByName(name)
        if summoner == -1:
            print("Summoner does not exist on NA Server")
            continue
        summonerId = summoner[name]["id"]

        # My ID: 28866449
        print("Suggestion by Champion to Champion Similarity")
        index.champSuggestionByChampion(summonerId)
        print("Suggestion by Summoner to Summoner Similarity")
        index.champSuggestionBySummoner(summonerId)

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

# main()