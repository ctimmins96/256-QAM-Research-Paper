"""
File: DataLogger.py

Author: Chase Timmins
Create Date: 15-Dec-2020

Description:

Methods:
 - dl_create
"""
### Import Statements
import numpy as np

### Function Definitions
def dl_create(real_time,bits,header1):
	# Open Log files
    f_csv = open("log.csv","w")
    f_bit = open("log.txt","w")

    header1 += '\n'
    f_csv.write(header1)
    f_bit.write("Received Bits:\n")

	# Write each string to each log file
    for i in range(len(real_time[0])):
		# Loop through real_time data and write to text file
        for j in range(len(real_time)):
            f_csv.write(str(real_time[j][i]))
            if (j != len(real_time) - 1):
                f_csv.write(',')
        f_csv.write('\n')

    for i in range(len(bits)):
        f_bit.write("Trial %d: 0x" % (i + 1))
        for j in range(len(bits[i])):
            f_bit.write(hex(int(np.floor(bits[i][j]/16)) % 16)[2] + hex(bits[i][j] % 16)[2])
        f_bit.write('\n')

    f_csv.close()
    f_bit.close()
