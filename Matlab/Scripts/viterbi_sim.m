%% 256-QAM Statistical Script With Viterbi
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
% different test conditions. This script will implement a Viterbi Algorithm to show the compatibility of
% QAM with error detecting / correcting algorithms.
%

if (count(py.sys.path,'C:\Users\Chase\Documents\MATLAB\EE460\final\Sources') == 0)
    insert(py.sys.path,int32(0),'C:\Users\Chase\Documents\MATLAB\EE460\final\Sources');
end

py.importlib.import_module('my_Viterbi');

%% Constant Definitions
L = 16;                                         % Symbol Vector Length
NUM = 5;                                       % Sample Size
ITER = 5;                                       % Iterations

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
nps = linspace(14,17,10);                      % NP in units of dB
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
        for kk = 1:ITER
            d_set = zeros([NUM, L]);
            for ll = 1:NUM
                if (ll == 1)
                    random_flag = 1;
                else
                    random_flag = 0;
                end
                master;
                d_set(ll,:) = bits_in;
            end
            
            py_dset = py.list({});
            
            for xx = 1:NUM
                py_tmp = py.list({});
                for yy = 1:length(d_set(1,:))
                    py_tmp.append(py.int(py.float(bitshift(d_set(xx,yy),-4))));
                    py_tmp.append(py.int(py.float(mod(d_set(xx,yy),16))));
                end
                py_dset.append(py_tmp);
            end
            
            path_py = py.my_Viterbi.viterbi_pathfind(py_dset);
            
            errors = 0;
            for zz = 1:length(in_data)
                tmp = bitshift(int64(path_py.pop(py.int(0))),4);
                tmp = tmp + int64(path_py.pop(py.int(0)));
                if (tmp ~= in_data(zz))
                    errors = errors + 1;
                end
            end
            
            if (errors > mx)
                mx = errors;
            end
            if (errors < mn_1)
                mn_1 = errors;
            end
            
            disp(['Iteration ', num2str(kk), ' Completed!']);
            
            sm = sm + errors;
            sm_sp = sm_sp + 10*log10(var(tx_r + tx_i));
        end
        avg = sm/(ITER);
        avg_p = sm_sp/(ITER);
        res(jjj + length(nps)*(iii-1),:) = [fdev,avg_p - NP,mn_1/L,avg/L,mx/L];
        
        disp(['Completed Data Set: SNR = ', num2str(avg_p - nps(jjj)), ' dB, fdev = ', num2str(fdev), ' Hz/V']);
    end
end
