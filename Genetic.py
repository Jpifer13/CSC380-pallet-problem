from PalletLoadingHelpers import *
import random

def runGenetic(coords, weightVars, palletDims, seed=0,
               popSize=100, generations=500, numParentPairs=50, mutationProb=0.1):

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

    # 25% chance each to splice just the route, just the pallet, both, or none (copy route1).
    # If one isn't changed, then it uses route1.
    choice = random.randint(0, 3)
    order = route1[0]
    pallet = route1[1]
    if choice == 0 or choice == 2:

        numItems = len(route1[0])

        # get a range from route1
        startIndex = random.randint(0, numItems - 2)
        endIndex = random.randint(startIndex + 1, numItems)
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
        numToTake = random.randint(0, numColumns)
        columnIndeces = list(range(numColumns))
        random.shuffle(columnIndeces)

        for i in range(numToTake):
            pallet[i] = copy.copy(route1[1][columnIndeces[i]])

        # fill in the rest of the columns randomly from the bottom up
        # using the remaining items from route2 in order
        remColumnHeights = [0] * numColumns
        remColumns = list(range(numColumns))
        col = 0
        while col < len(remColumnHeights):
            reachedTheTop = True
            i = 0
            while i < numRows:
                if pallet[remColumns[col]][i] == -1:
                    reachedTheTop = False
                    break
                i += 1
            if reachedTheTop:
                del remColumns[col]
                del remColumnHeights[col]
            else:
                remColumnHeights[col] = i
                col += 1

        r2Col = 0
        r2Row = 0
        usedItems = sum(pallet, []) # flattened pallet
        while r2Row < numRows:
            while route2[1][r2Col][r2Row] in usedItems:
                r2Col += 1
                if r2Col >= numColumns:
                    r2Col = 0
                    r2Row += 1
                if r2Row >= numRows:
                    return order, pallet

            # pick a random column (indexes from the end)
            col = random.randrange(0, len(remColumnHeights))
            pallet[remColumns[col]][remColumnHeights[col]] = \
                    route2[1][r2Col][r2Row]

            # update the indeces
            r2Col += 1
            if r2Col >= numColumns:
                r2Col = 0
                r2Row += 1

            remColumnHeights[col] += 1
            while remColumnHeights[col] < numRows and pallet[remColumns[col]][remColumnHeights[col]] >= 0:
                remColumnHeights[col] += 1
            if remColumnHeights[col] >= numRows:
                del remColumns[col]
                del remColumnHeights[col]

    return order, pallet

def mutatePopulation(population, mutationProb):

    for i in range(len(population)):
        if random.random() < mutationProb:
            oldIndividual = population[i]
            order, pallet, rngState = mutate(oldIndividual[0], oldIndividual[1], random.getstate())
            random.setstate(rngState)
            population[i] = (order, pallet)

def runGeneticXTrials(coords, weightVars, palletDims, numOfTrials=5, seed=0,
                      popSize=100, generations=500, numParentPairs=50, mutationProb=0.1):

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
        isValid = isValidPallet(order, pallet, weightVars)
        print("Pallet (", ("Valid" if isValid else "Invalid"), "):", sep='')
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

    runGeneticXTrials(coords, weightVars, palletDims, numOfTrials=10, seed=0,
                      popSize=100, generations=500, numParentPairs=50, mutationProb=0.1)

test()