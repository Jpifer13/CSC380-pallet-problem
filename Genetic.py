from PalletLoadingHelpers import *
import random

def runGenetic(coords, weightVars, palletDims, seed=0,
               popSize=100, generations=10000, numParentPairs=50, mutationProb=0.1):

    random.seed(seed)
    population = initPopulation(len(coords), palletDims, popSize)
    elite = min(population, key=lambda i: \
            calcCost(i[0], i[1], coords, weightVars))

    for generation in range(generations):

        parents = selectParentPairs(population, numParentPairs, coords, weightVars)
        children = crossover(parents, popSize // numParentPairs)
        mutatePopulation(children, mutationProb)
        # children.append(elite)
        population = children
        elite = min(population, key=lambda i: \
                calcCost(i[0], i[1], coords, weightVars))

    return elite[0], elite[1]

def initPopulation(numItems, palletDims, popSize):

    population = []
    for _ in range(popSize):
        order = shuffleOrder(numItems)
        pallet = shufflePallet(numItems, palletDims)
        population.append( (order, pallet) )
    return population

def selectParentPairs(population, numParentPairs, coords, weightVars):

    accumScores = []
    totalScore = 0
    for i in population:
        accumScores.append(totalScore)
        cost = calcCost(i[0], i[1], coords, weightVars)
        totalScore += 1 / (cost * cost)
    accumScores.append(totalScore)

    parentPairs = []
    for _ in range(numParentPairs):
        i1 = selectParent(accumScores)
        i2 = selectParent(accumScores)

        parentPairs.append( (population[i1], population[i2]) )

    return parentPairs

def selectParent(accumScores):

    score = random.random() * accumScores[-1]

    # find the bin that the score falls in
    index = len(accumScores) // 2
    minimum = 0
    maximum = len(accumScores) - 1
    while accumScores[index] > score or accumScores[index + 1] <= score:
        if accumScores[index] < score:
            minimum = index + 1
        else:
            maximum = index - 1
        index = (minimum + maximum) // 2

    return index

def crossover(parentPairs, childrenPerPair):

    children = []
    for pair in parentPairs:
        for _ in range(childrenPerPair):
            children.append(spliceAndFill(pair[0], pair[1]))
    return children

def spliceAndFill(route1, route2):

    # 50% chance to swap the routes
    if random.randint(0, 1) == 0:
        route1, route2 = route2, route1

    # 33% chance each to splice just the route, just the pallet, or both.
    # If one isn't changed, then it uses route1.
    choice = random.randint(0, 2)
    order = route1[0]
    pallet = route1[1]
    if choice == 0 or choice == 2:

        numItems = len(route1[0])

        # get a range from route1
        startIndex = random.randint(1, numItems - 2)
        endIndex = random.randint(startIndex, numItems)
        order = route1[0][startIndex:endIndex]

        # fill in the remaining elements from route2, in order
        i = 0
        for _ in range(0, startIndex):
            while route2[0][i] in order:
                i += 1
            order.insert(i, route2[0][i])
            i += 1
        for _ in range(endIndex, numItems):
            while route2[0][i] in order:
                i += 1
            order.insert(i, route2[0][i])
            i += 1

    if choice == 1 or choice == 2:

        numColumns = len(route1[1])
        numRows = len(route1[1][0])
        pallet = []
        for _ in range(numColumns):
            pallet.append([-1] * numRows)

        # pick columns to take straight from route1
        numToTake = random.randint(1, numColumns - 1)
        columnIndeces = list(range(numColumns))
        random.shuffle(columnIndeces)

        for i in range(numToTake):
            pallet[i] = route1[1][columnIndeces[i]]

        # fill in the rest of the columns randomly from the bottom up
        # using the remaining items from route2 in order
        remColumnHeights = [0] * numColumns
        for i in range(len(remColumnHeights)):
            
        r2CIndex = 0
        r2RIndex = 0
        usedItems = sum(pallet, [])
        while r2RIndex < numRows:
            while route2[1][r2CIndex][r2RIndex] in usedItems:
                r2CIndex += 1
                if r2CIndex >= numColumns:
                    r2CIndex = 0
                    r2RIndex += 1
                if r2RIndex >= numRows:
                    return order, pallet

            # pick a random column (indexes from the end)
            columnIndex = random.randrange(0, len(remColumnHeights))
            pallet[-1 - columnIndex][remColumnHeights[columnIndex]] = \
                    route2[1][r2CIndex][r2RIndex]

            # update the indeces
            r2CIndex += 1
            if r2CIndex >= numColumns:
                r2CIndex = 0
                r2RIndex += 1

            remColumnHeights[columnIndex] += 1
            if remColumnHeights[columnIndex] >= numRows:
                newIndex = len(remColumnHeights)
                pallet[-1 - columnIndex], pallet[-newIndex] = \
                        pallet[-newIndex], pallet[-1 - columnIndex]
                del remColumnHeights[columnIndex]

    return order, pallet

def mutatePopulation(population, mutationProb):

    for i in range(len(population)):
        if random.random() < mutationProb:
            oldIndividual = population[i]
            order, pallet, rngState = mutate(oldIndividual[0], oldIndividual[1], random.getstate())
            random.setstate(rngState)
            population[i] = (order, pallet)

def runGeneticXTrials(numOfTrials, coords, weightVars, palletDims, seed=0,
                      popSize=100, generations=10000, numParentPairs=50, mutationProb=0.1):

    trials = []
    bestTrial = 0
    bestCost = math.inf
    random.seed(seed)
    for trial in range(numOfTrials):
        trialSeed = random.random()
        rngState = random.getstate()

        order, pallet = runGenetic(coords, weightVars, palletDims, trialSeed,
                                   popSize, generations, numParentPairs, mutationProb)

        cost = calcCost(order, pallet, coords, weightVars)
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


def test():
    coords, weightVars = initPackages(20, 0, 100, 0, 100, 1, 2, 0, 8, seed=1)
    palletDims = [5, 5]

    print("Coordinates:", coords)
    print("Weight variables:", weightVars)

    print()

    runGeneticXTrials(10, coords, weightVars, palletDims, seed=0,
                      popSize=100, generations=1000, numParentPairs=50, mutationProb=0.1)

test()