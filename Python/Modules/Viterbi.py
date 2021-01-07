"""
File: Viterbi.py

Author: Chase Timmins
Create Date: 14-Dec-2020

Description:

Classes:

Method(s):
 - viterbi_pathfind
 - get_paths
"""
### Import Statements
from numpy import log2
from copy import deepcopy

### Function Definitions


def get_paths(legal):
    paths = []
    L = len(legal)
    done = False
    idx_s = [0]*L
    idx = len(idx_s) - 1
    while(not done):
        idx = len(idx_s) - 1
        tmp = []
        for i in range(len(idx_s)):
            tmp.append(legal[i][idx_s[i]])
        paths.append(tmp)

        # Adjust Index Vector
        rollover = True
        while (rollover):
            rollover = False
            if (idx >= 0):
                idx_s[idx] += 1
                if (idx_s[idx] == len(legal[idx])):
                    rollover = True
                    idx_s[idx] = 0
                    idx -= 1
            else:
                done = True
    return paths

## viterbi_pathfind
#|-----------------------------------------------------------------------------------------------------------------------
#|      Author: Chase Timmins
#|     Project: 256-QAM Communication System
#| Create Date: December 14, 2020
#|-----------------------------------------------------------------------------------------------------------------------
#
# Use: path = viterbi_pathfind(dataset,mthd)
#
# Description:
# 	 This function performs an implementation of the Viterbi Algorithm to serve as a "Maximum Likelihood Sequence" finder
# given a set of data to work off of and a user-chosen method.
#
# Parameters:
#|-----------------------------------------------------------------------------------------------------------------------
# dataset
# - Type: int[][]
# - Description:  Two dimensional array where each row is a separate data entry. Each integer in this matrix ranges from 0
#       to 15 (representative of hexadecimal symbol).
# mthd
# - Type: int
# - Description:  Either 0 or 1 (1 is default). Represents which method the user chooses to use for Viterbi: Fast (1) or
#       Multi-path (0).
#|-----------------------------------------------------------------------------------------------------------------------
#
# Returns:
#|-----------------------------------------------------------------------------------------------------------------------
# path
# - Type: int[]
# - Description:  The maximum likelihood path determined by the Viterbi algorithm.
#|-----------------------------------------------------------------------------------------------------------------------
#
# Dependencies:
#  - numpy
#

def viterbi_pathfind(dataset,mthd = 1):
    ## Obtain Constants from dataset
    L = len(dataset[0])
    SEQS = len(dataset)

    ## Calculate State Transition Probabilities
    # Overall Use: tran[i][j][k], gives probability for state transition between states 'j' and 'k' for event index 'i' to 'i+1'
    tran = []
    start = [0]*16
    for i in range(L - 1):
        temp = []
        for j in range(16):
            temp.append([0]*16)
        tran.append(temp)

    # Overall Use: apps[i][j], gives number of appearances of bit 'j' in position 'i+1'
    apps = []
    for i in range(L - 1):
        tmp = [0]*16
        for j in range(SEQS):
            tmp[dataset[j][i]] += 1
        apps.append(tmp)

    # Calculate Start bit probabilities
    for i in range(SEQS):
        start[dataset[i][0]] += 1/SEQS

    # Calculate State Transition Probabilities
    for i in range(L - 1):
        for j in range(SEQS):
            a = dataset[j][i]
            b = dataset[j][i + 1]
            tran[i][a][b] += round(1/apps[i][a],6)

    # Change method depending on user input
    path = []

    # Choose Path-finding Method
    if (mthd == 1): # Fast
        # Find maximum starting index
        mx = 0
        mx_idx = 0
        for i in range(len(start)):
            if (start[i] > mx):
                mx = start[i]
                mx_idx = i
        path.append(mx_idx)

        # Continue Procedurally throught the state transition matrix and determine the most likely path
        for i in range(len(tran)):
            mx = 0
            idx = 0
            for j in range(16):
                if (tran[i][path[len(path) - 1]][j] > mx):
                    mx = tran[i][path[len(path) - 1]][j]
                    idx = j
            path.append(idx)
    elif (mthd == 0): # Multi-path
        # Find legal positions of hex symbols
        # General Use: legal[i][j], legal[i] yields an array of legal characters in
        legal = []
        for i in range(L):
            tmp = []
            for j in range(SEQS):
                if (dataset[j][i] not in tmp):
                    tmp.append(dataset[j][i])
            legal.append(tmp)

        paths = get_paths(legal)

        # Calculate the probability of each path occurring and determine the maximum likelihood path
        mx_pth = -1e9
        for pth in paths:
            tmp = 0
            for i in range(len(pth)):
                if (i == 0):
                    tmp += 10*log2(start[pth[i]])
                elif (tran[i-1][pth[i-1]][pth[i]] == 0):
                    tmp += -1e9
                    break
                else:
                    tmp += 10*log2(tran[i-1][pth[i-1]][pth[i]])

            if (tmp > mx_pth):
                mx_pth = tmp
                path = deepcopy(pth)

    return path
