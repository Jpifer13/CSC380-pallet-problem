import copy
import math
from random import randint
from PalletLoadingHelpers import *

paths = []
distances = []

x1 = [1.0, 5.0, 2.0, 7.0, 5.1, 2.1, 5.2, 3.0, 5.3, 9.0]
y1 = [9, 4, 2, 6, 1, 8, 4, 2, 3, 6]


def distanceFormula(x1, x2, y1, y2):
    d = math.sqrt(((x2 - x1) * (x2 - x1)) + ((y2 - y1) * (y2 - y1)))
    return d


def exhaustiveTSP(x1, y1):
    tempx = copy.deepcopy(x1)
    tempy = copy.deepcopy(y1)
    fastestRoute = []

    distances = []
    temp = []
    initial = 0
    next = 1
    # while len(listx1) > 1:
    for i in range(len(x1) - 1):
        d = distanceFormula(x1[initial], x1[next], y1[initial], y1[next])
        # d = distanceFormula(x1[indexes[current]], x1[indexes[next]], y1
        distances.append(d)
        next = next + 1
    temp = copy.deepcopy(distances)
    next = 1
    print(distances)
    while len(distances) > 1:
        if distances[0] <= distances[- 1]:
            distances = distances[:-1]
        elif distances[0] > distances[-1]:
            distances = distances[1:]
    print(distances)
    found = 0
    search = 0
    position = 0
    while found != 1:
        if temp[search] == distances[0]:
            position = search
            found = 1
        elif temp[search] != distances[0]:
            search = search + 1
            found = 0
    print(position)
    fastestRoute.append([initial, position])
    # x1 = x1[1:]
    # y1 = y1[1:]
    # switchy = y1[0]
    # switchx = x1[0]
    # x1[0] = x1[position - 1]
    # x1[position - 1] = switchx
    # y1[0] = y1[position - 1]
    # y1[position - 1] = switchy
    # initial = 0
    # distances = []
    # temp = []
    print(fastestRoute)


# exhaustiveTSP(x1, y1)


def returnIndexPath(x1, path):
    temp = []
    for i in range(0, (len(x1) - 1)):
        if (path[i] != x1[0]):
            for q in range(0, (len(x1) - 1)):
                if (path[i] == x1[q]):
                    temp.append(q)
                    break
        else:
            temp.append(0)
    return temp


def randomTSP(x1, y1):
    tempx = copy.deepcopy(x1)
    tempy = copy.deepcopy(y1)
    path = []
    distance = 0
    start = randint(0, (len(tempx) - 1))
    print(start)
    path.append(tempx[start])
    while ((len(tempx) - 1) >= 1):
        n = randint(0, (len(tempx) - 1))
        if (start == n):
            while (start == n):
                n = randint(0, (len(tempx) - 1))
        print(n)
        d = distanceFormula(tempx[start], tempx[n], tempy[start], tempy[n])
        distance = distance + d
        path.append(tempx[n])
        tempx.remove(tempx[start])
        tempy.remove(tempy[start])
        print(tempx)

        start = n - 1
    print(tempx)
    path.append(tempx[0])
    print(path)
    print(returnIndexPath(x1, path))
    paths.append(path)
    distances.append(distance)
    return distance, path

def sort(distances, paths):
    routes = []
    for i in range(0, len(distances)):
        routes.append( (distances[i], paths[i]) )
    routes.sort(key = lambda route : route[0])
    #print(routes)
    return routes

def totalDistance(pathIndex, packages):
    total = 0
    for i in range(len(pathIndex)):
        total = total + distanceFormula(packages[pathIndex[i]][0], packages[pathIndex[i-1]][0], packages[pathIndex[i]][1], packages[pathIndex[i-1]][1])
    return total

def branchAndBound(x1, y1):
    distances = []
    paths = []
    route = []
    packages = []
    totalD = 0

    #This loop finds 50 of the best routes/bounds using a random function
    remainingIndex = [0, 0]
    for t in range(len(x1)):
        packages.append( (x1[t], y1[t], t) )
    remaining = list(range(len(packages)))
    print(remaining)
    #print(packages)
    for q in range(0,249):
        if(len(distances)<= 50):
            for i in range(0, 50):
                path = shuffleOrder(len(packages))
                distance = totalDistance(path, packages)
                distances.append(distance)
                paths.append(path)
            bestRoutes = sort(distances, paths)
            distances = []
            paths = []
        else:
            if bestRoutes[-1][0] > distances[0]:
                distances = distances[:-1]
                max = len(bestRoutes) -1
                mid = max//2
                min = 0
                while max > min:
                    if distances[0] < bestRoutes[mid][0]:
                        max = mid - 1
                    else:
                        min = mid + 1
                    mid = (min + max)//2
                bestRoutes.insert(mid, (distances[0], paths[0]) )
    print(bestRoutes)

    route.append((0,0)) #need to insert first tuple of packages (index, totalDistance)
    current = [remaining[0]]  # current index
    remaining.remove(0)

    while len(remaining) < len(packages):
        if len(remaining) == 0: #this is called when we found a route that is shorter then the longest bound and appends to best route list

            if bestRoutes[-1][0] > route[-1][1]:
                bestRoutes = bestRoutes[:-1]
                max = len(bestRoutes) -1
                mid = max//2
                min = 0
                while max > min:
                    if route[-1][1] < bestRoutes[mid][0]:
                        max = mid - 1
                    else:
                        min = mid + 1
                    mid = (min + max)//2
                if mid < 0:
                    mid = 0
                r = [x[0] for x in route]
                bestRoutes.insert(mid, (route[-1][1], r) )

            route.pop()
            remainingIndex.pop()
            remaining.insert(remainingIndex[-1], current[-1])
            remainingIndex[-1] += 1
            current.pop()
        elif remainingIndex[-1] >= len(remaining):#when last node of tree is up
            route.pop()
            remainingIndex.pop()
            remaining.insert(remainingIndex[-1], current[-1])
            remainingIndex[-1] += 1
            current.pop()
        elif route[-1][1] > bestRoutes[-1][0]:
            #when total distance of current becomes bigger then longest bound
            #pop last position in route as well as last remainingIndex
            route.pop()
            remainingIndex.pop()
            remaining.insert(remainingIndex[-1], current[-1])
            remainingIndex[-1] += 1
            current.pop()
        else:#current changes to next index, add current to route and the distnce to route, then remove current index from remaining, and add a 0 to remaingingIndex
            current.append(remaining[remainingIndex[-1]])
            route.append((current[-1], route[-1][1] + distanceFormula(x1[route[-1][0]], packages[current[-1]][0], y1[route[-1][0]], packages[current[-1]][1]))) #adding next location
            remaining.remove(current[-1])
            remainingIndex.append(0)

    return bestRoutes

def findBestBuild(bestRoutes, weightVars):
    pallet = []
    row = [0, 0, 0, 0, 0]
    for i in range(5):
        pallet.append(row)
    #print(pallet)
    index = []
    for x in range(len(weightVars)):
        index.append( (x, weightVars[x]) )
    print(index)
    list = weightVars
    for index in range(0, len(list)):
        iSmall = index
        for i in range(index, len(list)):
            if list[iSmall][1][1] > list[i][1][1]:
                iSmall = i
        list[index], list[iSmall] = list[iSmall], list[index]



#randomTSP(x1, y1)

def main():
    coords, weightVars = initPackages(10, 0, 100, 0, 100, 1, 2, 0, 8)
    x, y = tupletoList(coords)
    bestRoutes = branchAndBound(x, y)
    print(weightVars)
    findBestBuild(bestRoutes, weightVars)


main()




