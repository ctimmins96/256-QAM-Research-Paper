"""
File: SDR.py

Author: Chase Timmins
Create Date: 14-Dec-2020

Description:

Classes:

Method(s):
 - pluto_setup
 - bits2sine
 - pwr
 - norm_xcorr
 - near_neighbor
 - decode_QAM
 - encode_QAM
"""

### Import Statements
import numpy as np
import sys
import traceback
import adi
import copy

### Constant Definitions
KEY_256QAM = {
		 0 : (-7.5+7.5j),
		 1 : (-6.5+7.5j),
		 2 : (-5.5+7.5j),
		 3 : (-4.5+7.5j),
		 4 : (-3.5+7.5j),
		 5 : (-2.5+7.5j),
		 6 : (-1.5+7.5j),
		 7 : (-0.5+7.5j),
		 8 : (0.5+7.5j),
		 9 : (1.5+7.5j),
		 10 : (2.5+7.5j),
		 11 : (3.5+7.5j),
		 12 : (4.5+7.5j),
		 13 : (5.5+7.5j),
		 14 : (6.5+7.5j),
		 15 : (7.5+7.5j),
		 16 : (-7.5+6.5j),
		 17 : (-6.5+6.5j),
		 18 : (-5.5+6.5j),
		 19 : (-4.5+6.5j),
		 20 : (-3.5+6.5j),
		 21 : (-2.5+6.5j),
		 22 : (-1.5+6.5j),
		 23 : (-0.5+6.5j),
		 24 : (0.5+6.5j),
		 25 : (1.5+6.5j),
		 26 : (2.5+6.5j),
		 27 : (3.5+6.5j),
		 28 : (4.5+6.5j),
		 29 : (5.5+6.5j),
		 30 : (6.5+6.5j),
		 31 : (7.5+6.5j),
		 32 : (-7.5+5.5j),
		 33 : (-6.5+5.5j),
		 34 : (-5.5+5.5j),
		 35 : (-4.5+5.5j),
		 36 : (-3.5+5.5j),
		 37 : (-2.5+5.5j),
		 38 : (-1.5+5.5j),
		 39 : (-0.5+5.5j),
		 40 : (0.5+5.5j),
		 41 : (1.5+5.5j),
		 42 : (2.5+5.5j),
		 43 : (3.5+5.5j),
		 44 : (4.5+5.5j),
		 45 : (5.5+5.5j),
		 46 : (6.5+5.5j),
		 47 : (7.5+5.5j),
		 48 : (-7.5+4.5j),
		 49 : (-6.5+4.5j),
		 50 : (-5.5+4.5j),
		 51 : (-4.5+4.5j),
		 52 : (-3.5+4.5j),
		 53 : (-2.5+4.5j),
		 54 : (-1.5+4.5j),
		 55 : (-0.5+4.5j),
		 56 : (0.5+4.5j),
		 57 : (1.5+4.5j),
		 58 : (2.5+4.5j),
		 59 : (3.5+4.5j),
		 60 : (4.5+4.5j),
		 61 : (5.5+4.5j),
		 62 : (6.5+4.5j),
		 63 : (7.5+4.5j),
		 64 : (-7.5+3.5j),
		 65 : (-6.5+3.5j),
		 66 : (-5.5+3.5j),
		 67 : (-4.5+3.5j),
		 68 : (-3.5+3.5j),
		 69 : (-2.5+3.5j),
		 70 : (-1.5+3.5j),
		 71 : (-0.5+3.5j),
		 72 : (0.5+3.5j),
		 73 : (1.5+3.5j),
		 74 : (2.5+3.5j),
		 75 : (3.5+3.5j),
		 76 : (4.5+3.5j),
		 77 : (5.5+3.5j),
		 78 : (6.5+3.5j),
		 79 : (7.5+3.5j),
		 80 : (-7.5+2.5j),
		 81 : (-6.5+2.5j),
		 82 : (-5.5+2.5j),
		 83 : (-4.5+2.5j),
		 84 : (-3.5+2.5j),
		 85 : (-2.5+2.5j),
		 86 : (-1.5+2.5j),
		 87 : (-0.5+2.5j),
		 88 : (0.5+2.5j),
		 89 : (1.5+2.5j),
		 90 : (2.5+2.5j),
		 91 : (3.5+2.5j),
		 92 : (4.5+2.5j),
		 93 : (5.5+2.5j),
		 94 : (6.5+2.5j),
		 95 : (7.5+2.5j),
		 96 : (-7.5+1.5j),
		 97 : (-6.5+1.5j),
		 98 : (-5.5+1.5j),
		 99 : (-4.5+1.5j),
		 100 : (-3.5+1.5j),
		 101 : (-2.5+1.5j),
		 102 : (-1.5+1.5j),
		 103 : (-0.5+1.5j),
		 104 : (0.5+1.5j),
		 105 : (1.5+1.5j),
		 106 : (2.5+1.5j),
		 107 : (3.5+1.5j),
		 108 : (4.5+1.5j),
		 109 : (5.5+1.5j),
		 110 : (6.5+1.5j),
		 111 : (7.5+1.5j),
		 112 : (-7.5+0.5j),
		 113 : (-6.5+0.5j),
		 114 : (-5.5+0.5j),
		 115 : (-4.5+0.5j),
		 116 : (-3.5+0.5j),
		 117 : (-2.5+0.5j),
		 118 : (-1.5+0.5j),
		 119 : (-0.5+0.5j),
		 120 : (0.5+0.5j),
		 121 : (1.5+0.5j),
		 122 : (2.5+0.5j),
		 123 : (3.5+0.5j),
		 124 : (4.5+0.5j),
		 125 : (5.5+0.5j),
		 126 : (6.5+0.5j),
		 127 : (7.5+0.5j),
		 128 : (-7.5-0.5j),
		 129 : (-6.5-0.5j),
		 130 : (-5.5-0.5j),
		 131 : (-4.5-0.5j),
		 132 : (-3.5-0.5j),
		 133 : (-2.5-0.5j),
		 134 : (-1.5-0.5j),
		 135 : (-0.5-0.5j),
		 136 : (0.5-0.5j),
		 137 : (1.5-0.5j),
		 138 : (2.5-0.5j),
		 139 : (3.5-0.5j),
		 140 : (4.5-0.5j),
		 141 : (5.5-0.5j),
		 142 : (6.5-0.5j),
		 143 : (7.5-0.5j),
		 144 : (-7.5-1.5j),
		 145 : (-6.5-1.5j),
		 146 : (-5.5-1.5j),
		 147 : (-4.5-1.5j),
		 148 : (-3.5-1.5j),
		 149 : (-2.5-1.5j),
		 150 : (-1.5-1.5j),
		 151 : (-0.5-1.5j),
		 152 : (0.5-1.5j),
		 153 : (1.5-1.5j),
		 154 : (2.5-1.5j),
		 155 : (3.5-1.5j),
		 156 : (4.5-1.5j),
		 157 : (5.5-1.5j),
		 158 : (6.5-1.5j),
		 159 : (7.5-1.5j),
		 160 : (-7.5-2.5j),
		 161 : (-6.5-2.5j),
		 162 : (-5.5-2.5j),
		 163 : (-4.5-2.5j),
		 164 : (-3.5-2.5j),
		 165 : (-2.5-2.5j),
		 166 : (-1.5-2.5j),
		 167 : (-0.5-2.5j),
		 168 : (0.5-2.5j),
		 169 : (1.5-2.5j),
		 170 : (2.5-2.5j),
		 171 : (3.5-2.5j),
		 172 : (4.5-2.5j),
		 173 : (5.5-2.5j),
		 174 : (6.5-2.5j),
		 175 : (7.5-2.5j),
		 176 : (-7.5-3.5j),
		 177 : (-6.5-3.5j),
		 178 : (-5.5-3.5j),
		 179 : (-4.5-3.5j),
		 180 : (-3.5-3.5j),
		 181 : (-2.5-3.5j),
		 182 : (-1.5-3.5j),
		 183 : (-0.5-3.5j),
		 184 : (0.5-3.5j),
		 185 : (1.5-3.5j),
		 186 : (2.5-3.5j),
		 187 : (3.5-3.5j),
		 188 : (4.5-3.5j),
		 189 : (5.5-3.5j),
		 190 : (6.5-3.5j),
		 191 : (7.5-3.5j),
		 192 : (-7.5-4.5j),
		 193 : (-6.5-4.5j),
		 194 : (-5.5-4.5j),
		 195 : (-4.5-4.5j),
		 196 : (-3.5-4.5j),
		 197 : (-2.5-4.5j),
		 198 : (-1.5-4.5j),
		 199 : (-0.5-4.5j),
		 200 : (0.5-4.5j),
		 201 : (1.5-4.5j),
		 202 : (2.5-4.5j),
		 203 : (3.5-4.5j),
		 204 : (4.5-4.5j),
		 205 : (5.5-4.5j),
		 206 : (6.5-4.5j),
		 207 : (7.5-4.5j),
		 208 : (-7.5-5.5j),
		 209 : (-6.5-5.5j),
		 210 : (-5.5-5.5j),
		 211 : (-4.5-5.5j),
		 212 : (-3.5-5.5j),
		 213 : (-2.5-5.5j),
		 214 : (-1.5-5.5j),
		 215 : (-0.5-5.5j),
		 216 : (0.5-5.5j),
		 217 : (1.5-5.5j),
		 218 : (2.5-5.5j),
		 219 : (3.5-5.5j),
		 220 : (4.5-5.5j),
		 221 : (5.5-5.5j),
		 222 : (6.5-5.5j),
		 223 : (7.5-5.5j),
		 224 : (-7.5-6.5j),
		 225 : (-6.5-6.5j),
		 226 : (-5.5-6.5j),
		 227 : (-4.5-6.5j),
		 228 : (-3.5-6.5j),
		 229 : (-2.5-6.5j),
		 230 : (-1.5-6.5j),
		 231 : (-0.5-6.5j),
		 232 : (0.5-6.5j),
		 233 : (1.5-6.5j),
		 234 : (2.5-6.5j),
		 235 : (3.5-6.5j),
		 236 : (4.5-6.5j),
		 237 : (5.5-6.5j),
		 238 : (6.5-6.5j),
		 239 : (7.5-6.5j),
		 240 : (-7.5-7.5j),
		 241 : (-6.5-7.5j),
		 242 : (-5.5-7.5j),
		 243 : (-4.5-7.5j),
		 244 : (-3.5-7.5j),
		 245 : (-2.5-7.5j),
		 246 : (-1.5-7.5j),
		 247 : (-0.5-7.5j),
		 248 : (0.5-7.5j),
		 249 : (1.5-7.5j),
		 250 : (2.5-7.5j),
		 251 : (3.5-7.5j),
		 252 : (4.5-7.5j),
		 253 : (5.5-7.5j),
		 254 : (6.5-7.5j),
		 255 : (7.5-7.5j)
}

KEY_START_BITS = [15,  255]      # Message Start Symbols / Bits

KEY_END_BITS   = [221, 15]      # Message End Symbols / Bits

MSG_LEN = 8                     # Number of symbols in a message (in addition to the start and the end bits)

### Function Definitions

## pluto_setup
#|-------------------------------------------------------------------------------
#|      Author: Chase Timmins
#| Create Date: December 15, 2020
#|-------------------------------------------------------------------------------
#
# Use: sdr = pluto_setup(tx,fc_tx,cyclic,rx,fc_rx)
#
# Description:
# 	 Setup Pluto SDR Object in Python for general use
#
# Parameters:
#|-------------------------------------------------------------------------------
# tx
# - Type: bool
# - Description:  Determines whether or not to setup the tx portion of the sdr
# fc_tx
# - Type: double
# - Description:  LO Frequency for TX hardware
# cyclic
# - Type: bool
# - Description:  Determines whether the TX hardware uses tx data as a cyclic
#       buffer
# rx
# - Type: bool
# - Description:  Determines whether or not to setup the RX portion of the SDR
# fc_rx
# - Type: double
# - Description:  LO Frequency for RX hardware
# bw
# - Type: double
# - Description:  RF Bandwidth; usually twice baseband bandwidth
#|-------------------------------------------------------------------------------
#
# Returns:
#|-------------------------------------------------------------------------------
# sdr
# - Type: adi.Pluto
# - Description:  SDR Python object; used to transmit and receive wireless data
#|-------------------------------------------------------------------------------
#

def pluto_setup(tx = True,fc_tx=1e9,cyclic = True,rx=True,fc_rx=1e9):
	# Create device interface
    sdr = adi.Pluto('ip:192.168.2.1')

	# Configure properties
	# Check to see if tx or rx are asserted
    sdr.gain_contol_mode_chan0 = "manual"
    if (tx):
		# Configure Tx property
        sdr.tx_lo = int(fc_tx)
        sdr.tx_cyclic_buffer = cyclic
        sdr.tx_hardwaregain_chan0 = -40
        sdr.tx_rf_bandwidth = int(sdr.sample_rate)

    if (rx):
		# Configure Rx properties
        sdr.rx_lo = int(fc_rx)
        sdr.rx_rf_bandwidth = int(sdr.sample_rate)
        sdr.rx_hardwaregain_chan0 = 40


    return sdr

## bits2sine
#|-------------------------------------------------------------------------------
#|      Author: Chase Timmins
#| Create Date: December 15, 2020
#|-------------------------------------------------------------------------------
#
# Use: tx = bits2sine(tx_bits,fc,fs)
#
# Description:
# 	 Create QAM-keyed sine wave from bit sequence
#
# Parameters:
#|-------------------------------------------------------------------------------
# tx_bits
# - Type: int[]
# - Description:  Array of bits indicating which 256-QAM symbols to be used in the
#       waveform
# fc
# - Type: double
# - Description:  QAM Carrier Frequency
# fs
# - Type: double
# - Description:  Sampling Frequency
#|-------------------------------------------------------------------------------
#
# Returns:
#|-------------------------------------------------------------------------------
# tx
# - Type: double[]
# - Description:  Complex Sinusoid output to be transmitted by SDR
#|-------------------------------------------------------------------------------
#

def bits2sine(tx_bits,fc,fs):
    N = round(fs/fc)
    tx = [0]*(N*len(tx_bits))

    # Loop through tx_bits and generate the complex sinusoid
    for i in range(len(tx_bits)):
        for k in range(N):
            tx[k + N*i] = KEY_256QAM[tx_bits[i]]*np.sin(2*np.pi*fc*k/fs)
    return tx

## pwr
#|-------------------------------------------------------------------------------
#|      Author: Chase Timmins
#| Create Date: December 15, 2020
#|-------------------------------------------------------------------------------
#
# Use: p = pwr(x)
#
# Description:
# 	 Computes the Energy of a given signal, x (also called signal power).
#
# Parameters:
#|-------------------------------------------------------------------------------
# x
# - Type: double[] or (c) double[]
# - Description:  Input variable that will have it's energy measured
#|-------------------------------------------------------------------------------
#
# Returns:
#|-------------------------------------------------------------------------------
# p
# - Type: double
# - Description:  Calculated power of input vector
#|-------------------------------------------------------------------------------
#

def pwr(x):
    p = 0
    for i in range(len(x)):
        p += x[i]*np.conj(x[i])
    return p

## norm_xcorr
#|-------------------------------------------------------------------------------
#|      Author: Chase Timmins
#| Create Date: December 15, 2020
#|-------------------------------------------------------------------------------
#
# Use: xcorr = norm_xcorr(x1,x2)
#
# Description:
# 	 Computes normalized cross-correlation between the two vectors.
#
# Parameters:
#|-------------------------------------------------------------------------------
# x1
# - Type: (c) double[]
# - Description:  Array of complex doubles; first cross-correlation variable.
#       Assumed to be the shorter of the two inputs
# x2
# - Type: (c) double[]
# - Description:  Array of complex doubles; second cross-correlation variable.
#       Assumed to be the longer of the two inputs
#|-------------------------------------------------------------------------------
#
# Returns:
#|-------------------------------------------------------------------------------
# xcorr
# - Type: list
# - Description:  Contains maximum correlation value (double) and index at which it
#       occurs (int)
#|-------------------------------------------------------------------------------
#

def norm_xcorr(x1,x2):
    # Define Signal energies
    e1 = pwr(x1)

    # Create xcorr variable for storing index and max correlation
    xcorr = [0,0]

    # Loop through x2 and find the most likely instance of x1
    for i in range(len(x2) - len(x1) + 1):
        tmp = x2[i:(len(x1) + i)]
        e2 = pwr(tmp)

        xsum = 0
        for j in range(len(tmp)):
            xsum += x1[j]*np.conj(tmp[j])/((e1*e2)**0.5)
        if (np.real(xsum) > xcorr[0]):
            xcorr[0] = np.real(xsum)
            xcorr[1] = i
    return xcorr

## near_neighbor
#|-------------------------------------------------------------------------------
#|      Author: Chase Timmins
#| Create Date: December 15, 2020
#|-------------------------------------------------------------------------------
#
# Use: symbol = near_neighbor(part)
#
# Description:
# 	 Uses the nearest neighbor approximation on a given partition to determine the
# symbol that has been received
#
# Parameters:
#|-------------------------------------------------------------------------------
# part
# - Type: (c) double[]
# - Description:  Partition of a some larger input. Meant to contain exactly one
#       symbol
#|-------------------------------------------------------------------------------
#
# Returns:
#|-------------------------------------------------------------------------------
# symbol
# - Type: int
# - Description:  The closest symbol to the given partition; found by
#       cross-correlation
#|-------------------------------------------------------------------------------
#

def near_neighbor(part):
    N = len(part)

    part -= np.mean(part)
    # Create Base Sinusoid
    sin_base = []
    for i in range(N):
        sin_base.append(np.sin(2*np.pi*i/N))

    bit = 0
    diff = 100
    # Search for the bit that most corresponds to the input partition
    for i in range(256):
        tmp = []
        for j in range(N):
            tmp.append(KEY_256QAM[i]*sin_base[j] - part[j])
        # Compute Power of difference
        tmp1 = pwr(tmp)
        if (tmp1 < diff):
            diff = tmp1
            bit = i
    return bit

## decode_QAM
#|-------------------------------------------------------------------------------
#|      Author: Chase Timmins
#| Create Date: December 15, 2020
#|-------------------------------------------------------------------------------
#
# Use: symbols = decode_QAM(raw_data)
#
# Description:
# 	 Uses QAM Constants and functions defined in SDR.py to decode the raw input
# datafrom the receiver
#
# Parameters:
#|-------------------------------------------------------------------------------
# raw_data
# - Type: (c) double[]
# - Description:  Raw QAM Data recived from the RX hardware; Post FM Demodulation
# fc
# - Type: double
# - Description:  QAM Carrier Frequency
# fs
# - Type: double
# - Description:  Sampling Frequency
#|-------------------------------------------------------------------------------
#
# Returns:
#|-------------------------------------------------------------------------------
# symbols
# - Type: int[]
# - Description:  Determined 256-QAM symbol vector derived from the raw input
# encoded
# - Type: (c) double[]
# - Description: Complex array of doubles that contains the message signal
#|-------------------------------------------------------------------------------
#

def decode_QAM(raw_data,fc,fs):
    ## Find start of data packet
    # Take that known start bits and find the most likely index of occurrence in raw_data
    start_seq = bits2sine(KEY_START_BITS + [0]*MSG_LEN + KEY_END_BITS,fc,fs)

    xcorr = norm_xcorr(start_seq,raw_data)
    idx = int(len(start_seq)*2/(MSG_LEN + 4))
    #norm = sum(np.multiply(raw_data[xcorr[1]:xcorr[1]+idx],np.conj(start_seq[0:idx])))/pwr(raw_data[xcorr[1]:xcorr[1]+idx])

    # For proof, see Appendix D: Optimalized Normalization in my research paper
    nrm_r = sum(np.multiply(np.real(raw_data[xcorr[1]:xcorr[1] + idx]),np.real(start_seq[0:idx])))/pwr(np.real(raw_data[xcorr[1]:xcorr[1]+idx]))
    nrm_i = sum(np.multiply(np.imag(raw_data[xcorr[1]:xcorr[1] + idx]),np.imag(start_seq[0:idx])))/pwr(np.imag(raw_data[xcorr[1]:xcorr[1]+idx]))

    #data = np.multiply(raw_data,[abs(norm)]*len(raw_data))
    data = []
    for i in range(len(raw_data)):
        data.append(nrm_r*np.real(raw_data[i]) + 1j*nrm_i*np.imag(raw_data[i]))

    ## Split packet into digestible symbols
    N = round(fs/fc)            # Symbol Sample Length
    encoded = data[xcorr[1]:(xcorr[1] + N*(MSG_LEN + 4))]   # '+4' due to the start and end symbols

    symbols = []

    for i in range(MSG_LEN + 4):
        part = encoded[(i)*N:(i + 1)*N]

        ## Decode symbols
        symbols.append(near_neighbor(part))

    ## Return result
    return [symbols,encoded,start_seq]

## encode_QAM
#|-------------------------------------------------------------------------------
#|      Author: Chase Timmins
#| Create Date: December 16, 2020
#|-------------------------------------------------------------------------------
#
# Use: qam = encode_QAM(bits,fc,fs)
#
# Description:
# 	 Encodes input bits to be prepared for QAM Transmission
#
# Parameters:
#|-------------------------------------------------------------------------------
# bits
# - Type: int[]
# - Description:  Message bits to be encoded
# fc
# - Type: double
# - Description:  Carrier Frequency
# fs
# - Type: double
# - Description:  Sampling Frequency
# gain
# - Type: double
# - Description: Constant to multiply the transmit variable by
# pad
# - Type: bool
# - Description: flag to pad the TX waveform with 0's
#|-------------------------------------------------------------------------------
#
# Returns:
#|-------------------------------------------------------------------------------
# qam
# - Type: (c) double[]
# - Description:  Encoded QAM Sinusoid
#|-------------------------------------------------------------------------------
#

def encode_QAM(bits,fc,fs,gain,pad):
    ## Add start and end bits / symbols
    ## Create Sinusoid
    qam = bits2sine(KEY_START_BITS + bits + KEY_END_BITS,fc,fs)
    if (pad):
        qam = qam + [0j]*int(len(qam)/2)

    gains = [gain]*len(qam)
    qam = np.multiply(qam,gains)

    return qam

def find_full(rx,l):
    ## Given a signal length try and isolate a single instance of the signal
    l1 = round(l*1.4)
    margin = round(l*0.2)

    ## Find indices where the signal frame can be moved 'margin' amount and no
    # significant data is found (significant == data > threshold)
    threshold = 200
    clear1 = False
    clear2 = False
    i = margin

    while ((not clear1) and (not clear2) and (i + l1 + margin < len(rx))):
        r1 = [i-margin,i+margin]
        r2 = [i+l1-margin,i+l1+margin]
        clear1 = True
        clear2 = True

        test = rx[r1[0]:r1[1]]
        for j in range(len(test)):
            if abs(test[j]) > threshold:
                clear1 = False
        test = rx[r2[0]:r2[1]]
        for j in range(len(test)):
            if abs(test[j]) > threshold:
                clear2 = False

        i += 1

    return [i,i+l1]

## iq_find
#|-------------------------------------------------------------------------------
#|      Author: Chase Timmins
#| Create Date: December 18, 2020
#|-------------------------------------------------------------------------------
#
# Use: RX = iq_find(rx,fc,fs)
#
# Description:
# 	 Determines the optimum orientation of the IQ data to maximize correlation
# between the start bits of the received QAM data and known start bits
#
# Parameters:
#|-------------------------------------------------------------------------------
# rx
# - Type: (c) double[]
# - Description:  Raw Received Data
# fc
# - Type: double
# - Description:  Carrier Frequency
# fs
# - Type: double
# - Description:  Sampling Frequency
#|-------------------------------------------------------------------------------
#
# Returns:
#|-------------------------------------------------------------------------------
# RX
# - Type: (c) double[]
# - Description:  Optimized recieve data that (hopefully) matches the start bits
#|-------------------------------------------------------------------------------
#

def iq_find(rx,fc,fs):
    xcorr = 0
    RX = []

    for i in range(8):
        ctrl = [((i & 1)-0.5)*2,(((i >> 1) & 1)-0.5)*2,(i >> 2) & 1]
        tmp = []
        if (ctrl[2] == 0):
            for j in range(len(rx)):
                tmp.append(ctrl[0]*np.real(rx[j]) + 1j*ctrl[1]*np.imag(rx[j]))
        else:
            for j in range(len(rx)):
                tmp.append(ctrl[0]*np.imag(rx[j]) + 1j*ctrl[1]*np.real(rx[j]))
        cor = norm_xcorr(bits2sine(KEY_START_BITS,fc,fs),tmp)[0]
        if (cor > xcorr):
            xcorr = cor
            RX = copy.deepcopy(tmp)
    return RX
