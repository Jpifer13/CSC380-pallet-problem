def readPackages(fileName):
    """ Reads the package dimensions, weights, and capacities from the file.
        Returns the dimensions and coordinates as lists ([weight, capacity] and [x, y]). """
    return [0,0]*25, [0,0]*25

def tspAlgorithm(packageCoords):
    """ Dummy method.
        Returns the order as a list of indeces. """
    return list(range(len(packageCoords)))

def packingAlgorithm(packageVars, order, palletDims):
    """ Dummy method
        Returns the pallet coordinates of the packages (x, y),
            or None if no valid pallet can be constructed. """
    return list( (0,0) * len(order) )

def validate(packageVars, palletCoords, order, palletDims):
    """ Determines if the pallet meets all the constraints.
        Returns True if the pallet is valid, False otherwise. """
    return False

def main():
    packageVars, packageCoords = readPackages("file")
    palletDims = (0,0)

    order = tspAlgorithm(packageCoords)

    palletCoords = packingAlgorithm(packageVars, order, palletDims)

    isValid = validate(packageVars, palletCoords, order, palletDims)

    print("Time:", 0.0)
    if isValid:
        print("Valid")
    else:
        print("Invalid +(", "error type", ")", sep="")
