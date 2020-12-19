## Viterbi Algorithm Example
#|-----------------------------------------------------------------------------------------------------------------------
#|      Author: Chase Timmins
#|  Instructor: Dr. Tofighi
#|      Course: EE 460
#| Create Date: December 6, 2020
#|-----------------------------------------------------------------------------------------------------------------------
#
# Description:
#      This script is meant to serve as a short example of how the Viterbi Algorithm determines the most likely sequence of
# events given a set of data or a predetermined probability matrix.
#
### Import Statements
import random
import Viterbi

### Constant Definitions
# Create fresh random number generator
random.seed(random.randint(1,65536))

# Bit Error Rate (BER) Percentage
BER = 0.5

# Number of Sequences to Generate
SEQS = 20

### Functions

## Sequence Generation Function
#|-----------------------------------------------------------------------------------------------------------------------
#|      Author: Chase Timmins
#|  Instructor: Dr. Tofighi
#|      Course: EE 460
#| Create Date: December 6, 2020
#|-----------------------------------------------------------------------------------------------------------------------
#
# Use: res = generate_sequence(l)
#
# Description:
# 	 Generates sequences of pseudo-random integers between 0 and 15 with an array length of l.
#
# Parameters:
#|-----------------------------------------------------------------------------------------------------------------------
# l
# - Type: int
# - Description:  Length of sequence
#|-----------------------------------------------------------------------------------------------------------------------
#
# Returns
#|-----------------------------------------------------------------------------------------------------------------------
# res
# - Type: int[]
# - Description:  The generated sequence
#|-----------------------------------------------------------------------------------------------------------------------
#
def generate_sequence(l):
    arr = []
    for i in range(l):
        arr.append(random.randint(0,15))
    return arr

## get_variations
#|-----------------------------------------------------------------------------------------------------------------------
#|      Author: Chase Timmins
#|  Instructor: Dr. Tofighi
#|      Course: EE460
#| Create Date: December 6, 2020
#|-----------------------------------------------------------------------------------------------------------------------
#
# Use: res = get_variations(arr,num)
#
# Description:
# 	 Generate variations centered around a single sequence of integers with a BER set by the constant called BER
#
# Parameters:
#|-----------------------------------------------------------------------------------------------------------------------
# arr
# - Type: int[]
# - Description:  The sequence that shall be varied. The initial message signal that shall be modified
# num
# - Type: int
# - Description:  The number of variations to generate
#|-----------------------------------------------------------------------------------------------------------------------
#
# Returns:
#|-----------------------------------------------------------------------------------------------------------------------
# res
# - Type: int[][]
# - Description:  The generated variations of the message signal
#|-----------------------------------------------------------------------------------------------------------------------
#
def get_variations(arr,num):
    res = []
    for i in range(num):
        var = []
        for item in arr:
            if (random.random() <= BER):
                var.append(random.randint(0,15))
            else:
                var.append(item)
        res.append(var)
    return res
## arr_2_hex
#
# Generates hexadecimal string from integer array
#
def arr_2_hex(ints):
    res = ''
    for item in ints:
        if (len(res) < 1):
            res = hex(item)
        else:
            res += hex(item)[2:]

    return res

### Main
if __name__ == '__main__':
    # Generate Initial Sequence
    l = int(input('How long of a sequence would you like to generate?: '))
    seq = generate_sequence(l)
    print('Initial Message Sequence: ' + arr_2_hex(seq) + '\n\n')

    # Generate Variation (Error) Sequences
    rx = get_variations(seq,SEQS)
    print('Generated Sequence Variations: ')
    for i in range(SEQS):
        print(arr_2_hex(rx[i]) + '\n')

    ## Given the generated sequence, create a transition matrix
    s_bits = [0]*16

    # tran[i][j][k]
    # i - Event Index: Probability calculated for index i to i+1
    # j/k - States: Probability calculated for state transition from state j to state k
    #
    # Overall Use: tran[i][j][k], gives probability for state transition between states j and k for event index i to i+1
    tran = []
    for i in range(l-1):
        temp = []
        for j in range(16):
            temp.append([0]*16)
        tran.append(temp)

    # Calculate Start Bit Probability
    for i in range(16):
        s_sum = 0
        for j in range(SEQS):
            if (rx[j][0] == i):
                s_sum += 1
        s_bits[i] = s_sum/SEQS

    # Calculate State Transition Probabilities
    for i in range(l-1):
        for j in range(SEQS):
            a = rx[j][i]
            b = rx[j][i+1]
            tran[i][a][b] += round(1/SEQS,6)

    ## Find most probable path
    # Find the most probable starting path
    mx = max(s_bits)
    start = 0
    for i in range(len(s_bits)):
        if (s_bits[i] == mx):
            start = i

    path = Viterbi.viterbi_pathfind(rx,1)

    print('-'*(l+2) + '\n' + '-'*(l+2))
    print('  Result: ' + arr_2_hex(path))
    print('Original: ' + arr_2_hex(seq))
