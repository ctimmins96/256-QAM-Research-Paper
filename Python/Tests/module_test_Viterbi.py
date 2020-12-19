### Import Statements
from TESTING import *
from Viterbi import *
import random

### Main
if __name__ == '__main__':
    ## Test get_paths
    announce('\\get_paths\\ Test')
    succ = 0
    fail = 0
    for i in range(50):
        l = 1
        legal = []
        for j in range(8):
            tmp = []
            a = random.randint(1,4)
            l *= a
            for k in range(a):
                tmp.append(random.randint(0,255))
            legal.append(tmp)
        paths = get_paths(legal)

        #print('Test Case: %d' % (i+1))
        #print('Legal: ')
        #print(legal)
        #print('Generated Paths: ')
        #for j in range(len(paths)):
            #print(paths[j])
        if (len(paths) == l):
            #print('------------------ Success! ------------------\n')
            succ += 1
        else:
            #print('------------------ Failure! ------------------\n')
            fail += 1
    succ_fail(succ,fail)
