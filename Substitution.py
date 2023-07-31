import numpy as np

"""
Substitution(substitution, initialState, Iterations)
	Performs a substitution in the matter described by the subsitution dictionary,
	and performs it a number of times described by the number of iterations, from
	some initial state described by initialState. returns the result of the 
	substitution.

parameters:

	substitution: a dictionary, describing the substitution
	initialState: a String describing the intial state of the algorithm
	Iterations: the number of iteraterations to run the algorithm for 

return: The n'th iteration of the subsitution
"""


def Substitution(substitution, initialState, Iterations):
    # print(f"iteration: {Iterations}")
    # print(f"state: {initialState}")
    # base case: end of iterations
    if Iterations == 0:
        return initialState

    # replace each occurance of a character with its substitution
    newState = ""
    for char in initialState:
        newState = newState + substitution[char]

    # recursively call Substitution() with one less iteration
    return Substitution(substitution, newState, Iterations - 1)


"""
matrix(substitution)
	returns a Numpy matrix describing the given substitution. 

parameters: 
	substitution: a dictionary, describing the substitution

return: A Numpy matrix representing the substitution
"""


def matrix(substitution):
    matString = ""
    for key in substitution:
        for row in substitution:
            count = substitution[row].count(key)
            matString = matString + " " + str(count)
        matString = matString + ";"
    matString = matString[1:-1]
    mat = np.mat(matString)
    return mat.transpose()


"""
eigenValues(substitution)
	finds both the eigenvalues and eigenvectors of the substitution 
	described by the given dictionary. returns both in a list. 

parameters: 
	substitution: a dictionary, describing the substitution

return: a list containing two entries
	[0] - An array containing the eigenvalues calculated
	[1] - A matrix containing the right eigenvectors of the matrix
"""


def eigenValues(substitution):
    mat = matrix(substitution)
    try:
        eigenval = np.linalg.eig(mat)
    except:
        print("Eigenvalue computation does not converge")
        return

    return eigenval


"""
pfEigenVal(substitution)

finds the PF eigenvector of a given substitution

parameters: 
	substitution: a dictionary, describing the substitution

return: A matrix describing the PF eigenvecotr of the given matrix


"""


def pfEigenVal(substitution):
    eigval = eigenValues(substitution)
    eigenVectors = eigval[1]
    for i in range(len(eigenVectors)):
        vector = eigenVectors[:, i]
        if np.all(vector < 0) | (np.all(vector > 0)):
            return np.real(vector / (vector[len(substitution) - 1]))

    print("PF EigenVector Not Found")
    return None


"""
isPisot(substitution)

Determines if a given substitution is "Pisot", that is all other vectors
other than the Perron-Frobenius, has a norm less than 1.

parameters: 
	substitution: a dictionary, describing the substitution

return: True or False

"""


def isPisot(substitution):
    # find PF eigenvalue
    eigval, eigenVectors = eigenValues(substitution)

    # Case 1: All eigenvalues are integers
    if pisotCase1(eigval):
        return True  # helper funciton to handle Case 1

    # Case 2: All eigenvalues (excepting the PF eigenvalue) are less than 1
    # find PF eigenValue
    for i in range(len(eigenVectors)):
        vector = eigenVectors[:, i]
        if np.all(vector < 0) | (np.all(vector > 0)):
            eigenIndex = i
            break
    if eigenIndex == len(eigenVectors):
        print("PF EigenVector Not Found")
        return None
    # exclude PF eigenvalue
    eigval = np.delete(eigval, i, 0)
    absval = np.abs(eigval)
    for value in absval:  # check remaining eigenvalues against 1
        if (
            value > 0.99999999999999
        ):  # check slightly lower than 1, because of float rounding
            return False

    return True


"""-----------------------------------------------------------
Helper function to handle Case 1 for the Pisot Condition:
That all eigenvalues are integers. 
-----------------------------------------------------------"""


def pisotCase1(eigval):

    if isinstance(eigval[0], float):  # if the array is of real floats
        for eigenValue in eigval:
            if not eigenValue.is_integer():
                return False
        return True

    if isinstance(eigval[0], np.complex):  # if the array is complex
        # Rounds both imaginary portions, and real portions to see if
        # All portions are integers (within 15 decimal points)
        for eigenValue in eigval:
            if round(eigenValue.imag, 15) != 0:
                return False
            if not round(eigenValue.real, 15).is_integer():
                return False
        return True


"""
diffraction(sub, lowerbound=0, upperbound=10, interval=0.01, k=20)
	Generates a diffraction pattern given a substitution. Returns x and y values 
    to draw the substitution. 

parameters:
    sub: Dictionary representing a Substitution from which the diffraction pattern
         is generated. 
    lowerbound=0: The lower bound of the diffraction pattern
    upperbound=10: Upper bound of the diffraction pattern
    interval=0.01: Space between the individual data points along the x axis
    k=20: Number of points in the substitution for which to perform the diffraction
	

return: Two arrays x and y which represent the x and y coordinates of the points to
        draw the diffraction. 
"""


def diffraction(sub, lowerbound=0, upperbound=10, interval=0.01, k=20):

    # TODO Something else
    pfEigenVector = pfEigenVal(sub)

    symbolic = Substitution(
        sub, "a", 7
    )  # TODO figure out how many substitution iterations I need to do to reach a minimum of k points
    symbolic = symbolic[0:k]
    points = []
    xvalue = 0
    keys = list(sub.keys())

    for point in symbolic:
        xvalue += pfEigenVector[keys.index(point), 0]
        newPoint = xvalue
        points.append(newPoint)

    points = np.array(points)
    x = np.arange(lowerbound, upperbound, interval)
    t = x * 2 * np.pi
    y = []
    for time in t:
        out = points * time

        left = np.cos(out)
        left = np.sum(left)
        left = left**2
        right = np.sin(out)
        right = np.sum(right)
        right = right**2
        final = (1 / len(points) ** 2) * (left + right)
        y.append(final)

    return x, y


"""
isValid(sub)
	Returns a boolean value representing the validity of the substitution.

parameters:
    sub: Dictionary representing a Substitution of which the validity is to
	be determined
    
return: Boolean value
"""


def isValid(sub):

    if len(sub) == 0:
        return False
    # if a substitution contains a character which is not a variable, it is not valid
    for value in sub.values():
        for char in value:
            if char not in sub.keys():
                return False

    if type(eigenValues(sub)) == type(None):
        return False
    if type(pfEigenVal(sub)) == type(None):
        return False

    return True


"""
projection(sub, lowerbound=0, upperbound=10, interval=0.01, k=20)
	Generates a diffraction pattern given a substitution. Displays the diffraction
	as a projected pattern of lines.
parameters:
    sub: Dictionary representing a Substitution from which the diffraction pattern
         is generated. 
    lowerbound=0: The lower bound of the diffraction pattern
    upperbound=10: Upper bound of the diffraction pattern
    interval=0.01: Space between the individual data points along the x axis
    k=20: Number of points in the substitution for which to perform the diffraction
	

return: None
"""


def projection(sub, lowerbound=0, upperbound=10, interval=0.01, k=20):
    x, y = diffraction(sub, lowerbound, upperbound, interval, k)
    X, Y = np.meshgrid(y, x)
    return X
