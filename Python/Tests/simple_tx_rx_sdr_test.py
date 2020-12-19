## Hardware and Module Test for Pluto SDR
#|-------------------------------------------------------------------------------
#|      Author: Chase Timmins
#|  Instructor: Dr. Tofighi
#|      Course: EE 460
#|     Project: 256-QAM Research Project
#| Create Date: December 16, 2020
#|-------------------------------------------------------------------------------
#
# Description:
#        This script serves as the final test and SDR implementation of the 256-QAM
# Communication system with the addition of Viterbi Path-finding. This script will
# transmit and receive from the Pluto SDR and log both the raw and the encoded
# data.
#

### Import Statements
from SDR import *
from Viterbi import *
from DataLogger import *
import matplotlib.pyplot as plt
import random

### Main
if __name__ == '__main__':
    ## Setup SDR object
    sdr = pluto_setup(True, 1e9, True, True, 1e9)

    ## Set Sampling Rate and Carrier Frequency
    N = 100
    fs = sdr.sample_rate
    fc = fs/N

    # Set new bandwidth
    sdr.tx_rf_bandwidth = int(4*fc)
    sdr.rx_rf_bandwidth = int(4*fc)

    ## Set desired number of waveforms to receive
    M = 2

    ## Generate Symbol Sequence
    msg = [0]*MSG_LEN
    #for i in range(MSG_LEN):
    #    msg.append(random.randint(0,255))

    ## Encode QAM
    tx = encode_QAM(msg,fc,fs,256,True)

    ## Set RX buffer size
    sdr.rx_buffer_size = int(2*len(tx))
    rx_buf = []
    rx_bits = []
    rx_debg = []

    ## Transmit
    sdr.tx(tx)

    ## Receive
    for i in range(M):
        rx_buf.append(sdr.rx())
    # Adjust input; for some reason, the real portion of the complex received array is inverted
    idx = find_full(rx_buf[0],N*(MSG_LEN+4))
    rx_debg = rx_buf[0][idx[0]:idx[1]]
    ## Plot the data that the program thinks is the message signal
    t = np.linspace(0,len(rx_debg)/fs,len(rx_debg))
    fig, ax = plt.subplots(2)
    ax[0].plot(t,np.real(rx_debg),label='In-Phase')
    ax[0].plot(t,np.imag(rx_debg),label='Quadrature')
    ax[0].set_title('Found Data; Prior to iq_find')
    ax[0].legend()

    tst = iq_find(rx_debg,fc,fs)
    t2 = np.linspace(0,len(tst)/fs,len(tst))
    ax[1].plot(t,np.real(tst),label='In-Phase')
    ax[1].plot(t,np.imag(tst),label='Quadrature')
    ax[1].set_title('Found Data; Post iq_find')
    ax[1].legend()
    
    ax.show()
