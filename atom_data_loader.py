import json
import numpy as np

#Linear Algebra Solver for Gamma used in previous Code
def gammaSolver(BDEM1 , BDEM2 , BDEM1M2):
    A = np.array([[BDEM1,BDEM2],[1,1]])
    B = np.array([2*BDEM1M2,2])
    X = np.linalg.solve(A,B)
    (gamma_M1,gamma_M2) = X
    return round(gamma_M1,3) , round(gamma_M2,3)

#Function which takes file as input and outputs two dicitonaries
def dataOpener(jsonfilepath):

    #For Values not found in JSON file
    DOES_NOT_EXIST = 0.00

    #Openingn JSON file that is in the same folder as scratch file
    with open(jsonfilepath) as f:
        data = json.load(f)

    #Initializing the Gamma Dictionary
    gamma = {}

    for M1 in data['cebulk']:

        #Creating a temporary dictionary to append and add onto the gamma dictionary
        subEle = {}

        for M2 in data['cebulk']:

            #check for Heterolytic values
            if M1 == M2:
                subEle[M2] = 1.00

            #Check for if the values exist
            elif M1+M2 in data['bde']:
                temp , subEle[M2] = gammaSolver(data['bde'][M1+M1],data['bde'][M2+M2],data['bde'][M1+M2])

            elif M2+M1 in data['bde']:
                temp, subEle[M2] = gammaSolver(data['bde'][M1 + M1], data['bde'][M2 + M2], data['bde'][M2 + M1])

            #For when values do not exist within the JSON File
            elif M1 + M2 not in data['bde']:
                subEle[M2] = DOES_NOT_EXIST

            elif M2 + M1 not in data['bde']:
                subEle[M2] = DOES_NOT_EXIST

        gamma[M1] = subEle

    return data['cebulk'],gamma

cebulk , gamma = dataOpener('agaucu_data.json')

print(f'This is the ce_bulk Dictionary : {cebulk}')
print(f'This is the Gamma Dictionary : {gamma}')


