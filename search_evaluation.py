__author__ = 'Chris'
from index import *
from random import randint
from index import *



def avgPrecision(relevance):
    total_relevent = 0
    total = 0
    for i in range(0, len(relevance)):
        if relevance[i]:
            total_relevent += 1
            total += total_relevent/(i+1)
    if total_relevent == 0:
        return 0
    return total / total_relevent


def rPrecision(relevance):
    total_relevant = 0
    for i in range(0, len(relevance)):
        if relevance[i]:
            total_relevant += 1
    relevant_to_r = 0
    for i in range(0, total_relevant):
        if relevance[i]:
            relevant_to_r += 1

    if total_relevant == 0:
        return 0
    return relevant_to_r / total_relevant


def nPrecision(relevance, N=10):
    total_relevant = 0
    for i in range(0, N):
        if i >= len(relevance):
            break
        if relevance[i]:
            total_relevant += 1
    relevant_to_r = 0
    for i in range(0, total_relevant):
        if relevance[i]:
            relevant_to_r += 1

    if total_relevant == 0:
        return 0
    return relevant_to_r / total_relevant


def areaUnderCurve(relevance):
    total_relevant = 0
    total_irrelevant = 0
    for i in range(0, len(relevance)):
        if relevance[i]:
            total_relevant += 1
    total_irrelevant = len(relevance) - total_relevant
    if total_relevant == 0:
        return 0
    if total_irrelevant == 0:
        return 1

    area = 0
    relevant = 0
    for i in range(0, len(relevance)):
        if relevance[i]:
            relevant += 1
        else:
            area += (relevant/total_relevant) * (1/total_irrelevant)

    return area


def main():

    summonerResponses = {
        "chrispychips5": [0,0,1,1,1,0,1,1,1,0,1,1,1,1,0,1,1,1,0,1,0,0,0,1,0,1,1,0,1,0,0,0,1,1,1,1,1,1,1,0,1,1,1,0,1,1,0,0,1,0,1,1,1,0,1,1,1,1,1,1,1,1,1,0,1,0,1,1,1,1,0,0,1,1,1,1,1,1,1,1,1,0,1,1,1,0,0,1,1,0,0,1,0,0,1,1,0,1,1,1,1,1,0,0,0,0,0,1,1,1,1,0,0,1,0,1,1,1,0,1,1,1,1,1],
        "frozenbastion": [0,0,0,1,1,1,0,1,1,1,0,1,1,0,0,0,0,0,0,0,0,0,1,0,1,0,0,1,0,1,0,1,0,1,1,0,1,0,0,0,0,1,1,1,1,0,1,0,0,0,0,0,0,1,0,1,1,0,1,1,0,1,0,1,1,1,1,1,0,0,0,0,0,0,0,0,0,1,0,0,0,0,1,1,0,0,0,0,1,1,1,1,1,0,0,0,1,0,1,0,1,0,1,0,0,0,0,0,1,1,0,1,0,0,1,1,0,0,0,0,0,1,1,0],
        # "milkbone": [0,0,0,1,1,1,0,0,0,0,1,0,1,0,0,0,0,1,1,0,0,0,0,1,0,0,1,0,0,0,1,1,0,0,0,0,0,0,0,1,0,0,1,0,0,1,0,0,1,0,0,1,0,1,1,0,0,0,0,0,1,0,0,0,1,0,0,0,1,0,0,0,0,0,0,0,1,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0],
        # "pupperoni": [0,0,1,0,1,0,1,0,0,0,0,0,0,0,0,1,0,0,1,0,0,0,0,0,1,0,0,0,1,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,1,1,1,0,1,0,1,0,0,0,0,0,1,1,0,1,1,1,1,0,1,0,0,0,0,1,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,1,0,1,0,0,1,0,1,0,1,0,0,0,1,0,0,1],
        # "spriteknight": [0,0,0,1,1,0,0,0,0,1,1,1,1,0,0,1,0,0,0,1,1,0,0,0,0,0,1,1,1,1,0,1,1,1,1,0,0,1,0,0,1,0,1,1,0,1,0,0,1,0,0,0,1,1,1,0,1,1,0,1,0,1,1,1,1,1,1,1,0,0,1,0,1,0,0,0,1,1,1,0,0,0,0,1,0,0,0,1,1,0,0,1,1,1,0,0,1,1,1,0,1,0,1,0,0,1,0,0,0,1,1,0,1,1,1,1,1,0,1,1,1,1,1,0],
        # "happilymourning": [1,1,0,1,1,0,1,1,0,1,1,1,1,1,1,0,1,0,1,0,1,0,0,1,1,0,1,0,0,0,0,0,1,0,0,0,1,1,0,0,1,1,1,0,0,0,1,0,1,1,1,0,1,0,1,1,1,0,0,0,0,1,0,0,1,1,0,1,0,0,0,0,1,1,0,1,0,1,0,1,0,0,1,1,0,0,0,0,0,1,0,1,1,1,1,1,1,0,1,1,0,0,1,1,0,0,1,1,1,1,1,0,0,0,0,1,0,1,0,0,1,0,1,1],
        # # "nignagpoliwag": [0,0,0,1,0,0,0,0,0,0,0,0,1,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,0,0,0,1,1,1,1,0,0,0,1,0,0,0,0,0,0,1,1,0,0,0,0,0,0,1,1,0,0,1,0,0,1,1,0,0,0,0,0,0,0,0,0,1,1,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,1,0,1,0,0,0,0,1,0,0,0],
        # "siegemaximo": [1,0,0,0,0,0,0,0,0,0,1,1,1,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,1,0,0,0,0,1,1,0,0,0,0,0,0,0,1,0,1,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,1,0,0,0,1,0,0,0,0,0,0,0,0,0,0,1,1,0,0,0,0,0,0,0,0,0,1,0,0,0,0,1,0,0,1,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
        "cannedsheep": [1,1,1,1,1,1,1,1,1,0,1,0,0,1,1,1,1,1,1,1,0,0,1,0,0,1,0,0,1,1,1,1,1,0,1,1,0,1,1,1,1,0,1,0,0,1,1,1,1,1,1,1,0,1,1,1,1,1,1,1,1,0,1,0,1,0,1,1,1,0,0,1,0,1,1,1,0,0,1,1,0,0,1,1,0,1,1,1,1,1,0,0,1,0,1,1,1,1,0,1,0,1,0,0,0,1,1,1,1,1,1,0,0,0,1,1,1,1,0,1,0,1,0,1]
    }
    s2cRelavance = dict()
    for s in summonerResponses.keys():
        s2cRelavance[s] = dict()
        i = 0
        for champ in session.query(Champion).order_by(Champion.name):
            if summonerResponses[s][i] == 1:
                s2cRelavance[s][champ.championId] = True
            else:
                s2cRelavance[s][champ.championId] = False
            i += 1

    numResults = 15
    print("No Normalization, Champion Based, Not Content Based")
    idx = Index(False, False)
    testRecommendations(idx, summonerResponses, s2cRelavance, numResults)
    print("No Normalization, Champion Based, Content Based")
    idx = Index(False, True)
    testRecommendations(idx, summonerResponses, s2cRelavance, numResults)
    print("Normalization, Champion Based, Not Content Based")
    idx = Index(True, False)
    testRecommendations(idx, summonerResponses, s2cRelavance, numResults)
    print("Normalization, Champion Based, Content Based")
    idx = Index(True, True)
    testRecommendations(idx, summonerResponses, s2cRelavance, numResults)

    numResults = 15
    print("No Normalization, Summoner Based")
    idx = Index(False, False)
    testRecommendations(idx, summonerResponses, s2cRelavance, numResults, True)
    print("Normalization, Summoner Based")
    idx = Index(True, False)
    testRecommendations(idx, summonerResponses, s2cRelavance, numResults, True)
    # random_test()

def testRecommendations(idx, summonerResponses, s2cRelavance, numResults=3, bySummoner=False):
    nPrec = 0
    rPrec = 0
    avgPrec = 0
    auc = 0

    for query in summonerResponses.keys():
        summoner = idx.riot.getSummonerByName(query)[query]["id"]
        # print(query[1])
        if bySummoner:
            champsRecommended = idx.champSuggestionBySummoner(summoner, numResults)
        else:
            champsRecommended = idx.champSuggestionByChampion(summoner, numResults)
        if champsRecommended == -1:
            continue
        # print(score_lst[0])
        relevance = []
        for c in champsRecommended:
            if s2cRelavance[query][c]:
                relevance.append(True)
            else:
                relevance.append(False)
        # print(relevance)

        #### add shuffle for random baseline
        # shuffle(relevance)

        nPrec += nPrecision(relevance)
        rPrec += rPrecision(relevance)
        avgPrec += avgPrecision(relevance)
        auc += areaUnderCurve(relevance)
    nPrec /= len(summonerResponses)
    rPrec /= len(summonerResponses)
    avgPrec /= len(summonerResponses)
    auc /= len(summonerResponses)

    print("\tAverage Prec@10 ", nPrec)
    print("\tAverage Prec@R ", rPrec)
    print("\tAverage MAP ", avgPrec)
    print("\tAverage AUC ", auc)

    return


def random_test():
    idx = Index()
    nPrec = 0
    rPrec = 0
    avgPrec = 0
    auc = 0
    random_score = 0

    # N = len(idx.idx)
    N = 3
    relevance = []
    for s in range(0, N):
        if randint(0, 1) == 1:
            relevance.append(True)
        else:
            relevance.append(False)

    nPrec = nPrecision(relevance)
    rPrec = rPrecision(relevance)
    avgPrec = avgPrecision(relevance)
    auc = areaUnderCurve(relevance)
    print("Random: ")
    print("\tAverage Prec@10 ", nPrec)
    print("\tAverage Prec@R ", rPrec)
    print("\tAverage MAP ", avgPrec)
    print("\tAverage AUC ", auc)


def test():
    relevantA = [True, False, True, False, True, False, False, False]
    relevantB = [False, True, True, True, False, False, False, False]

    print("Prec@R for A: " + str(rPrecision(relevantA)))
    print("Prec@R for B: " + str(rPrecision(relevantB)))
    print("MAP for A: " + str(avgPrecision(relevantA)))
    print("MAP for B: " + str(avgPrecision(relevantB)))
    print("AUC for A: " + str(areaUnderCurve(relevantA)))
    print("AUC for B: " + str(areaUnderCurve(relevantB)))

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