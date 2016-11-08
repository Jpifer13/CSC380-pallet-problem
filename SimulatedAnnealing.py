import copy
import math
import random

def simulateAnnealing(packageCoords, packageVars, palletDims, seed=0,
                      iterations=2000, maxTries=10, initialTemp=100, k=0.001):
    order, pallet = init(len(packageCoords), palletDims)
    random.seed(seed)
    cost = calcCost(order, pallet, packageCoords, packageVars)

    for t in range(iterations):
        temp = initialTemp / (1 + math.log(1 + t))

        for i in range(maxTries):
            newOrder, newPallet = mutate(order, pallet)
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

        if t % (iterations / 10) == 0:
            print(format(t, "0>3"), ": ", cost, sep='')
            print(order)
            printPallet(pallet)
            print()

    return order, pallet

def mutate(order, pallet):
    newOrder = copy.deepcopy(order)
    newPallet = copy.deepcopy(pallet)

    # mutate either the newOrder or the newPallet
    choice = random.randint(0, 1)
    if choice == 0:
        # pick two places in the pick-up newOrder and swap them
        n = random.randint(0, len(newOrder) - 1)
        m = random.randint(0, len(newOrder) - 1)
        newOrder[n], newOrder[m] = newOrder[m], newOrder[n]
    else:
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

    return newOrder, newPallet

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

            # if the item beneath this one is placed after or empty,
            # add 2 to the multiplier
            if slot > 0:
                itemBeneath = pallet[column][slot-1]
                if itemBeneath == -1 \
                        or order.index(itemBeneath) > order.index(item):
                    multiplier += 2

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

def initVars(count, lowerBounds, upperBounds, seed=0):
    random.seed(seed)

    coords = []
    for i in range(count):
        x = random.randint(lowerBounds[0], upperBounds[0])
        y = random.randint(lowerBounds[1], upperBounds[1])
        coords.append([x, y])
    return coords

def printPallet(pallet):
    for j in range(len(pallet[0]) - 1, -1, -1):
        for i in range(len(pallet)):
            if pallet[i][j] == -1:
                print(" -- ", end="")
            else:
                print(format(pallet[i][j], ">3") + " ", end="")
        print()

def test():
    numItems = 20
    coords = initVars(numItems, [0, 0], [100, 100])
    # packageVars = [[1, 5]] * 10
    packageVars = initVars(numItems, [1, 0], [2, 8])
    palletDims = [5, 5]

    order, pallet = simulateAnnealing(coords, packageVars, palletDims, seed=3)

    print(calcCost(order, pallet, coords, packageVars))
    print(order)
    print()
    printPallet(pallet)
    print()
    print(coords)
    print(packageVars)

    

    # pallet = ["-"] * palletDims[0] * palletDims[1]
    # for i in range(numItems):
    #     pallet[coords[i][0], coords[i][1]] = str(i)
    # for j in range(len(pallet[0]), -1, -1):
    #     for i in range(len(pallet)):
    #         print(pallet[i, j], end="")
    #     print()

test()