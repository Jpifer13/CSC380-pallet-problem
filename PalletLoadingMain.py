def readPackages(fileName):
    """ Reads the package dimensions and coordinatess from the file.
        Returns the dimensions and coordinates as lists ([width, length] and [x, y]). """
    return [0,0]*25, [0,0]*25

def tspAlgorithm(packageCoords):
    """ Dummy method.
        Returns the order as a list of indeces. """
    return list(range(len(packageCoords)))

def packingAlgorithm(packageDims, order, palletDims):
    """ Dummy method
        Returns the pallet coordinates of the packages (x, y, z) """
    return list( (0,0,0) * len(order) )

def validate(packageDims, palletCoords, order, palletDims):
    """ Determines if the pallet meets all the constraints.
        Returns True if the pallet is valid, False otherwise. """
    return False

def main():
    packageDims, packageCoords = readPackages("file")
    palletDims = (0,0,0)

    order = tspAlgorithm(packageDims)

    palletCoords = packingAlgorithm(packageDims, order, palletDims)

    isValid = validate(packageDims, palletCoords, order, palletDims)

    print("Time:", 0.0)
    if isValid:
        print("Valid")
    else:
        print("Invalid +(", "error type", ")", sep="")





