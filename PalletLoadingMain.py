import datetime
import timeit
import inspect

from PalletLoadingHelpers import *
import BranchandBound
import Genetic
import SimulatedAnnealing

def defaultComparison(numOfRuns, numOfPackages, palletDims, minX, maxX, minY, maxY,
                      minWeight, maxWeight, minCapacity, maxCapacity, file):

    # write the method name and current date and time
    file.write("defaultComparison, " + datetime.datetime.now().strftime("%x %X") + "\n")
    # write the method arguments
    file.write(("numOfRuns={0}, numOfPackages={1}, palletDims={2}, minX={2}, maxX={3}, minY={4}, maxY={5}, "
                      + "minWeight={6}, maxWeight={7}, minCapacity={8}, maxCapacity={9}\n")
                .format(numOfRuns, numOfPackages, palletDims, minX, maxX, minY, maxY,
                        minWeight, maxWeight, minCapacity, maxCapacity))
    file.write("\n")

    babTimes = []
    babBests = []

    genTimes = []
    genBests = []
    genParams = inspect.signature(Genetic.runGeneticXTrials).parameters
    file.write("Genetic params: " + str(genParams) + "\n")
    genDefs = [ genParams["numOfTrials"].default,
                genParams["seed"].default,
                genParams["popSize"].default,
                genParams["generations"].default,
                genParams["numParentPairs"].default,
                genParams["mutationProb"].default ]

    annTimes = []
    annBests = []
    annParams = inspect.signature(SimulatedAnnealing.annealXTrials).parameters
    file.write("Annealing params: " + str(annParams) + "\n")
    annDefs = [ annParams["numOfTrials"].default,
                annParams["seed"].default,
                annParams["iterations"].default,
                annParams["maxTries"].default,
                annParams["initialTemp"].default,
                annParams["k"].default ]

    file.write("\n")
    file.flush()

    for i in range(numOfRuns):

        print("\n\nRUN " + str(i))
        file.write("====== Run " + str(i) + " ======\n")
        coords, weightVars = initPackages(numOfPackages, minX, maxX, minY, maxY,
                                          minWeight, maxWeight, minCapacity, maxCapacity, i)
        file.write("coords=" + str(coords) + "\n")
        file.write("weightVars=" + str(weightVars) + "\n")
        file.write("\n")

        print(coords)
        print(weightVars)
        print()

        print("\n\nBRANCH AND BOUNDS " + str(i))
        file.write("Branch and Bounds " + str(i) + "\n")
        babTime = timeit.timeit(
                lambda: BranchandBound.completeBranchAndBoundF(file, coords, weightVars, palletDims), number=1)
        babTimes.append(babTime)
        file.write(str(babTime) + "\n")
        file.write("\n")

        print("\n\nGENETIC " + str(i))
        file.write("Genetic " + str(i) + "\n")
        genTime = timeit.timeit(
                lambda: Genetic.runGeneticXTrialsF(file, coords, weightVars, palletDims,
                                                   1, genDefs[1], genDefs[2],
                                                   genDefs[3], genDefs[4], genDefs[5]), number=1)
        genTimes.append(genTime)
        file.write(str(genTime) + "\n")
        file.write("\n")

        print("\nANNEALING " + str(i))
        file.write("Annealing " + str(i) + "\n")
        annTime = timeit.timeit(
                lambda: SimulatedAnnealing.annealXTrialsF(file, coords, weightVars, palletDims,
                                                          1, annDefs[1], annDefs[2],
                                                          annDefs[3], annDefs[4], annDefs[5]), number=1)
        annTimes.append(annTime)
        file.write(str(annTime) + "\n")
        file.write("\n")

        file.flush()

    babAvgTime = sum(babTimes) / len(babTimes)
    genAvgTime = sum(genTimes) / len(genTimes)
    annAvgTime = sum(annTimes) / len(annTimes)
    file.write("====== Results =======\n")
    file.write("Branch and bound average=" + str(babAvgTime) + "\n")
    file.write("Genetic average=" + str(genAvgTime) + "\n")
    file.write("Simulated annealing average=" + str(annAvgTime) + "\n")
        
# lets timeit return the method's returns
# http://stackoverflow.com/questions/24812253/how-can-i-capture-return-value-with-python-timeit-module
def _template_func(setup, func):
    """Create a timer function. Used if the "statement" is a callable."""
    def inner(_it, _timer, _func=func):
        setup()
        _t0 = _timer()
        retval = None
        for _i in _it:
            retval = _func()
        _t1 = _timer()
        return _t1 - _t0, retval
    return inner

def averageCosts(fileName):

    file = open(fileName, 'r')

    costs = [[], [], []]
    invalidCounts = [0, 0, 0]
    costIndex = 0
    lineCounter = -1
    for line in file:
        if lineCounter == 0:
            start = line.split()[0].lower()
            if start in ("valid", "invalid"):
                invalidCounts[costIndex] += 1
            else:
                costs[costIndex].append(float(line.split(',')[0].strip()))
            costIndex += 1
            if costIndex >= len(costs):
                costIndex = 0
            lineCounter = -1
        elif lineCounter > 0:
            lineCounter -= 1
        else:
            parts = line.split()
            if len(parts) >= 2 and parts[0] in ("Branch", "Genetic", "Annealing") and parts[-1].isdigit():
                lineCounter = 0

    babAverage = sum(costs[0]) / len(costs[0])
    babInvalidRatio = invalidCounts[0] / (len(costs[0]) + invalidCounts[0]) / 100
    genAverage = sum(costs[1]) / len(costs[1])
    genInvalidRatio = invalidCounts[1] / (len(costs[1]) + invalidCounts[1]) / 100
    annAverage = sum(costs[2]) / len(costs[2])
    annInvalidRatio = invalidCounts[2] / (len(costs[2]) + invalidCounts[2]) / 100

    file.close()

    file = open(fileName, 'a')

    file.write("\n")
    file.write("====== AVERAGE COSTS ======\n")
    file.write("Branch Average: " + str(babAverage) + "(" + str(babInvalidRatio) + "% invalid)\n")
    file.write("Genetic Average: " + str(genAverage) + "(" + str(genInvalidRatio) + "% invalid)\n")
    file.write("Annealing Average: " + str(annAverage) + "(" + str(annInvalidRatio) + "% invalid)\n")

    file.close()

def main():

    # file = open("tests\\default0.txt", "w")
    # timeit._template_func = _template_func
    # defaultComparison(100, 8, (4, 4), 0, 100, 0, 100, 1, 2, 0, 4, file)
    # file.close()

    averageCosts("tests\\default0.txt")

main()
