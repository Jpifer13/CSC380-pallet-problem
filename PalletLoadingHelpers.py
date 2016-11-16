import random
import copy

def initPackages(count, minX, maxX, minY, maxY,
                minWeight, maxWeight, minCapacity, maxCapacity, seed=0):
    coords = initVars(count, [minX, minY], [maxX, maxY], seed)
    weightVars = initVars(count, [minWeight, minCapacity], [maxWeight, maxCapacity], seed)
    return coords, weightVars

def initVars(count, lowerBounds, upperBounds, seed=0):
    random.seed(seed)
    coords = []
    for i in range(count):
        x = random.randint(lowerBounds[0], upperBounds[0])
        y = random.randint(lowerBounds[1], upperBounds[1])
        coords.append([x, y])
    return coords

def mutate(order, pallet, rngState):

    random.setstate(rngState)

    newOrder = copy.deepcopy(order)
    newPallet = copy.deepcopy(pallet)

    # mutate the newOrder (0), the newPallet (1), or both
    choice = random.randint(0, 2)
    if choice in (0, 2):
        # pick two places in the pick-up newOrder and swap them
        n = random.randint(0, len(newOrder) - 1)
        m = random.randint(0, len(newOrder) - 1)
        newOrder[n], newOrder[m] = newOrder[m], newOrder[n]
    if choice in (1, 2):
        # pick two spots in the newPallet and swap them
        numColumns = len(newPallet)
        height = len(newPallet[0])

        # first newOrdered pair
        a = random.randint(0, numColumns - 1)
        b = random.randint(0, height - 1)

        # second newOrdered pair
        x = random.randint(0, numColumns - 1)
        y = random.randint(0, height - 1)

        # swap the items at the two coordinates
        newPallet[a][b], newPallet[x][y] = newPallet[x][y], newPallet[a][b]

    return newOrder, newPallet, random.getstate()