import math
import random
from PalletLoadingHelpers import *

def simulateAnnealing(packageCoords, packageVars, palletDims, seed=0,
                      iterations=10000, maxTries=2, initialTemp=100, k=0.0001,
                      printIntermediates=False):

    order = shuffleOrder(len(packageCoords))
    pallet = shufflePallet(len(packageCoords), palletDims)
    random.seed(seed)
    rngState = random.getstate()
    cost = calcCost(order, pallet, packageCoords, packageVars)

    for t in range(iterations):
        temp = initialTemp / (1 + math.log(1 + t))

        for i in range(maxTries):
            newOrder, newPallet, rngState = mutate(order, pallet, rngState)
            newCost = calcCost(newOrder, newPallet, packageCoords, packageVars)

            deltaF = newCost - cost

            if deltaF < 0:
                order = newOrder
                pallet = newPallet
                cost = newCost
            else:
                prob = math.exp(-deltaF / (k * temp))

                if random.random() < prob:
                    order = newOrder
                    pallet = newPallet
                    cost = newCost

        if printIntermediates and t % (iterations / 10) == 0:
            print(format(t, "0>3"), ": ", cost, sep='')
            print(order)
            printPallet(pallet)
            print()

    return order, pallet

def annealXTrials(coords, packageVars, palletDims, numOfTrials=5, seed=0,
                 iterations=5000, maxTries=2, initialTemp=100, k=0.0001):

    trials = []
    bestTrial = 0
    bestCost = math.inf
    random.seed(seed)
    for trial in range(numOfTrials):
        trialSeed = random.random()
        rngState = random.getstate()

        order, pallet = simulateAnnealing(coords, packageVars, palletDims, trialSeed,
                          iterations, maxTries, initialTemp, k)

        cost = calcCost(order, pallet, coords, packageVars)
        if cost < bestCost:
            bestTrial = trial
            bestCost = cost

        trials.append( (order, pallet, cost) )

        print("TRIAL", trial)
        print("Cost: ", cost, "\t(Best: ", bestCost, ")", sep="")
        print("Order:", order)
        print("Pallet:")
        printPallet(pallet)
        print()
        print()

        random.setstate(rngState)

    return trials, bestTrial

def annealXTrialsF(file, coords, weightVars, palletDims, numOfTrials, seed,
                 iterations, maxTries, initialTemp, k):
    annResult = annealXTrials(coords, weightVars, palletDims, numOfTrials, seed, iterations, maxTries, initialTemp, k)
    i = annResult[1]
    if isValidPallet(annResult[0][i][0], annResult[0][i][1], weightVars):
        file.write(str(annResult[0][i][2]) + "," + str(annResult[0][i][0]) + "," + str(annResult[0][i][1]) + "\n")
    else:
        file.write("Invalid (" + str(annResult[0][i][2]) + "," + str(annResult[0][i][0]) + "," + str(annResult[0][i][1]) + ")\n")

def test():
    coords, weightVars = initPackages(20, 0, 100, 0, 100, 1, 2, 0, 8, seed=1)
    palletDims = [5, 5]

    print("Coordinates:", coords)
    print("Weight variables:", weightVars)

    print()

    annealXTrials(coords, weightVars, palletDims, numOfTrials=5, seed=0,
                  iterations=50000, maxTries=2, initialTemp=100, k=0.0001)

    # pallet = ["-"] * palletDims[0] * palletDims[1]
    # for i in range(numItems):
    #     pallet[coords[i][0], coords[i][1]] = str(i)
    # for j in range(len(pallet[0]), -1, -1):
    #     for i in range(len(pallet)):
    #         print(pallet[i, j], end="")
    #     print()

# test()