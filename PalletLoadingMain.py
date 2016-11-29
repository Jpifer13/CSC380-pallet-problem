import datetime
import timeit

from PalletLoadingHelpers import *
import BranchandBound
import Genetic
import SimulatedAnnealing

def defaultComparison(numOfRuns, numOfPackages, palletDims, minX, maxX, minY, maxY,
                      minWeight, maxWeight, minCapacity, maxCapacity, file):

    # write the method name and current date and time
    file.write("defaultComparison, " + datetime.now().strftime("%x %X"))
    # write the method arguments
    file.write(("numOfRuns={0}, numOfPackages={1}, palletDims={2}, minX={2}, maxX={3}, minY={4}, maxY={5}, "
                      + "minWeight={6}, maxWeight={7}, minCapacity={8}, maxCapacity={9}")
                .format(numOfRuns, numOfPackages, palletDims, minX, maxX, minY, maxY,
                        minWeight, maxWeight, minCapacity, maxCapacity))
    file.write()

    babTimes = []
    babBests = []

    geneticTimes = []
    geneticBests = []
    geneticDefaults =

    annealingTimes = []
    annealingBests = []

    for i in range(numOfRuns):

        file.write("======Run " + i + "======")
        coords, weightVars = initPackages(numOfPackages, minX, maxX, minY, maxY,
                                          minWeight, maxWeight, minCapacity, maxCapacity, i)
        file.write("coords=" + str(coords))
        file.write("weightVars=" + str(weightVars))
        file.write()

        file.write("Branch and Bounds " + i)


def main():

    file = open("default0.txt", "w")
    defaultComparison(100, 8, (4, 4), 0, 100, 0, 100, 1, 2, 0, 4, file)

main()
