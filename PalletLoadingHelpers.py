import random
import copy
import math

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

def shuffleOrder(numItems):
    # initialize the order by starting in increasing order
    # and then swapping each spot with another once
    order = list(range(numItems))
    for i in range(numItems):
        j = random.randint(0, len(order) - 1)
        order[i], order[j] = order[j], order[i]
    return order

def shufflePallet(numItems, palletDims):
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

    return pallet

def calcDistance(coords1, coords2):
    return math.sqrt((coords1[0] - coords2[0])**2 + (coords1[1] - coords2[1])**2)

def calcRouteDistance(order, coords):
    distance = 0
    for i in coords:
        distance += distance(coords[order[i]], coords[order[i-1]])
    return distance

def calcPalletPenalty(order, pallet, packageVars):
    penalty = 1
    for column in range(len(pallet)):
        for slot in range(len(pallet[column])):
            item = pallet[column][slot]
            if item == -1:
                continue

            # if the item beneath this one is empty,
            # add 1 to the penalty plus the weight of this item
            # else if it is placed after this item, add 1
            if slot > 0:
                itemBeneath = pallet[column][slot - 1]
                if itemBeneath == -1:
                    penalty += 1 + packageVars[item][0]
                elif order.index(itemBeneath) > order.index(item):
                    penalty += 1

            # if the total weight above this item is greater
            # than its capacity, increment the penalty
            totalWeight = 0
            for itemAbove in pallet[column][slot + 1:]:
                if itemAbove == -1:
                    break
                totalWeight += packageVars[itemAbove][0]
            if totalWeight > packageVars[item][1]:
                penalty += 1
    return penalty

def calcCost(order, pallet, coords, packageVars):

    # get the total distance of the route (the base cost)
    # and rack up a multiplier for each error in the pallet

    baseCost = calcRouteDistance(order, coords)

    # multiply it for each error in the pallet
    multiplier = calcPalletPenalty(order, pallet, packageVars)
    cost = baseCost * multiplier

    return cost

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