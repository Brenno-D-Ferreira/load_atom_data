import json
import numpy as np
from pprint import pprint

#For Values not found in JSON file
DOES_NOT_EXIST = 0.00

#Linear Algebra Solver for Gamma used in previous Code
def gammaSolver(BDEM1 , BDEM2 , BDEM1M2):

    #Check if heteroatomic
    if BDEM1 == BDEM2 == BDEM1M2:
        return 1.0, 1.0

    # Return 0's if no BDEM1M2
    elif 0 in [BDEM1, BDEM2, BDEM1M2]:
        return DOES_NOT_EXIST, DOES_NOT_EXIST


    A = np.array([[BDEM1,BDEM2],[1,1]])
    B = np.array([2*BDEM1M2,2])
    X = np.linalg.solve(A,B)
    (gamma_M1,gamma_M2) = X

    return gamma_M1, gamma_M2

#Function which takes file as input and outputs two dicitonaries
def dataOpener(jsonfilepath):

    #Openingn JSON file that is in the same folder as scratch file
    with open(jsonfilepath) as f:
        data = json.load(f)

    #Initializing the Gamma Dictionary
    gamma = {m: {} for m in data['cebulk']}


    for M1 in data['cebulk']:

        for M2 in data['cebulk']:

            if M2 in gamma[M1]:
                continue

            # get the heteroatomic BDE (check both metal orders)
            bde = data['bde']
            ab = bde.get(M1 + M2, bde.get(M2 + M1, 0))

            # get homoatomic BDEs
            aa = bde.get(M1 + M1, 0)
            bb = bde.get(M2 + M2, 0)

            # if BDE is not found, ab will be 0
            # if aa, bb, or ab = 0, gammas will be 0
            gamma[M1][M2] , gamma[M2][M1] = gammaSolver(aa, bb, ab)

    return data['cebulk'],gamma

cebulk , gamma = dataOpener('agaucu_data.json')

#print(gammaSolver(3, 3, 3))

pprint(gamma)
pprint(cebulk)

