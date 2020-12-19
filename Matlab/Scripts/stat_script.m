%% 256-QAM Statistical Script
%|-----------------------------------------------------------------------------------------------------------------------
%|      Author: Chase Timmins
%|  Instructor: Dr. Tofighi
%|      Course: EE 460
%|     Project: 256-QAM Communication System
%| Create Date: December 11, 2020
%|-----------------------------------------------------------------------------------------------------------------------
%
% Description:
%        This script will control and run the simulation script and record various statistics like BER and SNR under
% different test conditions. This script will also (eventually) implement a Viterbi Algorithm to show the compatibility of
% QAM with error detecting / correcting algorithms.
%

%% Constant Definitions
L = 16;                                         % Symbol Vector Length
NUM = 10;                                       % Sample Size

%% Create Iterative Loop for General Testing (Record BER for a single input given different noise power)
%
% Independent Variables:
% - Noise Power (SNR)
% - Frequency Deviation (FM)
%
% Dependent Variables:
% - BER (Best, Average, Worst cases)

% Create vectors to Set SNR and Frequency Deviation
% NPs = 0.1:((9.9)/7):10;
nps = 0:20;                            % NP in units of dB
fdevs = [2,3]*1.333e6;

% Create Vectors to store the results in
res = zeros([length(nps)*length(fdevs),5]);    % [SNR, fdev, BER_B,BER_A,BER_W]

% Begin Loop
for iii = 1:length(fdevs)
    fdev = fdevs(iii);
    for jjj = 1:length(nps)
        NP = nps(jjj);
        mn_1 = 9999;
        mx = 0;
        sm = 0;
        sm_sp = 0;
        for kk = 1:NUM
            master;
            sm = sm + errors;
            sm_sp = sm_sp + 10*log10(var(tx_r + tx_i));
            if (errors > mx)
                mx = errors;
            end
            if (errors < mn_1)
                mn_1 = errors;
            end
        end
        avg = sm/NUM;
        avg_p = sm_sp/NUM;
        res(jjj + length(nps)*(iii-1),:) = [fdev,avg_p - nps(jjj),mn_1/L,avg/L,mx/L];
        
        disp(['Completed Data Set: SNR = ', num2str(avg_p - nps(jjj)), ' dB, fdev = ', num2str(fdev), ' Hz/V']);
    end
end

%fdev = ;
%NP = 0;

%% Same iterative loop as above but with the use of Viterbi
%
% Independent Variables:
% - Sample Size
% - Noise Power
% - Path-finding Method
%
% Dependent Variables:
% - BER (Best, Average, and Worst cases