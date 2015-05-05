__author__ = 'Chris'
from index import *
from WebDB import *
from ranked_search import *
from random import randint
from random import shuffle


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
    db = WebDB("data/cache.db")
    print("Enter document weighting scheme: ")
    doc_weight = input()
    print("Enter query weighting scheme: ")
    query_weight = input()

    print("Loading Index . . .")
    idx = Index(db, doc_weight)
    print("Index Loaded")
    rs = RankedSearch(db, idx, query_weight)

    items = db.execute("select * from Item").fetchall()

    nPrec = 0
    rPrec = 0
    avgPrec = 0
    auc = 0

    for query in items:
        # print(query[1])
        score_lst = rs.search(query[1])
        # print(score_lst[0])
        relevance = []
        for s in score_lst:
            # print("\t" + db.lookupItem_byID(db.lookupItem_byURL(s[0]))[0])
            if db.lookupItem_byID(db.lookupItem_byURL(s[0]))[0] == query[1]:
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
    nPrec /= len(items)
    rPrec /= len(items)
    avgPrec /= len(items)
    auc /= len(items)

    print("Average Prec@10 ", nPrec)
    print("Average Prec@R ", rPrec)
    print("Average MAP ", avgPrec)
    print("Average AUC ", auc)

    return


def random_test():
    db = WebDB("data/cache.db")
    nPrec = 0
    rPrec = 0
    avgPrec = 0
    auc = 0
    random_score = 0

    N = len(db.execute("select * from CachedURL").fetchall())
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

    print("Average Prec@10 ", nPrec)
    print("Average Prec@R ", rPrec)
    print("Average MAP ", avgPrec)
    print("Average AUC ", auc)


def test():
    relevantA = [True, False, True, False, True, False, False, False]
    relevantB = [False, True, True, True, False, False, False, False]

    print("Prec@R for A: " + str(rPrecision(relevantA)))
    print("Prec@R for B: " + str(rPrecision(relevantB)))
    print("MAP for A: " + str(avgPrecision(relevantA)))
    print("MAP for B: " + str(avgPrecision(relevantB)))
    print("AUC for A: " + str(areaUnderCurve(relevantA)))
    print("AUC for B: " + str(areaUnderCurve(relevantB)))

main()
# random_test()