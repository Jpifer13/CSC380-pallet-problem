import copy
import math
from random import randint

paths = []

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
    return distance


def branchAndBound():
    distances = []
    global paths
    dindex = 0
    for i in range(0, 999):
        distances.append(randomTSP(x1, y1))
    tempd = copy.deepcopy(distances)
    while (len(tempd) > 1):
        if (tempd[0] < tempd[-1]):
            tempd = tempd[0, -1]
        elif (tempd[0] >= tempd[-1]):
            tempd = tempd[1:]
    for a in range(0, len(distances)):
        if(tempd[0] == distances[0]):
            dindex = 0
            break
        elif(tempd[0] == distances[a]):
            dindex = a
