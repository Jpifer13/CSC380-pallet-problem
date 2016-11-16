import math
import random
from PalletLoadingHelpers import initPackages
from PalletLoadingHelpers import mutate

def simulateAnnealing(packageCoords, packageVars, palletDims, seed=0,
                      iterations=5000, maxTries=10, initialTemp=100, k=0.001,
                      printIntermediates=False):

    order, pallet = init(len(packageCoords), palletDims)
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

def init(numItems, palletDims):
    # initialize the order by starting in increasing order
    # and then swapping each spot with another once
    order = list(range(numItems))
    for i in range(numItems):
        j = random.randint(0, len(order) - 1)
        order[i], order[j] = order[j], order[i]

    # initalize the pallet by starting with the packages placed
    # systematically and then swapping each spot with another once
    numColumns = palletDims[0]
    height = palletDims[1]
    pallet = []
    for i in range(numColumns):
        pallet.append([-1] * height)

    i, j = 0, 0
    for item in list(range(numItems)):
        pallet[i][j] = item
        i += 1
        if i >= numColumns:
            i = 0
            j += 1

    for i in range(numColumns):
        for j in range(height):
            x = random.randint(0, numColumns - 1)
            y = random.randint(0, height - 1)
            pallet[i][j], pallet[x][y] = pallet[x][y], pallet[i][j]
    
    return order, pallet

def calcCost(order, pallet, coords, packageVars):

    # get the total distance of the route (the base cost)
    # and rack up a multiplier for each error in the pallet
    baseCost = 0
    for i in order:
        baseCost += distance(coords[order[i]], coords[order[i - 1]])

    # multiply it for each error in the pallet
    multiplier = 1
    for column in range(len(pallet)):
        for slot in range(len(pallet[column])):
            item = pallet[column][slot]
            if item == -1:
                continue

            # if the item beneath this one is empty,
            # add 1 to the multiplier plus the weight of this item
            # else if it is placed after this item, add 1
            if slot > 0:
                itemBeneath = pallet[column][slot-1]
                if itemBeneath == -1:
                    multiplier += 1 + packageVars[item][0]
                elif order.index(itemBeneath) > order.index(item):
                    multiplier += 1

            # if the total weight above this item is greater
            # than its capacity, increment the multiplier
            totalWeight = 0
            for itemAbove in pallet[column][slot+1:]:
                if itemAbove == -1:
                    break
                totalWeight += packageVars[itemAbove][0]
            if totalWeight > packageVars[item][1]:
                multiplier += 1
    cost = baseCost * multiplier

    return cost

def distance(coords1, coords2):
    return math.sqrt((coords1[0] - coords2[0])**2 + (coords1[1] - coords2[1])**2)

def palletToCoords(pallet, itemCount):
    coords = [] * itemCount
    for column in range(len(pallet)):
        for slot in range(len(pallet[column])):
            item = pallet[column][slot]
            if item >= 0:
                coords[item] = [column, slot]
    return coords

def printPallet(pallet):
    for j in range(len(pallet[0]) - 1, -1, -1):
        for i in range(len(pallet)):
            if pallet[i][j] == -1:
                print(" -- ", end="")
            else:
                print(format(pallet[i][j], ">3") + " ", end="")
        print()

def annealXTrials(numOfTrials, coords, packageVars, palletDims, seed=0,
                 iterations=5000, maxTries=10, initialTemp=100, k=0.001):

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

        trials.append((order, pallet, cost))

        print("TRIAL", trial)
        print("Cost: ", cost, "\t(Best: ", bestCost, ")", sep="")
        print("Order:", order)
        print("Pallet:")
        printPallet(pallet)
        print()
        print()

        random.setstate(rngState)

    return trials, bestTrial

def test():
    numItems = 20
    coords, weightVars = initPackages(numItems, 0, 100, 0, 100, 1, 2, 0, 8, seed=0)
    palletDims = [5, 5]

    #routes = [(distance, [index0, index1, index2])] * 50
    #routes.sort(key = lambda route : route[0])

    print("Coordinates:", coords)
    print("Weight variables:", weightVars)

    print()

    annealXTrials(10, coords, weightVars, palletDims, seed=0,
                  iterations=50000, maxTries=2, initialTemp=100, k=0.0001)

    # pallet = ["-"] * palletDims[0] * palletDims[1]
    # for i in range(numItems):
    #     pallet[coords[i][0], coords[i][1]] = str(i)
    # for j in range(len(pallet[0]), -1, -1):
    #     for i in range(len(pallet)):
    #         print(pallet[i, j], end="")
    #     print()

test()