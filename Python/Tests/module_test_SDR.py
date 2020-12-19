"""
File: sdrLib_test.py

Author: Chase Timmins
Create Date: 14-Dec-2020

Description: Basic module test to ensure that all functions work as intended
"""

### Import Statement
from SDR import *
from TESTING import *
import matplotlib.pyplot as plt
import numpy as np
import random

### Constant Definitions
fs = 1e9
fc = fs/20

### Main

if __name__ == '__main__':
    ## Intro

    ## Test var function
    announce('\\pwr\\ Test')
    tsts = [[1,2,4,3],[1,0,-1,0],[1,2,-1,-2],[1+1j,1-1j,-1+1j,-1-1j]]
    results = [30,2,10,8]
    succ = 0
    fail = 0
    for i in range(len(tsts)):
        #print('Test Case %d:' % (i+1))
        #print(tsts[i])
        #print('Expected: %d;\tResult: %d' % (results[i],np.real(pwr(tsts[i]))))

        if (results[i] == np.real(pwr(tsts[i]))):
            #print('------------------ Success! ------------------\n')
            succ += 1
        else:
            #print('------------------ Failure! ------------------\n')
            fail += 1
    succ_fail(succ,fail)

    ## Test bits2sine function
    announce('\\bits2sine\\ Test')
    sin_base = [0.0, 0.3090169943749474, 0.5877852522924731, 0.8090169943749475, 0.9510565162951535, 1.0, 0.9510565162951536, 0.8090169943749475, 0.5877852522924732, 0.3090169943749475, 1.2246467991473532e-16, -0.3090169943749469, -0.587785252292473, -0.8090169943749473, -0.9510565162951535, -1.0, -0.9510565162951536, -0.8090169943749476, -0.5877852522924734, -0.3090169943749477]
    results = []
    succ = 0
    fail = 0
    for i in range(256):
        tmp = []
        res = bits2sine([i],fc,fs)
        for j in range(len(sin_base)):
            tmp.append(KEY_256QAM[i]*sin_base[j] - res[j])
        #print('Test Case: %d;\t tx_bit = %d' % (i+1,i))
        if (pwr(tmp) < 0.00001*pwr(res)):
            #print('------------------ Success! ------------------\n')
            succ += 1
        else:
            #print('------------------ Failure! ------------------\n')
            fail += 1
    succ_fail(succ,fail)

    ## Test norm_xcorr function
    announce('\\norm_xcorr\\ Test')
    succ = 0
    fail = 0
    tsts = [
        [[1,2,3,4],[0,0,1,2,3,4,0,0,0,0,0,0,0,0,0]],
        [[1+1j,0,-1+1j,-1-1j,1-1j,0],[0,1,1,3,8,2,5,7,4,4,1+1j,0,-1+1j,-1-1j,1-1j,0]],
        [[12,25,39,25,12],[0,0,12,25,39,25,12,0,0,0,0,12,25,39,25,17,0,0,0,0,0,0,12,25,39,25,9]],
        [[1,0,1,0,1],[0,0,1,0,1,0,1,0,0,0,0,2,0,1,0,2,0,0,0,1,0,2,0,1]],
        [[1,2,3,4,5,6,7],[0,0,1,2,3,4,5,6,7,0,0,0,0,0,1,2,3,4]]
    ]
    expect = [[1.0,2],[1.0,10],[1.0,2],[1.0,2],[1.0,2]]
    for i in range(len(tsts)):
        tmp = norm_xcorr(tsts[i][0],tsts[i][1])
        #print('Test Case %d:' % (i+1))
        #print('Expected: ')
        #print(expect[i])
        #print('Results: ')
        #print(tmp)
        if (abs(tmp[0] - expect[i][0]) < 0.001 and tmp[1] == expect[i][1]):
            #print('------------------ Success! ------------------\n')
            succ += 1
        else:
            #print('------------------ Failure! ------------------\n')
            fail += 1
    succ_fail(succ,fail)

    ## Test near_neighbor function
    

    ## Test decode_QAM function
    announce('\\decode_QAM\\ Test')
    succ = 0
    fail = 0
    tsts = [KEY_START_BITS + [1,2,88,199,225,1,2,88] + KEY_END_BITS,KEY_START_BITS + [255,199,2,88,15,199,2,88] + KEY_END_BITS,KEY_START_BITS + [66,77,88,99,87,111,122,222] + KEY_END_BITS,KEY_START_BITS + [22,122,222,233,133,0,99,39] + KEY_END_BITS,KEY_START_BITS + [100,50,26,242,175,50,26,242] + KEY_END_BITS]
    for i in range(len(tsts)):
        tst = bits2sine(tsts[i],fc,fs)
        s_pad = []
        e_pad = []
        l1 = random.randint(round(len(tst)/2),len(tst)*3)
        l2 = random.randint(round(len(tst)/2),len(tst)*3)

        for j in range(l1):
            s_pad.append(-2 + 4*(random.random() + 1j*random.random()))
        for j in range(l2):
            e_pad.append(-2 + 4*(random.random() + 1j*random.random()))

        tmp = decode_QAM(s_pad + tst + e_pad,fc,fs)
        print('Test Case %d:' % (i+1))
        print('Expected: ')
        print(tsts[i])
        print('Results: ')
        print(tmp[0])
        if (tsts[i] == tmp[0]):
            print('------------------ Success! ------------------\n')
            succ += 1
        else:
            print('------------------ Failure! ------------------\n')
            fail += 1
    succ_fail(succ,fail)
